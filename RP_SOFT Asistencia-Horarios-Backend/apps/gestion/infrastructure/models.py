# gestion_horario/infrastructure/models.py
from django.db import models

class Horario(models.Model):
    practicante_id = models.IntegerField()
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=20, default="pendiente")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'horarios'
        unique_together = ('practicante_id', 'fecha', 'hora_inicio')
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"Horario {self.practicante_id} - {self.fecha}"