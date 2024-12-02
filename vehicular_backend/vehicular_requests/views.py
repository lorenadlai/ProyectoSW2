from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VehicularRequest, Vehiculo, Incidencias, Persona
from .serializers import VehicularRequestSerializer, VehiculoSerializer, IncidenciasSerializer, PersonaSerializer
from django.contrib.auth import authenticate, login
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class SaveRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VehicularRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Solicitud guardada correctamente."}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Obtener el grupo al que pertenece el usuario
            groups = user.groups.all()
            group_names = [group.name for group in groups]
            
            return Response({
                'message': 'Login successful',
                'user': user.username,
                'groups': group_names
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class VehicularRequestsByStatus(APIView):
    def get(self, request):
        # Obtén el valor de 'status' desde los parámetros de consulta
        status = request.query_params.get('status', None)
        
        # Si no se proporciona 'status', devuelve todos los registros
        if status:
            requests = VehicularRequest.objects.filter(status=status)
        else:
            requests = VehicularRequest.objects.all()

        serializer = VehicularRequestSerializer(requests, many=True)
        return Response(serializer.data)
    
class UpdateStatusView(APIView):
    def post(self, request, format=None):
        request_id = request.data.get('id')  # Obtener el ID de la solicitud

        # Validar si el ID está presente
        if not request_id:
            return Response({'error': 'El ID de la solicitud es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicular_request = VehicularRequest.objects.get(id=request_id)  # Buscar la solicitud por ID
        except VehicularRequest.DoesNotExist:
            return Response({'error': 'Solicitud no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el estado es "abierto" y cambiarlo a "cerrado"
        if vehicular_request.status == 'abierto':
            vehicular_request.status = 'cerrado'
            vehicular_request.save()
            return Response({
                'message': 'Estado actualizado con éxito a "cerrado"',
                'request_id': vehicular_request.id,
                'new_status': vehicular_request.status
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'El estado de la solicitud ya es "{vehicular_request.status}"'
            }, status=status.HTTP_200_OK)

class SendMessageToBot(APIView):
    def post(self, request):
        # Obtener datos del frontend: teléfono y mensaje a enviar
        phone = request.data.get('phone')
        message = request.data.get('message')

        # Validar los datos
        if not phone or not message:
            return Response({'error': 'phone and message are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Enviar el mensaje al bot (suponiendo que el bot corre en localhost:3000)
            response = requests.post('http://localhost:3001/send-message', json={'phone': phone, 'message': message})

            # Verificar la respuesta del bot
            if response.status_code == 200:
                return Response({'success': 'Message sent to bot successfully'})
            else:
                return Response({'error': 'Failed to send message to bot'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class VehiculoDetallesView(APIView):
    def get(self, request):
        plate = request.GET.get('plate')
        serial_number = request.GET.get('serial_number')

        if not plate or not serial_number:
            return Response({'error': 'Parámetros plate y serial_number son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener los detalles del vehículo basados en la placa y número de serie
            vehiculo = Vehiculo.objects.get(placa=plate, numero_serie=serial_number)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'Vehículo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Serializar los datos del vehículo, incluyendo la información del propietario
        serializer = VehiculoSerializer(vehiculo)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class VehiculosListView(APIView):
    def get(self, request):
        # Obtener todos los vehículos
        vehiculos = Vehiculo.objects.all()
        
        # Serializar los datos de todos los vehículos
        serializer = VehiculoSerializer(vehiculos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class IncidenciasAPIView(APIView):
    def get(self, request):
        request_number = request.GET.get('request_number')

        if not request_number:
            return Response({'error': 'El parámetro request_number es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener la incidencia basada en el request_number
            incidencia = Incidencias.objects.get(request_number=request_number)
        except Incidencias.DoesNotExist:
            return Response({'error': 'Incidencia no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Serializar los datos de la incidencia, incluyendo los datos del policía si es necesario
        serializer = IncidenciasSerializer(incidencia)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class PersonaDetallesView(APIView):
    def get(self, request):
        nombre = request.GET.get('nombre')
        apellido = request.GET.get('apellido_p')

        if not nombre or not apellido:
            return Response({'error': 'Parámetros nombre y apellido son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener el registro de la persona basado en nombre y apellido
            persona = Persona.objects.get(nombre=nombre, apellido_p=apellido)
            # Serializar los datos de la persona
            serializer = PersonaSerializer(persona)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Persona.DoesNotExist:
            return Response({'error': 'Persona no encontrada'}, status=status.HTTP_404_NOT_FOUND)