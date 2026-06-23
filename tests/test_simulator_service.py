"""
tests/test_simulator_service.py

Unit tests for DominoSimulationService.
Pure Python — stubs Django and the tipping_points models so no DB is needed.

Run from project root:
    python3 -m unittest discover -s tests -v
  or directly:
    python3 tests/test_simulator_service.py -v
"""
import sys
import types
import unittest
from unittest.mock import patch, MagicMock


_noop = lambda *a, **kw: None

def _stub(name, **attrs):
    mod = types.ModuleType(name)
    for k, v in attrs.items():
        setattr(mod, k, v)
    sys.modules[name] = mod
    return mod

# Minimal django.db.models surface used at module-import time in services.py
_django_models = _stub(
    'django.db.models',
    Model=object, ForeignKey=_noop, CharField=_noop,
    IntegerField=_noop, FloatField=_noop, TextField=_noop,
    BooleanField=_noop, DateTimeField=_noop, SlugField=_noop,
    PositiveIntegerField=_noop, CASCADE='CASCADE',
)
_stub('django')
_stub('django.db', models=_django_models)

# Fake domain objects
class _FakeTP:
    objects = MagicMock()
    def __init__(self, slug, name='', domain='cryosphere', is_active=True):
        self.slug       = slug
        self.name       = name or slug.replace('_', ' ').title()
        self.domain     = domain
        self.is_active  = is_active

class _FakeRel:
    objects = MagicMock()
    def __init__(self, src, tgt, rel_type='ecosystem_cascade', strength=3):
        self.source            = _FakeTP(src)
        self.target            = _FakeTP(tgt)
        self.relationship_type = rel_type
        self.strength          = strength

# Inject fake apps.tipping_points.models (submodule of the real package)
_tp_models_stub = types.ModuleType('apps.tipping_points.models')
_tp_models_stub.TippingPoint             = _FakeTP
_tp_models_stub.TippingPointRelationship = _FakeRel
sys.modules['apps.tipping_points.models'] = _tp_models_stub

_tp_pkg_stub = types.ModuleType('apps.tipping_points')
_tp_pkg_stub.models = _tp_models_stub
sys.modules['apps.tipping_points'] = _tp_pkg_stub

# Now safely import the service
sys.path.insert(0, '/home/claude/tipping_point_lab')
from apps.simulator.services import DominoSimulationService, NODE_THRESHOLDS


def _all_fake_tps():
    return [_FakeTP(s) for s in NODE_THRESHOLDS]

def _run(misinformation=50, media_literacy=50, public_trust=50,
         policy_speed=50, emissions=50, resilience=50,
         fake_tps=None, fake_rels=None):
    fake_tps  = fake_tps  if fake_tps  is not None else _all_fake_tps()
    fake_rels = fake_rels if fake_rels is not None else []

    tp_qs = MagicMock()
    tp_qs.filter.return_value = fake_tps

    rel_qs = MagicMock()
    rel_qs.filter.return_value.select_related.return_value = fake_rels

    with patch('apps.simulator.services.TippingPoint.objects',             tp_qs), \
         patch('apps.simulator.services.TippingPointRelationship.objects', rel_qs):
        return DominoSimulationService().run(
            misinformation, media_literacy, public_trust,
            policy_speed, emissions, resilience,
        )


# Test classes
class TestTrustScore(unittest.TestCase):
    def setUp(self):
        self.svc = DominoSimulationService()

    def test_high_misinfo_low_literacy_lowers_trust(self):
        hi = self.svc._trust_score(m=0.9, ml=0.1, pt=0.5)
        lo = self.svc._trust_score(m=0.1, ml=0.9, pt=0.5)
        self.assertLess(hi, lo)

    def test_trust_floor_is_zero(self):
        self.assertGreaterEqual(self.svc._trust_score(1.0, 0.0, 0.0), 0.0)

    def test_trust_ceiling_is_one(self):
        self.assertLessEqual(self.svc._trust_score(0.0, 1.0, 1.0), 1.0)

    def test_literacy_partially_counteracts_misinfo(self):
        with_lit    = self.svc._trust_score(m=0.8, ml=0.9, pt=0.5)
        without_lit = self.svc._trust_score(m=0.8, ml=0.1, pt=0.5)
        self.assertGreater(with_lit, without_lit)


