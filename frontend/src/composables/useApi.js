import { ref } from 'vue'

// Change this to your Vercel backend URL when deploying
const API_BASE = 'https://photo-solver.vercel.app'

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  async function request(endpoint, options = {}) {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
      })
      if (!response.ok) {
        const text = await response.text()
        throw new Error(text || `Request failed (${response.status})`)
      }
      const data = await response.json()
      return data
    } catch (err) {
      error.value = err.message || 'Network error'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function solveProblem(imageBase64, filename) {
    return request('/api/solve', {
      method: 'POST',
      body: JSON.stringify({ image: imageBase64, filename: filename || 'photo.jpg' }),
    })
  }

  async function getHistory() {
    return request('/api/history')
  }

  async function getHistoryItem(id) {
    return request(`/api/history/${id}`)
  }

  async function deleteHistory(id) {
    return request(`/api/history/${id}`, { method: 'DELETE' })
  }

  return {
    loading, error,
    solveProblem, getHistory, getHistoryItem, deleteHistory,
  }
}
