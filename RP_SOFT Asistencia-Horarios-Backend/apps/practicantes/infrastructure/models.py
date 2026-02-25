from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo que representa un practicante
class Practicante(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        EN_RECUPERACION = 'en_recuperacion', 'En Recuperación'
        EN_RIESGO = 'en_riesgo', 'En Riesgo'

    id_discord = models.BigIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    semestre = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)]) # Semestre entre 1 y 6
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )

    class Meta:
        db_table = "practicante"
        verbose_name = "Practicante"
        verbose_name_plural = "Practicantes"

    def __str__(self):
        return f'{self.nombre} {self.apellido}'
