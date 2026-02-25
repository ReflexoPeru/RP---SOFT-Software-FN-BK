from rest_framework import serializers
from apps.practicantes.infrastructure.models import Practicante
from apps.puntualidad.infrastructure.models import Asistencia, EstadoAsistencia


class JustificacionCreateSerializer(serializers.Serializer):
    """Serializer para crear una nueva justificación
    Basado en los requisitos del sistema:
    - Máximo 3 tickets por mes
    - SLA de 24 horas para revisión
    - Evidencia opcional pero recomendada
    """
    practicante_id = serializers.IntegerField(required=True)
    fecha = serializers.DateField(required=True)
    motivo = serializers.CharField(max_length=255, required=True, allow_blank=False)
    tiene_evidencia = serializers.BooleanField(default=False, required=False)
    ticket_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_practicante_id(self, value):
        """Validar que el practicante exista y esté activo"""
        try:
            practicante = Practicante.objects.get(id=value, estado='activo')
            return value
        except Practicante.DoesNotExist:
            raise serializers.ValidationError("El practicante no existe o no está activo")
    
    def validate_fecha(self, value):
        """Validar que la fecha no sea futura"""
        from django.utils import timezone
        hoy = timezone.now().date()
        if value > hoy:
            raise serializers.ValidationError("No se puede justificar una fecha futura")
        return value
    
    def validate_motivo(self, value):
        """Validar que el motivo no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El motivo es requerido")
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El motivo debe tener al menos 5 caracteres")
        return value.strip()


class JustificacionUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar una justificación (aprobar/rechazar)"""
    justificacion_id = serializers.IntegerField(required=True)
    accion = serializers.ChoiceField(
        choices=['aprobar', 'rechazar'],
        required=True
    )
    motivo_rechazo = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True
    )
    
    def validate_justificacion_id(self, value):
        """Validar que la justificación exista"""
        try:
            asistencia = Asistencia.objects.get(id=value)
            return value
        except Asistencia.DoesNotExist:
            raise serializers.ValidationError("La justificación no existe")
    
    def validate(self, data):
        """Validar que si se rechaza, haya motivo de rechazo"""
        if data.get('accion') == 'rechazar' and not data.get('motivo_rechazo'):
            raise serializers.ValidationError({
                'motivo_rechazo': 'El motivo de rechazo es requerido cuando se rechaza una justificación'
            })
        return data

