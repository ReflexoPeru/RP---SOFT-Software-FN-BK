from django.urls import path
from .views import (
    resumen_puntualidad, 
    alertas_puntualidad, 
    practicantes_puntualidad,
    practicantes_activos,
    justificaciones,
    recuperaciones,
    crear_justificacion,
    aprobar_justificacion,
    rechazar_justificacion
)

urlpatterns = [
    path('resumen/', resumen_puntualidad),
    path('alertas/', alertas_puntualidad),
    path('practicantes/', practicantes_puntualidad),
    path('practicantes/activos/', practicantes_activos),
    path('justificaciones/', justificaciones),
    path('justificaciones/crear/', crear_justificacion),
    path('justificaciones/<int:pk>/aprobar/', aprobar_justificacion),
    path('justificaciones/<int:pk>/rechazar/', rechazar_justificacion),
    path('recuperaciones/', recuperaciones),
]
