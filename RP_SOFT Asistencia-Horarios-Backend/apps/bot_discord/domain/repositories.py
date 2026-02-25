from abc import ABC, abstractmethod
from typing import List
from .entities import MetricasGlobalesBot, EstadoBot, ServidoresBot

class BotMetricasRepository(ABC):
    @abstractmethod
    def save(self, metricas: MetricasGlobalesBot) -> MetricasGlobalesBot:
        pass

    @abstractmethod
    def get(self) -> MetricasGlobalesBot:
        pass

class BotEstadoRepository(ABC):
    @abstractmethod
    def save(self, estado: EstadoBot) -> EstadoBot:
        pass

    @abstractmethod
    def get(self) -> EstadoBot:
        pass

class ServerMetricasRepository(ABC):
    @abstractmethod
    def save_all(self, servidores: List[ServidoresBot]) -> List[ServidoresBot]:
        pass

    @abstractmethod
    def get_all(self) -> List[ServidoresBot]:
        pass

    @abstractmethod
    def find_by_server_id(self, server_id: int) -> ServidoresBot:
        pass
