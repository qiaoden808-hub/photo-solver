<script setup>
import { computed } from 'vue'

const props = defineProps({
  solution: { type: Object, required: true },
})

const emit = defineEmits(['take-another'])

const subjectColors = {
  '数学': { bg: '#E8F0FE', text: '#4A90D9', light: 'rgba(74, 144, 217, 0.1)' },
  '语文': { bg: '#FFF0F0', text: '#FF6B6B', light: 'rgba(255, 107, 107, 0.1)' },
  '英语': { bg: '#E8F8F0', text: '#2ECC71', light: 'rgba(46, 204, 113, 0.1)' },
  '科学': { bg: '#F0E8FF', text: '#9B59B6', light: 'rgba(155, 89, 182, 0.1)' },
}

const subjectStyle = computed(() => {
  return subjectColors[props.solution.subject] || subjectColors['数学']
})

const steps = computed(() => {
  return props.solution.solution || []
})

function getStepEmoji(index) {
  const emojis = ['🔍', '💡', '📝', '✏️', '🧮', '✅', '🎯', '🌟', '📌', '⭐']
  return emojis[index % emojis.length]
}
</script>

<template>
  <div class="solution-page">
    <div class="solution-header">
      <div class="subject-badge" :style="{ background: subjectStyle.bg, color: subjectStyle.text }">
        {{ solution.subject || '未分类' }}
      </div>
      <div class="solution-time" v-if="solution.created_at">
        {{ new Date(solution.created_at).toLocaleString('zh-CN') }}
      </div>
    </div>

    <div class="problem-section">
      <h3 class="section-title">📝 题目</h3>
      <div class="problem-content">
        {{ solution.problem }}
      </div>
    </div>

    <div class="steps-section">
      <h3 class="section-title">💡 解题步骤</h3>

      <div class="steps-container">
        <div
          v-for="(step, index) in steps"
          :key="step.step || index"
          class="step-card"
          :style="{ borderColor: subjectStyle.text }"
        >
          <div class="step-header">
            <div class="step-number" :style="{ background: subjectStyle.text }">
              <span class="step-emoji">{{ getStepEmoji(index) }}</span>
            </div>
            <div class="step-title-area">
              <span class="step-label">第 {{ step.step || index + 1 }} 步</span>
              <h4 class="step-title">{{ step.title || '' }}</h4>
            </div>
          </div>
          <div class="step-content" v-if="step.content">
            {{ step.content }}
          </div>
          <div v-if="index < steps.length - 1" class="step-connector">
            <div class="connector-line" :style="{ background: subjectStyle.text }"></div>
            <div class="connector-arrow" :style="{ color: subjectStyle.text }">▼</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="solution.tips" class="tips-section">
      <h3 class="section-title">🌟 解题小技巧</h3>
      <div class="tips-content">
        {{ solution.tips }}
      </div>
    </div>

    <div class="solution-footer">
      <button class="btn-again" @click="$emit('take-another')">
        📸 再拍一题
      </button>
    </div>
  </div>
</template>

<style scoped>
.solution-page {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #F8F9FE;
}

.solution-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.subject-badge {
  display: inline-block;
  padding: 6px 18px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
}

.solution-time {
  font-size: 12px;
  color: #aaa;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
}

.problem-section {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  margin-bottom: 20px;
}

.problem-content {
  font-size: 16px;
  line-height: 1.8;
  color: #444;
}

.steps-section {
  margin-bottom: 20px;
}

.steps-container {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.step-card {
  background: white;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  border-left: 4px solid;
}

.step-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-emoji {
  font-size: 18px;
}

.step-title-area {
  flex: 1;
}

.step-label {
  font-size: 12px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.step-title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  margin-top: 2px;
}

.step-content {
  font-size: 15px;
  line-height: 1.8;
  color: #555;
  padding: 0 0 0 52px;
}

.step-connector {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
  margin-left: 20px;
}

.connector-line {
  width: 2px;
  height: 24px;
  opacity: 0.3;
}

.connector-arrow {
  font-size: 12px;
  opacity: 0.5;
  margin-top: -2px;
}

.tips-section {
  background: linear-gradient(135deg, #FFF9E6, #FFF3CC);
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 20px;
  border: 2px solid #FFE66D;
}

.tips-content {
  font-size: 15px;
  line-height: 1.8;
  color: #666;
}

.solution-footer {
  text-align: center;
  padding: 20px 0 32px;
}

.btn-again {
  background: linear-gradient(135deg, #6C63FF, #8B83FF);
  color: white;
  border: none;
  padding: 16px 40px;
  border-radius: 20px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
  transition: all 0.2s;
}

.btn-again:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
}
</style>
