"""
Tipping Points serializers
"""
from rest_framework import serializers
from .models import TippingPoint, TippingPointRelationship, SourceReference


class SourceReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SourceReference
        fields = ['id', 'url', 'title', 'notes']


class TippingPointRelationshipSerializer(serializers.ModelSerializer):
    source_slug = serializers.CharField(source='source.slug', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)
    target_slug = serializers.CharField(source='target.slug', read_only=True)
    target_name = serializers.CharField(source='target.name', read_only=True)

    class Meta:
        model  = TippingPointRelationship
        fields = [
            'id',
            'source_slug', 'source_name',
            'target_slug', 'target_name',
            'relationship_type', 'description',
            'strength', 'is_bidirectional',
        ]



# Card serializer. minimal fields for the explorer grid
class TippingPointCardSerializer(serializers.ModelSerializer):
    """Lightweight serializer for grid/list views."""

    class Meta:
        model  = TippingPoint
        fields = [
            'id', 'slug', 'name',
            'domain', 'domain_raw', 'scale', 'icon_label',
            'severity', 'near_term_status',
            'app_card_summary',
            'misinformation_angle',
            'display_order',
        ]


# Full detail serializer. all fields for the detail page
class TippingPointDetailSerializer(serializers.ModelSerializer):
    source_references    = SourceReferenceSerializer(many=True, read_only=True)
    outgoing_relationships = TippingPointRelationshipSerializer(many=True, read_only=True)
    incoming_relationships = TippingPointRelationshipSerializer(many=True, read_only=True)

    class Meta:
        model  = TippingPoint
        fields = [
            'id', 'slug', 'name',
            'domain', 'domain_raw', 'scale', 'icon_label',
            'severity', 'near_term_status', 'warming_context',
            'primary_causes', 'effects', 'interactions',
            'domino_summary', 'app_card_summary',
            'misinformation_angle', 'suggested_ui',
            'source_urls', 'source_references',
            'outgoing_relationships', 'incoming_relationships',
            'display_order', 'is_active',
            'created_at', 'updated_at',
        ]
