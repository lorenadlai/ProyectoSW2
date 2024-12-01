const { createBot, createFlow, addKeyword } = require('@bot-whatsapp/bot');
const BaileysProvider = require('@bot-whatsapp/provider/baileys');
const MockAdapter = require('@bot-whatsapp/database/mock');
const  QRPortalWeb = require('@bot-whatsapp/portal')
const axios = require('axios');
const express = require('express');

// Inicializamos Express
const app = express();
app.use(express.json());

// Objeto para almacenar los datos temporales del usuario
let userData = {};
let adapterProvider;

// Flujo para capturar datos paso a paso
const flujoConsulta = addKeyword(['hola', 'buenas', 'consulta', 'Hola'])
    .addAnswer(
        '¡Hola! Vamos a realizar una consulta vehicular. Por favor responde a las siguientes preguntas.',
        { capture: false },
        (ctx) => {
            console.log('Iniciando consulta:', ctx.from);
            userData.phone_number = ctx.from
        }
    )
    .addAnswer(
        '¿Cuál es tu nombre?',
        { capture: true },
        (ctx) => {
            userData.name = ctx.body; // Guarda el nombre del usuario
        }
    )
    .addAnswer(
        '¿Cuál es tu apellido?',
        { capture: true },
        (ctx) => {
            userData.last_name = ctx.body; // Guarda el nombre del usuario
        }
    )
    .addAnswer(
        '¿Cuál es tu número de solicitud?',
        { capture: true },
        (ctx) => {
            userData.request_number = ctx.body; // Guarda el número de solicitud
        }
    )
    .addAnswer(
        '¿Cuál es la placa del vehículo?',
        { capture: true },
        (ctx) => {
            userData.plate = ctx.body; // Guarda la placa del vehículo
        }
    )
    .addAnswer(
        '¿Cuál es el número de serie del vehículo?',
        { capture: true },
        async (ctx, { endFlow }) => {
            userData.serial_number = ctx.body; // Guarda el número de serie

            // Enviar los datos al backend
            try {
                const response = await axios.post(
                    'http://127.0.0.1:8000/api/v1/save-request/',
                    userData
                );
                console.log('Datos enviados al backend:', response.data);

                // Mensaje de confirmación
                return endFlow(
                    '¡Gracias! Tu solicitud ha sido enviada al sistema para su análisis.'
                );
            } catch (error) {
                if (error.response) {
                    console.log(error.response.data);  // Detalles del error
                    console.log(error.response.status);
                  } else {
                    console.log('Error: ', error.message);
                  }
                return endFlow(
                    'Hubo un problema al enviar tu solicitud. Por favor, inténtalo más tarde.'
                );
            }
        }
    );

// Configuración principal del bot
const main = async () => {
    const adapterDB = new MockAdapter(); // Base de datos simulada
    const adapterFlow = createFlow([flujoConsulta]); // Flujo principal
    adapterProvider = new BaileysProvider(); // Proveedor de WhatsApp

    createBot({
        flow: adapterFlow,
        provider: adapterProvider,
        database: adapterDB,
    });

    // Muestra el código QR en un portal web
    QRPortalWeb();
};

// Endpoint para recibir y enviar mensajes desde el backend al bot
app.post('/send-message', async (req, res) => {
    const { phone, message } = req.body;
    console.log(req.body);
    if (!phone || !message) {
        return res.status(400).json({ error: 'phone and message are required' });
    }

    // Formatear el número de teléfono en el formato adecuado
    const formattedPhone = `${phone.replace('+', '')}@s.whatsapp.net`; // Eliminar el "+" si lo recibes en ese formato.
    console.log('Formatted phone:', formattedPhone);

    try {
        // Usar el provider para enviar el mensaje
        const response = await adapterProvider.sendText(formattedPhone, message);
        res.json({ success: true, response });
    } catch (error) {
        if (error.response) {
            console.log(error.response.data);  // Detalles del error
            console.log(error.response.status);
        } else {
            console.log('Error: ', error.message);
        }
        res.status(500).json({ success: false, error: 'Error al enviar el mensaje' });
    }
});



// Iniciar el servidor Express en el puerto 3001
app.listen(3001, () => {
    console.log('Servidor escuchando en http://localhost:3001');
});

// Ejecutar el bot
main();