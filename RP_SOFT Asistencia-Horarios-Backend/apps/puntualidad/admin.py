from django.contrib import admin
from .infrastructure.models import EstadoAsistencia, HorarioClases, Asistencia, AsistenciaRecuperacion


@admin.register(EstadoAsistencia)
class EstadoAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'estado')
    search_fields = ('estado',)


@admin.register(HorarioClases)
class HorarioClasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'practicante', 'dia_clase', 'dia_recuperacion')
    list_filter = ('dia_clase', 'dia_recuperacion')
    search_fields = ('practicante__nombre', 'practicante__apellido')


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'practicante', 'fecha', 'hora_entrada', 'estado', 'motivo')
    list_filter = ('estado', 'fecha')
    search_fields = ('practicante__nombre', 'practicante__apellido', 'motivo')
    date_hierarchy = 'fecha'


@admin.register(AsistenciaRecuperacion)
class AsistenciaRecuperacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'asistencia', 'fecha_recuperacion', 'hora_entrada', 'estado')
    list_filter = ('estado', 'fecha_recuperacion')
    search_fields = ('asistencia__practicante__nombre', 'asistencia__practicante__apellido')
