from rest_framework import serializers
from .models import VehicularRequest

class VehicularRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicularRequest
        fields = '__all__'
