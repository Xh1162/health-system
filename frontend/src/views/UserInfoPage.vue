<template>
  <div class="user-info-page">
    <div class="info-card">
      <h2>开始您的健康之旅</h2>
      <p class="subtitle">请告诉我们一些基本信息，以便为您提供个性化建议</p>
      
      <form @submit.prevent="handleSubmit" class="info-form">
        <div class="form-group">
          <label>身高 (cm)</label>
          <div class="number-input">
            <button type="button" @click="adjustHeight(-1)" class="adjust-btn">-</button>
            <input 
              type="number" 
              v-model="height"
              min="100"
              max="220"
              step="1"
              required
            />
            <button type="button" @click="adjustHeight(1)" class="adjust-btn">+</button>
          </div>
        </div>

        <div class="form-group">
          <label>体重 (kg)</label>
          <div class="number-input">
            <button type="button" @click="adjustWeight(-1)" class="adjust-btn">-</button>
            <input 
              type="number" 
              v-model="weight"
              min="30"
              max="200"
              step="0.1"
              required
            />
            <button type="button" @click="adjustWeight(1)" class="adjust-btn">+</button>
          </div>
        </div>

        <div class="form-group">
          <label>出生日期</label>
          <input 
            type="date" 
            v-model="birthDate"
            required
            :max="maxDate"
          />
        </div>

        <div class="form-group">
          <label>性别</label>
          <div class="gender-options">
            <button 
              type="button"
              class="gender-btn"
              :class="{ active: gender === 'male' }"
              @click="gender = 'male'"
            >
              <span class="gender-icon">👨</span>
              <span>男</span>
            </button>
            <button 
              type="button"
              class="gender-btn"
              :class="{ active: gender === 'female' }"
              @click="gender = 'female'"
            >
              <span class="gender-icon">👩</span>
              <span>女</span>
            </button>
          </div>
        </div>

        <button type="submit" class="submit-btn">继续</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import useUserStore from '../stores/userStore'

const router = useRouter()
const userStore = useUserStore()
const height = ref(170)
const weight = ref(65)
const birthDate = ref('')
const gender = ref('')

// 计算最大日期（今天）
const maxDate = new Date().toISOString().split('T')[0]

const adjustHeight = (delta) => {
  const newHeight = height.value + delta
  if (newHeight >= 100 && newHeight <= 220) {
    height.value = newHeight
  }
}

const adjustWeight = (delta) => {
  const newWeight = parseFloat((weight.value + delta).toFixed(1))
  if (newWeight >= 30 && newWeight <= 200) {
    weight.value = newWeight
  }
}

const handleSubmit = () => {
  if (!gender.value) {
    alert('请选择性别')
    return
  }

  // 保存用户信息
  localStorage.setItem('userInfo', JSON.stringify({
    height: height.value,
    weight: weight.value,
    birthDate: birthDate.value,
    gender: gender.value
  }))

  // 跳转到下一步
  router.push('/auth')
}
</script>

<style scoped>
.user-info-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f8fafc 0%, #e0f7ff 100%);
  padding: 1rem;
}

.info-card {
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  width: 90%;
  max-width: 440px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

h2 {
  color: #1e293b;
  margin-bottom: 0.75rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.025em;
}

.subtitle {
  color: #64748b;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 1rem;
}

.info-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #1e293b;
  font-size: 1rem;
  font-weight: 500;
}

.number-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

input[type="number"],
input[type="date"] {
  flex: 1;
  padding: 0.875rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 1rem;
  color: #1e293b;
  background: white;
  transition: all 0.3s ease;
  text-align: center;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

input[type="number"]:focus,
input[type="date"]:focus {
  border-color: #3b82f6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.adjust-btn {
  width: 2.5rem;
  height: 2.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #1e293b;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.adjust-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-1px);
}

.gender-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.gender-btn {
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #1e293b;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.gender-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-1px);
}

.gender-btn.active {
  border-color: #3b82f6;
  background-color: #f0f9ff;
  color: #3b82f6;
}

.gender-icon {
  font-size: 1.25rem;
}

.submit-btn {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.submit-btn:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}

/* 移除数字输入框的箭头 */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  margin: 0;
}

input[type="number"] {
  -webkit-appearance: textfield;
  -moz-appearance: textfield;
  appearance: textfield;
}

@media (max-width: 480px) {
  .info-card {
    padding: 1.5rem;
  }
  
  h2 {
    font-size: 1.25rem;
  }
  
  .subtitle {
    font-size: 0.875rem;
    margin-bottom: 1.5rem;
  }
  
  input[type="number"],
  input[type="date"],
  .adjust-btn {
    padding: 0.75rem;
  }
  
  .gender-btn {
    padding: 0.75rem;
  }
}
</style> 