<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Fournisseurs</h2>
        <p class="text-muted">{{ suppliers.length }} fournisseur(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouveau fournisseur' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouveau fournisseur</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group"><label>Nom</label><input v-model="form.name" required /></div>
            <div class="form-group"><label>Contact</label><input v-model="form.contact_name" /></div>
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
      <div v-if="suppliers.length === 0" class="empty-state">Aucun fournisseur.</div>
      <table v-else>
        <thead><tr><th>Nom</th><th>Contact</th><th>Email</th><th>Téléphone</th><th></th></tr></thead>
        <tbody>
          <tr v-for="s in suppliers" :key="s.id">
            <td>{{ s.name }}</td>
            <td>{{ s.contact_name || '—' }}</td>
            <td>{{ s.email || '—' }}</td>
            <td>{{ s.phone || '—' }}</td>
            <td><button class="btn btn-danger btn-sm" @click="handleDelete(s.id)">Supprimer</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const suppliers = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')
const form = ref({ name: '', contact_name: '', email: '', phone: '', address: '' })

async function loadSuppliers() {
  const { data } = await api.get('/api/suppliers/')
  suppliers.value = data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/api/suppliers/', form.value)
    showForm.value = false
    form.value = { name: '', contact_name: '', email: '', phone: '', address: '' }
    await loadSuppliers()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la création'
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Supprimer ce fournisseur ?')) return
  await api.delete(`/api/suppliers/${id}`)
  await loadSuppliers()
}

onMounted(loadSuppliers)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
