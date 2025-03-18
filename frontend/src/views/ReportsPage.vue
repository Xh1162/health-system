<template>
  <div class="reports-page">
    <header class="glass-header">
      <div class="header-content">
        <div class="logo">健康生活</div>
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-item">首页</router-link>
          <router-link to="/records" class="nav-item">记录</router-link>
          <router-link to="/reports" class="nav-item active">报告</router-link>
        </nav>
        <div class="user-menu" @click="toggleUserMenu" ref="userMenuRef">
          <div class="user-info">
            <div class="avatar">
              <img :src="avatarUrl" :alt="username" />
            </div>
            <span class="username">{{ username }}</span>
            <span class="dropdown-arrow" :class="{ 'rotated': showUserMenu }">▼</span>
          </div>
          
          <!-- 下拉菜单 -->
          <div v-if="showUserMenu" class="user-dropdown">
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

    <main class="main-content">
      <div class="page-header">
        <h1>个性化健康生活方案</h1>
        <p class="subtitle">根据您的真实记录数据，为您量身定制健康生活方式</p>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>正在生成您的健康方案...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <div class="error-icon">❌</div>
        <h3>获取数据失败</h3>
        <p>{{ error }}</p>
        <button class="retry-button" @click="fetchReportData">重试</button>
      </div>

      <div v-else class="reports-content">
        <Recommendations :recommendations-data="recommendationsData" />
        <DataAnalysis :analysis-data="analysisData" />
        <TrendAnalysis :trend-data="trendData" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import DataAnalysis from '../components/reports/DataAnalysis.vue'
import TrendAnalysis from '../components/reports/TrendAnalysis.vue'
import Recommendations from '../components/reports/Recommendations.vue'
import useUserStore from '../stores/userStore'
import { getReportsSummary } from '../api/reports'

const router = useRouter()
const userStore = useUserStore()
const showUserMenu = ref(false)
const loading = ref(true)
const error = ref(null)
const userMenuRef = ref(null)

// 用户信息
const username = computed(() => userStore.state.userData?.username || '用户')
const avatarUrl = computed(() => {
  const avatar = userStore.state.userData?.avatar
  if (!avatar) {
    return 'https://via.placeholder.com/100'
  }
  return avatar
})

// 处理用户菜单
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

// 处理登出
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

// 分析数据
const analysisData = ref({
  exerciseStats: {
    totalMinutes: 0,
    averagePerDay: 0,
    mostFrequentType: 'walking',
    intensityDistribution: {
      light: 0,
      medium: 0,
      high: 0
    }
  },
  moodStats: {
    distribution: {
      happy: 0,
      calm: 0,
      sad: 0,
      angry: 0,
      anxious: 0,
      tired: 0,
      excited: 0,
      bored: 0
    },
    mostFrequent: 'calm'
  },
  healthStats: {
    commonIssues: []
  }
})

// 趋势数据
const trendData = ref({
  exerciseTrends: {
    weeklyMinutes: 0,
    weeklyChange: 0,
    intensityAvg: 'medium',
    intensityChange: 0,
    frequency: 0,
    frequencyChange: 0
  },
  moodTrends: {
    positiveRate: 0,
    positiveChange: 0,
    stability: 'medium',
    stabilityChange: 0,
    previousMood: 'calm',
    currentMood: 'calm'
  },
  healthTrends: {
    sleepQuality: 'medium',
    sleepChange: 0,
    issueFrequency: 0,
    issueChange: 0,
    overallScore: 0,
    scoreChange: 0
  },
  dateRange: {
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
    end: new Date()
  }
})

// 推荐数据
const recommendationsData = ref({
  healthTips: [
    { type: 'exercise', content: '根据您的运动记录，建议今天进行30分钟的中等强度运动，如快走或游泳。' },
    { type: 'diet', content: '保持均衡饮食，多吃蔬菜水果，适量摄入蛋白质，避免过度加工食品。' },
    { type: 'sleep', content: '保持规律的作息时间，确保7-8小时的优质睡眠，睡前避免使用电子设备。' },
    { type: 'mental', content: '保持积极乐观的心态，适当进行冥想或深呼吸练习，缓解压力。' }
  ],
  personalizedRecommendations: [
    {
      type: 'exercise',
      title: '运动计划',
      items: [
        '周一：30分钟快走',
        '周三：45分钟游泳',
        '周五：60分钟瑜伽',
        '周日：40分钟骑行'
      ]
    },
    {
      type: 'diet',
      title: '营养食谱',
      items: [
        '早餐：全麦面包 + 鸡蛋 + 牛奶',
        '午餐：糙米饭 + 鸡胸肉 + 西兰花',
        '晚餐：三文鱼 + 藜麦 + 沙拉',
        '加餐：水果 + 坚果'
      ]
    },
    {
      type: 'knowledge',
      title: '健康知识',
      items: [
        '了解运动强度与心率的关系',
        '学习营养均衡的饮食搭配',
        '掌握压力管理技巧',
        '了解睡眠质量的影响因素'
      ]
    }
  ]
})

