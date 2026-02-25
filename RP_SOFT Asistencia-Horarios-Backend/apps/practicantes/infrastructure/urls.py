from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PracticanteViewSet

app_name = "practicantes"

router = DefaultRouter()
router.register(r'', PracticanteViewSet, basename='practicante')

urlpatterns = [
    path('', include(router.urls)),
    
    # Estas líneas ahora encuentran las funciones definidas en views.py
    path("advertencias/mes/", views.advertencias_mes_actual, name="warnings-current"),
    path("advertencias/historico/", views.advertencias_historico, name="warnings-history"),
    path("permisos/semana/", views.permisos_semana_actual, name="permissions-week"),
    path("permisos/practicante/", views.permisos_por_practicante, name="permissions-employee"),
    path("exportar/semanal/", views.export_reporte_semanal, name="export-weekly"),
    path("exportar/mensual/", views.export_reporte_mensual, name="export-monthly"),
    path("cumplimiento/detalle/", views.detalle_cumplimiento_horas, name="compliance-detail"),
    path("resumen/global/", views.resumen_global_horas, name="global-summary"),
]
