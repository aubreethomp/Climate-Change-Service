"""
Tipping Points models
=====================
Two primary models:
  - TippingPoint       : one card / detail page per tipping point
  - TippingPointRelationship : directed edge between two tipping points for the domino graph
"""

from django.db import models


class TippingPoint(models.Model):
    """
    Each row in the seed CSV maps to one TippingPoint record.
    All text fields are kept intentionally wide so the frontend can choose
    how much to display on a card vs. a detail page.
    """

   # Identity
    slug = models.SlugField(
        unique=True,
        help_text="URL-safe identifier, e.g. 'gis_collapse'. Sourced from CSV id column.",
    )
    name = models.CharField(max_length=200)

    # Classification
    DOMAIN_CHOICES = [
        ('cryosphere',                   'Cryosphere'),
        ('biosphere',                     'Biosphere'),
        ('ocean_atmosphere_circulation',  'Ocean-atmosphere circulation'),
        ('cryosphere_carbon_cycle',       'Cryosphere / Carbon cycle'),
        ('biosphere_ocean',               'Biosphere / Ocean'),
        ('cryosphere_ocean',              'Cryosphere / Ocean'),
        ('cryosphere_water',              'Cryosphere / Water systems'),
        ('atmosphere_hydrology',          'Atmosphere / Hydrology'),
        ('biosphere_hydrology',           'Biosphere / Hydrology'),
        ('biosphere_freshwater',          'Biosphere / Freshwater'),
        ('biosphere_food',                'Biosphere / Food systems'),
        ('biosphere_coastal',             'Biosphere / Coastal systems'),
    ]
    domain = models.CharField(max_length=100, choices=DOMAIN_CHOICES)
    domain_raw = models.CharField(
        max_length=150,
        blank=True,
        help_text="Raw domain string from CSV, kept for display.",
    )

    SCALE_CHOICES = [
        ('global_core',   'Global core'),
        ('regional',      'Regional'),
        ('local',         'Local'),
        ('multi_scale',   'Multi-scale'),
    ]
    scale = models.CharField(max_length=100)

    # Display / UI
    icon_label = models.CharField(max_length=100, blank=True)

    # Severity 
    SEVERITY_CHOICES = [
        ('extreme', 'Extreme'),
        ('high',    'High'),
        ('medium',  'Medium'),
        ('low',     'Low'),
    ]
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES)

    near_term_status = models.TextField(
        help_text="Short description of likelihood at current/near-term warming."
    )
    warming_context = models.TextField(
        help_text="Longer scientific context and warming level thresholds."
    )

    # Cause / effect / interactions
    primary_causes = models.TextField()
    effects        = models.TextField()
    interactions   = models.TextField(
        help_text="How this tipping point interacts with or amplifies others."
    )

    # tab summaries
    domino_summary  = models.TextField(
        help_text="Short narrative of the domino chain this tipping point initiates."
    )
    app_card_summary = models.TextField(
        help_text="Two-sentence card blurb shown in the explorer grid."
    )

    # Media literacy
    misinformation_angle = models.TextField(
        help_text="Common misleading claim or framing associated with this tipping point."
    )

    # UI hints
    suggested_ui = models.TextField(
        blank=True,
        help_text="Designer notes: animations, icons, downstream domino suggestions.",
    )

   # Sources
    source_urls = models.TextField(
        blank=True,
        help_text="Pipe-separated list of source URLs. Parsed into SourceReference on save.",
    )

    # Metadata
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name        = 'Tipping Point'
        verbose_name_plural = 'Tipping Points'

    def __str__(self):
        return self.name

    def get_source_url_list(self):
        """Return source_urls as a Python list, splitting on ' | '."""
        if not self.source_urls:
            return []
        return [u.strip() for u in self.source_urls.split('|') if u.strip()]


# Relationship graph
class TippingPointRelationship(models.Model):
    """
    A directed edge in the domino graph.
    source → target means 'source tipping point can trigger or amplify target'.
    """

    RELATIONSHIP_TYPES = [
        ('carbon_feedback',         'Carbon feedback'),
        ('freshwater_circulation',  'Freshwater / circulation interaction'),
        ('rainfall_recycling',      'Rainfall recycling'),
        ('habitat_livelihood',      'Habitat / livelihood cascade'),
        ('sea_level',               'Sea-level cascade'),
        ('temperature_amplification', 'Temperature amplification'),
        ('ecosystem_cascade',       'Ecosystem cascade'),
        ('ocean_chemistry',         'Ocean chemistry change'),
        ('albedo_feedback',         'Albedo feedback'),
        ('monsoon_shift',           'Monsoon / precipitation shift'),
        ('other',                   'Other'),
    ]

    source = models.ForeignKey(
        TippingPoint,
        related_name='outgoing_relationships',
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        TippingPoint,
        related_name='incoming_relationships',
        on_delete=models.CASCADE,
    )
    relationship_type = models.CharField(max_length=100, choices=RELATIONSHIP_TYPES)
    description = models.TextField(blank=True)

    # 1 = weak influence, 5 = strong / well-documented cascade
    strength = models.IntegerField(
        default=1,
        choices=[(i, str(i)) for i in range(1, 6)],
    )

    is_bidirectional = models.BooleanField(
        default=False,
        help_text="True if the influence runs strongly in both directions.",
    )

    class Meta:
        unique_together = ('source', 'target', 'relationship_type')
        verbose_name        = 'Tipping Point Relationship'
        verbose_name_plural = 'Tipping Point Relationships'

    def __str__(self):
        return f'{self.source.slug} → {self.target.slug} ({self.relationship_type})'


# Source references (normalised from the pipe-separated source_urls field)
class SourceReference(models.Model):
    tipping_point = models.ForeignKey(
        TippingPoint,
        related_name='source_references',
        on_delete=models.CASCADE,
    )
    url   = models.URLField(max_length=500)
    title = models.CharField(max_length=300, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['id']
        verbose_name        = 'Source Reference'
        verbose_name_plural = 'Source References'

    def __str__(self):
        return self.url
