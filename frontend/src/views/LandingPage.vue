<template>
  <div class="landing-page">
    <!-- 右上角登录按钮 -->
    <div class="auth-buttons">
      <button class="user-icon-btn" @click="goToAuth">
        <span class="user-icon">👤</span>
      </button>
    </div>

    <!-- 中心内容区 -->
    <div class="center-content">
      <h1 class="main-title">健康饮食，快乐生活</h1>
      <p class="subtitle">不是每一种改变都需要那么困难</p>
      <button class="start-journey-btn" @click="startJourney">
        开启健康之旅
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const startJourney = () => {
  router.push('/onboarding')
}

const goToAuth = () => {
  // 创建一个包含登录和注册选项的页面
  router.push('/auth')
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  position: relative;
  background: linear-gradient(to right bottom, #e0f2fe, #dbeafe);
}

.auth-buttons {
  position: absolute;
  top: 2rem;
  right: 2rem;
  display: flex;
  gap: 1rem;
}

.auth-buttons button {
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  font-size: 1rem;
  transition: all 0.3s;
}

.user-icon-btn {
  background-color: var(--primary-color);
  color: white;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
  border: none;
}

.user-icon-btn:hover {
  transform: scale(1.1);
  background-color: var(--primary-light);
}

.user-icon {
  font-size: 1.2rem;
}

.center-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.main-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: var(--text-color);
}

.subtitle {
  font-size: 1.2rem;
  color: #64748b;
  margin-bottom: 2rem;
}

.start-journey-btn {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 2rem;
  cursor: pointer;
  transition: transform 0.3s, background-color 0.3s;
}

.start-journey-btn:hover {
  transform: scale(1.05);
  background-color: var(--primary-light);
}
</style> 