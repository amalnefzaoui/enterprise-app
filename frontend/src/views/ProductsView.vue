<template>
  <div>
    <div class="page-header flex-between">
      <div>
        <h2>Produits &amp; Stock</h2>
        <p class="text-muted">{{ products.length }} produit(s)</p>
      </div>
      <button class="btn btn-primary" @click="showForm = !showForm">
        {{ showForm ? 'Annuler' : '+ Nouveau produit' }}
      </button>
    </div>

    <div v-if="showForm" class="card mb-24">
      <div class="card-header"><h3>Nouveau produit</h3></div>
      <div class="card-body">
        <form @submit.prevent="handleCreate">
          <div class="form-row">
            <div class="form-group">
              <label>SKU</label>
              <input v-model="form.sku" required />
            </div>
            <div class="form-group">
              <label>Nom</label>
              <input v-model="form.name" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Prix d'achat (unit_cost)</label>
              <input v-model.number="form.unit_cost" type="number" step="0.01" />
            </div>
            <div class="form-group">
              <label>Prix de vente (unit_price)</label>
              <input v-model.number="form.unit_price" type="number" step="0.01" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Stock initial</label>
              <input v-model.number="form.stock_quantity" type="number" />
            </div>
            <div class="form-group">
              <label>Seuil d'alerte</label>
              <input v-model.number="form.reorder_level" type="number" />
            </div>
          </div>
          <div class="form-group">
            <label>Fournisseur</label>
            <select v-model="form.supplier_id">
              <option :value="null">Aucun</option>
              <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <p v-if="error" class="form-error">{{ error }}</p>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Création...' : 'Créer le produit' }}
          </button>
        </form>
      </div>
    </div>

    <div class="card">
      <div v-if="products.length === 0" class="empty-state">Aucun produit pour le moment.</div>
      <table v-else>
        <thead>
          <tr><th>SKU</th><th>Nom</th><th>Prix vente</th><th>Stock</th><th>Alerte</th><th>Ajuster</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td class="mono">{{ p.sku }}</td>
            <td>{{ p.name }}</td>
            <td>{{ p.unit_price }} DT</td>
            <td>{{ p.stock_quantity }}</td>
            <td>
              <StatusPill v-if="p.low_stock" label="stock bas" tone="warning" />
              <StatusPill v-else label="ok" tone="success" />
            </td>
            <td>
              <div class="flex gap-8">
                <button class="btn btn-secondary btn-sm" @click="adjustStock(p.id, 1)">+1</button>
                <button class="btn btn-secondary btn-sm" @click="adjustStock(p.id, -1)">-1</button>
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
import StatusPill from '../components/StatusPill.vue'

const products = ref([])
const suppliers = ref([])
const showForm = ref(false)
const loading = ref(false)
const error = ref('')

const form = ref({
  sku: '', name: '', unit_cost: 0, unit_price: 0,
  stock_quantity: 0, reorder_level: 10, supplier_id: null
})

async function loadData() {
  const [productsRes, suppliersRes] = await Promise.all([
    api.get('/api/products/'),
    api.get('/api/suppliers/')
  ])
  products.value = productsRes.data
  suppliers.value = suppliersRes.data
}

async function handleCreate() {
  error.value = ''
  loading.value = true
  try {
    await api.post('/api/products/', form.value)
    showForm.value = false
    form.value = { sku: '', name: '', unit_cost: 0, unit_price: 0, stock_quantity: 0, reorder_level: 10, supplier_id: null }
    await loadData()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors de la création du produit'
  } finally {
    loading.value = false
  }
}

async function adjustStock(id, delta) {
  try {
    await api.patch(`/api/products/${id}/stock`, {
      quantity: Math.abs(delta),
      operation: delta > 0 ? 'add' : 'remove'
    })
    await loadData()
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors de l'ajustement du stock")
  }
}

onMounted(loadData)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }
.form-error { color: var(--color-danger); font-size: 13px; margin-bottom: 12px; }
</style>
