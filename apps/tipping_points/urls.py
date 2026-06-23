from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TippingPointViewSet

app_name = 'tipping_points'

router = DefaultRouter()
router.register(r'', TippingPointViewSet, basename='tippingpoint')

urlpatterns = [
    path('', include(router.urls)),
]
