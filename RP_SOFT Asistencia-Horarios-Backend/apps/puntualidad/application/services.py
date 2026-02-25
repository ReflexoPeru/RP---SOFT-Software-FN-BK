from typing import List, Dict, Optional
from datetime import date, time
from django.utils import timezone

from ..domain.entities import (
    EstadoAsistencia,
    Asistencia,
    AsistenciaRecuperacion,
    EstadoAsistenciaEnum,
    DiaSemanaEnum,
    EstadoRecuperacionEnum
)
from ..domain.repositories import (
    EstadoAsistenciaRepository,
    AsistenciaRepository,
    HorarioClasesRepository,
    AsistenciaRecuperacionRepository
)


class ResumenPuntualidadService:
    """Servicio para obtener el resumen de puntualidad del día"""
    
    def __init__(
        self,
        estado_repo: EstadoAsistenciaRepository,
        asistencia_repo: AsistenciaRepository,
        horario_repo: HorarioClasesRepository
    ):
        self.estado_repo = estado_repo
        self.asistencia_repo = asistencia_repo
        self.horario_repo = horario_repo
    
    def execute(self, fecha: date = None) -> Dict:
        """Ejecuta el caso de uso de resumen de puntualidad"""
        if fecha is None:
            fecha = timezone.now().date()
        
        # Obtener día de la semana
        dias_semana = {
            0: DiaSemanaEnum.LUNES,
            1: DiaSemanaEnum.MARTES,
            2: DiaSemanaEnum.MIERCOLES,
            3: DiaSemanaEnum.JUEVES,
            4: DiaSemanaEnum.VIERNES,
            5: DiaSemanaEnum.SABADO,
            6: DiaSemanaEnum.DOMINGO
        }
        dia_hoy = dias_semana.get(fecha.weekday())
        
        # Obtener estados
        estado_presente = self.estado_repo.get_or_create(EstadoAsistenciaEnum.PRESENTE)
        estado_tardanza = self.estado_repo.get_or_create(EstadoAsistenciaEnum.TARDANZA)
        estado_ausente_just = self.estado_repo.get_or_create(EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO)
        estado_ausente_sin = self.estado_repo.get_or_create(EstadoAsistenciaEnum.AUSENTE_SIN_JUSTIFICAR)
        
        # Contar asistencias por estado
        presentes = self.asistencia_repo.count_by_estado_and_fecha(EstadoAsistenciaEnum.PRESENTE, fecha)
        tardanzas = self.asistencia_repo.count_by_estado_and_fecha(EstadoAsistenciaEnum.TARDANZA, fecha)
        ausentes_justificados = self.asistencia_repo.count_by_estado_and_fecha(
            EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO, fecha
        )
        ausentes_sin_justificar = self.asistencia_repo.count_by_estado_and_fecha(
            EstadoAsistenciaEnum.AUSENTE_SIN_JUSTIFICAR, fecha
        )
        
        # Obtener practicantes con clases hoy
        if dia_hoy:
            horarios_hoy = self.horario_repo.get_by_dia(dia_hoy)
            con_clases = len(horarios_hoy)
        else:
            con_clases = 0
        
        total_deben_asistir = con_clases  # Simplificado, debería incluir practicantes activos
        
        return {
            "asistencias": presentes,
            "tardanzas": tardanzas,
            "faltas": ausentes_justificados + ausentes_sin_justificar,
            "total": total_deben_asistir,
            "con_clases": con_clases,
            "ausentes_justificados": ausentes_justificados,
            "ausentes_sin_justificar": ausentes_sin_justificar
        }


