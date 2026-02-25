from typing import List
from ..domain.entities import MetricasGlobalesBot, EstadoBot, ServidoresBot, BotStatus, ServerStatus
from ..domain.repositories import BotMetricasRepository, BotEstadoRepository, ServerMetricasRepository
from .models import MetricasGlobalesBot, EstadoBot, ServidoresBot

class DjangoORMBotMetricasRepository(BotMetricasRepository):
    def save(self, metricas: MetricasGlobalesBot) -> MetricasGlobalesBot:
        metricas_model, _ = MetricasGlobalesBot.objects.update_or_create(
            id=1,
            defaults={
                'servidores_conectados': metricas.servidores_conectados,
                'eventos_procesados_hoy': metricas.eventos_procesados_hoy,
                'uptime_porcentaje': metricas.uptime_porcentaje,
                'ultima_sincronizacion': metricas.ultima_sincronizacion,
            }
        )
        return self._to_entity(metricas_model)

    def get(self) -> MetricasGlobalesBot:
        metricas_model = MetricasGlobalesBot.objects.first()
        return self._to_entity(metricas_model) if metricas_model else None

    def _to_entity(self, model: MetricasGlobalesBot) -> MetricasGlobalesBot:
        return MetricasGlobalesBot(
            id=model.id,
            servidores_conectados=model.servidores_conectados,
            eventos_procesados_hoy=model.eventos_procesados_hoy,
            uptime_porcentaje=model.uptime_porcentaje,
            ultima_sincronizacion=model.ultima_sincronizacion
        )

class DjangoORMBotEstadoRepository(BotEstadoRepository):
    def save(self, estado: EstadoBot) -> EstadoBot:
        estado_model, _ = EstadoBot.objects.update_or_create(
            id=1,
            defaults={
                'status': estado.status.value,
                'uptime_dias': estado.uptime_dias,
                'latencia_ms': estado.latencia_ms,
                'ultima_conexion': estado.ultima_conexion,
            }
        )
        return self._to_entity(estado_model)

    def get(self) -> EstadoBot:
        estado_model = EstadoBot.objects.first()
        return self._to_entity(estado_model) if estado_model else None

    def _to_entity(self, model: EstadoBot) -> EstadoBot:
        return EstadoBot(
            id=model.id,
            status=BotStatus(model.status),
            uptime_dias=model.uptime_dias,
            latencia_ms=model.latencia_ms,
            ultima_conexion=model.ultima_conexion
        )

class DjangoORMServerMetricasRepository(ServerMetricasRepository):
    def save_all(self, servidores: List[ServidoresBot]) -> List[ServidoresBot]:
        for servidor in servidores:
            ServidoresBot.objects.update_or_create(
                server_id=servidor.server_id,
                defaults={
                    'server_name': servidor.server_name,
                    'miembros': servidor.miembros,
                    'canales': servidor.canales,
                    'status': servidor.status.value,
                    'ultima_actualizacion': servidor.ultima_actualizacion,
                }
            )
        return servidores

    def get_all(self) -> List[ServidoresBot]:
        return [self._to_entity(model) for model in ServidoresBot.objects.all()]

    def find_by_server_id(self, server_id: int) -> ServidoresBot:
        model = ServidoresBot.objects.filter(server_id=server_id).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: ServidoresBot) -> ServidoresBot:
        return ServidoresBot(
            id=model.id,
            server_id=model.server_id,
            server_name=model.server_name,
            miembros=model.miembros,
            canales=model.canales,
            status=ServerStatus(model.status),
            ultima_actualizacion=model.ultima_actualizacion
        )
