<template>
  <div>
    <div class="page-header">
      <h2>Pointage</h2>
      <p class="text-muted">Enregistrer une entrée/sortie et consulter le rapport mensuel</p>
    </div>

    <div class="card mb-24">
      <div class="card-header"><h3>Pointer un employé</h3></div>
      <div class="card-body">
        <div class="form-row checkin-row">
          <div class="form-group">
            <label>Employé</label>
            <select v-model="selectedEmployee" :disabled="isEmployeeRole">
              <option disabled value="">Choisir un employé</option>
              <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                {{ emp.first_name }} {{ emp.last_name }}
              </option>
            </select>
          </div>
          <div class="flex gap-12 checkin-actions">
            <button class="btn btn-primary" :disabled="!selectedEmployee" @click="checkIn">Pointer l'entrée</button>
            <button class="btn btn-secondary" :disabled="!selectedEmployee" @click="checkOut">Pointer la sortie</button>
          </div>
        </div>
        <p v-if="message" class="checkin-message">{{ message }}</p>
      </div>
    </div>

    <div class="card">
      <div class="card-header"><h3>Rapport du mois</h3></div>
      <div class="card-body">
        <div v-if="report.length === 0" class="empty-state">Aucun pointage ce mois-ci.</div>
        <table v-else>
          <thead>
            <tr><th>Employé</th><th>Date</th><th>Entrée</th><th>Sortie</th><th>Statut</th></tr>
          </thead>
          <tbody>
            <tr v-for="r in report" :key="r.id">
              <td>{{ employeeName(r.employee_id) }}</td>
              <td>{{ r.date }}</td>
              <td class="mono">{{ r.check_in || '—' }}</td>
              <td class="mono">{{ r.check_out || '—' }}</td>
              <td><StatusPill :label="r.status" :tone="statusTone(r.status)" /></td>
            </tr>
          </tbody>
        </table>
      </div>
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

const employees = ref([])
const report = ref([])
const selectedEmployee = ref('')
const message = ref('')

function employeeName(id) {
  const emp = employees.value.find(e => e.id === id)
  return emp ? `${emp.first_name} ${emp.last_name}` : `#${id}`
}

async function loadData() {
  const [employeesRes, reportRes] = await Promise.all([
    api.get('/api/employees/'),
    api.get('/api/attendance/report')
  ])
  employees.value = employeesRes.data
  report.value = reportRes.data

  if (isEmployeeRole.value && auth.employeeId) {
    selectedEmployee.value = auth.employeeId
  }
}

async function checkIn() {
  message.value = ''
  try {
    await api.post('/api/attendance/checkin', { employee_id: selectedEmployee.value })
    message.value = 'Entrée enregistrée ✓'
    await loadData()
  } catch (err) {
    message.value = err.response?.data?.detail || 'Erreur lors du pointage'
  }
}

async function checkOut() {
  message.value = ''
  try {
    await api.post('/api/attendance/checkout', { employee_id: selectedEmployee.value })
    message.value = 'Sortie enregistrée ✓'
    await loadData()
  } catch (err) {
    message.value = err.response?.data?.detail || 'Erreur lors du pointage'
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.checkin-row { align-items: end; grid-template-columns: 1fr auto; }
.checkin-actions { padding-bottom: 14px; }
.checkin-message { font-size: 13px; color: var(--color-accent); margin: 0; }
</style>
