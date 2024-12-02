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
    {title: 'Id', key: 'id', align: 'center'},
    { title: 'Nombre', key: 'name', align: 'center' },
    { title: 'Apellido', key: 'last_name', align: 'center' },
    { title: 'Telefono', key: 'phone_number', align: 'center' },
    { title: 'Num. de Solicitud', key: 'request_number', align: 'center' },
    { title: 'Placas', key: 'plate', align: 'center' },
    { title: 'Numero de Serie', key: 'serial_number', align: 'center' },
    { title: 'Detenido Nombre', key: 'person_name', align: 'center' },
    { title: 'Detenido AP', key: 'person_last_name', align: 'center' },
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

// Variables para el modal
const dialogVisible = ref(false);
const vehicleDetails = ref(null); // Datos del vehículo encontrados
const dialogVisible2 = ref(false);
const personDetails = ref(null);
const detenidoDetails = ref(null)
const persona_detenido = ref(null)
const phoneNumber = ref(null)
// Función para abrir el modal y realizar la consulta
const openDialog = async (item) => {
    try {
        // Realizamos la consulta al vehículo con plate y serial_number
        const response = await axios.get('http://127.0.0.1:8000/api/v1/vehicle/', {
            params: {
                plate: item.plate,
                serial_number: item.serial_number
            }
        });

        if (response.data) {
            vehicleData.value = response.data; // Asignamos los datos obtenidos al modal
            dialogVisible.value = true; // Mostramos el modal
        } else {
            console.log('Vehículo no encontrado');
            vehicleData.value = null; // Limpiamos los datos en caso de no encontrar el vehículo
        }
    } catch (error) {
        console.error('Error al consultar el vehículo:', error);
    }
};

// Función para cerrar el modal
const closeDialog = () => {
    dialogVisible.value = false;
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

const sendNotFoundVehicleMessage = async (phone, message) => {
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


const updateRequestStatus = async (requestId) => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/update-status/', {
            id: requestId  // Usamos solo el ID de la solicitud
        });
        if (response.status === 200) {
            location.reload();  // Recargar la página
        } else {
            console.log('Error al actualizar el estado');
        }
    } catch (error) {
        console.error('Error al actualizar el estado:', error.response ? error.response.data : error);
    }
};

const getVehicleDetails = async (plate, serial_number) => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/vehiculo-detalles?plate=${plate}&serial_number=${serial_number}`);
        vehicleDetails.value = response.data;
        dialogVisible.value = true;
    } catch (error) {
        console.error('Error al obtener detalles del vehículo:', error);
    }
};

const getPersonDetails = async (request_number) => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/get_incidencias?request_number=${request_number}`);
        personDetails.value = response.data;
        console.log(personDetails.value)

    } catch (error) {
        console.error('Error al obtener detalles de la persona:', error);
    }
};

const getPersona = async (nombre, apellido) => {
  try {
    // Realizamos la llamada GET con los parámetros nombre y apellido
    const response = await axios.get('http://127.0.0.1:8000/api/v1/persona-detalles/', {
      params: {
        nombre: nombre,
        apellido_p: apellido,
      }
    });

    persona_detenido.value = response.data;
    dialogVisible2.value = true;
    console.log("Persona Obtenida: ", persona_detenido.value)
  } catch (error) {
    console.error('Error al obtener detalles de la persona:', error);
  }
};

const validateRequest = (item) => {
  phoneNumber.value = item.phone_number
  if(item.person_name == '.'){
    detenidoDetails.value = item
    getPersonDetails(item.request_number)
    getVehicleDetails(item.plate, item.serial_number)
  }else{
    if(item.serial_number == '.'){ //datos de personas
      detenidoDetails.value = item
      console.log('Detenido Details: ', detenidoDetails.value)
      getPersonDetails(item.request_number)
      getPersona(item.person_name, item.person_last_name)
    } 
  }
}
const enviarDatosVehiculo = (item) => {
  console.log("Contenido Item: ", item)
  console.log("Contenido Details: ", detenidoDetails.value)
  console.log("Person Details: ", personDetails.value)
  let message = `
    NUESTRO ANALISTA ENCONTRÓ LA SIGUIENTE INFORMACIÓN ACERCA DEL VEHÍCULO 🚗🚗🚗 🎉🎉🎉
                    SOLICITUD DE CONSULTA: ${personDetails.value.request_number}
                    FECHA: ${personDetails.value.request_number}

                    POLICÍA: ${personDetails.value.policia.nombre} ${personDetails.value.policia.apellido}
                    NÓMINA: ${personDetails.value.policia.nomina}
                    UNIDAD: ${personDetails.value.policia.unidad}

                    UBICACIÓN: ${personDetails.value.ubicacion}

                    MARCA: ${item.marca}
                    MODELO: ${item.modelo}
                    SERIE: ${item.numero_serie}
                    PLACAS: ${item.placa}
                    COLOR: ${item.color}


                    VEHÍCULO CON CONDUCTOR (SI/NO): SI
                    NOMBRE DEL CONDUCTOR DEL VEHÍCULO: ${item.propietario.nombre}${item.propietario.apellido_p}
                    `;
                    sendNotFoundVehicleMessage(phoneNumber.value, message)
                    dialogVisible.value = false
                    updateRequestStatus(detenidoDetails.value.id)
}

