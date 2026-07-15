<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Inscriptions</h2>
        <p class="text-muted">{{ enrollments.length }} inscription(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Inscrire un employé' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Inscrire un employé à une formation</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group">
              <label>Employé</label>
              <select v-model="form.employeeId" required>
                <option disabled value="">Choisir un employé</option>
                <option v-for="emp in employees" :key="emp.id" :value="emp.id">
                  {{ emp.first_name }} {{ emp.last_name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Formation</label>
              <select v-model="form.courseId" required>
                <option disabled value="">Choisir une formation</option>
                <option v-for="c in courses" :key="c.id" :value="c.id">{{ c.title }}</option>
              </select>
            </div>
          </div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Inscription...' : "Inscrire" }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="enrollments.length === 0" class="empty-state">Aucune inscription.</div>
      <table v-else>
        <thead>
          <tr><th>Employé</th><th>Formation</th><th>Progression</th><th>Statut</th><th>Mettre à jour</th></tr>
        </thead>
        <tbody>
          <tr v-for="e in enrollments" :key="e.id">
            <td>{{ employeeName(e.employeeId) }}</td>
            <td>{{ e.Course?.title || `#${e.courseId}` }}</td>
            <td>{{ e.progressPercent }}%</td>
            <td><StatusPill :label="e.completionStatus" :tone="statusTone(e.completionStatus)" /></td>
            <td>
              <div class="flex gap-8">
                <button class="btn btn-secondary btn-sm" @click="updateProgress(e.id, Math.min(100, e.progressPercent + 25))">
                  +25%
                </button>
              </div>
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
import trainingApi from '../services/trainingApi'
import StatusPill from '../components/StatusPill.vue'
import { statusTone } from '../utils/statusTones'

const enrollments = ref([])
const employees = ref([])
const courses = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')
const form = ref({ employeeId: '', courseId: '' })

function employeeName(id) {
  const emp = employees.value.find(e => e.id === id)
  return emp ? `${emp.first_name} ${emp.last_name}` : `#${id}`
}

async function loadData() {
  const [enrollmentsRes, employeesRes, coursesRes] = await Promise.all([
    trainingApi.get('/api/enrollments'),
    api.get('/api/employees/'),
    trainingApi.get('/api/courses')
  ])
  enrollments.value = enrollmentsRes.data
  employees.value = employeesRes.data
  courses.value = coursesRes.data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await trainingApi.post('/api/enrollments', form.value)
    showForm.value = false
    form.value = { employeeId: '', courseId: '' }
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.error || "Erreur lors de l'inscription"
  } finally {
    loading.value = false
  }
}

async function updateProgress(id, progressPercent) {
  try {
    await trainingApi.patch(`/api/enrollments/${id}/progress`, { progressPercent })
    await loadData()
  } catch (err) {
    alert(err.response?.data?.error || 'Erreur lors de la mise à jour')
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
