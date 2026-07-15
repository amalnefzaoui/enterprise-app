<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Factures</h2>
        <p class="text-muted">{{ invoices.length }} facture(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Générer une facture' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Générer une facture</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group">
              <label>Type</label>
              <select v-model="form.type">
                <option value="vente">Vente</option>
                <option value="achat">Achat</option>
              </select>
            </div>
            <div class="form-group">
              <label>Commande de référence (ID)</label>
              <input v-model.number="form.reference_order_id" type="number" required />
            </div>
          </div>
          <div class="form-group">
            <label>Date d'échéance</label>
            <input v-model="form.due_date" type="date" />
          </div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Génération...' : 'Générer la facture' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="invoices.length === 0" class="empty-state">Aucune facture.</div>
      <table v-else>
        <thead>
          <tr><th>N° Facture</th><th>Type</th><th>Montant</th><th>Échéance</th><th>Statut</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="inv in invoices" :key="inv.id">
            <td class="mono">{{ inv.invoice_number }}</td>
            <td>{{ inv.type }}</td>
            <td>{{ inv.amount }} DT</td>
            <td>{{ inv.due_date || '—' }}</td>
            <td><StatusPill :label="inv.status" :tone="statusTone(inv.status)" /></td>
            <td>
              <select v-if="inv.status !== 'payée'" @change="updateStatus(inv.id, $event.target.value)" class="status-select">
                <option value="" disabled selected>Changer</option>
                <option value="payée">Marquer payée</option>
                <option value="en_retard">Marquer en retard</option>
              </select>
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

const invoices = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')
const form = ref({ type: 'vente', reference_order_id: null, due_date: '' })

async function loadInvoices() {
  const { data } = await api.get('/api/invoices/')
  invoices.value = data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    const payload = { ...form.value }
    if (!payload.due_date) delete payload.due_date
    await api.post('/api/invoices/', payload)
    showForm.value = false
    form.value = { type: 'vente', reference_order_id: null, due_date: '' }
    await loadInvoices()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la génération de la facture'
  } finally {
    loading.value = false
  }
}

async function updateStatus(id, status) {
  try {
    await api.patch(`/api/invoices/${id}/status`, { status })
    await loadInvoices()
  } catch (err) {
    alert(err.response?.data?.detail || "Action non autorisée (rôle admin/manager requis)")
  }
}

onMounted(loadInvoices)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
.status-select {
  padding: 6px 10px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 13px;
}
</style>
