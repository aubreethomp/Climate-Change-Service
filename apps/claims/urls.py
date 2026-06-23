from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClimateClaimViewSet, MisinformationTechniqueViewSet

app_name = 'claims'

router = DefaultRouter()
router.register(r'techniques', MisinformationTechniqueViewSet, basename='technique')
router.register(r'',           ClimateClaimViewSet,            basename='claim')

urlpatterns = [
    path('', include(router.urls)),
]
