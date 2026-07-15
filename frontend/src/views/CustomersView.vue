<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Clients</h2>
        <p class="text-muted">{{ customers.length }} client(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouveau client' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouveau client</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group"><label>Nom</label><input v-model="form.name" required /></div>
            <div class="form-group">
              <label>Type</label>
              <select v-model="form.type">
                <option value="entreprise">Entreprise</option>
                <option value="particulier">Particulier</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group"><label>Email</label><input v-model="form.email" type="email" /></div>
            <div class="form-group"><label>Téléphone</label><input v-model="form.phone" /></div>
          </div>
          <div class="form-group"><label>Adresse</label><input v-model="form.address" /></div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Création...' : 'Créer' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="customers.length === 0" class="empty-state">Aucun client.</div>
      <table v-else>
        <thead><tr><th>Nom</th><th>Type</th><th>Email</th><th>Téléphone</th><th></th></tr></thead>
        <tbody>
          <tr v-for="c in customers" :key="c.id">
            <td>{{ c.name }}</td>
            <td>{{ c.type }}</td>
            <td>{{ c.email || '—' }}</td>
            <td>{{ c.phone || '—' }}</td>
            <td><button class="btn btn-danger btn-sm" @click="handleDelete(c.id)">Supprimer</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const customers = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')
const form = ref({ name: '', type: 'entreprise', email: '', phone: '', address: '' })

async function loadCustomers() {
  const { data } = await api.get('/api/customers/')
  customers.value = data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/api/customers/', form.value)
    showForm.value = false
    form.value = { name: '', type: 'entreprise', email: '', phone: '', address: '' }
    await loadCustomers()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la création'
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Supprimer ce client ?')) return
  await api.delete(`/api/customers/${id}`)
  await loadCustomers()
}

onMounted(loadCustomers)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
