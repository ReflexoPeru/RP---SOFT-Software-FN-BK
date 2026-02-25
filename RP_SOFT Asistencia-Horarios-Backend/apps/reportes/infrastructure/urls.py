from django.urls import path
from .views import (
    DashboardSummaryView,
    AdvertenciasMesActualView,
    HistorialAdvertenciasView,
    PermisosSemanaActualView,
    ResumenPermisosPracticanteView,
    ResumenGlobalHorasView,
    DetalleCumplimientoHorasView,
    export_reporte_semanal,
    export_reporte_mensual,
)

app_name = "reportes"

urlpatterns = [
    path("summary/", DashboardSummaryView.as_view(), name="summary"),
    path("advertencias/mes/", AdvertenciasMesActualView.as_view(), name="advertencias_mes_actual"),
    path("advertencias/historico/", HistorialAdvertenciasView.as_view(), name="advertencias_historico"),
    path("permisos/semana/", PermisosSemanaActualView.as_view(), name="permisos_semana_actual"),
    path("permisos/practicante/", ResumenPermisosPracticanteView.as_view(), name="permisos_por_practicante"),
    path("horas/resumen/", ResumenGlobalHorasView.as_view(), name="resumen_global_horas"),
    path("horas/detalle/", DetalleCumplimientoHorasView.as_view(), name="detalle_cumplimiento_horas"),
    path("export/semanal/", export_reporte_semanal, name="export_reporte_semanal"),
    path("export/mensual/", export_reporte_mensual, name="export_reporte_mensual"),
]
