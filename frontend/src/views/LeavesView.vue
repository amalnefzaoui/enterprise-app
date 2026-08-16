<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Congés</h2>
        <p class="text-muted">{{ leaves.length }} demande(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouvelle demande' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouvelle demande de congé</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group">
              <label>Employé</label>
              <select v-model="form.employee_id" required :disabled="isEmployeeRole">
                <option disabled value="">Choisir un employé</option>
                <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                  {{ emp.first_name }} {{ emp.last_name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Type</label>
              <select v-model="form.type">
                <option value="congé_payé">Congé payé</option>
                <option value="maladie">Maladie</option>
                <option value="sans_solde">Sans solde</option>
                <option value="autre">Autre</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Date début</label>
              <input v-model="form.start_date" type="date" required />
            </div>
            <div class="form-group">
              <label>Date fin</label>
              <input v-model="form.end_date" type="date" required />
            </div>
          </div>
          <div class="form-group">
            <label>Motif (optionnel)</label>
            <textarea v-model="form.reason" rows="2"></textarea>
          </div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Envoi...' : 'Soumettre la demande' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="leaves.length === 0" class="empty-state">Aucune demande de congé.</div>
      <table v-else>
        <thead>
          <tr><th>Employé</th><th>Type</th><th>Période</th><th>Jours</th><th>Statut</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="lv in leaves" :key="lv.id">
            <td>{{ employeeName(lv.employee_id) }}</td>
            <td>{{ lv.type }}</td>
            <td>{{ lv.start_date }} → {{ lv.end_date }}</td>
            <td>{{ lv.days_count }}</td>
            <td><StatusPill :label="lv.status" :tone="statusTone(lv.status)" /></td>
            <td v-if="lv.status === 'en_attente' && canApprove">
              <div class="flex gap-8">
                <button class="btn btn-primary btn-sm" @click="updateStatus(lv.id, 'approuvé')">Approuver</button>
                <button class="btn btn-danger btn-sm" @click="updateStatus(lv.id, 'refusé')">Refuser</button>
              </div>
            </td>
            <td v-else></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import StatusPill from '../components/StatusPill.vue'
import { statusTone } from '../utils/statusTones'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isEmployeeRole = computed(() => auth.role === 'employee')
const canApprove = computed(() => ['admin', 'rh'].includes(auth.role))

const leaves = ref([])
const employees = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')

const form = ref({ employee_id: '', type: 'congé_payé', start_date: '', end_date: '', reason: '' })

function employeeName(id) {
  const emp = employees.value.find(e => e.id === id)
  return emp ? `${emp.first_name} ${emp.last_name}` : `#${id}`
}

async function loadData() {
  const [leavesRes, employeesRes] = await Promise.all([
    api.get('/api/leaves/'),
    api.get('/api/employees/')
  ])
  leaves.value = leavesRes.data
  employees.value = employeesRes.data

  if (isEmployeeRole.value && auth.employeeId) {
    form.value.employee_id = auth.employeeId
  }
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/api/leaves/', form.value)
    showForm.value = false
    form.value = { employee_id: '', type: 'congé_payé', start_date: '', end_date: '', reason: '' }
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la création de la demande'
  } finally {
    loading.value = false
  }
}

async function updateStatus(id, status) {
  try {
    await api.patch(`/api/leaves/${id}/status`, { status })
    await loadData()
  } catch (err) {
    alert(err.response?.data?.detail || "Action non autorisée (rôle admin/manager requis)")
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
