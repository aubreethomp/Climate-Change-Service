from django.contrib import admin
from .models import TippingPoint, TippingPointRelationship, SourceReference


class SourceReferenceInline(admin.TabularInline):
    model = SourceReference
    extra = 1


class OutgoingRelationshipInline(admin.TabularInline):
    model = TippingPointRelationship
    fk_name = 'source'
    extra   = 1
    verbose_name        = 'Outgoing relationship'
    verbose_name_plural = 'Outgoing relationships'


@admin.register(TippingPoint)
class TippingPointAdmin(admin.ModelAdmin):
    list_display  = ['name', 'domain_raw', 'severity', 'scale', 'display_order', 'is_active']
    list_filter   = ['domain', 'severity', 'is_active']
    search_fields = ['name', 'slug', 'primary_causes', 'effects']
    prepopulated_fields = {'slug': ('name',)}
    ordering      = ['display_order']
    inlines       = [SourceReferenceInline, OutgoingRelationshipInline]
    fieldsets = (
        ('Identity', {'fields': ('slug', 'name', 'domain', 'domain_raw', 'scale', 'display_order', 'is_active')}),
        ('Display', {'fields': ('icon_label',)}),
        ('Status', {'fields': ('severity', 'near_term_status', 'warming_context')}),
        ('Science', {'fields': ('primary_causes', 'effects', 'interactions')}),
        ('App Content', {'fields': ('domino_summary', 'app_card_summary', 'misinformation_angle', 'suggested_ui')}),
        ('Sources', {'fields': ('source_urls',)}),
    )


@admin.register(TippingPointRelationship)
class TippingPointRelationshipAdmin(admin.ModelAdmin):
    list_display  = ['source', 'target', 'relationship_type', 'strength', 'is_bidirectional']
    list_filter   = ['relationship_type', 'strength']
    search_fields = ['source__name', 'target__name']


@admin.register(SourceReference)
class SourceReferenceAdmin(admin.ModelAdmin):
    list_display  = ['tipping_point', 'url', 'title']
    search_fields = ['url', 'title']
