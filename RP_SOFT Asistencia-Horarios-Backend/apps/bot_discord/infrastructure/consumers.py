import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MetricasBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'metricas_bot'

        # Unirse al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje del WebSocket (no se usa en este caso)
    async def receive(self, text_data):
        pass

    # Recibir mensaje del grupo de la sala
    async def metricas_update(self, event):
        message = event['message']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps(message))