class AlertasPuntualidadService:
    """Servicio para obtener alertas automáticas de puntualidad"""
    
    def __init__(
        self,
        estado_repo: EstadoAsistenciaRepository,
        asistencia_repo: AsistenciaRepository,
        horario_repo: HorarioClasesRepository
    ):
        self.estado_repo = estado_repo
        self.asistencia_repo = asistencia_repo
        self.horario_repo = horario_repo
    
    def execute(self, fecha: date = None) -> List[Dict]:
        """Ejecuta el caso de uso de alertas"""
        if fecha is None:
            fecha = timezone.now().date()
        
        alertas = []
        
        # Alerta 1: Tardanzas
        asistencias_fecha = self.asistencia_repo.get_by_fecha(fecha)
        tardanzas = [a for a in asistencias_fecha if a.es_tardanza()]
        
        if tardanzas:
            alertas.append({
                "tipo": "tardanza",
                "titulo": "Tardanza potencial detectada",
                "cantidad": len(tardanzas),
                "hora": "8:05 a.m.",
                "descripcion": "Gracia de 5 minutos aplicada",
                "practicantes": [f"{t.practicante_id}" for t in tardanzas[:5]]
            })
        
        # Alerta 2: Ausencias sin clase
        ausentes = [a for a in asistencias_fecha if a.estado == EstadoAsistenciaEnum.AUSENTE_SIN_JUSTIFICAR]
        
        if ausentes:
            alertas.append({
                "tipo": "ausencia",
                "titulo": "Ausencias sin clase registrada",
                "cantidad": len(ausentes),
                "hora": "8:30 a.m.",
                "descripcion": "No tienen clases programadas hoy",
                "practicantes": [f"{a.practicante_id}" for a in ausentes[:5]]
            })
        
        # Alerta 3: Practicantes en riesgo
        inicio_mes = fecha.replace(day=1)
        # Esta lógica necesita más implementación en el repositorio
        
        return alertas


class CrearJustificacionService:
    """Servicio para crear una justificación"""
    
    def __init__(
        self,
        estado_repo: EstadoAsistenciaRepository,
        asistencia_repo: AsistenciaRepository
    ):
        self.estado_repo = estado_repo
        self.asistencia_repo = asistencia_repo
    
    def execute(
        self,
        practicante_id: int,
        fecha: date,
        motivo: str,
        ticket_id: Optional[str] = None
    ) -> Dict:
        """Ejecuta el caso de uso de crear justificación"""
        # Validar límite de tickets (máximo 3 por mes)
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        tickets_mes = self.asistencia_repo.count_tickets_mes(
            practicante_id, inicio_mes, hoy
        )
        
        if tickets_mes >= 3:
            raise ValueError(f"Límite de tickets alcanzado. Ya has usado {tickets_mes}/3 tickets este mes.")
        
        # Verificar si ya existe asistencia para esta fecha
        asistencia_existente = self.asistencia_repo.get_by_practicante_and_fecha(
            practicante_id, fecha
        )
        
        estado_justificado = self.estado_repo.get_or_create(EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO)
        
        motivo_final = motivo
        if ticket_id:
            motivo_final = f"{ticket_id} - {motivo}"
        
        if asistencia_existente:
            # Actualizar existente
            asistencia_existente.estado = EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO
            asistencia_existente.motivo = motivo_final
            asistencia = self.asistencia_repo.save(asistencia_existente)
        else:
            # Crear nueva
            nueva_asistencia = Asistencia(
                practicante_id=practicante_id,
                fecha=fecha,
                estado=EstadoAsistenciaEnum.AUSENTE_JUSTIFICADO,
                motivo=motivo_final
            )
            asistencia = self.asistencia_repo.save(nueva_asistencia)
        
        return {
            "mensaje": "Justificación creada exitosamente",
            "id": asistencia.id,
            "tickets_mes": tickets_mes + 1,
            "tickets_max": 3,
            "sla_horas": 24
        }


class AprobarJustificacionService:
    """Servicio para aprobar una justificación"""
    
    def __init__(self, asistencia_repo: AsistenciaRepository):
        self.asistencia_repo = asistencia_repo
    
    def execute(self, asistencia_id: int) -> Dict:
        """Ejecuta el caso de uso de aprobar justificación"""
        asistencia = self.asistencia_repo.get_by_id(asistencia_id)
        
        if not asistencia:
            raise ValueError("La justificación no existe")
        
        if not asistencia.es_justificada():
            raise ValueError("Esta asistencia no es una justificación")
        
        # Aprobar: establecer hora de entrada y salida
        ahora = timezone.now()
        asistencia.hora_entrada = ahora.time()
        asistencia.hora_salida = ahora.time()
        
        asistencia = self.asistencia_repo.save(asistencia)
        
        return {
            "mensaje": "Justificación aprobada exitosamente",
            "id": asistencia.id,
            "estado": "aprobado"
        }


