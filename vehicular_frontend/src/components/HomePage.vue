<script setup>
import { ref, onMounted } from 'vue';    
import axios from 'axios';

// Obtener el usuario del localStorage
const user = JSON.parse(localStorage.getItem('user')) || {};

// Función para cerrar sesión
const logout = () => {
    localStorage.removeItem('user');
    location.reload(); // Redirige a Login automáticamente
};

// Datos para la tabla
const selectedServices = ref([]);

// Cabeceras de la tabla
const headers = [
    { title: 'Nombre', key: 'name', align: 'center' },
    { title: 'Apellido', key: 'last_name', align: 'center' },
    { title: 'Telefono', key: 'phone_number', align: 'center' },
    { title: 'Num. de Solicitud', key: 'request_number', align: 'center' },
    { title: 'Placas', key: 'plate', align: 'center' },
    { title: 'Numero de Serie', key: 'serial_number', align: 'center' },
    { title: 'Acciones', key: 'action', align: 'center', sortable: false },
];

// Cargar solicitudes
const loadRequest = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/vehicular-requests/?status=abierto');
        selectedServices.value = response.data;
        console.log('Servicios cargados:', selectedServices.value);
    } catch (error) {
        console.error('Error al cargar servicios:', error);
    }
};
const sendMessage = async (phone, message) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/send-message/', {
            phone: phone,  // Número de teléfono del usuario de WhatsApp
            message: message,  // Mensaje que quieres enviar (por ejemplo, "Información no encontrada")
        });
        console.log('Mensaje enviado correctamente:', response.data);
    } catch (error) {
        console.error('Error al enviar el mensaje:', error);
    }
};
// Ejecutar al montar el componente
onMounted(() => {
    loadRequest();
});
</script>

<template>
  <v-container>
    <h1>Bienvenido, {{ user.username }}</h1>
    <v-btn color="error" @click="logout">Cerrar Sesión</v-btn>
    <v-row class="pt-6">
      <v-col cols="12">
        <!-- Tabla para mostrar servicios seleccionados -->
        <v-data-table
          :headers="headers"
          :items="selectedServices"
          item-key="id"
        >
          <template v-slot:item.action="{ item }">
            <v-icon
              color="green"
              @click="sendMessage(item.phone_number, 'Hola si estuvo el pedo')"
            >
                mdi-check-circle
            </v-icon>
            <v-icon
              color="red"
            >
                mdi-close-circle
            </v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>
