<template>
  <div class="login-screen">
    <div class="login-card card">
      <div class="login-brand">
        <div class="brand-mark">EA</div>
        <h1>Enterprise App</h1>
        <p class="text-muted">Gestion RH &amp; Achat/Vente</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" placeholder="admin@entreprise.local" required />
        </div>
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input id="password" v-model="password" type="password" placeholder="••••••••" required />
        </div>

        <p v-if="error" class="login-error">{{ error }}</p>

        <button type="submit" class="btn btn-primary login-submit" :disabled="loading">
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>

      <p class="login-hint text-muted">
        Pas encore de compte ? Crée-en un via
        <code class="mono">POST /api/auth/register</code>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push({ name: 'dashboard' })
  } catch (err) {
    error.value = err.response?.data?.detail || 'Email ou mot de passe incorrect'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-screen {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary);
  background-image: radial-gradient(circle at 20% 20%, rgba(14,148,136,0.25), transparent 40%),
                     radial-gradient(circle at 80% 80%, rgba(14,148,136,0.15), transparent 40%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 380px;
  padding: 36px 32px;
}

.login-brand {
  text-align: center;
  margin-bottom: 28px;
}
.login-brand .brand-mark {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: var(--color-accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-weight: 700;
  margin: 0 auto 14px;
}
.login-brand h1 {
  font-size: 20px;
  margin-bottom: 4px;
}
.login-brand p {
  font-size: 13px;
  margin: 0;
}

.login-submit {
  width: 100%;
  justify-content: center;
  margin-top: 6px;
}

.login-error {
  color: var(--color-danger);
  font-size: 13px;
  margin: 0 0 12px;
}

.login-hint {
  text-align: center;
  font-size: 12px;
  margin-top: 22px;
  margin-bottom: 0;
}
</style>
