from rest_framework import serializers
from .models import VehicularRequest, Persona, Vehiculo, Incidencias, Policia

class VehicularRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicularRequest
        fields = '__all__'

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona  # Asegúrate de que la clase Persona esté correctamente definida
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    propietario = PersonaSerializer()

    class Meta:
        model = Vehiculo
        fields = '__all__'
        
        
class PoliciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Policia
        fields = ['nombre', 'apellido', 'nomina', 'unidad']

class IncidenciasSerializer(serializers.ModelSerializer):
    # Incluir los detalles del policía usando un serializer anidado
    policia = PoliciaSerializer()

    class Meta:
        model = Incidencias
        fields = ['request_number', 'fecha', 'ubicacion', 'colonia', 'policia']

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'
