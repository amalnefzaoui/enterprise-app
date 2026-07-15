import axios from 'axios'

const trainingClient = axios.create({
  baseURL: import.meta.env.VITE_TRAINING_URL || 'http://localhost:5000',
  headers: { 'Content-Type': 'application/json' }
})

export default trainingClient
