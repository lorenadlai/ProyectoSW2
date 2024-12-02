from django.contrib import admin
from .models import VehicularRequest, Persona, Vehiculo, Analista, Policia, Incidencias

@admin.register(VehicularRequest)
class VehicularRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'request_number', 'plate', 'serial_number', 'created_at', 'status')
    search_fields = ('name', 'request_number', 'plate', 'serial_number')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_p','nacionalidad','edad', 'direccion', 'telefono', 'fecha_nacimiento')
    search_fields = ('nombre', 'apellido_p', 'telefono')
    ordering = ('nombre',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'año', 'placa', 'color', 'propietario')
    search_fields = ('marca', 'modelo', 'placa', 'propietario__nombre')
    list_filter = ('año', 'color')
    ordering = ('marca',)

@admin.register(Analista)
class AnalistaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'numero_de_consultas')
    search_fields = ('usuario__username',)
    ordering = ('usuario',)
    
@admin.register(Policia)
class PoliciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'nomina', 'unidad')  # Campos que se muestran en la lista
    search_fields = ('nombre', 'apellido', 'nomina')  # Campos por los que se puede buscar
    list_filter = ('unidad',)  # Filtros para que el admin pueda filtrar por unidad
    ordering = ('apellido',)  # Ordenar por apellido

# Personalización de la vista de Incidencias en el Admin
@admin.register(Incidencias)

class IncidenciasAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'fecha', 'ubicacion', 'colonia', 'policia')  # Campos a mostrar en la lista
    search_fields = ('request_number', 'ubicacion', 'colonia')  # Campos por los que se puede buscar
    list_filter = ('fecha', 'policia')  # Filtros por fecha y policía
    ordering = ('fecha',)  # Ordenar por fecha