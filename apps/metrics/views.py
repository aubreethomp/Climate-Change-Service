from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ClimateMetric, StatisticCard
from .serializers import ClimateMetricSerializer, StatisticCardSerializer


class ClimateMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/metrics/
    GET /api/metrics/{slug}/
    GET /api/metrics/stat-cards/
    """
    queryset     = ClimateMetric.objects.prefetch_related('data_points').all()
    serializer_class = ClimateMetricSerializer
    lookup_field = 'slug'

    @action(detail=False, url_path='stat-cards', methods=['get'])
    def stat_cards(self, request):
        cards = StatisticCard.objects.filter(is_active=True)
        serializer = StatisticCardSerializer(cards, many=True)
        return Response(serializer.data)
