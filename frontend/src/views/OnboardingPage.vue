<template>
  <div class="onboarding-page">
    <div class="question-card">
      <h2>健康之旅</h2>
      <p class="subtitle">确认您的健康目标</p>
      
      <div class="options">
        <div 
          v-for="(option, index) in healthOptions" 
          :key="index"
          class="option-item"
          :class="{ 'selected': selectedOption === index }"
          @click="selectOption(index)"
        >
          <div class="option-content">
            <span class="option-icon">{{ option.icon }}</span>
            <span class="option-text">{{ option.text }}</span>
          </div>
        </div>
      </div>
      
      <div class="action-buttons">
        <button 
          class="next-btn"
          @click="goToNextStep"
          :disabled="selectedOption === null"
        >
          继续
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedOption = ref(null)

const healthOptions = [
  {
    icon: '❤️',
    text: '为了健康更好的生活'
  },
  {
    icon: '❤️',
    text: '为了健康更好的生活'
  },
  {
    icon: '❤️',
    text: '为了健康更好的生活'
  },
  {
    icon: '❤️',
    text: '为了健康更好的生活'
  }
]

const selectOption = (index) => {
  selectedOption.value = index
}

const goToNextStep = () => {
  if (selectedOption.value !== null) {
    localStorage.setItem('healthReason', healthOptions[selectedOption.value].text)
    router.push('/activity-level')
  }
}
</script>

<style scoped>
.onboarding-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e0f7ff 100%);
  padding: 1rem;
}

.question-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

h2 {
  color: #1e293b;
  margin-bottom: 0.5rem;
  text-align: center;
  font-size: 1.8rem;
}

.subtitle {
  color: #64748b;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 1.1rem;
}

.options {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.option-item {
  padding: 1rem 1.25rem;
  border-radius: 1rem;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.option-item:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.option-item.selected {
  border-color: #3b82f6;
  background: #f0f9ff;
}

.option-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.option-icon {
  font-size: 1.5rem;
}

.option-text {
  font-size: 1.1rem;
  color: #1e293b;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  justify-content: center;
}

.next-btn {
  padding: 0.875rem 2rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  width: 100%;
  transition: all 0.3s ease;
}

.next-btn:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.next-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

@media (min-width: 640px) {
  .question-card {
    padding: 2.5rem;
  }
}
</style> 