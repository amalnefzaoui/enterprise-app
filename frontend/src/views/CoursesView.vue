<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Formations</h2>
        <p class="text-muted">{{ courses.length }} formation(s) — service Node.js (remplace Moodle)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouvelle formation' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouvelle formation</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-group"><label>Titre</label><input v-model="form.title" required /></div>
          <div class="form-row">
            <div class="form-group"><label>Catégorie</label><input v-model="form.category" /></div>
            <div class="form-group"><label>Durée (heures)</label><input v-model.number="form.durationHours" type="number" /></div>
          </div>
          <div class="form-group"><label>Description</label><textarea v-model="form.description" rows="2"></textarea></div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Création...' : 'Créer la formation' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="courses.length === 0" class="empty-state">Aucune formation.</div>
      <table v-else>
        <thead><tr><th>Titre</th><th>Catégorie</th><th>Durée</th><th>Statut</th><th></th></tr></thead>
        <tbody>
          <tr v-for="c in courses" :key="c.id">
            <td>{{ c.title }}</td>
            <td>{{ c.category || '—' }}</td>
            <td>{{ c.durationHours }}h</td>
            <td><StatusPill :label="c.status" :tone="c.status === 'actif' ? 'success' : 'neutral'" /></td>
            <td><button class="btn btn-danger btn-sm" @click="handleDelete(c.id)">Supprimer</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import trainingApi from '../services/trainingApi'
import StatusPill from '../components/StatusPill.vue'

const courses = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')
const form = ref({ title: '', category: '', durationHours: 1, description: '' })

async function loadCourses() {
  const { data } = await trainingApi.get('/api/courses')
  courses.value = data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await trainingApi.post('/api/courses', form.value)
    showForm.value = false
    form.value = { title: '', category: '', durationHours: 1, description: '' }
    await loadCourses()
  } catch (err) {
    error.value = err.response?.data?.error || 'Erreur lors de la création'
  } finally {
    loading.value = false
  }
}

async function handleDelete(id) {
  if (!confirm('Supprimer cette formation ?')) return
  await trainingApi.delete(`/api/courses/${id}`)
  await loadCourses()
}

onMounted(loadCourses)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
