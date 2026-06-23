from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClimateMetricViewSet

app_name = 'metrics'

router = DefaultRouter()
router.register(r'', ClimateMetricViewSet, basename='metric')

urlpatterns = [path('', include(router.urls))]