class RechazarJustificacionService:
    """Servicio para rechazar una justificación"""
    
    def __init__(self, asistencia_repo: AsistenciaRepository):
        self.asistencia_repo = asistencia_repo
    
    def execute(self, asistencia_id: int, motivo_rechazo: str) -> Dict:
        """Ejecuta el caso de uso de rechazar justificación"""
        if not motivo_rechazo or not motivo_rechazo.strip():
            raise ValueError("El motivo de rechazo es requerido")
        
        asistencia = self.asistencia_repo.get_by_id(asistencia_id)
        
        if not asistencia:
            raise ValueError("La justificación no existe")
        
        if not asistencia.es_justificada():
            raise ValueError("Esta asistencia no es una justificación")
        
        # Rechazar: actualizar motivo con razón de rechazo
        motivo_original = asistencia.motivo or ""
        motivo_completo = f"{motivo_original} [RECHAZADO: {motivo_rechazo}]"
        asistencia.motivo = motivo_completo
        
        asistencia = self.asistencia_repo.save(asistencia)
        
        return {
            "mensaje": "Justificación rechazada",
            "id": asistencia.id,
            "estado": "rechazado",
            "motivo_rechazo": motivo_rechazo
        }


class ListarJustificacionesService:
    """Servicio para listar justificaciones"""
    
    def __init__(self, asistencia_repo: AsistenciaRepository):
        self.asistencia_repo = asistencia_repo
    
    def execute(self, fecha_inicio: date = None, fecha_fin: date = None) -> List[Dict]:
        """Ejecuta el caso de uso de listar justificaciones"""
        if fecha_inicio is None or fecha_fin is None:
            hoy = timezone.now().date()
            fecha_inicio = hoy.replace(day=1)
            fecha_fin = hoy
        
        justificaciones = self.asistencia_repo.get_justificadas(fecha_inicio, fecha_fin)
        
        # Convertir a formato de respuesta
        data = []
        for just in justificaciones:
            # Calcular tickets del mes para este practicante
            inicio_mes = fecha_inicio.replace(day=1)
            tickets_mes = self.asistencia_repo.count_tickets_mes(
                just.practicante_id, inicio_mes, fecha_fin
            )
            
            # Determinar estado
            estado_just = 'pendiente'
            if just.hora_entrada and just.hora_salida:
                estado_just = 'aprobado'
            elif just.hora_entrada:
                estado_just = 'pendiente'
            
            # Calcular SLA
            sla_restante = None
            tiempo_transcurrido = (timezone.now().date() - just.fecha).days * 24
            horas_restantes = 24 - tiempo_transcurrido
            
            if horas_restantes <= 0 and estado_just == 'pendiente':
                estado_just = 'vencido'
            elif horas_restantes > 0:
                sla_restante = f"{int(horas_restantes)}h"
            
            data.append({
                "id": just.id,
                "practicante_id": just.practicante_id,
                "fecha": just.fecha.isoformat(),
                "motivo": just.motivo,
                "estado": estado_just,
                "tickets_mes": tickets_mes,
                "tickets_max": 3,
                "sla_restante": sla_restante
            })
        
        return data


class ListarRecuperacionesService:
    """Servicio para listar recuperaciones"""
    
    def __init__(self, recuperacion_repo: AsistenciaRecuperacionRepository):
        self.recuperacion_repo = recuperacion_repo
    
    def execute(self, limit: int = 100) -> List[Dict]:
        """Ejecuta el caso de uso de listar recuperaciones"""
        recuperaciones = self.recuperacion_repo.get_all(limit)
        
        data = []
        for rec in recuperaciones:
            horas_completadas = rec.calcular_horas_completadas()
            horas_totales = 12  # Valor por defecto
            
            estado_map = {
                EstadoRecuperacionEnum.PENDIENTE: 'programado',
                EstadoRecuperacionEnum.EN_PROGRESO: 'en-progreso',
                EstadoRecuperacionEnum.COMPLETADO: 'completado',
                EstadoRecuperacionEnum.CANCELADO: 'programado'
            }
            estado_frontend = estado_map.get(rec.estado, 'programado')
            
            if horas_completadas > 0 and estado_frontend == 'programado':
                estado_frontend = 'en-progreso'
            if horas_completadas >= horas_totales:
                estado_frontend = 'completado'
            
            data.append({
                "id": rec.id,
                "asistencia_id": rec.asistencia_id,
                "fecha_recuperacion": rec.fecha_recuperacion.isoformat(),
                "estado": estado_frontend,
                "horasCompletadas": int(horas_completadas),
                "horasTotales": horas_totales
            })
        
        return data
