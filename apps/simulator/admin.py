from django.contrib import admin
from .models import SimulationScenario, SimulationRun, ActivatedNode


class ActivatedNodeInline(admin.TabularInline):
    model = ActivatedNode
    extra = 0
    readonly_fields = ['tipping_point', 'activation_score', 'triggered_by']


@admin.register(SimulationScenario)
class SimulationScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SimulationRun)
class SimulationRunAdmin(admin.ModelAdmin):
    list_display  = ['pk', 'created_at', 'climate_pressure', 'risk_level_display', 'scenario']
    list_filter   = ['scenario']
    inlines       = [ActivatedNodeInline]
    readonly_fields = ['trust_score', 'delay_risk', 'climate_pressure', 'narrative', 'created_at']

    def risk_level_display(self, obj):
        from apps.simulator.services import DominoSimulationService
        n_active = obj.activated_nodes.count()
        return DominoSimulationService._risk_level(obj.climate_pressure / 100, n_active)
    risk_level_display.short_description = 'Risk Level'