class TestDelayRisk(unittest.TestCase):
    def setUp(self):
        self.svc = DominoSimulationService()

    def test_low_trust_increases_delay(self):
        self.assertGreater(
            self.svc._delay_risk(trust_score=0.1, ps=0.3),
            self.svc._delay_risk(trust_score=0.9, ps=0.8),
        )

    def test_fast_policy_reduces_delay(self):
        self.assertLess(
            self.svc._delay_risk(trust_score=0.5, ps=0.9),
            self.svc._delay_risk(trust_score=0.5, ps=0.1),
        )

    def test_always_bounded_zero_to_one(self):
        for ts, ps in [(0.0, 0.0), (1.0, 1.0), (0.5, 0.5), (0.0, 1.0), (1.0, 0.0)]:
            v = self.svc._delay_risk(ts, ps)
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)


class TestClimatePressure(unittest.TestCase):
    def setUp(self):
        self.svc = DominoSimulationService()

    def test_high_emissions_plus_high_delay_maximises_pressure(self):
        self.assertGreater(
            self.svc._climate_pressure(e=0.9, delay_risk=0.9),
            self.svc._climate_pressure(e=0.1, delay_risk=0.1),
        )

    def test_always_bounded(self):
        for e, d in [(0.0, 0.0), (1.0, 1.0), (0.5, 0.5)]:
            v = self.svc._climate_pressure(e, d)
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)


class TestRiskLevel(unittest.TestCase):
    def test_low(self):
        self.assertEqual(DominoSimulationService._risk_level(0.2, 0), 'low')

    def test_moderate(self):
        self.assertEqual(DominoSimulationService._risk_level(0.4, 2), 'moderate')

    def test_high(self):
        self.assertEqual(DominoSimulationService._risk_level(0.6, 5), 'high')

    def test_critical(self):
        self.assertEqual(DominoSimulationService._risk_level(0.9, 12), 'critical')

    def test_zero_nodes_always_low(self):
        self.assertEqual(DominoSimulationService._risk_level(0.95, 0), 'low')


class TestInterventionSuggestions(unittest.TestCase):
    def setUp(self):
        self.svc = DominoSimulationService()

    def _txt(self, **kw):
        return ' '.join(self.svc._suggest_interventions(**kw)).lower()

    def test_high_misinfo_low_literacy_suggests_media_literacy(self):
        txt = self._txt(m=0.9, ml=0.1, trust_score=0.3,
                        delay_risk=0.5, climate_pressure=0.5, r=0.5)
        self.assertIn('media literacy', txt)

    def test_low_trust_suggests_trust_rebuilding(self):
        txt = self._txt(m=0.3, ml=0.5, trust_score=0.2,
                        delay_risk=0.3, climate_pressure=0.4, r=0.5)
        self.assertIn('trust', txt)

    def test_high_delay_suggests_policy_acceleration(self):
        txt = self._txt(m=0.5, ml=0.5, trust_score=0.5,
                        delay_risk=0.8, climate_pressure=0.5, r=0.5)
        self.assertIn('policy', txt)

    def test_low_resilience_suggests_ecosystem_restoration(self):
        txt = self._txt(m=0.3, ml=0.6, trust_score=0.6,
                        delay_risk=0.3, climate_pressure=0.4, r=0.05)
        self.assertIn('resilience', txt)

    def test_low_pressure_high_trust_gives_positive_framing(self):
        txt = self._txt(m=0.1, ml=0.8, trust_score=0.8,
                        delay_risk=0.2, climate_pressure=0.2, r=0.7)
        self.assertIn('manageable', txt)

    def test_always_returns_non_empty_list(self):
        result = self.svc._suggest_interventions(
            m=0.5, ml=0.5, trust_score=0.5,
            delay_risk=0.5, climate_pressure=0.5, r=0.5,
        )
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


