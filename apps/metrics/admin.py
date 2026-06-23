from django.contrib import admin
from .models import ClimateMetric, MetricDataPoint, StatisticCard


class DataPointInline(admin.TabularInline):
    model = MetricDataPoint
    extra = 0


@admin.register(ClimateMetric)
class ClimateMetricAdmin(admin.ModelAdmin):
    list_display  = ['name', 'metric_type', 'unit', 'last_updated']
    prepopulated_fields = {'slug': ('name',)}
    inlines       = [DataPointInline]


@admin.register(StatisticCard)
class StatisticCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
