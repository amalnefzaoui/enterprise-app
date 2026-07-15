<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Employés</h2>
        <p class="text-muted">{{ employees.length }} employé(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouvel employé' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouvel employé</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group">
              <label>Prénom</label>
              <input v-model="form.first_name" required />
            </div>
            <div class="form-group">
              <label>Nom</label>
              <input v-model="form.last_name" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Email</label>
              <input v-model="form.email" type="email" required />
            </div>
            <div class="form-group">
              <label>Poste</label>
              <input v-model="form.position" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Département</label>
              <input v-model="form.department" />
            </div>
            <div class="form-group">
              <label>Date d'embauche</label>
              <input v-model="form.hire_date" type="date" />
            </div>
          </div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Création...' : 'Créer l\'employé' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="employees.length === 0" class="empty-state">
        Aucun employé pour le moment. Ajoute le premier avec le bouton ci-dessus.
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>Nom</th><th>Email</th><th>Poste</th><th>Département</th>
            <th>Solde congés</th><th>Statut</th><th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in employees" :key="emp.id">
            <td>{{ emp.first_name }} {{ emp.last_name }}</td>
            <td>{{ emp.email }}</td>
            <td>{{ emp.position || '—' }}</td>
            <td>{{ emp.department || '—' }}</td>
            <td>{{ emp.leave_balance }} jours</td>
            <td><StatusPill :label="emp.status" :tone="statusTone(emp.status)" /></td>
            <td>
              <button class="btn btn-danger btn-sm" @click="handleDelete(emp.id)">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import StatusPill from '../components/StatusPill.vue'
import { statusTone } from '../utils/statusTones'

const employees = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')

const form = ref({
  first_name: '', last_name: '', email: '', position: '', department: '', hire_date: ''
})

async function loadEmployees() {
  const { data } = await api.get('/api/employees/')
  employees.value = data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    const payload = { ...form.value }
    if (!payload.hire_date) delete payload.hire_date
    await api.post('/api/employees/', payload)
    showForm.value = false
    form.value = { first_name: '', last_name: '', email: '', position: '', department: '', hire_date: '' }
    await loadEmployees()
  } catch (err) {
    error.value = err.response?.data?.detail || "Erreur lors de la création (vérifie que tu es connecté en tant qu'admin)"
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Supprimer cet employé ?')) return
  try {
    await api.delete(`/api/employees/${id}`)
    await loadEmployees()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erreur lors de la suppression')
  }
}

onMounted(loadEmployees)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
