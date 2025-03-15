<template>
  <div class="recommendations-page">
    <header class="glass-header">
      <div class="header-content">
        <div class="logo">健康生活</div>
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-item">首页</router-link>
          <router-link to="/records" class="nav-item">记录</router-link>
          <router-link to="/recommendations" class="nav-item active">推荐</router-link>
          <router-link to="/reports" class="nav-item">报告</router-link>
        </nav>
        <div class="user-menu" @click="toggleDropdown" ref="userMenuRef">
          <div class="user-info">
            <div class="avatar">
              <UserAvatar />
            </div>
            <span class="username">{{ username }}</span>
            <span class="dropdown-arrow" :class="{ 'rotated': isDropdownVisible }">▼</span>
          </div>
          
          <!-- 下拉菜单 -->
          <div v-if="isDropdownVisible" class="user-dropdown">
            <div class="dropdown-header">
              <div class="header-info">
                <span class="signed-in">登录为</span>
                <strong>{{ username }}</strong>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" class="dropdown-item">
              <span class="item-icon">👤</span>
              个人主页
            </router-link>
            <router-link to="/settings" class="dropdown-item">
              <span class="item-icon">⚙️</span>
              设置
            </router-link>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item" @click="handleLogout">
              <span class="item-icon">🚪</span>
              退出
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="recommendations-content">
      <!-- 健康建议卡片 -->
      <section class="health-tips">
        <h2>今日健康建议</h2>
        <div class="tips-grid">
          <div class="tip-card">
            <div class="tip-icon">💪</div>
            <h3>运动建议</h3>
            <p>根据您的运动记录，建议今天进行30分钟的中等强度运动，如快走或游泳。</p>
          </div>
          <div class="tip-card">
            <div class="tip-icon">🍽️</div>
            <h3>饮食建议</h3>
            <p>保持均衡饮食，多吃蔬菜水果，适量摄入蛋白质，避免过度加工食品。</p>
          </div>
          <div class="tip-card">
            <div class="tip-icon">😴</div>
            <h3>睡眠建议</h3>
            <p>保持规律的作息时间，确保7-8小时的优质睡眠，睡前避免使用电子设备。</p>
          </div>
          <div class="tip-card">
            <div class="tip-icon">🧘</div>
            <h3>心理建议</h3>
            <p>保持积极乐观的心态，适当进行冥想或深呼吸练习，缓解压力。</p>
          </div>
        </div>
      </section>

      <!-- 个性化推荐 -->
      <section class="personalized-recommendations">
        <h2>为您推荐</h2>
        <div class="recommendations-grid">
          <div class="recommendation-card">
            <div class="card-header">
              <span class="card-icon">🏃</span>
              <h3>运动计划</h3>
            </div>
            <div class="card-content">
              <ul class="recommendation-list">
                <li>周一：30分钟快走</li>
                <li>周三：45分钟游泳</li>
                <li>周五：60分钟瑜伽</li>
                <li>周日：40分钟骑行</li>
              </ul>
            </div>
          </div>
          <div class="recommendation-card">
            <div class="card-header">
              <span class="card-icon">🥗</span>
              <h3>营养食谱</h3>
            </div>
            <div class="card-content">
              <ul class="recommendation-list">
                <li>早餐：全麦面包 + 鸡蛋 + 牛奶</li>
                <li>午餐：糙米饭 + 鸡胸肉 + 西兰花</li>
                <li>晚餐：三文鱼 + 藜麦 + 沙拉</li>
                <li>加餐：水果 + 坚果</li>
              </ul>
            </div>
          </div>
          <div class="recommendation-card">
            <div class="card-header">
              <span class="card-icon">📚</span>
              <h3>健康知识</h3>
            </div>
            <div class="card-content">
              <ul class="recommendation-list">
                <li>了解运动强度与心率的关系</li>
                <li>学习营养均衡的饮食搭配</li>
                <li>掌握压力管理技巧</li>
                <li>了解睡眠质量的影响因素</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 健康目标 -->
      <section class="health-goals">
        <h2>健康目标</h2>
        <div class="goals-grid">
          <div class="goal-card">
            <div class="goal-progress">
              <div class="progress-circle">
                <span class="progress-value">75%</span>
              </div>
            </div>
            <h3>每周运动目标</h3>
            <p>目标：150分钟</p>
            <p>已完成：112分钟</p>
          </div>
          <div class="goal-card">
            <div class="goal-progress">
              <div class="progress-circle">
                <span class="progress-value">60%</span>
              </div>
            </div>
            <h3>睡眠质量目标</h3>
            <p>目标：优质睡眠7小时</p>
            <p>达标天数：4/7天</p>
          </div>
          <div class="goal-card">
            <div class="goal-progress">
              <div class="progress-circle">
                <span class="progress-value">85%</span>
              </div>
            </div>
            <h3>饮食均衡目标</h3>
            <p>目标：每日营养均衡</p>
            <p>达标天数：6/7天</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import UserAvatar from '../components/UserAvatar.vue'
import userStore from '../stores/userStore'
import axios from 'axios'

