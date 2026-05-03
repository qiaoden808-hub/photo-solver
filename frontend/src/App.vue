<script setup>
import { ref } from 'vue'
import HomePage from './components/HomePage.vue'
import CameraCapture from './components/CameraCapture.vue'
import ImagePreview from './components/ImagePreview.vue'
import SolvingView from './components/SolvingView.vue'
import SolutionView from './components/SolutionView.vue'
import HistoryList from './components/HistoryList.vue'
import SettingsPage from './components/SettingsPage.vue'
import { useApi } from './composables/useApi.js'

const API_BASE = 'http://localhost:8000'
const { solveProblem } = useApi()

const currentView = ref('home')
const currentSolution = ref(null)
const currentImage = ref(null)
const solvingError = ref(null)

function goToCamera() {
  currentImage.value = null
  currentSolution.value = null
  solvingError.value = null
  currentView.value = 'camera'
}

function goToHome() {
  currentImage.value = null
  currentSolution.value = null
  solvingError.value = null
  currentView.value = 'home'
}

function goToHistory() {
  currentView.value = 'history'
}

function goToSettings() {
  currentView.value = 'settings'
}

function onImageCaptured(imageUrl) {
  currentImage.value = imageUrl
  currentView.value = 'preview'
}

async function onStartSolving(imageUrl) {
  currentView.value = 'solving'
  solvingError.value = null

  try {
    const base64 = imageUrl.includes('base64,')
      ? imageUrl.split('base64,')[1]
      : imageUrl
    const result = await solveProblem(base64, 'photo.jpg')
    currentSolution.value = result
    currentView.value = 'solution'
  } catch (err) {
    solvingError.value = err.message || 'Solving failed'
  }
}

function onRetry() {
  if (currentImage.value) {
    onStartSolving(currentImage.value)
  }
}

function showViewFromHistory(solution) {
  currentSolution.value = solution
  currentView.value = 'solution'
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-left">
        <button v-if="currentView !== 'home'" class="back-btn" @click="goToHome">
          ← Back
        </button>
      </div>
      <div class="header-title" @click="goToHome">
        <span class="header-icon">📚</span>
        <h1>Photo Solver</h1>
      </div>
      <div class="header-right">
        <button class="header-btn" @click="goToHistory" title="History">
          📋
        </button>
        <button class="header-btn" @click="goToSettings" title="Settings">
          ⚙️
        </button>
      </div>
    </header>

    <main class="main-content">
      <HomePage
        v-if="currentView === 'home'"
        @go-to-camera="goToCamera"
        @image-selected="onImageCaptured"
      />

      <CameraCapture
        v-else-if="currentView === 'camera'"
        @image-captured="onImageCaptured"
        @go-back="goToHome"
      />

      <ImagePreview
        v-else-if="currentView === 'preview'"
        :image-url="currentImage"
        @retake="goToCamera"
        @start-solving="onStartSolving(currentImage)"
      />

      <SolvingView
        v-else-if="currentView === 'solving'"
        :error="solvingError"
        @back="goToHome"
        @retry="onRetry"
      />

      <SolutionView
        v-else-if="currentView === 'solution'"
        :solution="currentSolution"
        @take-another="goToHome"
      />

      <HistoryList
        v-else-if="currentView === 'history'"
        @go-back="goToHome"
        @view-solution="showViewFromHistory"
      />

      <SettingsPage
        v-else-if="currentView === 'settings'"
        @go-back="goToHome"
      />
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background-color: #F8F9FE;
  color: #333;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  max-width: 480px;
  margin: 0 auto;
  background: #fff;
  box-shadow: 0 0 20px rgba(108, 99, 255, 0.08);
}

.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: linear-gradient(135deg, #6C63FF, #8B83FF);
  color: white;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(108, 99, 255, 0.3);
}

.header-left {
  width: 60px;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
}

.header-icon {
  font-size: 24px;
}

.header-title h1 {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 2px;
}

.header-right {
  display: flex;
  gap: 8px;
}

.header-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
}

.header-btn:hover {
  background: rgba(255, 255, 255, 0.35);
}

.back-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.35);
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
