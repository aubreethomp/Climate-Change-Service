"""
Simulator views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SimulationScenario, SimulationRun, ActivatedNode
from .serializers import (
    SimulationScenarioSerializer,
    SimulationInputSerializer,
    SimulationResultSerializer,
)
from .services import DominoSimulationService
from apps.tipping_points.models import TippingPoint


class ScenarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/simulator/scenarios/
    GET /api/simulator/scenarios/{slug}/
    """
    queryset         = SimulationScenario.objects.all()
    serializer_class = SimulationScenarioSerializer
    lookup_field     = 'slug'


class RunSimulatorView(APIView):
    """
    POST /api/simulator/run/
    Body: SimulationInputSerializer fields
    Returns: full SimulationResult
    """

    def post(self, request):
        input_serializer = SimulationInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        service = DominoSimulationService()
        result  = service.run(
            misinformation = data['misinformation'],
            media_literacy = data['media_literacy'],
            public_trust   = data['public_trust'],
            policy_speed   = data['policy_speed'],
            emissions      = data['emissions'],
            resilience     = data['resilience'],
        )

        run_id = None

        # Persist the run if requested (for share/revisit links)
        if data.get('save_run'):
            scenario = None
            if data.get('scenario_slug'):
                try:
                    scenario = SimulationScenario.objects.get(slug=data['scenario_slug'])
                except SimulationScenario.DoesNotExist:
                    pass

            run = SimulationRun.objects.create(
                session_key     = request.session.session_key or '',
                scenario        = scenario,
                misinformation  = data['misinformation'],
                media_literacy  = data['media_literacy'],
                public_trust    = data['public_trust'],
                policy_speed    = data['policy_speed'],
                emissions       = data['emissions'],
                resilience      = data['resilience'],
                trust_score     = result.trust_score,
                delay_risk      = result.delay_risk,
                climate_pressure= result.climate_pressure,
                narrative       = result.narrative,
            )

            # Store activated nodes
            tp_map = {tp.slug: tp for tp in TippingPoint.objects.filter(is_active=True)}
            for node in result.activated_nodes:
                tp = tp_map.get(node.slug)
                if tp:
                    ActivatedNode.objects.create(
                        run              = run,
                        tipping_point    = tp,
                        activation_score = node.activation_score,
                        triggered_by     = ','.join(node.triggered_by),
                    )
            run_id = run.id

        output = {
            'trust_score':       result.trust_score,
            'delay_risk':        result.delay_risk,
            'climate_pressure':  result.climate_pressure,
            'activated_nodes': [
                {
                    'slug':             n.slug,
                    'name':             n.name,
                    'domain':           n.domain,
                    'activation_score': n.activation_score,
                    'triggered_by':     n.triggered_by,
                }
                for n in result.activated_nodes
            ],
            'interventions': result.interventions,
            'narrative':     result.narrative,
            'risk_level':    result.risk_level,
            'run_id':        run_id,
        }

        serializer = SimulationResultSerializer(data=output)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
