from rest_framework import serializers
from .models import ClimateMetric, MetricDataPoint, StatisticCard


class MetricDataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model  = MetricDataPoint
        fields = ['year', 'value', 'note']


class ClimateMetricSerializer(serializers.ModelSerializer):
    data_points = MetricDataPointSerializer(many=True, read_only=True)

    class Meta:
        model  = ClimateMetric
        fields = [
            'id', 'slug', 'name', 'metric_type', 'unit',
            'description', 'source_name', 'source_url',
            'last_updated', 'data_points',
        ]


class StatisticCardSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StatisticCard
        fields = ['id', 'title', 'value', 'context', 'source_name', 'source_url', 'display_order']
