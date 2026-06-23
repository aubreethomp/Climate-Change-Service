from django.contrib import admin
from .models import ClimateClaim, EvidenceSentence, MisinformationTechnique, ClaimTopic, ClaimTechniqueLink


class EvidenceInline(admin.TabularInline):
    model = EvidenceSentence
    extra = 1


class TechniqueInline(admin.TabularInline):
    model = ClaimTechniqueLink
    extra = 1


@admin.register(ClimateClaim)
class ClimateClaimAdmin(admin.ModelAdmin):
    list_display  = ['claim_text_short', 'label', 'topic', 'difficulty', 'is_active']
    list_filter   = ['label', 'difficulty', 'topic', 'is_active']
    search_fields = ['claim_text', 'explanation']
    inlines       = [EvidenceInline, TechniqueInline]

    def claim_text_short(self, obj):
        return obj.claim_text[:80]
    claim_text_short.short_description = 'Claim'


@admin.register(MisinformationTechnique)
class MisinformationTechniqueAdmin(admin.ModelAdmin):
    list_display  = ['name', 'technique', 'flicc_category']
    search_fields = ['name', 'description', 'example']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ClaimTopic)
class ClaimTopicAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name']


@admin.register(EvidenceSentence)
class EvidenceSentenceAdmin(admin.ModelAdmin):
    list_display  = ['claim', 'stance', 'text_short']
    list_filter   = ['stance']

    def text_short(self, obj):
        return obj.text[:60]
    text_short.short_description = 'Text'