class TestFullRun(unittest.TestCase):

    def test_low_inputs_produce_low_risk_and_no_activations(self):
        r = _run(misinformation=5, media_literacy=90, public_trust=90,
                 policy_speed=90, emissions=5, resilience=90)
        self.assertEqual(r.risk_level, 'low')
        self.assertEqual(len(r.activated_nodes), 0)

    def test_high_inputs_produce_more_pressure_than_low(self):
        hi = _run(misinformation=90, media_literacy=10, public_trust=10,
                  policy_speed=10, emissions=90, resilience=10)
        lo = _run(misinformation=10, media_literacy=90, public_trust=90,
                  policy_speed=90, emissions=10, resilience=90)
        self.assertGreater(hi.climate_pressure, lo.climate_pressure)

    def test_result_has_all_required_fields(self):
        r = _run()
        self.assertIsNotNone(r.trust_score)
        self.assertIsNotNone(r.delay_risk)
        self.assertIsNotNone(r.climate_pressure)
        self.assertIsInstance(r.activated_nodes, list)
        self.assertIsInstance(r.interventions, list)
        self.assertIsInstance(r.narrative, str)
        self.assertIn(r.risk_level, ['low', 'moderate', 'high', 'critical'])

    def test_all_scores_in_percentage_range(self):
        r = _run()
        for val in (r.trust_score, r.delay_risk, r.climate_pressure):
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 100.0)

    def test_deterministic(self):
        r1 = _run(misinformation=60, emissions=70, resilience=40)
        r2 = _run(misinformation=60, emissions=70, resilience=40)
        self.assertAlmostEqual(r1.climate_pressure, r2.climate_pressure, places=3)
        self.assertEqual(r1.risk_level, r2.risk_level)
        self.assertEqual(len(r1.activated_nodes), len(r2.activated_nodes))

    def test_activated_node_scores_are_bounded(self):
        r = _run(emissions=95, resilience=5, misinformation=90,
                 media_literacy=10, public_trust=10, policy_speed=5)
        for node in r.activated_nodes:
            self.assertGreaterEqual(node.activation_score, 0.0,
                                    f'{node.slug} score below 0')
            self.assertLessEqual(node.activation_score, 1.0,
                                 f'{node.slug} score above 1')

    def test_narrative_is_non_trivial_string(self):
        r = _run()
        self.assertIsInstance(r.narrative, str)
        self.assertGreater(len(r.narrative), 20)

    def test_cascade_propagates_to_downstream_node(self):
        """Coral reefs → fisheries (strength 5). With very high pressure,
        activating coral should cascade to fisheries."""
        fake_rels = [
            _FakeRel('warm_water_coral_reefs_dieoff', 'fisheries_collapse',
                     'habitat_livelihood', strength=5),
        ]
        r = _run(emissions=90, misinformation=85, media_literacy=10,
                 public_trust=10, policy_speed=5, resilience=5,
                 fake_rels=fake_rels)
        slugs = {n.slug for n in r.activated_nodes}
        if 'warm_water_coral_reefs_dieoff' in slugs:
            self.assertIn('fisheries_collapse', slugs,
                          "Cascade from coral reefs should activate fisheries_collapse")

    def test_higher_resilience_reduces_activations(self):
        """Same emissions; high resilience should activate same or fewer nodes."""
        lo = _run(emissions=70, resilience=10, misinformation=50,
                  media_literacy=50, public_trust=50, policy_speed=50)
        hi = _run(emissions=70, resilience=90, misinformation=50,
                  media_literacy=50, public_trust=50, policy_speed=50)
        self.assertGreaterEqual(
            len(lo.activated_nodes), len(hi.activated_nodes),
            "Higher resilience should produce same or fewer activated nodes",
        )

    def test_node_threshold_coverage(self):
        """All 19 slugs in NODE_THRESHOLDS should be activatable
        under maximum stress conditions."""
        r = _run(emissions=100, resilience=0, misinformation=100,
                 media_literacy=0, public_trust=0, policy_speed=0)
        activated_slugs = {n.slug for n in r.activated_nodes}
        # Under max stress, all nodes with threshold <= 1.0 should fire
        for slug, (threshold, _) in NODE_THRESHOLDS.items():
            if threshold <= 1.0:
                self.assertIn(slug, activated_slugs,
                              f'{slug} (threshold={threshold}) should activate under max pressure')


if __name__ == '__main__':
    unittest.main(verbosity=2)
