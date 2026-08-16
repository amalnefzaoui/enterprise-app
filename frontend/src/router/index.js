import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue'), meta: { public: true } },
  {
    path: '/',
    component: () => import('../components/AppLayout.vue'),
    children: [
      { path: '', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
      { path: 'employees', name: 'employees', component: () => import('../views/EmployeesView.vue'), meta: { roles: ['admin', 'rh'] } },
      { path: 'leaves', name: 'leaves', component: () => import('../views/LeavesView.vue') },
      { path: 'attendance', name: 'attendance', component: () => import('../views/AttendanceView.vue') },
      { path: 'products', name: 'products', component: () => import('../views/ProductsView.vue'), meta: { roles: ['admin', 'manager'] } },
      { path: 'suppliers', name: 'suppliers', component: () => import('../views/SuppliersView.vue'), meta: { roles: ['admin', 'manager'] } },
      { path: 'customers', name: 'customers', component: () => import('../views/CustomersView.vue'), meta: { roles: ['admin', 'manager'] } },
      { path: 'purchase-orders', name: 'purchase-orders', component: () => import('../views/PurchaseOrdersView.vue'), meta: { roles: ['admin', 'manager'] } },
      { path: 'sales-orders', name: 'sales-orders', component: () => import('../views/SalesOrdersView.vue'), meta: { roles: ['admin', 'manager'] } },
      { path: 'invoices', name: 'invoices', component: () => import('../views/InvoicesView.vue'), meta: { roles: ['admin', 'manager'] } },
      { path: 'courses', name: 'courses', component: () => import('../views/CoursesView.vue') },
      { path: 'enrollments', name: 'enrollments', component: () => import('../views/EnrollmentsView.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login' }
  }
  if (to.name === 'login' && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
  if (to.meta.roles && !to.meta.roles.includes(auth.role)) {
    return { name: 'dashboard' }
  }
})

export default router