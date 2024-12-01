<template>
  <v-container>
    <v-card class="mx-auto my-12" max-width="400">
      <v-card-title>Iniciar Sesión</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            label="Usuario"
            v-model="username"
            outlined
            required
          ></v-text-field>
          <v-text-field
            label="Contraseña"
            v-model="password"
            type="password"
            outlined
            required
          ></v-text-field>
          <v-alert
            v-if="error"
            type="error"
            class="mt-4"
          >
            {{ error }}
          </v-alert>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="login">Iniciar Sesión</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';
    import axios from 'axios';

    const username = ref('');
    const password = ref('');
    const error = ref(null);
    const router = useRouter();

    const login = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/api/v1/login/', {
        username: username.value,
        password: password.value,
        });
        if (response.status === 200) {
        localStorage.setItem('user', JSON.stringify(response.data));
        router.push({ name: 'HomePage' }); // Redirige a HomePage
        }
    } catch (err) {
        error.value = 'Error de inicio de sesión. Verifica tus credenciales.';
    }
    };
</script>
