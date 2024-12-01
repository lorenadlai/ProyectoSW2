from django.contrib import admin
from .models import VehicularRequest
# Register your models here.

@admin.register(VehicularRequest)
class VehicularRequest(admin.ModelAdmin):
    pass