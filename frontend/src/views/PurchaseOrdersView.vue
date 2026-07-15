<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Commandes d'achat</h2>
        <p class="text-muted">{{ orders.length }} commande(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouvelle commande' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouvelle commande d'achat</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-group">
            <label>Fournisseur</label>
            <select v-model="form.supplier_id" required>
              <option disabled value="">Choisir un fournisseur</option>
              <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>

          <label class="items-label">Produits</label>
          <div v-for="(item, idx) in form.items" :key="idx" class="item-row">
            <select v-model="item.product_id" required>
              <option disabled value="">Produit</option>
              <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
            <input v-model.number="item.quantity" type="number" placeholder="Qté" min="1" required />
            <input v-model.number="item.unit_cost" type="number" step="0.01" placeholder="Prix unitaire" required />
            <button type="button" class="btn btn-danger btn-sm" @click="form.items.splice(idx, 1)">✕</button>
          </div>
          <button type="button" class="btn btn-secondary btn-sm mb-16" @click="addItem">+ Ajouter un produit</button>

          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Création...' : 'Créer la commande' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="orders.length === 0" class="empty-state">Aucune commande d'achat.</div>
      <table v-else>
        <thead>
          <tr><th>#</th><th>Fournisseur</th><th>Montant</th><th>Statut</th><th>Action</th></tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id">
            <td class="mono">#{{ o.id }}</td>
            <td>{{ supplierName(o.supplier_id) }}</td>
            <td>{{ o.total_amount }} DT</td>
            <td><StatusPill :label="o.status" :tone="statusTone(o.status)" /></td>
            <td>
              <select v-if="o.status !== 'reçue' && o.status !== 'annulée'"
                      @change="updateStatus(o.id, $event.target.value)" class="status-select">
                <option value="" disabled selected>Changer le statut</option>
                <option value="envoyée">Envoyée</option>
                <option value="reçue">Reçue (+ stock)</option>
                <option value="annulée">Annulée</option>
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

const orders = ref([])
const suppliers = ref([])
const products = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')

const form = ref({ supplier_id: '', items: [{ product_id: '', quantity: 1, unit_cost: 0 }] })

function addItem() {
  form.value.items.push({ product_id: '', quantity: 1, unit_cost: 0 })
}

function supplierName(id) {
  const s = suppliers.value.find(x => x.id === id)
  return s ? s.name : `#${id}`
}

async function loadData() {
  const [ordersRes, suppliersRes, productsRes] = await Promise.all([
    api.get('/api/purchase-orders/'),
    api.get('/api/suppliers/'),
    api.get('/api/products/')
  ])
  orders.value = ordersRes.data
  suppliers.value = suppliersRes.data
  products.value = productsRes.data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/api/purchase-orders/', form.value)
    showForm.value = false
    form.value = { supplier_id: '', items: [{ product_id: '', quantity: 1, unit_cost: 0 }] }
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la création de la commande'
  } finally {
    loading.value = false
  }
}

async function updateStatus(id, status) {
  try {
    await api.patch(`/api/purchase-orders/${id}/status`, { status })
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
.items-label { display: block; font-size: 13px; font-weight: 600; color: var(--color-text-muted); margin-bottom: 8px; }
.item-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto;
  gap: 10px;
  margin-bottom: 10px;
}
.item-row select, .item-row input {
  padding: 9px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
}
.status-select {
  padding: 6px 10px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 13px;
}
</style>
