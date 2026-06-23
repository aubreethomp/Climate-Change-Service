"""
Metrics models
==============
Supports the Evidence Dashboard with curated climate statistics.
Data is loaded via the seed_metrics management command.
External API calls (NASA, Our World in Data) are handled by scripts/ utilities.
"""

from django.db import models


class ClimateMetric(models.Model):
    """
    A named time-series metric (e.g., 'Global CO₂', 'Temperature Anomaly').
    """
    METRIC_TYPES = [
        ('co2_emissions',       'CO₂ Emissions'),
        ('temperature_anomaly', 'Temperature Anomaly'),
        ('sea_level_rise',      'Sea Level Rise'),
        ('arctic_sea_ice',      'Arctic Sea Ice Extent'),
        ('ocean_heat',          'Ocean Heat Content'),
        ('glacier_mass',        'Glacier Mass Balance'),
    ]

    slug        = models.SlugField(unique=True)
    name        = models.CharField(max_length=150)
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    unit        = models.CharField(max_length=50, help_text='e.g. ppm, °C, mm, km²')
    description = models.TextField(blank=True)
    source_name = models.CharField(max_length=200, blank=True)
    source_url  = models.URLField(max_length=500, blank=True)
    last_updated = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['metric_type', 'name']

    def __str__(self):
        return self.name


class MetricDataPoint(models.Model):
    """One year/value row for a ClimateMetric."""
    metric = models.ForeignKey(ClimateMetric, related_name='data_points', on_delete=models.CASCADE)
    year   = models.IntegerField()
    value  = models.FloatField()
    note   = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('metric', 'year')
        ordering        = ['year']

    def __str__(self):
        return f'{self.metric.slug} {self.year}: {self.value}'


class StatisticCard(models.Model):
    """
    A single headline statistic for the dashboard (e.g., '420 ppm – current CO₂').
    Updated manually or via a management command.
    """
    title       = models.CharField(max_length=150)
    value       = models.CharField(max_length=100, help_text='Display value, e.g. "420 ppm"')
    context     = models.TextField(help_text='One-sentence context for the number.')
    source_name = models.CharField(max_length=200, blank=True)
    source_url  = models.URLField(max_length=500, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f'{self.title}: {self.value}'
