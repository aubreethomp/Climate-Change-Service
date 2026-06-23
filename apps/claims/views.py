"""
Claims views
============
Powers the Media Literacy Lab quiz flow.
"""

import random

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ClimateClaim, MisinformationTechnique
from .serializers import (
    ClimateClaimSerializer,
    ClimateClaimQuizSerializer,
    MisinformationTechniqueSerializer,
    AnswerCheckSerializer,
)


class ClimateClaimViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list   → GET /api/claims/
    detail → GET /api/claims/{id}/   (full – use after reveal)

    Extra actions:
      GET  /api/claims/random/           – random quiz card (redacted)
      POST /api/claims/{id}/check-answer/ – evaluate user answer
      GET  /api/claims/search/           – keyword search (?q=)
    """
    queryset = ClimateClaim.objects.filter(is_active=True).prefetch_related(
        'evidence', 'techniques', 'related_tipping_points', 'topic'
    )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClimateClaimSerializer
        return ClimateClaimQuizSerializer

    # Random quiz card
    @action(detail=False, url_path='random', methods=['get'])
    def random(self, request):
        """
        GET /api/claims/random/?difficulty=medium
        Returns a single claim card with the answer redacted.
        """
        qs = self.get_queryset()
        difficulty = request.query_params.get('difficulty')
        topic_id   = request.query_params.get('topic')

        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        if topic_id:
            qs = qs.filter(topic_id=topic_id)

        ids = list(qs.values_list('id', flat=True))
        if not ids:
            return Response({'detail': 'No claims found.'}, status=status.HTTP_404_NOT_FOUND)

        claim = qs.get(id=random.choice(ids))
        serializer = ClimateClaimQuizSerializer(claim)
        return Response(serializer.data)

    # Answer check
    @action(detail=True, url_path='check-answer', methods=['post'])
    def check_answer(self, request, pk=None):
        """
        POST /api/claims/{id}/check-answer/
        Body: { "user_answer": "refutes", "user_technique": "cherry_picking" }
        Returns correctness + full reveal data.
        """
        claim = self.get_object()

        input_serializer = AnswerCheckSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user_answer    = input_serializer.validated_data['user_answer']
        user_technique = input_serializer.validated_data.get('user_technique', '')

        label_correct = (user_answer == claim.label)

        # Check technique match (partial – technique slug or name substring)
        correct_techniques = list(claim.techniques.values_list('slug', flat=True))
        technique_correct = user_technique.lower() in [t.lower() for t in correct_techniques] if user_technique else None

        full_data = ClimateClaimSerializer(claim).data

        return Response({
            'label_correct':     label_correct,
            'technique_correct': technique_correct,
            'correct_label':     claim.label,
            'correct_techniques': correct_techniques,
            'explanation':        claim.explanation,
            'claim':              full_data,
        })

    # Keyword search (TF-IDF stub – replace with sentence-transformer later)
    @action(detail=False, url_path='search', methods=['get'])
    def search(self, request):
        """
        GET /api/claims/search/?q=natural+variability
        Simple icontains search; upgrade to TF-IDF / embedding similarity later.
        """
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response({'detail': 'Provide ?q= query param.'}, status=400)

        results = ClimateClaim.objects.filter(
            is_active=True,
            claim_text__icontains=q,
        )[:10]

        serializer = ClimateClaimQuizSerializer(results, many=True)
        return Response(serializer.data)


class MisinformationTechniqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/claims/techniques/
    """
    queryset = MisinformationTechnique.objects.all()
    serializer_class = MisinformationTechniqueSerializer