const enviarDatosPersona = (item) => {
  console.log("Esto es el item:", item)
  console.log("Person Details:", personDetails.value)

  let message = `
    NUESTRO ANALISTA ENCONTRÓ LA SIGUIENTE INFORMACIÓN ACERCA DE LA PERSONA 🕵️🕵️🕵️ 🎉🎉🎉
                    SOLICITUD DE CONSULTA: ${item.request_number}
                    FECHA: ${item.fecha}

                    POLICÍA: ${item.policia.nombre} ${item.policia.apellido}
                    NÓMINA: ${item.policia.nomina}
                    UNIDAD: ${item.policia.unidad}

                    UBICACIÓN: ${item.ubicacion}
                    COLONIA: ${item.colonia}

                    NOMBRE DEL DETENIDO: ${persona_detenido.value.nombre} ${persona_detenido.value.nombre}
                    EDAD: ${persona_detenido.value.edad}
                    FECHA DE NACIMIENTO:${persona_detenido.value.fecha_nacimiento}
                    NACIONALIDAD: ${persona_detenido.value.nacionalidad}
                    DOMICILIO: ${persona_detenido.value.direccion}

                    `;
                    sendNotFoundVehicleMessage(phoneNumber.value, message)

                    dialogVisible2.value = false
                    //location.reload()
                    updateRequestStatus(detenidoDetails.value.id)
}
const validateType = (phone, item) => {
  console.log(item)
  //validar si se consulta datos del vehiculo
  if(item.person_name == '.'){ //buscó datos del vehiculo
    let message = `
    REGISTRO NO ENCONTRADO, ENVIA LA SIGUIENTE INFORMACION COMPLEMENTARIA 👍👍👍
                    SOLICITUD DE CONSULTA: ${item.request_number}
                    FECHA: xx/xx/2024

                    POLICÍA: ${item.name} ${item.last_name}
                    NÓMINA: xxx
                    UNIDAD: xxx

                    UBICACIÓN: xxx
                    COLONIA: xxx
                    SECTOR: xxx

                    MOTIVO DE LA CONSULTA: xxxx

                    SERIE: ${item.serial_number}
                    PLACAS: ${item.plate}

                    CARACTERÍSTICAS DEL VEHÍCULO: xxxx
                    CONDICIONES DEL VEHÍCULO: xxxx

                    VEHÍCULO CON CONDUCTOR (SI/NO): SI
                    NOMBRE DEL CONDUCTOR DEL VEHÍCULO: xxxx

                    REFERENCIA: xxx
                    `;
                    sendNotFoundVehicleMessage(phone, message)
  }

  if(item.plate == '.'){
    let message = `
        REGISTRO NO ENCONTRADO, ENVIA LA SIGUIENTE INFORMACION COMPLEMENTARIA 👍👍👍

                  SOLICITUD DE CONSULTA: ${item.request_number}
                  FECHA: xxx

                  POLICÍA: ${item.name} ${item.last_name}
                  NÓMINA: xxx
                  UNIDAD: xxx

                  UBICACIÓN: xxx
                  COLONIA: xxx
                  SECTOR: xxx

                  MOTIVO DE LA CONSULTA: xxx

                  NOMBRE DEL DETENIDO: ${item.person} ${item.person_last_name}
                  EDAD: xxx
                  FECHA DE NACIMIENTO:xxx
                  NACIONALIDAD: xxx
                  DOMICILIO: xxx

                  REFERENCIA: xxx
                  `;
                  sendNotFoundVehicleMessage(phone, message)
  }
  updateRequestStatus(item.id)
}

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
              @click="validateRequest(item)"
            >
              mdi-clipboard-search-outline
            </v-icon>
            <v-icon
              color="red"
              @click="validateType(item.phone_number, item)"
            >
                mdi-close-circle
            </v-icon>
          </template>
        </v-data-table>
      </v-col>

      <!-- Modal para mostrar los detalles del vehículo -->
      <v-dialog v-model="dialogVisible" max-width="800px">
        <v-card>
          <v-card-title>
            <span class="headline">Datos del Incidente</span>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.placa"
                  label="Placa"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.numero_serie"
                  label="Número de Serie"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.marca"
                  label="Marca"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.modelo"
                  label="Modelo"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.año"
                  label="Año"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.color"
                  label="Color"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.propietario.nombre"
                  label="Nombre del Propietario"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.propietario.apellido_p"
                  label="Apellido del Propietario"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.propietario.telefono"
                  label="Teléfono del Propietario"
                  disabled
                />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field
                  v-model="vehicleDetails.propietario.fecha_nacimiento"
                  label="Fecha de Nacimiento"
                  disabled
                />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" @click="enviarDatosVehiculo(vehicleDetails)">Enviar Datos</v-btn>
            <v-btn color="red" @click="dialogVisible = false">Cerrar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Modal para mostrar los detalles de la persona -->
      <v-dialog v-model="dialogVisible2" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="headline">Datos de la Incidencia</span>
        </v-card-title>
        <v-card-text>
          <!-- Detalles de la incidencia -->
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.request_number"
                label="Request Number"
                disabled
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.fecha"
                label="Fecha"
                disabled
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.ubicacion"
                label="Ubicación"
                disabled
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.colonia"
                label="Colonia"
                disabled
              />
            </v-col>
          </v-row>

          <!-- Detalles del policía asociado -->
          <v-row v-if="personDetails && personDetails.policia">
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.policia.nombre"
                label="Nombre Policía"
                disabled
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.policia.apellido"
                label="Apellido Policía"
                disabled
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="personDetails.policia.unidad"
                label="Unidad Policía"
                disabled
              />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" @click="enviarDatosPersona(personDetails)">Enviar Datos</v-btn>
          <v-btn color="red" @click="dialogVisible2 = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    </v-row>
  </v-container>
</template>
