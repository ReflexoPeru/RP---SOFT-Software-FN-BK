from django.test import TestCase
from datetime import datetime
from .application.services import (
    GuardarMetricasBotService,
    ObtenerResumenGlobalService,
    ObtenerEstadoBotService,
    ListarServidoresService,
    MetricasPayload,
    ResumenPayload,
    EstadoPayload,
    ServerPayload,
)
from .infrastructure.in_memory_repository import (
    InMemoryBotMetricasRepository,
    InMemoryBotEstadoRepository,
    InMemoryServerMetricasRepository,
)
from .domain.entities import BotStatus, ServerStatus

class BotDiscordServiceTests(TestCase):
    def setUp(self):
        self.metricas_repo = InMemoryBotMetricasRepository()
        self.estado_repo = InMemoryBotEstadoRepository()
        self.server_repo = InMemoryServerMetricasRepository()

    def test_guardar_y_obtener_metricas(self):
        # Arrange
        payload = MetricasPayload(
            resumen=ResumenPayload(
                servidores_conectados=10,
                eventos_procesados_hoy=1500,
                uptime_porcentaje=99.9,
                ultima_sincronizacion=datetime.now()
            ),
            estado=EstadoPayload(
                status="online",
                uptime_dias=20,
                latencia_ms=50.5,
                ultima_conexion=datetime.now()
            ),
            servers=[
                ServerPayload(
                    server_id=123,
                    server_name="Test Server",
                    miembros=100,
                    canales=10,
                    status="conectado"
                )
            ]
        )
        
        # Act
        guardar_service = GuardarMetricasBotService(self.metricas_repo, self.estado_repo, self.server_repo)
        guardar_service.execute(payload)

        # Assert
        resumen_service = ObtenerResumenGlobalService(self.metricas_repo)
        resumen = resumen_service.execute()
        self.assertEqual(resumen.servidores_conectados, 10)

        estado_service = ObtenerEstadoBotService(self.estado_repo)
        estado = estado_service.execute()
        self.assertEqual(estado.status, BotStatus.ONLINE)

        servidores_service = ListarServidoresService(self.server_repo)
        servidores = servidores_service.execute()
        self.assertEqual(len(servidores), 1)
        self.assertEqual(servidores[0].server_name, "Test Server")
