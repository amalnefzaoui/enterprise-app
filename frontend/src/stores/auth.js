import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role || null,
    employeeId: (state) => state.user?.employee_id || null
  },

  actions: {
    async login(email, password) {
      const { data } = await api.post('/api/auth/login', { email, password })
      this.token = data.token
      localStorage.setItem('token', data.token)

      // Récupère les infos complètes (dont employee_id) via /me
      const me = await api.get('/api/auth/me')
      this.user = { ...data.user, employee_id: me.data.employee_id }
      localStorage.setItem('user', JSON.stringify(this.user))
    },

    async register(email, password, role = 'employee') {
      const { data } = await api.post('/api/auth/register', { email, password, role })
      return data
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }
})
