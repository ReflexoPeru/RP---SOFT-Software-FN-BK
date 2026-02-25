from django.db import models

class MetricasGlobalesBot(models.Model):
    servidores_conectados = models.IntegerField(default=0)
    eventos_procesados_hoy = models.IntegerField(default=0)
    uptime_porcentaje = models.FloatField(default=100.0)
    ultima_sincronizacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "metricas_globales_bot"
        verbose_name = "Métricas Globales del Bot"
        verbose_name_plural = "Métricas Globales del Bot"

class EstadoBot(models.Model):
    STATUS_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("maintenance", "Maintenance"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offline")
    uptime_dias = models.IntegerField(default=0)
    latencia_ms = models.FloatField(default=0.0)
    ultima_conexion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "estado_bot"
        verbose_name = "Estado del Bot"
        verbose_name_plural = "Estados del Bot"

class ServidoresBot(models.Model):
    STATUS_CHOICES = [
        ("conectado", "Conectado"),
        ("desconectado", "Desconectado"),
    ]
    server_id = models.BigIntegerField(unique=True)
    server_name = models.CharField(max_length=255)
    miembros = models.IntegerField(default=0)
    canales = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="desconectado")
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "servidores_bot"
        verbose_name = "Servidor del Bot"
        verbose_name_plural = "Servidores del Bot"
