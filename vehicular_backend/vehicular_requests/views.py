from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VehicularRequest
from .serializers import VehicularRequestSerializer
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