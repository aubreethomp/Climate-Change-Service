from rest_framework import serializers
from .models import ClimateClaim, EvidenceSentence, MisinformationTechnique, ClaimTopic


class MisinformationTechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model  = MisinformationTechnique
        fields = ['id', 'slug', 'name', 'description', 'example', 'media_literacy_tip', 'flicc_category']


class EvidenceSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = EvidenceSentence
        fields = ['id', 'text', 'stance', 'source_name', 'source_url']


class ClaimTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ClaimTopic
        fields = ['id', 'name', 'description']


class ClimateClaimSerializer(serializers.ModelSerializer):
    """Full serializer for detail / reveal view."""
    evidence              = EvidenceSentenceSerializer(many=True, read_only=True)
    techniques            = MisinformationTechniqueSerializer(many=True, read_only=True)
    topic                 = ClaimTopicSerializer(read_only=True)
    related_tipping_points = serializers.SerializerMethodField()

    class Meta:
        model  = ClimateClaim
        fields = [
            'id', 'claim_text', 'label', 'topic',
            'explanation', 'difficulty',
            'evidence', 'techniques',
            'related_tipping_points',
            'source_dataset',
        ]

    def get_related_tipping_points(self, obj):
        return [
            {'slug': tp.slug, 'name': tp.name}
            for tp in obj.related_tipping_points.all()
        ]


class ClimateClaimQuizSerializer(serializers.ModelSerializer):
    """
    Redacted serializer for the quiz card – hides label, evidence, and explanation
    so the user can guess before the reveal.
    """
    topic = ClaimTopicSerializer(read_only=True)

    class Meta:
        model  = ClimateClaim
        fields = ['id', 'claim_text', 'topic', 'difficulty']


class AnswerCheckSerializer(serializers.Serializer):
    """Request body for POST /api/claims/{id}/check-answer/"""
    user_answer = serializers.ChoiceField(
        choices=['supports', 'refutes', 'not_enough_info', 'misleading']
    )
    user_technique = serializers.CharField(required=False, allow_blank=True)
