# infrastructure/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # DASHBOARD
    path('dashboard/summary/', views.get_dashboard_summary, name='dashboard_summary'),

    # VISTA SEMANAL
    path('horarios/semanales/', views.get_vista_semanal, name='vista_semanal'),

    # PRACTICANTES
    path('practicantes/', views.listar_practicantes, name='listar_practicantes'),
    
    # RUTA GET para obtener horario
    path('practicantes/<int:practicante_id>/horario/', views.get_horario_practicante, name='horario_practicante'),
    
    # RUTA POST/PUT para actualizar horario (solicitudes PUT/POST DEBEN usar el slash final)
    path('practicantes/<int:practicante_id>/horario/actualizar/', views.actualizar_horario_practicante, name='actualizar_horario_practicante'),

    # RECUPERACIONES
    path('recuperaciones/pendientes/', views.get_pendientes_aprobacion, name='pendientes_recuperacion'),
    path('recuperaciones/<int:id>/', views.get_detalle_recuperacion, name='detalle_recuperacion'),
    path('recuperaciones/<int:id>/aprobar/', views.aprobar_recuperacion, name='aprobar_recuperacion'),
    path('recuperaciones/<int:id>/rechazar/', views.rechazar_recuperacion, name='rechazar_recuperacion'),

    # REGISTRO CON EVIDENCIA
    path('practicantes/<int:practicante_id>/registrar/', views.registrar_horario_con_evidencia, name='registrar_horario_con_evidencia'),

    # SERVIDORES
    path('servidores/', views.get_servidores, name='get_servidores'),
]