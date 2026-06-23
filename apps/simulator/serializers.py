from rest_framework import serializers
from .models import SimulationScenario, SimulationRun, ActivatedNode


class SimulationScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SimulationScenario
        fields = [
            'id', 'slug', 'name', 'description', 'is_featured',
            'default_misinformation', 'default_media_literacy',
            'default_public_trust', 'default_policy_speed',
            'default_emissions', 'default_resilience',
        ]


class SimulationInputSerializer(serializers.Serializer):
    """Validates the POST body for /api/simulator/run/."""
    misinformation = serializers.IntegerField(min_value=0, max_value=100)
    media_literacy = serializers.IntegerField(min_value=0, max_value=100)
    public_trust   = serializers.IntegerField(min_value=0, max_value=100)
    policy_speed   = serializers.IntegerField(min_value=0, max_value=100)
    emissions      = serializers.IntegerField(min_value=0, max_value=100)
    resilience     = serializers.IntegerField(min_value=0, max_value=100)
    scenario_slug  = serializers.SlugField(required=False, allow_blank=True)
    save_run       = serializers.BooleanField(default=False)


class ActivatedNodeSerializer(serializers.Serializer):
    slug             = serializers.CharField()
    name             = serializers.CharField()
    domain           = serializers.CharField()
    activation_score = serializers.FloatField()
    triggered_by     = serializers.ListField(child=serializers.CharField())


class SimulationResultSerializer(serializers.Serializer):
    trust_score      = serializers.FloatField()
    delay_risk       = serializers.FloatField()
    climate_pressure = serializers.FloatField()
    activated_nodes  = ActivatedNodeSerializer(many=True)
    interventions    = serializers.ListField(child=serializers.CharField())
    narrative        = serializers.CharField()
    risk_level       = serializers.CharField()
    run_id           = serializers.IntegerField(required=False, allow_null=True)
