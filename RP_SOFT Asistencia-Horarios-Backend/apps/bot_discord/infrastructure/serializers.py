from rest_framework import serializers

class ResumenSerializer(serializers.Serializer):
    servidores_conectados = serializers.IntegerField()
    eventos_procesados_hoy = serializers.IntegerField()
    uptime_porcentaje = serializers.FloatField()
    ultima_sincronizacion = serializers.DateTimeField()

class EstadoSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["online", "offline", "maintenance"])
    uptime_dias = serializers.IntegerField()
    latencia_ms = serializers.FloatField()
    ultima_conexion = serializers.DateTimeField()

class ServerSerializer(serializers.Serializer):
    server_id = serializers.IntegerField()
    server_name = serializers.CharField(max_length=255)
    miembros = serializers.IntegerField()
    canales = serializers.IntegerField()
    status = serializers.ChoiceField(choices=["conectado", "desconectado"])

class MetricasPayloadSerializer(serializers.Serializer):
    resumen = ResumenSerializer()
    estado = EstadoSerializer()
    servers = serializers.ListField(child=ServerSerializer())

class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["online", "offline", "maintenance"])
