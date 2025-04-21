<template>
  <div class="activity-page">
    <div class="activity-card">
      <h2>您平时的运动量是？</h2>
      <p class="subtitle">选择最符合您日常情况的选项</p>
      
      <div class="options">
        <div 
          v-for="(level, index) in activityLevels" 
          :key="index"
          class="option-item"
          :class="{ 'selected': selectedLevel === index }"
          @click="selectLevel(index)"
        >
          <div class="option-content">
            <div class="option-header">
              <span class="option-icon">{{ level.icon }}</span>
              <span class="option-title">{{ level.title }}</span>
            </div>
            <p class="option-description">{{ level.description }}</p>
          </div>
        </div>
      </div>
      
      <div class="action-buttons">
        <button class="back-btn" @click="goBack">返回</button>
        <button 
          class="next-btn"
          :disabled="selectedLevel === null"
          @click="goToNextStep"
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
const selectedLevel = ref(null)

const activityLevels = [
  {
    icon: '🧘',
    title: '轻度活动',
    description: '以静态活动为主，偶尔步行或轻度运动'
  },
  {
    icon: '🚶',
    title: '中度活动',
    description: '经常步行，每周进行2-3次运动'
  },
  {
    icon: '🏃',
    title: '活跃运动',
    description: '保持规律运动，每周运动3-5次'
  },
  {
    icon: '🏋️',
    title: '高强度运动',
    description: '频繁进行高强度训练，或从事体力劳动'
  }
]

const selectLevel = (index) => {
  selectedLevel.value = index
}

const goToNextStep = () => {
  if (selectedLevel.value !== null) {
    // 保存活动水平
    localStorage.setItem('activityLevel', activityLevels[selectedLevel.value].title)
    
    // 跳转到用户信息页面
    router.push('/user-info')
  }
}

const goBack = () => {
  router.push('/onboarding')
}
</script>

<style scoped>
.activity-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  padding: 1rem;
}

.activity-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  width: 90%;
  max-width: 600px;
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
  margin-bottom: 2.5rem;
  text-align: center;
  font-size: 1.1rem;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2.5rem;
}

.option-item {
  padding: 1.25rem;
  border-radius: 1rem;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.option-item.selected {
  border-color: #3b82f6;
  background-color: #f0f9ff;
}

.option-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.option-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.option-icon {
  font-size: 1.5rem;
}

.option-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1e293b;
}

.option-description {
  color: #64748b;
  font-size: 0.95rem;
  margin-left: 2.5rem;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}

.back-btn,
.next-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn {
  background-color: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.back-btn:hover {
  background-color: #f8fafc;
  color: #334155;
}

.next-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
}

.next-btn:hover:not(:disabled) {
  background-color: #2563eb;
  transform: translateY(-2px);
}

.next-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .activity-card {
    padding: 2rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .option-title {
    font-size: 1rem;
  }
  
  .option-description {
    font-size: 0.875rem;
  }
  
  .action-buttons {
    flex-direction: column-reverse;
  }
  
  .back-btn, .next-btn {
    width: 100%;
  }
}
</style> 