// 获取报告数据
const fetchReportData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // 检查是否有token
    if (!userStore.state.token) {
      console.log('未登录，使用模拟数据')
      useMockData()
      return
    }
    
    // 尝试从API获取数据
    try {
      const data = await getReportsSummary()
      console.log('获取到的报告数据:', data)
      
      if (!data || ((!data.analysis || Object.keys(data.analysis).length === 0) && 
                   (!data.trends || Object.keys(data.trends).length === 0))) {
        console.log('API返回为空，使用模拟数据')
        useMockData()
      } else {
        // 更新分析数据
        if (data.analysis && typeof data.analysis === 'object') {
          analysisData.value = {
            ...analysisData.value,
            ...data.analysis
          }
        }
        
        // 更新趋势数据
        if (data.trends && typeof data.trends === 'object') {
          trendData.value = {
            ...trendData.value,
            ...data.trends
          }
        }
      }
    } catch (apiError) {
      console.error('API调用失败:', apiError)
      // 在开发环境中使用模拟数据
      console.log('使用模拟数据，因为API调用失败')
      useMockData()
    }
  } catch (error) {
    console.error('获取报告数据失败:', error)
    error.value = error.message || '获取数据时发生错误'
    
    // 在开发环境中使用模拟数据
    console.log('使用模拟数据，因为发生错误')
    useMockData()
  } finally {
    loading.value = false
  }
}

// 使用模拟数据（用于开发和演示）
const useMockData = () => {
  // 模拟分析数据
  analysisData.value = {
    exerciseStats: {
      totalMinutes: 840,
      averagePerDay: 28,
      mostFrequentType: 'walking',
      intensityDistribution: {
        light: 45,
        medium: 35,
        high: 20
      }
    },
    moodStats: {
      distribution: {
        happy: 30,
        calm: 25,
        sad: 10,
        angry: 5,
        anxious: 15,
        tired: 10,
        excited: 5,
        bored: 0
      },
      mostFrequent: 'happy'
    },
    healthStats: {
      commonIssues: [
        { type: 'sleep_bad', count: 3 },
        { type: 'headache', count: 2 },
        { type: 'fatigue', count: 4 }
      ]
    }
  }
  
  // 模拟趋势数据
  trendData.value = {
    exerciseTrends: {
      weeklyMinutes: 210,
      weeklyChange: 15,
      intensityAvg: 'medium',
      intensityChange: 5,
      frequency: 5,
      frequencyChange: 10
    },
    moodTrends: {
      positiveRate: 65,
      positiveChange: 8,
      stability: 'high',
      stabilityChange: 12,
      previousMood: 'calm',
      currentMood: 'happy'
    },
    healthTrends: {
      sleepQuality: 'medium',
      sleepChange: 5,
      issueFrequency: 2,
      issueChange: -15,
      overallScore: 78,
      scoreChange: 6
    },
    dateRange: {
      start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      end: new Date()
    }
  }
}

// 点击外部关闭菜单
onMounted(() => {
  document.addEventListener('click', (event) => {
    if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
      showUserMenu.value = false
    }
  })
  
  // 获取报告数据
  fetchReportData()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', () => {})
})
</script>

<style scoped>
.reports-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
}

/* 毛玻璃效果导航栏 */
.glass-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.main-nav {
  display: flex;
  gap: 2rem;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.nav-item {
  color: #1e293b;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  position: relative;
  transition: all 0.3s ease;
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  transition: width 0.3s ease;
}

.nav-item:hover::after,
.nav-item.active::after {
  width: 100%;
}

.user-menu {
  position: relative;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.username {
  font-weight: 500;
  color: #1e293b;
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
  top: calc(100% + 0.75rem);
  right: 0;
  width: 240px;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 10;
  animation: dropdownFadeIn 0.2s ease-out;
}

@keyframes dropdownFadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-header {
  padding: 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.signed-in {
  font-size: 0.75rem;
  color: #64748b;
}

.dropdown-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 0.5rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #1e293b;
  text-decoration: none;
  transition: background 0.2s ease;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-size: 1rem;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.item-icon {
  font-size: 1.25rem;
}

/* 主要内容区域 */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 6rem 1.5rem 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #64748b;
  font-size: 1.125rem;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1.5rem;
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid rgba(59, 130, 246, 0.1);
  border-left-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 错误状态 */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1rem;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.retry-button:hover {
  background: #2563eb;
  transform: translateY(-2px);
}

/* 报告内容 */
.reports-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .main-nav {
    position: static;
    transform: none;
    margin-left: 2rem;
  }
  
  .header-content {
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .main-content {
    padding: 5rem 1rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .main-nav {
    gap: 1rem;
    margin-left: 1rem;
  }
  
  .user-info .username {
    display: none;
  }
  
  .page-header h1 {
    font-size: 1.75rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}
</style> 
