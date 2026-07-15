<template>
  <div>
    <div class="page-header">
      <h2>Tableau de bord</h2>
      <p class="text-muted">Vue d'ensemble RH et Achat/Vente</p>
    </div>

    <div class="stat-grid">
      <div class="stat-card card">
        <div class="stat-label">Employés</div>
        <div class="stat-value">{{ stats.employees }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">Congés en attente</div>
        <div class="stat-value">{{ stats.pendingLeaves }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">Produits en stock bas</div>
        <div class="stat-value" :class="{ 'stat-alert': stats.lowStock > 0 }">{{ stats.lowStock }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">Factures impayées</div>
        <div class="stat-value">{{ stats.unpaidInvoices }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">Commandes vente (brouillon)</div>
        <div class="stat-value">{{ stats.draftSalesOrders }}</div>
      </div>
      <div class="stat-card card">
        <div class="stat-label">Formations actives</div>
        <div class="stat-value">{{ stats.courses }}</div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h3>Alertes stock bas</h3>
      </div>
      <div class="card-body">
        <div v-if="lowStockProducts.length === 0" class="empty-state">
          Aucune alerte de stock pour le moment.
        </div>
        <table v-else>
          <thead>
            <tr><th>SKU</th><th>Produit</th><th>Stock actuel</th><th>Seuil</th></tr>
          </thead>
          <tbody>
            <tr v-for="p in lowStockProducts" :key="p.id">
              <td class="mono">{{ p.sku }}</td>
              <td>{{ p.name }}</td>
              <td>{{ p.stock_quantity }}</td>
              <td>{{ p.reorder_level }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import trainingApi from '../services/trainingApi'

const stats = ref({
  employees: '—',
  pendingLeaves: '—',
  lowStock: '—',
  unpaidInvoices: '—',
  draftSalesOrders: '—',
  courses: '—'
})
const lowStockProducts = ref([])

async function loadStats() {
  try {
    const [employees, leaves, products, invoices, salesOrders, courses] = await Promise.all([
      api.get('/api/employees/'),
      api.get('/api/leaves/', { params: { status_filter: 'en_attente' } }),
      api.get('/api/products/'),
      api.get('/api/invoices/', { params: { status_filter: 'impayée' } }),
      api.get('/api/sales-orders/', { params: { status_filter: 'brouillon' } }),
      trainingApi.get('/api/courses')
    ])

    stats.value.employees = employees.data.length
    stats.value.pendingLeaves = leaves.data.length
    stats.value.unpaidInvoices = invoices.data.length
    stats.value.draftSalesOrders = salesOrders.data.length
    stats.value.courses = courses.data.filter(c => c.status === 'actif').length

    lowStockProducts.value = products.data.filter(p => p.low_stock)
    stats.value.lowStock = lowStockProducts.value.length
  } catch (err) {
    console.error('Erreur de chargement du tableau de bord', err)
  }
}

onMounted(loadStats)
</script>

<style scoped>
.page-header { margin-bottom: 24px; }
.page-header p { margin-top: 4px; }

.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card { padding: 20px; }
.stat-label {
  font-size: 12.5px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}
.stat-value {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 700;
}
.stat-alert { color: var(--color-warning); }
</style>
