<script setup>
defineProps({
  imageUrl: { type: String, required: true },
})

const emit = defineEmits(['retake', 'start-solving'])
</script>

<template>
  <div class="preview-page">
    <div class="preview-container">
      <img :src="imageUrl" alt="Image preview" class="preview-image" />
    </div>

    <div class="preview-actions">
      <button class="action-btn retake-btn" @click="$emit('retake')">
        Retake
      </button>
      <button class="action-btn submit-btn" @click="$emit('start-solving')">
        Solve
      </button>
    </div>
  </div>
</template>

<style scoped>
.preview-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  background: #F8F9FE;
}

.preview-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 20px;
  padding: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  margin-bottom: 20px;
}

.preview-image {
  max-width: 100%;
  max-height: 60vh;
  border-radius: 12px;
  object-fit: contain;
}

.preview-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  padding: 16px;
  border: none;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.retake-btn {
  background: white;
  color: #6C63FF;
  border: 2px solid #6C63FF;
}

.retake-btn:hover {
  background: #f5f3ff;
}

.submit-btn {
  background: linear-gradient(135deg, #6C63FF, #8B83FF);
  color: white;
  box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4);
}
</style>
