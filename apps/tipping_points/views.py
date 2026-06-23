"""
Tipping Points views
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TippingPoint, TippingPointRelationship
from .serializers import (
    TippingPointCardSerializer,
    TippingPointDetailSerializer,
    TippingPointRelationshipSerializer,
)


class TippingPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list  -> GET /api/tipping-points/
    detail -> GET /api/tipping-points/{slug}/
    """
    queryset = TippingPoint.objects.filter(is_active=True).prefetch_related(
        'source_references',
        'outgoing_relationships__target',
        'incoming_relationships__source',
    )
    lookup_field = 'slug'

    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['name', 'domain_raw', 'primary_causes', 'effects', 'app_card_summary']
    ordering_fields  = ['severity', 'display_order', 'name']
    ordering         = ['display_order']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TippingPointDetailSerializer
        return TippingPointCardSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        domain   = self.request.query_params.get('domain')
        severity = self.request.query_params.get('severity')
        if domain:
            qs = qs.filter(domain__icontains=domain)
        if severity:
            qs = qs.filter(severity__iexact=severity)
        return qs

    # return relationships as graph-ready nodes/edges
    @action(detail=False, url_path='graph', methods=['get'])
    def graph(self, request):
        """
        GET /api/tipping-points/graph/
        Returns all tipping points as nodes and all relationships as edges
        in a format ready for a frontend graph library (e.g. D3, Cytoscape).
        """
        nodes = TippingPoint.objects.filter(is_active=True).values(
            'slug', 'name', 'domain', 'severity'
        )
        edges = TippingPointRelationship.objects.select_related('source', 'target').all()
        edge_data = [
            {
                'source': e.source.slug,
                'target': e.target.slug,
                'type':   e.relationship_type,
                'strength': e.strength,
            }
            for e in edges
        ]
        return Response({'nodes': list(nodes), 'edges': edge_data})

    # relationships for a single tipping point
    @action(detail=True, url_path='relationships', methods=['get'])
    def relationships(self, request, slug=None):
        """
        GET /api/tipping-points/{slug}/relationships/
        """
        tp = self.get_object()
        outgoing = tp.outgoing_relationships.select_related('target')
        incoming = tp.incoming_relationships.select_related('source')
        return Response({
            'outgoing': TippingPointRelationshipSerializer(outgoing, many=True).data,
            'incoming': TippingPointRelationshipSerializer(incoming, many=True).data,
        })

    # filter by domain
    @action(detail=False, url_path='by-domain', methods=['get'])
    def by_domain(self, request):
        """
        GET /api/tipping-points/by-domain/
        Returns tipping points grouped by domain for the filter sidebar.
        """
        from django.db.models import Count
        domains = (
            TippingPoint.objects
            .filter(is_active=True)
            .values('domain', 'domain_raw')
            .annotate(count=Count('id'))
            .order_by('domain')
        )
        return Response(list(domains))
