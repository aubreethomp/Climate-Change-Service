from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScenarioViewSet, RunSimulatorView

app_name = 'simulator'

router = DefaultRouter()
router.register(r'scenarios', ScenarioViewSet, basename='scenario')

urlpatterns = [
    path('run/', RunSimulatorView.as_view(), name='run'),
    path('', include(router.urls)),
]
