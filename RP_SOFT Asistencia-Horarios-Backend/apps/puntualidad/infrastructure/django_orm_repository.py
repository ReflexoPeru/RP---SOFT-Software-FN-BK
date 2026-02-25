from typing import List, Optional
from datetime import date
from django.db.models import Count, Q
from django.db import OperationalError

from ..domain.entities import (
    EstadoAsistencia,
    HorarioClases,
    Asistencia,
    AsistenciaRecuperacion,
    EstadoAsistenciaEnum,
    DiaSemanaEnum,
    EstadoRecuperacionEnum
)
from ..domain.repositories import (
    EstadoAsistenciaRepository,
    HorarioClasesRepository,
    AsistenciaRepository,
    AsistenciaRecuperacionRepository
)
from .models import (
    EstadoAsistencia as EstadoAsistenciaModel,
    HorarioClases as HorarioClasesModel,
    Asistencia as AsistenciaModel,
    AsistenciaRecuperacion as AsistenciaRecuperacionModel
)


class DjangoEstadoAsistenciaRepository(EstadoAsistenciaRepository):
    """Implementación del repositorio de estados usando Django ORM"""
    
    def _to_domain(self, model: EstadoAsistenciaModel) -> EstadoAsistencia:
        """Convierte modelo a entidad de dominio"""
        estado_enum = EstadoAsistenciaEnum(model.estado)
        return EstadoAsistencia(id=model.id, estado=estado_enum)
    
    def get_by_nombre(self, nombre: str) -> Optional[EstadoAsistencia]:
        try:
            model = EstadoAsistenciaModel.objects.filter(estado=nombre).first()
            return self._to_domain(model) if model else None
        except OperationalError:
            return None
    
    def get_or_create(self, estado: EstadoAsistenciaEnum) -> EstadoAsistencia:
        try:
            model, _ = EstadoAsistenciaModel.objects.get_or_create(
                estado=estado.value,
                defaults={'estado': estado.value}
            )
            return self._to_domain(model)
        except OperationalError:
            # Si la tabla no existe, retornar entidad sin ID
            return EstadoAsistencia(estado=estado)
    
    def get_all(self) -> List[EstadoAsistencia]:
        try:
            return [self._to_domain(m) for m in EstadoAsistenciaModel.objects.all()]
        except OperationalError:
            return []


class DjangoHorarioClasesRepository(HorarioClasesRepository):
    """Implementación del repositorio de horarios usando Django ORM"""
    
    def _to_domain(self, model: HorarioClasesModel) -> HorarioClases:
        """Convierte modelo a entidad de dominio"""
        dia_clase = DiaSemanaEnum(model.dia_clase) if model.dia_clase else None
        dia_recuperacion = DiaSemanaEnum(model.dia_recuperacion) if model.dia_recuperacion else None
        
        return HorarioClases(
            id=model.id,
            practicante_id=model.practicante_id,
            dia_clase=dia_clase,
            dia_recuperacion=dia_recuperacion
        )
    
    def get_by_practicante(self, practicante_id: int) -> Optional[HorarioClases]:
        try:
            model = HorarioClasesModel.objects.filter(practicante_id=practicante_id).first()
            return self._to_domain(model) if model else None
        except OperationalError:
            return None
    
    def get_by_dia(self, dia: DiaSemanaEnum) -> List[HorarioClases]:
        try:
            models = HorarioClasesModel.objects.filter(dia_clase=dia.value)
            return [self._to_domain(m) for m in models]
        except OperationalError:
            return []
    
    def save(self, horario: HorarioClases) -> HorarioClases:
        try:
            if horario.id:
                model = HorarioClasesModel.objects.get(id=horario.id)
            else:
                model = HorarioClasesModel()
            
            model.practicante_id = horario.practicante_id
            model.dia_clase = horario.dia_clase.value if horario.dia_clase else None
            model.dia_recuperacion = horario.dia_recuperacion.value if horario.dia_recuperacion else None
            model.save()
            
            return self._to_domain(model)
        except OperationalError:
            raise ValueError("Error al guardar horario")


