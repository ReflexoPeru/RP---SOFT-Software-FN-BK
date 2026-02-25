from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class BotStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"

class ServerStatus(Enum):
    CONECTADO = "conectado"
    DESCONECTADO = "desconectado"

@dataclass
class MetricasGlobalesBot:
    id: int = None
    servidores_conectados: int = 0
    eventos_procesados_hoy: int = 0
    uptime_porcentaje: float = 100.0
    ultima_sincronizacion: datetime = None

@dataclass
class EstadoBot:
    id: int = None
    status: BotStatus = BotStatus.OFFLINE
    uptime_dias: int = 0
    latencia_ms: float = 0.0
    ultima_conexion: datetime = None

@dataclass
class ServidoresBot:
    id: int = None
    server_id: int = 0
    server_name: str = ""
    miembros: int = 0
    canales: int = 0
    status: ServerStatus = ServerStatus.DESCONECTADO
    ultima_actualizacion: datetime = None
