<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <div class="brand-mark">EA</div>
        <div>
          <div class="brand-title">Enterprise App</div>
          <div class="brand-subtitle">RH &amp; Achat/Vente</div>
        </div>
      </div>

      <nav class="nav-group">
        <div class="nav-label">Vue d'ensemble</div>
        <RouterLink to="/" class="nav-link" exact-active-class="nav-link-active">
          <span class="nav-dot" /> Tableau de bord
        </RouterLink>
      </nav>

      <nav class="nav-group">
        <div class="nav-label">Ressources Humaines</div>
        <RouterLink v-if="canManageRH" to="/employees" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Employés
        </RouterLink>
        <RouterLink to="/leaves" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Congés
        </RouterLink>
        <RouterLink to="/attendance" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Pointage
        </RouterLink>
        <RouterLink to="/courses" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Formations
        </RouterLink>
        <RouterLink to="/enrollments" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Inscriptions
        </RouterLink>
      </nav>

      <nav v-if="canManageAchatVente" class="nav-group">
        <div class="nav-label">Achat / Vente</div>
        <RouterLink to="/products" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Produits &amp; Stock
        </RouterLink>
        <RouterLink to="/suppliers" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Fournisseurs
        </RouterLink>
        <RouterLink to="/customers" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Clients
        </RouterLink>
        <RouterLink to="/purchase-orders" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Commandes achat
        </RouterLink>
        <RouterLink to="/sales-orders" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Commandes vente
        </RouterLink>
        <RouterLink to="/invoices" class="nav-link" active-class="nav-link-active">
          <span class="nav-dot" /> Factures
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="user-chip">
          <div class="user-avatar">{{ initials }}</div>
          <div class="user-meta">
            <div class="user-email">{{ auth.user?.email }}</div>
            <div class="user-role">{{ auth.role }}</div>
          </div>
        </div>
        <button class="btn btn-secondary btn-sm logout-btn" @click="handleLogout">
          Déconnexion
        </button>
      </div>
    </aside>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const initials = computed(() => {
  const email = auth.user?.email || '?'
  return email.slice(0, 2).toUpperCase()
})

const canManageRH = computed(() => ['admin', 'rh'].includes(auth.role))
const canManageAchatVente = computed(() => ['admin', 'manager'].includes(auth.role))

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: var(--sidebar-width);
  flex-shrink: 0;
  background: var(--color-primary);
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px 14px;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.12);
  margin-bottom: 16px;
}

.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
}

.brand-title {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 14px;
  line-height: 1.2;
}
.brand-subtitle {
  font-size: 11px;
  color: rgba(255,255,255,0.6);
}

.nav-group {
  margin-bottom: 18px;
}
.nav-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(255,255,255,0.45);
  padding: 0 10px 6px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: var(--radius-sm);
  font-size: 13.5px;
  color: rgba(255,255,255,0.8);
  border-left: 2px solid transparent;
  transition: background 0.15s ease, color 0.15s ease;
}
.nav-link:hover {
  background: rgba(255,255,255,0.06);
  color: white;
}
.nav-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.6;
  flex-shrink: 0;
}
.nav-link-active {
  background: rgba(255,255,255,0.1);
  color: white;
  border-left-color: var(--color-accent);
  font-weight: 600;
}
.nav-link-active .nav-dot {
  background: var(--color-accent);
  opacity: 1;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid rgba(255,255,255,0.12);
}
.user-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  margin-bottom: 10px;
}
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-accent-light);
  color: var(--color-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  flex-shrink: 0;
}
.user-meta { min-width: 0; }
.user-email {
  font-size: 12.5px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.user-role {
  font-size: 11px;
  color: rgba(255,255,255,0.5);
  text-transform: capitalize;
}
.logout-btn {
  width: 100%;
  justify-content: center;
}

.content {
  flex: 1;
  padding: 28px 32px;
  min-width: 0;
}

@media (max-width: 900px) {
  .layout { flex-direction: column; }
  .sidebar { width: 100%; height: auto; position: relative; }
  .content { padding: 20px; }
}
</style>
