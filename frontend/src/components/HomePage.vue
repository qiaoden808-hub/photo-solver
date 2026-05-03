<script setup>
import { ref } from 'vue'

const emit = defineEmits(['go-to-camera'])

const fileInput = ref(null)

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      emit('image-selected', e.target.result)
    }
    reader.readAsDataURL(file)
  }
}

function triggerFileUpload() {
  fileInput.value.click()
}

function goToCamera() {
  emit('go-to-camera')
}
</script>

<template>
  <div class="home-page">
    <div class="hero-section">
      <div class="hero-icon">📸</div>
      <h2 class="hero-title">拍照解题</h2>
      <p class="hero-subtitle">遇到难题不用怕，拍一拍就有答案！</p>
    </div>

    <div class="action-buttons">
      <button class="action-btn camera-btn" @click="goToCamera">
        <span class="btn-icon">📷</span>
        <span class="btn-text">拍题</span>
      </button>

      <button class="action-btn album-btn" @click="triggerFileUpload">
        <span class="btn-icon">📁</span>
        <span class="btn-text">从相册选择</span>
      </button>

      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        style="display: none"
        @change="handleFileUpload"
      />
    </div>

    <div class="instructions">
      <div class="instruction-card">
        <div class="instruction-icon">📸</div>
        <div class="instruction-text">
          <h4>第一步</h4>
          <p>拍下不会做的题目</p>
        </div>
      </div>
      <div class="instruction-arrow">↓</div>
      <div class="instruction-card">
        <div class="instruction-icon">🤖</div>
        <div class="instruction-text">
          <h4>第二步</h4>
          <p>AI 老师自动识别解答</p>
        </div>
      </div>
      <div class="instruction-arrow">↓</div>
      <div class="instruction-card">
        <div class="instruction-icon">✅</div>
        <div class="instruction-text">
          <h4>第三步</h4>
          <p>分步骤学会解题方法</p>
        </div>
      </div>
    </div>

    <div class="subjects-tags">
      <span class="subject-tag math">数学</span>
      <span class="subject-tag chinese">语文</span>
      <span class="subject-tag english">英语</span>
      <span class="subject-tag science">科学</span>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 24px;
  overflow-y: auto;
}

.hero-section {
  text-align: center;
  margin-bottom: 32px;
}

.hero-icon {
  font-size: 64px;
  margin-bottom: 12px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

.hero-title {
  font-size: 32px;
  font-weight: 800;
  color: #6C63FF;
  margin-bottom: 8px;
  letter-spacing: 4px;
}

.hero-subtitle {
  font-size: 16px;
  color: #888;
  line-height: 1.5;
}

.action-buttons {
  display: flex;
  gap: 16px;
  margin-bottom: 36px;
  width: 100%;
  max-width: 320px;
}

.action-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px 16px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.25s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.action-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.action-btn:active {
  transform: translateY(0);
}

.camera-btn {
  background: linear-gradient(135deg, #6C63FF, #8B83FF);
  color: white;
}

.album-btn {
  background: linear-gradient(135deg, #4ECDC4, #6EE7DE);
  color: white;
}

.btn-icon {
  font-size: 36px;
}

.btn-text {
  font-size: 18px;
  font-weight: 700;
}

.instructions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 32px;
  width: 100%;
  max-width: 320px;
}

.instruction-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  padding: 16px 20px;
  border-radius: 16px;
  width: 100%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  border: 2px solid #f0f0ff;
}

.instruction-icon {
  font-size: 28px;
  flex-shrink: 0;
}

.instruction-text h4 {
  font-size: 15px;
  font-weight: 700;
  color: #6C63FF;
  margin-bottom: 2px;
}

.instruction-text p {
  font-size: 14px;
  color: #888;
}

.instruction-arrow {
  font-size: 20px;
  color: #ccc;
  font-weight: bold;
}

.subjects-tags {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.subject-tag {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: white;
}

.subject-tag.math {
  background: #4A90D9;
}

.subject-tag.chinese {
  background: #FF6B6B;
}

.subject-tag.english {
  background: #2ECC71;
}

.subject-tag.science {
  background: #9B59B6;
}
</style>
