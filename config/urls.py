from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API namespaces
    path('api/tipping-points/', include('apps.tipping_points.urls', namespace='tipping_points')),
    path('api/claims/',         include('apps.claims.urls',          namespace='claims')),
    path('api/simulator/',      include('apps.simulator.urls',       namespace='simulator')),
    path('api/metrics/',        include('apps.metrics.urls',         namespace='metrics')),
]
