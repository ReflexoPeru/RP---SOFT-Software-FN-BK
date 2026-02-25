from rest_framework import serializers
from apps.practicantes.domain.practicante import Practicante, EstadoPracticante

# Serializer para entidades de dominio Practicante
class PracticanteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    id_discord = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    correo = serializers.EmailField()
    semestre = serializers.IntegerField()
    estado = serializers.ChoiceField(choices=[e.value for e in EstadoPracticante])

    def create(self, validated_data):
        # Convertir validated_data a entidad de dominio
        return Practicante(**validated_data)

    def update(self, instance: Practicante, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        return instance


# Serializer para las estadísticas de practicantes
class EstadisticasSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    activos = serializers.IntegerField()
    en_recuperacion = serializers.IntegerField()
    en_riesgo = serializers.IntegerField()
