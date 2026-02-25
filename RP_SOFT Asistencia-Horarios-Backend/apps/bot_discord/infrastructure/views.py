from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import BasePermission
from .serializers import MetricasPayloadSerializer, StatusUpdateSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..application.services import (
    GuardarMetricasBotService,
    ObtenerResumenGlobalService,
    ObtenerEstadoBotService,
    ListarServidoresService,
    ActualizarEstadoBotService,
    ResumenPayload,
    EstadoPayload,
    ServerPayload,
    MetricasPayload,
)
from .django_orm_repository import (
    DjangoORMBotMetricasRepository,
    DjangoORMBotEstadoRepository,
    DjangoORMServerMetricasRepository,
)

class BotAuthentication(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return False
        
        try:
            _, token = auth_header.split()
            return token == settings.BOT_API_KEY
        except ValueError:
            return False

class MetricasBotView(APIView):
    permission_classes = [BotAuthentication]

    def post(self, request):
        serializer = MetricasPayloadSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            resumen_data = ResumenPayload(**data['resumen'])
            estado_data = EstadoPayload(**data['estado'])
            servers_data = [ServerPayload(**s) for s in data['servers']]
            
            payload = MetricasPayload(
                resumen=resumen_data,
                estado=estado_data,
                servers=servers_data
            )

            metricas_repo = DjangoORMBotMetricasRepository()
            estado_repo = DjangoORMBotEstadoRepository()
            server_repo = DjangoORMServerMetricasRepository()
            
            service = GuardarMetricasBotService(metricas_repo, estado_repo, server_repo)
            service.execute(payload)
            
            # Emitir actualización por WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'metricas_bot',
                {
                    'type': 'metricas_update',
                    'message': serializer.data
                }
            )
            
            return Response({"message": "Métricas recibidas y emitidas"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResumenBotView(APIView):
    def get(self, request):
        metricas_repo = DjangoORMBotMetricasRepository()
        service = ObtenerResumenGlobalService(metricas_repo)
        resumen = service.execute()
        if resumen:
            data = {
                "servidores_conectados": resumen.servidores_conectados,
                "eventos_procesados_hoy": resumen.eventos_procesados_hoy,
                "uptime_porcentaje": resumen.uptime_porcentaje,
                "ultima_sincronizacion": resumen.ultima_sincronizacion,
            }
            return Response(data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

class EstadoBotView(APIView):
    def get(self, request):
        estado_repo = DjangoORMBotEstadoRepository()
        service = ObtenerEstadoBotService(estado_repo)
        estado = service.execute()
        if estado:
            data = {
                "status": estado.status.value,
                "uptime_dias": estado.uptime_dias,
                "latencia_ms": estado.latencia_ms,
                "ultima_conexion": estado.ultima_conexion,
            }
            return Response(data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

class ServidoresBotView(APIView):
    def get(self, request):
        server_repo = DjangoORMServerMetricasRepository()
        service = ListarServidoresService(server_repo)
        servidores = service.execute()
        data = [
            {
                "server_id": s.server_id,
                "server_name": s.server_name,
                "miembros": s.miembros,
                "canales": s.canales,
                "status": s.status.value,
                "ultima_actualizacion": s.ultima_actualizacion,
            }
            for s in servidores
        ]
        return Response(data)

class BotStatusUpdateView(APIView):
    permission_classes = [BotAuthentication]

    def post(self, request):
        serializer = StatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            status_val = serializer.validated_data['status']
            
            estado_repo = DjangoORMBotEstadoRepository()
            service = ActualizarEstadoBotService(estado_repo)
            service.execute(status_val)

            # Notificar a los clientes WebSocket sobre el cambio de estado
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'metricas_bot',
                {
                    'type': 'metricas_update',
                    'message': {'estado': {'status': status_val}}
                }
            )

            return Response({"message": f"Estado del bot actualizado a {status_val}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
