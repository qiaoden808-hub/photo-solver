import { ref } from 'vue'

function getBaseUrl() {
  return localStorage.getItem('backend_url') || 'http://localhost:8000'
}

export function setBackendUrl(url) {
  localStorage.setItem('backend_url', url)
}

export function getBackendUrl() {
  return localStorage.getItem('backend_url') || ''
}

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  async function request(endpoint, options = {}) {
    loading.value = true
    error.value = null
    try {
      const base = getBaseUrl()
      const response = await fetch(`${base}${endpoint}`, {
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

  async function saveConfig(apiKey, endpoint, model) {
    return request('/api/config', {
      method: 'POST',
      body: JSON.stringify({ api_key: apiKey, endpoint, model }),
    })
  }

  async function getConfig() {
    return request('/api/config')
  }

  return {
    loading, error,
    solveProblem, getHistory, getHistoryItem,
    deleteHistory, saveConfig, getConfig,
  }
}
