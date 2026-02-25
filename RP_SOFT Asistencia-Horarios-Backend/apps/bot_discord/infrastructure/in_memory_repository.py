from typing import List
from ..domain.entities import MetricasGlobalesBot, EstadoBot, ServidoresBot
from ..domain.repositories import BotMetricasRepository, BotEstadoRepository, ServerMetricasRepository

class InMemoryBotMetricasRepository(BotMetricasRepository):
    def __init__(self):
        self.metricas = None

    def save(self, metricas: MetricasGlobalesBot) -> MetricasGlobalesBot:
        self.metricas = metricas
        return self.metricas

    def get(self) -> MetricasGlobalesBot:
        return self.metricas

class InMemoryBotEstadoRepository(BotEstadoRepository):
    def __init__(self):
        self.estado = None

    def save(self, estado: EstadoBot) -> EstadoBot:
        self.estado = estado
        return self.estado

    def get(self) -> EstadoBot:
        return self.estado

class InMemoryServerMetricasRepository(ServerMetricasRepository):
    def __init__(self):
        self.servidores = {}

    def save_all(self, servidores: List[ServidoresBot]) -> List[ServidoresBot]:
        for s in servidores:
            self.servidores[s.server_id] = s
        return list(self.servidores.values())

    def get_all(self) -> List[ServidoresBot]:
        return list(self.servidores.values())

    def find_by_server_id(self, server_id: int) -> ServidoresBot:
        return self.servidores.get(server_id)
