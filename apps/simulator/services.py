"""
Domino Simulation Service
=========================
Educational simulation – NOT a predictive climate model.
All values are designed to demonstrate cascading relationships, not forecast outcomes.

Scoring pipeline:
  inputs (0-100 sliders)
    → trust_score
    → delay_risk
    → climate_pressure
    → activated_nodes (per tipping-point activation)
    → intervention suggestions
    → narrative

Slider meanings (0 = minimum, 100 = maximum of that factor):
  misinformation  – how much misinformation is circulating
  media_literacy  – how literate the public is at evaluating claims
  public_trust    – baseline public trust in climate science/institutions
  policy_speed    – how fast governments enact meaningful policy
  emissions       – current emissions pressure (relative to present-day)
  resilience      – combined ecosystem + social resilience
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from apps.tipping_points.models import TippingPoint, TippingPointRelationship

# Tipping point base thresholds
# Each entry: (slug, base_activation_threshold, domain_weight)
# threshold: 0–1; nodes activate when climate_pressure exceeds threshold.
# domain_weight: how much this domain amplifies cascades in others.

NODE_THRESHOLDS: dict[str, tuple[float, float]] = {
    'abrupt_permafrost_thaw':          (0.45, 1.4),   # high carbon feedback
    'permafrost_yedoma_carbon':        (0.50, 1.5),
    'amazon_rainforest_dieback':       (0.55, 1.3),
    'boreal_forest_southern_dieback':  (0.60, 1.1),
    'boreal_forest_northern_expansion':(0.65, 0.9),
    'warm_water_coral_reefs_dieoff':   (0.40, 1.2),
    'mangrove_seagrass_dieoff':        (0.45, 1.1),
    'gis_collapse':                    (0.70, 1.3),
    'wais_collapse':                   (0.75, 1.3),
    'east_antarctic_subglacial_basins':(0.85, 1.2),
    'barents_sea_ice_loss':            (0.35, 1.0),
    'mountain_glacier_loss':           (0.40, 1.0),
    'amoc_collapse':                   (0.65, 1.4),
    'labrador_irminger_convection':    (0.60, 1.2),
    'southern_ocean_overturning':      (0.70, 1.2),
    'west_african_monsoon_shift':      (0.55, 1.1),
    'sahel_greening':                  (0.50, 0.9),
    'lake_eutrophication':             (0.35, 0.8),
    'fisheries_collapse':              (0.45, 1.0),
}


@dataclass
class NodeActivation:
    slug:             str
    name:             str
    domain:           str
    activation_score: float   # 0–1
    triggered_by:     List[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    trust_score:      float
    delay_risk:       float
    climate_pressure: float
    activated_nodes:  List[NodeActivation]
    interventions:    List[str]
    narrative:        str
    risk_level:       str   # 'low' | 'moderate' | 'high' | 'critical'


class DominoSimulationService:
    """
    Stateless service; instantiate and call run() for each request.
    All intermediate calculations are kept as floats in [0, 1].
    Slider inputs are normalised from [0, 100] → [0, 1] internally.
    """

    def run(
        self,
        misinformation:  int,
        media_literacy:  int,
        public_trust:    int,
        policy_speed:    int,
        emissions:       int,
        resilience:      int,
    ) -> SimulationResult:
        # Normalise
        m   = misinformation / 100.0
        ml  = media_literacy / 100.0
        pt  = public_trust   / 100.0
        ps  = policy_speed   / 100.0
        e   = emissions      / 100.0
        r   = resilience     / 100.0

        trust_score     = self._trust_score(m, ml, pt)
        delay_risk      = self._delay_risk(trust_score, ps)
        climate_pressure = self._climate_pressure(e, delay_risk)
        activated       = self._activate_nodes(climate_pressure, r)
        interventions   = self._suggest_interventions(m, ml, trust_score, delay_risk, climate_pressure, r)
        narrative       = self._build_narrative(trust_score, delay_risk, climate_pressure, activated)
        risk_level      = self._risk_level(climate_pressure, len(activated))

        return SimulationResult(
            trust_score      = round(trust_score * 100, 1),
            delay_risk       = round(delay_risk   * 100, 1),
            climate_pressure = round(climate_pressure * 100, 1),
            activated_nodes  = activated,
            interventions    = interventions,
            narrative        = narrative,
            risk_level       = risk_level,
        )

    # Internal scoring methods
    def _trust_score(self, m: float, ml: float, pt: float) -> float:
        """
        High misinformation + low media literacy → erodes trust.
        Strong media literacy partly counteracts misinformation.
        """
        erosion = m * (1.0 - ml * 0.7)         # misinformation effect, weakenedby literacy
        base    = pt * 0.5 + 0.5                # trust anchors above 0 even if base_trust=0
        score   = base - (erosion * 0.6)
        return max(0.0, min(1.0, score))

    def _delay_risk(self, trust_score: float, ps: float) -> float:
        """
        Low trust + slow policy → high delay risk.
        Even strong policy can't fully compensate for zero trust.
        """
        trust_drag  = (1.0 - trust_score) * 0.6
        policy_drag = (1.0 - ps)          * 0.4
        return max(0.0, min(1.0, trust_drag + policy_drag))

    def _climate_pressure(self, e: float, delay_risk: float) -> float:
        """
        Emissions are the direct driver; delay multiplies the risk
        because delayed action allows emissions to compound.
        """
        base_pressure = e * 0.6
        delay_factor  = delay_risk * 0.4
        return max(0.0, min(1.0, base_pressure + delay_factor))

    def _activate_nodes(self, climate_pressure: float, r: float) -> list[NodeActivation]:
        """
        Each tipping point has a base threshold.
        Low resilience lowers the effective threshold (easier to activate).
        Cascade: activated nodes can lower thresholds for connected nodes.
        """
        # Load tipping points once
        tp_map: dict[str, TippingPoint] = {
            tp.slug: tp for tp in TippingPoint.objects.filter(is_active=True)
        }

        # Resilience RAISES effective thresholds: a resilient ecosystem is harder to tip.
        # r=0.1 (low)  -> factor=1.04 (barely protected)
        # r=0.9 (high) -> factor=1.36 (well protected, needs 36% more pressure to tip)
        resilience_factor = 1.0 + (r * 0.4)

        # First pass: direct activation
        activated_slugs: dict[str, NodeActivation] = {}
        for slug, (base_threshold, _) in NODE_THRESHOLDS.items():
            effective_threshold = base_threshold * resilience_factor
            if climate_pressure >= effective_threshold:
                tp = tp_map.get(slug)
                if tp:
                    score = min(1.0, (climate_pressure - effective_threshold) / (1.0 - effective_threshold + 0.001))
                    activated_slugs[slug] = NodeActivation(
                        slug             = slug,
                        name             = tp.name,
                        domain           = tp.domain,
                        activation_score = round(score, 3),
                        triggered_by     = [],
                    )

        # Cascade pass: activated nodes lower thresholds for their targets
        relationships = TippingPointRelationship.objects.filter(
            source__slug__in=activated_slugs.keys()
        ).select_related('source', 'target')

        cascade_boost: dict[str, float] = {}
        for rel in relationships:
            source_node = activated_slugs.get(rel.source.slug)
            if source_node:
                boost = source_node.activation_score * (rel.strength / 5.0) * 0.2
                cascade_boost[rel.target.slug] = cascade_boost.get(rel.target.slug, 0) + boost

        # Second pass: cascade activations
        for slug, boost in cascade_boost.items():
            if slug in activated_slugs:
                # Already active, strengthen the score
                activated_slugs[slug].activation_score = min(
                    1.0, activated_slugs[slug].activation_score + boost
                )
            else:
                base_threshold, _ = NODE_THRESHOLDS.get(slug, (1.0, 1.0))
                effective_threshold = base_threshold * resilience_factor - boost
                if climate_pressure >= effective_threshold:
                    tp = tp_map.get(slug)
                    if tp:
                        # Find which nodes triggered this
                        triggering = [
                            r.source.slug for r in relationships
                            if r.target.slug == slug and r.source.slug in activated_slugs
                        ]
                        score = min(1.0, boost * 2)
                        activated_slugs[slug] = NodeActivation(
                            slug             = slug,
                            name             = tp.name,
                            domain           = tp.domain,
                            activation_score = round(score, 3),
                            triggered_by     = triggering,
                        )

        # Sort by activation score descending
        return sorted(activated_slugs.values(), key=lambda n: n.activation_score, reverse=True)

    def _suggest_interventions(
        self,
        m: float, ml: float,
        trust_score: float, delay_risk: float,
        climate_pressure: float, r: float,
    ) -> list[str]:
        suggestions = []

        if m > 0.6 and ml < 0.4:
            suggestions.append('Invest in media literacy education and public science communication.')
        if trust_score < 0.4:
            suggestions.append('Rebuild public trust through transparent, community-level climate communication.')
        if delay_risk > 0.6:
            suggestions.append('Accelerate policy timelines. Delayed action compounds climate pressure non-linearly.')
        if climate_pressure > 0.7:
            suggestions.append('Emissions reductions alone may not prevent cascades at this pressure level; adaptation planning is urgent.')
        if r < 0.4:
            suggestions.append('Strengthen ecosystem resilience through habitat restoration and biodiversity protection.')
        if climate_pressure < 0.4 and trust_score > 0.6:
            suggestions.append('Current trajectory appears manageable. Maintain or increase action to lock in gains.')
        if not suggestions:
            suggestions.append('Continue monitoring. Balanced inputs suggest moderate risk; sustained effort is key.')

        return suggestions

    def _build_narrative(
        self,
        trust_score: float,
        delay_risk: float,
        climate_pressure: float,
        activated: list[NodeActivation],
    ) -> str:
        n_activated = len(activated)
        level = self._risk_level(climate_pressure, n_activated)
        
        climate_change_trust = 'strong' if trust_score > 0.6 else 'weakened'
        lack_of_action = 'slowing' if trust_score > 0.6 else 'amplifying'

        intro = {
            'low':      'Under these conditions, cascading tipping-point interactions appear limited.',
            'moderate': 'Under these conditions, several tipping points are approaching their activation thresholds.',
            'high':     'Under these conditions, multiple tipping-point cascades are active and reinforcing each other.',
            'critical': 'Under these conditions, the simulation shows widespread tipping-point activation — a cascade state.',
        }[level]

        trust_note = (
            f'Public trust in climate science is {climate_change_trust}, '
            f'{lack_of_action} policy delays.'
        )

        if n_activated == 0:
            activated_note = 'No tipping point nodes are activated at these slider values.'
        elif n_activated <= 3:
            names = ', '.join(n.name for n in activated[:3])
            activated_note = f'Activated: {names}.'
        else:
            names = ', '.join(n.name for n in activated[:3])
            activated_note = f'Activated {n_activated} nodes, including {names}, and more.'

        return f'{intro} {trust_note} {activated_note}'

    @staticmethod
    def _risk_level(climate_pressure: float, n_activated: int) -> str:
        if climate_pressure < 0.3 or n_activated == 0:
            return 'low'
        elif climate_pressure < 0.5 or n_activated <= 3:
            return 'moderate'
        elif climate_pressure < 0.75 or n_activated <= 7:
            return 'high'
        else:
            return 'critical'
