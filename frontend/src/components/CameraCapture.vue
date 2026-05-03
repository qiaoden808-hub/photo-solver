<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['image-captured', 'go-back'])

const video = ref(null)
const canvas = ref(null)
const cameraAvailable = ref(false)
const cameraError = ref(null)
const permissionDenied = ref(false)
const fileInput = ref(null)
let stream = null

onMounted(async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: false,
    })
    if (video.value) {
      video.value.srcObject = stream
      cameraAvailable.value = true
    }
  } catch (err) {
    console.error('Camera error:', err)
    cameraAvailable.value = false
    if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
      permissionDenied.value = true
      cameraError.value = '摄像头权限被拒绝，请使用相册上传'
    } else {
      cameraError.value = '摄像头不可用，请使用相册上传'
    }
  }
})

onUnmounted(() => {
  stopCamera()
})

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
}

function capturePhoto() {
  if (!video.value || !canvas.value) return
  const v = video.value
  const c = canvas.value
  c.width = v.videoWidth
  c.height = v.videoHeight
  const ctx = c.getContext('2d')
  ctx.drawImage(v, 0, 0, c.width, c.height)
  const imageUrl = c.toDataURL('image/jpeg', 0.9)
  stopCamera()
  emit('image-captured', imageUrl)
}

function triggerFileUpload() {
  fileInput.value.click()
}

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      stopCamera()
      emit('image-captured', e.target.result)
    }
    reader.readAsDataURL(file)
  }
}
</script>

<template>
  <div class="camera-page">
    <div v-if="cameraAvailable" class="camera-container">
      <video ref="video" autoplay playsinline class="camera-video"></video>
      <canvas ref="canvas" style="display: none"></canvas>

      <div class="camera-footer">
        <button class="capture-btn" @click="capturePhoto">
          <span class="capture-circle"></span>
        </button>
      </div>

      <button class="upload-alt-btn" @click="triggerFileUpload">
        📁 从相册选择
      </button>
    </div>

    <div v-else class="camera-unavailable">
      <div class="unavailable-icon">📷</div>
      <p class="unavailable-text">{{ cameraError || '无法使用相机' }}</p>
      <button class="btn-primary" @click="triggerFileUpload">
        📁 从相册选择图片
      </button>
      <button class="btn-secondary" @click="$emit('go-back')">
        ← 返回首页
      </button>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleFileUpload"
    />
  </div>
</template>

<style scoped>
.camera-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #1a1a2e;
}

.camera-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.camera-video {
  flex: 1;
  width: 100%;
  object-fit: cover;
}

.camera-footer {
  position: absolute;
  bottom: 30px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
}

.capture-btn {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 4px solid white;
  background: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.capture-btn:hover {
  transform: scale(1.05);
}

.capture-btn:active {
  transform: scale(0.95);
}

.capture-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: white;
  display: block;
}

.upload-alt-btn {
  position: absolute;
  bottom: 30px;
  right: 24px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 10px 16px;
  border-radius: 12px;
  font-size: 14px;
  cursor: pointer;
  backdrop-filter: blur(4px);
}

.upload-alt-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}

.camera-unavailable {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  background: #F8F9FE;
  gap: 16px;
}

.unavailable-icon {
  font-size: 64px;
  margin-bottom: 8px;
}

.unavailable-text {
  font-size: 16px;
  color: #666;
  text-align: center;
  margin-bottom: 16px;
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
