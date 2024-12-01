from django.db import models

class VehicularRequest(models.Model):
    STATUS_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, default="")
    request_number = models.CharField(max_length=50, unique=True)
    plate = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='abierto'
    )

    def __str__(self):
        return f"Solicitud {self.request_number} - {self.name}"