from dataclasses import dataclass
from datetime import date, time
from enum import Enum
from typing import Optional


class EstadoAsistenciaEnum(Enum):
    """Estados posibles de una asistencia"""
    PRESENTE = "Presente"
    TARDANZA = "Tardanza"
    AUSENTE_JUSTIFICADO = "Ausente Justificado"
    AUSENTE_SIN_JUSTIFICAR = "Ausente Sin Justificar"


class DiaSemanaEnum(Enum):
    """Días de la semana"""
    LUNES = "Lunes"
    MARTES = "Martes"
    MIERCOLES = "Miércoles"
    JUEVES = "Jueves"
    VIERNES = "Viernes"
    SABADO = "Sábado"
    DOMINGO = "Domingo"


class EstadoRecuperacionEnum(Enum):
    """Estados de una recuperación"""
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En Progreso"
    COMPLETADO = "Completado"
    CANCELADO = "Cancelado"


@dataclass
class EstadoAsistencia:
    """Entidad de dominio que representa un estado de asistencia"""
    id: Optional[int] = None
    estado: EstadoAsistenciaEnum = EstadoAsistenciaEnum.PRESENTE

    def __str__(self):
        return self.estado.value


@dataclass
class HorarioClases:
    """Entidad de dominio que representa el horario de clases de un practicante"""
    practicante_id: int
    dia_clase: Optional[DiaSemanaEnum] = None
    dia_recuperacion: Optional[DiaSemanaEnum] = None
    id: Optional[int] = None

    def tiene_clase_hoy(self, dia_actual: DiaSemanaEnum) -> bool:
        """Verifica si el practicante tiene clase en el día especificado"""
        return self.dia_clase == dia_actual


@dataclass
class Asistencia:
    """Entidad de dominio que representa un registro de asistencia"""
    practicante_id: int
    fecha: date
    estado: EstadoAsistenciaEnum
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None
    motivo: Optional[str] = None
    id: Optional[int] = None

    def es_justificada(self) -> bool:
        """Verifica si la asistencia está justificada"""
        return self.estado == EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO

    def es_presente(self) -> bool:
        """Verifica si el practicante está presente"""
        return self.estado == EstadoAsistenciaEnum.PRESENTE

    def es_tardanza(self) -> bool:
        """Verifica si el practicante llegó tarde"""
        return self.estado == EstadoAsistenciaEnum.TARDANZA

    def tiene_motivo(self) -> bool:
        """Verifica si tiene motivo (ticket)"""
        return bool(self.motivo and self.motivo.strip())


@dataclass
class AsistenciaRecuperacion:
    """Entidad de dominio que representa una recuperación de horas"""
    asistencia_id: int
    fecha_recuperacion: date
    estado: EstadoRecuperacionEnum = EstadoRecuperacionEnum.PENDIENTE
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None
    id: Optional[int] = None

    def calcular_horas_completadas(self) -> float:
        """Calcula las horas completadas basándose en entrada y salida"""
        if not self.hora_entrada or not self.hora_salida:
            return 0.0
        
        from datetime import datetime, timedelta
        entrada = datetime.combine(self.fecha_recuperacion, self.hora_entrada)
        salida = datetime.combine(self.fecha_recuperacion, self.hora_salida)
        
        if salida <= entrada:
            return 0.0
        
        diferencia = salida - entrada
        horas = diferencia.total_seconds() / 3600
        return min(round(horas, 2), 12.0)  # Máximo 12 horas

    def esta_completada(self) -> bool:
        """Verifica si la recuperación está completada"""
        return self.estado == EstadoRecuperacionEnum.COMPLETADO

