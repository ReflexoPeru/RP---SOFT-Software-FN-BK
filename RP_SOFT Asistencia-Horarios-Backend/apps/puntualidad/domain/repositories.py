from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from .entities import (
    EstadoAsistencia,
    HorarioClases,
    Asistencia,
    AsistenciaRecuperacion,
    EstadoAsistenciaEnum,
    DiaSemanaEnum
)


class EstadoAsistenciaRepository(ABC):
    """Interfaz del repositorio para estados de asistencia"""
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[EstadoAsistencia]:
        """Obtiene un estado por su nombre"""
        pass
    
    @abstractmethod
    def get_or_create(self, estado: EstadoAsistenciaEnum) -> EstadoAsistencia:
        """Obtiene o crea un estado de asistencia"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[EstadoAsistencia]:
        """Obtiene todos los estados"""
        pass


class HorarioClasesRepository(ABC):
    """Interfaz del repositorio para horarios de clases"""
    
    @abstractmethod
    def get_by_practicante(self, practicante_id: int) -> Optional[HorarioClases]:
        """Obtiene el horario de un practicante"""
        pass
    
    @abstractmethod
    def get_by_dia(self, dia: DiaSemanaEnum) -> List[HorarioClases]:
        """Obtiene todos los horarios para un día específico"""
        pass
    
    @abstractmethod
    def save(self, horario: HorarioClases) -> HorarioClases:
        """Guarda un horario"""
        pass


class AsistenciaRepository(ABC):
    """Interfaz del repositorio para asistencias"""
    
    @abstractmethod
    def get_by_id(self, asistencia_id: int) -> Optional[Asistencia]:
        """Obtiene una asistencia por ID"""
        pass
    
    @abstractmethod
    def get_by_practicante_and_fecha(self, practicante_id: int, fecha: date) -> Optional[Asistencia]:
        """Obtiene una asistencia por practicante y fecha"""
        pass
    
    @abstractmethod
    def get_by_fecha(self, fecha: date) -> List[Asistencia]:
        """Obtiene todas las asistencias de una fecha"""
        pass
    
    @abstractmethod
    def get_by_practicante_and_rango(self, practicante_id: int, fecha_inicio: date, fecha_fin: date) -> List[Asistencia]:
        """Obtiene asistencias de un practicante en un rango de fechas"""
        pass
    
    @abstractmethod
    def get_justificadas(self, fecha_inicio: date, fecha_fin: date) -> List[Asistencia]:
        """Obtiene asistencias justificadas en un rango de fechas"""
        pass
    
    @abstractmethod
    def save(self, asistencia: Asistencia) -> Asistencia:
        """Guarda una asistencia"""
        pass
    
    @abstractmethod
    def count_by_estado_and_fecha(self, estado: EstadoAsistenciaEnum, fecha: date) -> int:
        """Cuenta asistencias por estado y fecha"""
        pass
    
    @abstractmethod
    def count_tickets_mes(self, practicante_id: int, fecha_inicio: date, fecha_fin: date) -> int:
        """Cuenta tickets (justificaciones) de un practicante en un mes"""
        pass


class AsistenciaRecuperacionRepository(ABC):
    """Interfaz del repositorio para recuperaciones"""
    
    @abstractmethod
    def get_by_id(self, recuperacion_id: int) -> Optional[AsistenciaRecuperacion]:
        """Obtiene una recuperación por ID"""
        pass
    
    @abstractmethod
    def get_by_asistencia(self, asistencia_id: int) -> List[AsistenciaRecuperacion]:
        """Obtiene recuperaciones de una asistencia"""
        pass
    
    @abstractmethod
    def get_all(self, limit: int = 100) -> List[AsistenciaRecuperacion]:
        """Obtiene todas las recuperaciones"""
        pass
    
    @abstractmethod
    def save(self, recuperacion: AsistenciaRecuperacion) -> AsistenciaRecuperacion:
        """Guarda una recuperación"""
        pass

