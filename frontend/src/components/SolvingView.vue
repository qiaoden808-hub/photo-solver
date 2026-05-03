<script setup>
defineProps({
  error: { type: [String, null], default: null },
})

const emit = defineEmits(['back', 'retry'])
</script>

<template>
  <div class="solving-page">
    <div v-if="!error" class="solving-content">
      <div class="solving-animation">
        <div class="book-icon">📖</div>
      </div>
      <h2 class="solving-title">AI 老师正在解题...</h2>
      <p class="solving-subtitle">请稍等片刻</p>

      <div class="thinking-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>

      <div class="fun-facts">
        <p>💡 你知道吗？AI 老师一秒能看 100 本书！</p>
      </div>
    </div>

    <div v-else class="error-content">
      <div class="error-icon">😅</div>
      <h2 class="error-title">哎呀，出错了</h2>
      <p class="error-message">{{ error }}</p>
      <div class="error-actions">
        <button class="btn-primary" @click="$emit('retry')">
          🔄 重新尝试
        </button>
        <button class="btn-secondary" @click="$emit('back')">
          ← 返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.solving-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #F8F9FE;
}

.solving-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.solving-animation {
  margin-bottom: 8px;
}

.book-icon {
  font-size: 72px;
  animation: bookSpin 1.8s ease-in-out infinite;
}

@keyframes bookSpin {
  0% { transform: rotateY(0deg) scale(1); }
  25% { transform: rotateY(20deg) scale(1.05); }
  50% { transform: rotateY(0deg) scale(1); }
  75% { transform: rotateY(-20deg) scale(1.05); }
  100% { transform: rotateY(0deg) scale(1); }
}

.solving-title {
  font-size: 24px;
  font-weight: 800;
  color: #6C63FF;
}

.solving-subtitle {
  font-size: 16px;
  color: #999;
}

.thinking-dots {
  display: flex;
  gap: 8px;
  margin: 12px 0;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #6C63FF;
  animation: dotBounce 1.4s ease-in-out infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }
.dot:nth-child(4) { animation-delay: 0.6s; }

@keyframes dotBounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

.fun-facts {
  margin-top: 32px;
  padding: 12px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  border: 2px solid #FFE66D;
}

.fun-facts p {
  font-size: 14px;
  color: #888;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 8px;
}

.error-title {
  font-size: 24px;
  font-weight: 800;
  color: #FF6B6B;
}

.error-message {
  font-size: 15px;
  color: #888;
  max-width: 280px;
  margin-bottom: 16px;
}

.error-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 240px;
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
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: #6C63FF;
  border: 2px solid #6C63FF;
  padding: 12px 28px;
  border-radius: 16px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}
</style>
