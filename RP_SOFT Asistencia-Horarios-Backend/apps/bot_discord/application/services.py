from dataclasses import dataclass
from datetime import datetime
from typing import List
from ..domain.entities import MetricasGlobalesBot, EstadoBot, ServidoresBot, BotStatus, ServerStatus
from ..domain.repositories import BotMetricasRepository, BotEstadoRepository, ServerMetricasRepository

@dataclass
class ResumenPayload:
    servidores_conectados: int
    eventos_procesados_hoy: int
    uptime_porcentaje: float
    ultima_sincronizacion: datetime

@dataclass
class EstadoPayload:
    status: str
    uptime_dias: int
    latencia_ms: float
    ultima_conexion: datetime

@dataclass
class ServerPayload:
    server_id: int
    server_name: str
    miembros: int
    canales: int
    status: str

@dataclass
class MetricasPayload:
    resumen: ResumenPayload
    estado: EstadoPayload
    servers: List[ServerPayload]

class GuardarMetricasBotService:
    def __init__(self, metricas_repo: BotMetricasRepository, estado_repo: BotEstadoRepository, server_repo: ServerMetricasRepository):
        self.metricas_repo = metricas_repo
        self.estado_repo = estado_repo
        self.server_repo = server_repo

    def execute(self, payload: MetricasPayload):
        # Guardar métricas globales
        metricas = MetricasGlobalesBot(
            servidores_conectados=payload.resumen.servidores_conectados,
            eventos_procesados_hoy=payload.resumen.eventos_procesados_hoy,
            uptime_porcentaje=payload.resumen.uptime_porcentaje,
            ultima_sincronizacion=payload.resumen.ultima_sincronizacion
        )
        self.metricas_repo.save(metricas)

        # Guardar estado del bot
        estado = EstadoBot(
            status=BotStatus(payload.estado.status),
            uptime_dias=payload.estado.uptime_dias,
            latencia_ms=payload.estado.latencia_ms,
            ultima_conexion=payload.estado.ultima_conexion
        )
        self.estado_repo.save(estado)

        # Guardar métricas de servidores
        servidores = []
        for s in payload.servers:
            servidor = ServidoresBot(
                server_id=s.server_id,
                server_name=s.server_name,
                miembros=s.miembros,
                canales=s.canales,
                status=ServerStatus(s.status),
                ultima_actualizacion=datetime.now()
            )
            servidores.append(servidor)
        self.server_repo.save_all(servidores)

class ObtenerResumenGlobalService:
    def __init__(self, metricas_repo: BotMetricasRepository):
        self.metricas_repo = metricas_repo

    def execute(self) -> MetricasGlobalesBot:
        return self.metricas_repo.get()

class ObtenerEstadoBotService:
    def __init__(self, estado_repo: BotEstadoRepository):
        self.estado_repo = estado_repo

    def execute(self) -> EstadoBot:
        return self.estado_repo.get()

class ListarServidoresService:
    def __init__(self, server_repo: ServerMetricasRepository):
        self.server_repo = server_repo

    def execute(self) -> List[ServidoresBot]:
        return self.server_repo.get_all()

class ActualizarEstadoBotService:
    def __init__(self, estado_repo: BotEstadoRepository):
        self.estado_repo = estado_repo

    def execute(self, status: str):
        estado = self.estado_repo.get()
        if estado is None:
            # Si no existe un estado, crea uno nuevo.
            estado = EstadoBot(status=BotStatus(status), ultima_conexion=datetime.now())
        else:
            estado.status = BotStatus(status)
            estado.ultima_conexion = datetime.now()
        
        self.estado_repo.save(estado)
        return estado
