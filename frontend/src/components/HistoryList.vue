<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi.js'

const emit = defineEmits(['go-back', 'view-solution'])

const { getHistory, getHistoryItem, deleteHistory, loading } = useApi()
const historyList = ref([])
const loadError = ref(null)
const deletingId = ref(null)

onMounted(() => {
  loadHistory()
})

async function loadHistory() {
  loadError.value = null
  try {
    historyList.value = await getHistory()
  } catch (err) {
    loadError.value = err.message || '加载历史记录失败'
  }
}

async function viewDetail(item) {
  try {
    const detail = await getHistoryItem(item.id)
    if (detail) {
      emit('view-solution', detail)
    }
  } catch (err) {
    loadError.value = err.message || '加载解题详情失败'
  }
}

async function confirmDelete(id) {
  if (confirm('确定要删除这条记录吗？')) {
    deletingId.value = id
    try {
      await deleteHistory(id)
      historyList.value = historyList.value.filter(item => item.id !== id)
    } catch (err) {
      loadError.value = err.message || '删除失败'
    } finally {
      deletingId.value = null
    }
  }
}

const subjectColors = {
  '数学': '#4A90D9',
  '语文': '#FF6B6B',
  '英语': '#2ECC71',
  '科学': '#9B59B6',
}

function getSubjectColor(subject) {
  return subjectColors[subject] || '#888'
}

function truncateProblem(text, maxLen = 30) {
  if (!text) return ''
  return text.length > maxLen ? text.slice(0, maxLen) + '...' : text
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hour = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${month}-${day} ${hour}:${min}`
}
</script>

<template>
  <div class="history-page">
    <div v-if="loading && historyList.length === 0" class="loading-state">
      <div class="loading-book">📖</div>
      <p>加载中...</p>
    </div>

    <div v-else-if="loadError" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ loadError }}</p>
      <button class="btn-retry" @click="loadHistory">重试</button>
    </div>

    <div v-else-if="historyList.length === 0" class="empty-state">
      <div class="empty-icon">📭</div>
      <h3>还没有解题记录</h3>
      <p>快去拍一题试试吧！</p>
      <button class="btn-primary" @click="$emit('go-back')">
        📸 去拍照
      </button>
    </div>

    <div v-else class="history-list">
      <div class="list-header">
        <h3>📋 历史记录 ({{ historyList.length }})</h3>
      </div>

      <div
        v-for="item in historyList"
        :key="item.id"
        class="history-card"
        @click="viewDetail(item)"
      >
        <div class="card-left">
          <div
            class="subject-dot"
            :style="{ background: getSubjectColor(item.subject) }"
          ></div>
          <div class="card-info">
            <div class="card-problem">
              {{ truncateProblem(item.problem) }}
            </div>
            <div class="card-meta">
              <span
                class="card-subject"
                :style="{ color: getSubjectColor(item.subject) }"
              >
                {{ item.subject || '未分类' }}
              </span>
              <span class="card-time">{{ formatTime(item.created_at) }}</span>
            </div>
          </div>
        </div>
        <button
          class="delete-btn"
          :disabled="deletingId === item.id"
          @click.stop="confirmDelete(item.id)"
          title="删除"
        >
          {{ deletingId === item.id ? '...' : '🗑️' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.history-page {
  flex: 1;
  padding: 16px;
  background: #F8F9FE;
  overflow-y: auto;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 24px;
  gap: 12px;
  text-align: center;
}

.loading-book {
  font-size: 48px;
  animation: bookSpin 1.8s ease-in-out infinite;
}

@keyframes bookSpin {
  0%, 100% { transform: rotateY(0deg); }
  50% { transform: rotateY(30deg); }
}

.loading-state p {
  font-size: 16px;
  color: #888;
}

.error-icon,
.empty-icon {
  font-size: 48px;
}

.error-state p,
.empty-state p {
  font-size: 15px;
  color: #888;
}

.empty-state h3 {
  font-size: 18px;
  color: #666;
}

.btn-retry {
  background: #6C63FF;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
}

.btn-primary {
  background: linear-gradient(135deg, #6C63FF, #8B83FF);
  color: white;
  border: none;
  padding: 14px 32px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 8px;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.list-header {
  margin-bottom: 12px;
}

.list-header h3 {
  font-size: 16px;
  color: #666;
  font-weight: 600;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.2s;
}

.history-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.history-card:active {
  transform: scale(0.98);
}

.card-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.subject-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-problem {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-subject {
  font-size: 12px;
  font-weight: 600;
}

.card-time {
  font-size: 12px;
  color: #aaa;
}

.delete-btn {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
  border-radius: 10px;
  transition: background 0.2s;
  flex-shrink: 0;
}

.delete-btn:hover {
  background: #fff0f0;
}

.delete-btn:disabled {
  opacity: 0.5;
}
</style>