class DjangoAsistenciaRepository(AsistenciaRepository):
    """Implementación del repositorio de asistencias usando Django ORM"""
    
    def _to_domain(self, model: AsistenciaModel) -> Asistencia:
        """Convierte modelo a entidad de dominio"""
        estado_enum = EstadoAsistenciaEnum(model.estado.estado)
        
        return Asistencia(
            id=model.id,
            practicante_id=model.practicante_id,
            fecha=model.fecha,
            estado=estado_enum,
            hora_entrada=model.hora_entrada,
            hora_salida=model.hora_salida,
            motivo=model.motivo
        )
    
    def get_by_id(self, asistencia_id: int) -> Optional[Asistencia]:
        try:
            model = AsistenciaModel.objects.filter(id=asistencia_id).select_related('estado', 'practicante').first()
            return self._to_domain(model) if model else None
        except OperationalError:
            return None
    
    def get_by_practicante_and_fecha(self, practicante_id: int, fecha: date) -> Optional[Asistencia]:
        try:
            model = AsistenciaModel.objects.filter(
                practicante_id=practicante_id,
                fecha=fecha
            ).select_related('estado').first()
            return self._to_domain(model) if model else None
        except OperationalError:
            return None
    
    def get_by_fecha(self, fecha: date) -> List[Asistencia]:
        try:
            models = AsistenciaModel.objects.filter(fecha=fecha).select_related('estado', 'practicante')
            return [self._to_domain(m) for m in models]
        except OperationalError:
            return []
    
    def get_by_practicante_and_rango(self, practicante_id: int, fecha_inicio: date, fecha_fin: date) -> List[Asistencia]:
        try:
            models = AsistenciaModel.objects.filter(
                practicante_id=practicante_id,
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin
            ).select_related('estado')
            return [self._to_domain(m) for m in models]
        except OperationalError:
            return []
    
    def get_justificadas(self, fecha_inicio: date, fecha_fin: date) -> List[Asistencia]:
        try:
            estado_just = EstadoAsistenciaModel.objects.filter(estado=EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO.value).first()
            if not estado_just:
                return []
            
            models = AsistenciaModel.objects.filter(
                estado=estado_just,
                motivo__isnull=False,
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin
            ).exclude(motivo='').select_related('practicante', 'estado')
            
            return [self._to_domain(m) for m in models]
        except OperationalError:
            return []
    
    def save(self, asistencia: Asistencia) -> Asistencia:
        try:
            if asistencia.id:
                model = AsistenciaModel.objects.get(id=asistencia.id)
            else:
                model = AsistenciaModel()
            
            model.practicante_id = asistencia.practicante_id
            model.fecha = asistencia.fecha
            model.hora_entrada = asistencia.hora_entrada
            model.hora_salida = asistencia.hora_salida
            model.motivo = asistencia.motivo
            
            # Obtener o crear estado
            estado_model = EstadoAsistenciaModel.objects.get_or_create(
                estado=asistencia.estado.value,
                defaults={'estado': asistencia.estado.value}
            )[0]
            model.estado = estado_model
            
            model.save()
            return self._to_domain(model)
        except OperationalError as e:
            raise ValueError(f"Error al guardar asistencia: {str(e)}")
    
    def count_by_estado_and_fecha(self, estado: EstadoAsistenciaEnum, fecha: date) -> int:
        try:
            estado_model = EstadoAsistenciaModel.objects.filter(estado=estado.value).first()
            if not estado_model:
                return 0
            
            return AsistenciaModel.objects.filter(
                estado=estado_model,
                fecha=fecha
            ).count()
        except OperationalError:
            return 0
    
    def count_tickets_mes(self, practicante_id: int, fecha_inicio: date, fecha_fin: date) -> int:
        try:
            estado_just = EstadoAsistenciaModel.objects.filter(
                estado=EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO.value
            ).first()
            if not estado_just:
                return 0
            
            return AsistenciaModel.objects.filter(
                practicante_id=practicante_id,
                estado=estado_just,
                motivo__isnull=False,
                fecha__gte=fecha_inicio,
                fecha__lte=fecha_fin
            ).exclude(motivo='').count()
        except OperationalError:
            return 0


class DjangoAsistenciaRecuperacionRepository(AsistenciaRecuperacionRepository):
    """Implementación del repositorio de recuperaciones usando Django ORM"""
    
    def _to_domain(self, model: AsistenciaRecuperacionModel) -> AsistenciaRecuperacion:
        """Convierte modelo a entidad de dominio"""
        estado_enum = EstadoRecuperacionEnum(model.estado)
        
        return AsistenciaRecuperacion(
            id=model.id,
            asistencia_id=model.asistencia_id,
            fecha_recuperacion=model.fecha_recuperacion,
            estado=estado_enum,
            hora_entrada=model.hora_entrada,
            hora_salida=model.hora_salida
        )
    
    def get_by_id(self, recuperacion_id: int) -> Optional[AsistenciaRecuperacion]:
        try:
            model = AsistenciaRecuperacionModel.objects.filter(id=recuperacion_id).select_related('asistencia').first()
            return self._to_domain(model) if model else None
        except OperationalError:
            return None
    
    def get_by_asistencia(self, asistencia_id: int) -> List[AsistenciaRecuperacion]:
        try:
            models = AsistenciaRecuperacionModel.objects.filter(asistencia_id=asistencia_id)
            return [self._to_domain(m) for m in models]
        except OperationalError:
            return []
    
    def get_all(self, limit: int = 100) -> List[AsistenciaRecuperacion]:
        try:
            models = AsistenciaRecuperacionModel.objects.select_related(
                'asistencia',
                'asistencia__practicante'
            ).filter(asistencia__isnull=False)[:limit]
            return [self._to_domain(m) for m in models]
        except OperationalError:
            return []
    
    def save(self, recuperacion: AsistenciaRecuperacion) -> AsistenciaRecuperacion:
        try:
            if recuperacion.id:
                model = AsistenciaRecuperacionModel.objects.get(id=recuperacion.id)
            else:
                model = AsistenciaRecuperacionModel()
            
            model.asistencia_id = recuperacion.asistencia_id
            model.fecha_recuperacion = recuperacion.fecha_recuperacion
            model.estado = recuperacion.estado.value
            model.hora_entrada = recuperacion.hora_entrada
            model.hora_salida = recuperacion.hora_salida
            model.save()
            
            return self._to_domain(model)
        except OperationalError as e:
            raise ValueError(f"Error al guardar recuperación: {str(e)}")

