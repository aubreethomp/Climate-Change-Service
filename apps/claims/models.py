"""
Claims models
=============
Powers the Media Literacy Lab.

ClimateClaim          – one quiz question (sourced from CLIMATE-FEVER)
EvidenceSentence      – evidence sentences linked to a claim
MisinformationTechnique – FLICC/CARDS fallacy types
ClaimTechniqueLink    – many-to-many between claims and techniques
"""

from django.db import models
from apps.tipping_points.models import TippingPoint


class MisinformationTechnique(models.Model):
    """
    A reasoning fallacy or contrarian technique used in climate misinformation.
    Based on FLICC/CARDS taxonomy.
    """

    TECHNIQUE_CHOICES = [
        ('cherry_picking',          'Cherry-picking'),
        ('fake_expert',             'Fake expert'),
        ('conspiracy_framing',      'Conspiracy framing'),
        ('false_balance',           'False balance'),
        ('anecdotal_evidence',      'Anecdotal evidence'),
        ('oversimplification',      'Oversimplification'),
        ('impossible_expectations', 'Impossible expectations'),
        ('misrepresentation',       'Misrepresentation'),
        ('slothful_induction',      'Slothful induction'),
        ('red_herring',             'Red herring'),
        ('appeal_to_nature',        'Appeal to nature'),
        ('moving_goalposts',        'Moving goalposts'),
        ('other',                   'Other'),
    ]

    slug        = models.SlugField(unique=True)
    name        = models.CharField(max_length=100)
    technique   = models.CharField(max_length=60, choices=TECHNIQUE_CHOICES, blank=True)
    description = models.TextField()
    example     = models.TextField(help_text='A concrete example of this technique in climate discourse.')
    media_literacy_tip = models.TextField(
        help_text='How to spot and counter this technique.'
    )
    flicc_category = models.CharField(
        max_length=100, blank=True,
        help_text='FLICC/CARDS category label if applicable.',
    )

    class Meta:
        ordering = ['name']
        verbose_name        = 'Misinformation Technique'
        verbose_name_plural = 'Misinformation Techniques'

    def __str__(self):
        return self.name


class ClaimTopic(models.Model):
    """
    Broad topic grouping for claims (e.g. 'Sea level', 'Arctic', 'Attribution').
    """
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ClimateClaim(models.Model):
    """
    One climate-change claim that users evaluate in the Media Literacy Lab.
    Intended to be populated from CLIMATE-FEVER or similar public datasets.
    """

    LABEL_CHOICES = [
        ('supports',             'Supports'),       # evidence supports claim
        ('refutes',              'Refutes'),         # evidence refutes claim
        ('not_enough_info',      'Not enough info'), # NEI
        ('misleading',           'Misleading'),      # partially true but framed to mislead
    ]

    claim_text = models.TextField()
    label      = models.CharField(max_length=20, choices=LABEL_CHOICES)

    topic = models.ForeignKey(
        ClaimTopic,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='claims',
    )

    # Link to related tipping point(s)
    related_tipping_points = models.ManyToManyField(
        TippingPoint,
        blank=True,
        related_name='related_claims',
        help_text='Which tipping points does this claim relate to?',
    )

    # Misinformation technique(s) used (may be empty for accurate claims)
    techniques = models.ManyToManyField(
        MisinformationTechnique,
        through='ClaimTechniqueLink',
        blank=True,
        related_name='claims',
    )

    # Source dataset metadata
    source_dataset = models.CharField(
        max_length=100, blank=True,
        help_text='e.g. CLIMATE-FEVER, hand-curated',
    )
    source_id = models.CharField(
        max_length=100, blank=True,
        help_text='Original ID in the source dataset for traceability.',
    )

    # Quiz UX helpers
    explanation = models.TextField(
        blank=True,
        help_text='Plain-language explanation shown after the user answers.',
    )
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium',
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        verbose_name        = 'Climate Claim'
        verbose_name_plural = 'Climate Claims'

    def __str__(self):
        return self.claim_text[:80]


class EvidenceSentence(models.Model):
    """
    One piece of evidence linked to a ClimateClaim.
    CLIMATE-FEVER provides up to 5 evidence sentences per claim.
    """

    STANCE_CHOICES = [
        ('supports',        'Supports'),
        ('refutes',         'Refutes'),
        ('not_enough_info', 'Not enough info'),
    ]

    claim       = models.ForeignKey(ClimateClaim, related_name='evidence', on_delete=models.CASCADE)
    text        = models.TextField()
    stance      = models.CharField(max_length=20, choices=STANCE_CHOICES)
    source_name = models.CharField(max_length=255, blank=True)
    source_url  = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name        = 'Evidence Sentence'
        verbose_name_plural = 'Evidence Sentences'

    def __str__(self):
        return f'[{self.stance}] {self.text[:60]}'


class ClaimTechniqueLink(models.Model):
    """Through table for Claim ↔ MisinformationTechnique with notes."""
    claim     = models.ForeignKey(ClimateClaim, on_delete=models.CASCADE)
    technique = models.ForeignKey(MisinformationTechnique, on_delete=models.CASCADE)
    notes     = models.TextField(blank=True)

    class Meta:
        unique_together = ('claim', 'technique')

    def __str__(self):
        return f'{self.claim_id} ↔ {self.technique.name}'
