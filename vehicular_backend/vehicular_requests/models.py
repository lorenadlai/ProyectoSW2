from django.db import models
from django.contrib.auth.models import User

class VehicularRequest(models.Model):
    STATUS_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]
    TYPE_CHOICES = [
        ('antecedentes_persona', 'Persona'),
        ('datos_vehiculares', 'Vehiculo')
    ]
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default="")
    request_number = models.CharField(max_length=50, unique=True)
    
    plate = models.CharField(max_length=20, default='')
    serial_number = models.CharField(max_length=50, default='')
    
    person_name = models.CharField(max_length=50, default='')
    person_last_name = models.CharField(max_length=50, default='')
    
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='abierto'
    )
    def __str__(self):
        return f"Solicitud {self.request_number} - {self.name}"
    

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_p = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField(default='1980-11-01')
    nacionalidad = models.CharField(max_length=50, default='Mexicana')
    edad = models.IntegerField(default=44)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.IntegerField()
    placa = models.CharField(max_length=20, unique=True)
    numero_serie = models.CharField(max_length=20, unique=True, default='00000')
    color = models.CharField(max_length=30)
    propietario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='vehiculos')

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.placa})'

class Analista(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas')
    numero_de_consultas = models.IntegerField(default=0)

    def __str__(self):
        return f"Consulta de {self.usuario.username} - {self.numero_de_consultas} consultas"


class Policia(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nomina = models.CharField(max_length=50)
    unidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.nomina}"

class Incidencias(models.Model):
    request_number = models.CharField(max_length=100, primary_key=True)
    fecha = models.DateField()
    ubicacion = models.CharField(max_length=255)
    colonia = models.CharField(max_length=255)
    policia = models.ForeignKey(Policia, on_delete=models.CASCADE, related_name='incidencias')

    def __str__(self):
        return f"Incidencia {self.request_number} - {self.ubicacion}"