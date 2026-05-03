<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi.js'
import { getBackendUrl, setBackendUrl } from '../composables/useApi.js'

const emit = defineEmits(['go-back'])

const { saveConfig, getConfig, loading } = useApi()

const apiKey = ref('')
const endpoint = ref('https://api.openai.com/v1')
const model = ref('gpt-4o')
const backendUrl = ref('')
const saveSuccess = ref(false)
const saveError = ref(null)
const configLoaded = ref(false)

onMounted(async () => {
  try {
    const config = await getConfig()
    if (config) {
      apiKey.value = config.api_key || ''
      endpoint.value = config.endpoint || 'https://api.openai.com/v1'
      model.value = config.model || 'gpt-4o'
    }
  } catch (err) {
    console.log('No existing config')
  }
  backendUrl.value = getBackendUrl()
  configLoaded.value = true
})

async function handleSave() {
  saveSuccess.value = false
  saveError.value = null

  if (!apiKey.value.trim()) {
    saveError.value = 'Please enter API Key'
    return
  }

  try {
    // Save backend URL locally
    setBackendUrl(backendUrl.value.trim())
    // Save API config to backend
    await saveConfig(apiKey.value.trim(), endpoint.value.trim(), model.value.trim())
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 3000)
  } catch (err) {
    saveError.value = err.message || 'Save failed'
  }
}
</script>

<template>
  <div class="settings-page">
    <div class="settings-header">
      <h2>⚙️ Settings</h2>
      <p class="settings-desc">Configure AI & Backend</p>
    </div>

    <div v-if="!configLoaded" class="loading-state"><p>Loading...</p></div>

    <div v-else class="settings-form">
      <div class="form-group">
        <label class="form-label"><span class="label-icon">🔑</span>API Key</label>
        <input v-model="apiKey" type="password" class="form-input" placeholder="sk-... or AIza..." />
      </div>

      <div class="form-group">
        <label class="form-label"><span class="label-icon">🤖</span>Model</label>
        <input v-model="model" type="text" class="form-input" placeholder="gemini-3-flash-preview" />
      </div>

      <div class="form-group">
        <label class="form-label"><span class="label-icon">🔗</span>Endpoint</label>
        <input v-model="endpoint" type="text" class="form-input" placeholder="https://api.openai.com/v1" />
        <p class="form-tip">Ignored for Gemini keys</p>
      </div>

      <div class="form-group">
        <label class="form-label"><span class="label-icon">🌐</span>Backend URL</label>
        <input v-model="backendUrl" type="text" class="form-input" placeholder="http://localhost:8000" />
        <p class="form-tip">Change this after deploying to Vercel (e.g. https://xxx.vercel.app)</p>
      </div>

      <button class="btn-save" :disabled="loading" @click="handleSave">
        {{ loading ? 'Saving...' : '💾 Save' }}
      </button>

      <div v-if="saveSuccess" class="success-message">✅ Saved!</div>
      <div v-if="saveError" class="error-message">⚠️ {{ saveError }}</div>

      <div class="help-section">
        <h4>❓ How to get API Key?</h4>
        <ol>
          <li>OpenAI: <a href="https://platform.openai.com/api-keys" target="_blank">platform.openai.com</a></li>
          <li>Gemini: <a href="https://aistudio.google.com/apikey" target="_blank">aistudio.google.com</a></li>
          <li>Paste the key above</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<style scoped>
.settings-page { flex:1; padding:24px; background:#F8F9FE; overflow-y:auto; }
.settings-header { margin-bottom:24px; }
.settings-header h2 { font-size:22px; font-weight:800; color:#333; margin-bottom:4px; }
.settings-desc { font-size:14px; color:#888; }
.loading-state { text-align:center; padding:40px; color:#888; }
.settings-form { display:flex; flex-direction:column; gap:20px; }
.form-group { display:flex; flex-direction:column; gap:8px; }
.form-label { font-size:15px; font-weight:700; color:#444; display:flex; align-items:center; gap:6px; }
.label-icon { font-size:16px; }
.form-input { padding:14px 16px; border:2px solid #e8e8e8; border-radius:14px; font-size:15px; color:#333; background:white; outline:none; }
.form-input:focus { border-color:#6C63FF; box-shadow:0 0 0 3px rgba(108,99,255,0.1); }
.form-input::placeholder { color:#ccc; }
.form-tip { font-size:12px; color:#aaa; }
.btn-save { background:linear-gradient(135deg,#6C63FF,#8B83FF); color:white; border:none; padding:16px; border-radius:16px; font-size:16px; font-weight:700; cursor:pointer; margin-top:8px; }
.btn-save:hover:not(:disabled) { transform:translateY(-2px); }
.btn-save:disabled { opacity:0.6; cursor:not-allowed; }
.success-message { padding:12px 16px; background:#E8F8F0; border-radius:12px; color:#2ECC71; font-size:14px; font-weight:600; text-align:center; }
.error-message { padding:12px 16px; background:#FFF0F0; border-radius:12px; color:#FF6B6B; font-size:14px; text-align:center; }
.help-section { background:white; padding:20px; border-radius:16px; margin-top:12px; }
.help-section h4 { font-size:15px; font-weight:700; color:#444; margin-bottom:12px; }
.help-section ol { padding-left:24px; display:flex; flex-direction:column; gap:8px; }
.help-section li { font-size:14px; color:#666; }
.help-section a { color:#6C63FF; text-decoration:none; font-weight:600; }
</style>
