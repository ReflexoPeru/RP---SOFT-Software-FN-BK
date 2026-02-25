from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/practicantes/', include('apps.practicantes.infrastructure.urls')),
    path('api/bot/', include('apps.bot_discord.infrastructure.urls')),

    # Rutas de gestion-horario
    path('api/v1/', include('apps.gestion.infrastructure.urls')),
    path('api/puntualidad/', include('apps.puntualidad.infrastructure.urls')),

    # Rutas de reportes (rama main)
    path("api/reportes/", include(("apps.reportes.infrastructure.urls", "reportes"), namespace="reportes")),
]