const router = useRouter()
const isDropdownVisible = ref(false)
const userMenuRef = ref(null)
const loading = ref(true)
const recommendations = ref({
  season: 'spring',
  healthSummary: {
    sleepQuality: 'normal',
    commonIssues: [],
    moodStatus: 'neutral',
    exerciseLevel: 'medium'
  },
  recommendations: {
    food: [],
    exercise: [],
    lifestyle: []
  }
})

const username = computed(() => userStore.state.username)

// 获取推荐数据
const fetchRecommendations = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:5000/api/recommendations', {
      headers: {
        'Authorization': `Bearer ${userStore.state.token}`
      }
    })
    recommendations.value = response.data
    console.log('获取到的推荐数据:', recommendations.value)
  } catch (error) {
    console.error('获取推荐数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取季节图标
const getSeasonIcon = (season) => {
  const icons = {
    spring: '🌸',
    summer: '☀️',
    autumn: '🍂',
    winter: '❄️'
  }
  return icons[season] || '🌍'
}

// 获取季节名称
const getSeasonName = (season) => {
  const names = {
    spring: '春',
    summer: '夏',
    autumn: '秋',
    winter: '冬'
  }
  return names[season] || '当前'
}

// 获取睡眠质量文本
const getSleepQualityText = (quality) => {
  const texts = {
    good: '良好',
    normal: '一般',
    bad: '不佳'
  }
  return texts[quality] || '一般'
}

// 获取睡眠质量样式类
const getSleepQualityClass = (quality) => {
  const classes = {
    good: 'status-good',
    normal: 'status-normal',
    bad: 'status-bad'
  }
  return classes[quality] || 'status-normal'
}

// 获取情绪状态文本
const getMoodStatusText = (status) => {
  const texts = {
    positive: '积极',
    neutral: '平稳',
    negative: '消极'
  }
  return texts[status] || '平稳'
}

// 获取情绪状态样式类
const getMoodStatusClass = (status) => {
  const classes = {
    positive: 'status-good',
    neutral: 'status-normal',
    negative: 'status-bad'
  }
  return classes[status] || 'status-normal'
}

// 获取运动水平文本
const getExerciseLevelText = (level) => {
  const texts = {
    high: '活跃',
    medium: '适中',
    low: '较少'
  }
  return texts[level] || '适中'
}

// 获取运动水平样式类
const getExerciseLevelClass = (level) => {
  const classes = {
    high: 'status-good',
    medium: 'status-normal',
    low: 'status-warning'
  }
  return classes[level] || 'status-normal'
}

// 获取健康问题文本
const getHealthIssueText = (issue) => {
  const texts = {
    sleep_well: '睡眠充足',
    sleep_bad: '睡眠不足',
    appetite_good: '胃口好',
    appetite_bad: '没胃口',
    energetic: '精力充沛',
    fatigue: '疲劳乏力',
    muscle_sore: '肌肉酸痛',
    headache: '头疼',
    throat: '咽喉不适',
    stomach: '胃部不适',
    cold: '感冒发烧',
    allergy: '过敏'
  }
  return texts[issue] || issue
}

const toggleDropdown = () => {
  isDropdownVisible.value = !isDropdownVisible.value
}

const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    isDropdownVisible.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  fetchRecommendations()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.recommendations-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e0f7ff 100%);
}

.glass-header {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding: 1rem 2rem;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.main-nav {
  display: flex;
  gap: 2rem;
}

.nav-item {
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: #3b82f6;
}

.nav-item.active {
  color: #3b82f6;
}

.user-menu {
  position: relative;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  overflow: hidden;
}

.username {
  color: #1e293b;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: #64748b;
  transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  min-width: 200px;
  margin-top: 0.5rem;
  z-index: 1000;
}

.dropdown-header {
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.signed-in {
  font-size: 0.875rem;
  color: #64748b;
}

.dropdown-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 0.5rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #1e293b;
  text-decoration: none;
  transition: background-color 0.3s ease;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f8fafc;
}

.item-icon {
  font-size: 1.25rem;
}

.recommendations-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

section {
  margin-bottom: 3rem;
}

h2 {
  color: #1e293b;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.tip-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-5px);
}

.tip-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.tip-card h3 {
  color: #1e293b;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
}

.tip-card p {
  color: #64748b;
  line-height: 1.6;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.recommendation-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.card-icon {
  font-size: 1.5rem;
}

.card-header h3 {
  color: #1e293b;
  font-size: 1.25rem;
  margin: 0;
}

.recommendation-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendation-list li {
  color: #64748b;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.recommendation-list li:last-child {
  border-bottom: none;
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.goal-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.goal-progress {
  margin-bottom: 1rem;
}

.progress-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
}

.progress-circle::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: conic-gradient(#3b82f6 var(--progress), #e2e8f0 0deg);
  --progress: 75%;
}

.progress-value {
  position: relative;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.goal-card h3 {
  color: #1e293b;
  font-size: 1.25rem;
  margin-bottom: 0.75rem;
}

.goal-card p {
  color: #64748b;
  margin: 0.25rem 0;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .main-nav {
    gap: 1rem;
  }

  .recommendations-content {
    padding: 0 1rem;
  }

  .tips-grid,
  .recommendations-grid,
  .goals-grid {
    grid-template-columns: 1fr;
  }
}
</style> 