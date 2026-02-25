from django.db import models
from apps.practicantes.infrastructure.models import Practicante


class EstadoAsistencia(models.Model):
    """Modelo que representa los estados posibles de una asistencia"""
    estado = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = "estado_asistencia"
        verbose_name = "Estado de Asistencia"
        verbose_name_plural = "Estados de Asistencia"
    
    def __str__(self):
        return self.estado


class HorarioClases(models.Model):
    """Modelo que representa los horarios de clases de un practicante"""
    class DiaSemana(models.TextChoices):
        LUNES = 'Lunes', 'Lunes'
        MARTES = 'Martes', 'Martes'
        MIERCOLES = 'Miércoles', 'Miércoles'
        JUEVES = 'Jueves', 'Jueves'
        VIERNES = 'Viernes', 'Viernes'
        SABADO = 'Sábado', 'Sábado'
        DOMINGO = 'Domingo', 'Domingo'
    
    practicante = models.ForeignKey(
        Practicante,
        on_delete=models.CASCADE,
        related_name='horarios_clases',
        db_column='practicante_id'
    )
    dia_clase = models.CharField(
        max_length=10,
        choices=DiaSemana.choices,
        null=True,
        blank=True,
        help_text="Día de la semana para clases regulares"
    )
    dia_recuperacion = models.CharField(
        max_length=10,
        choices=DiaSemana.choices,
        null=True,
        blank=True,
        help_text="Día de la semana para clases de recuperación"
    )
    
    class Meta:
        db_table = "horario_clases"
        verbose_name = "Horario de Clases"
        verbose_name_plural = "Horarios de Clases"
    
    def __str__(self):
        return f"{self.practicante} - {self.dia_clase or 'Sin día regular'}"


class Asistencia(models.Model):
    """Modelo que representa un registro de asistencia de un practicante"""
    practicante = models.ForeignKey(
        Practicante,
        on_delete=models.CASCADE,
        related_name='asistencias',
        db_column='practicante_id'
    )
    fecha = models.DateField()
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.ForeignKey(
        EstadoAsistencia,
        on_delete=models.PROTECT,
        related_name='asistencias',
        db_column='estado_id'
    )
    motivo = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = "asistencia"
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        unique_together = [['practicante', 'fecha']]
        indexes = [
            models.Index(fields=['fecha']),
            models.Index(fields=['practicante', 'fecha']),
        ]
    
    def __str__(self):
        return f"{self.practicante} - {self.fecha} - {self.estado}"


class AsistenciaRecuperacion(models.Model):
    """Modelo que representa un registro de asistencia de recuperación"""
    class EstadoRecuperacion(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        EN_PROGRESO = 'En Progreso', 'En Progreso'
        COMPLETADO = 'Completado', 'Completado'
        CANCELADO = 'Cancelado', 'Cancelado'
    
    asistencia = models.ForeignKey(
        Asistencia,
        on_delete=models.CASCADE,
        related_name='recuperaciones',
        db_column='asistencia_id'
    )
    fecha_recuperacion = models.DateField()
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=EstadoRecuperacion.choices,
        default=EstadoRecuperacion.PENDIENTE
    )
    
    class Meta:
        db_table = "asistencia_recuperacion"
        verbose_name = "Asistencia de Recuperación"
        verbose_name_plural = "Asistencias de Recuperación"
        indexes = [
            models.Index(fields=['fecha_recuperacion']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self):
        return f"Recuperación de {self.asistencia} - {self.fecha_recuperacion}"
