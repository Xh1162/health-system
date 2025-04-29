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
        <!-- 移除 Recommendations 和 DataAnalysis 组件 -->
        <!-- <Recommendations :recommendations-data="recommendationsData" /> -->
        <!-- <DataAnalysis :analysis-data="analysisData" /> -->

        <!-- Trends Section -->
        <section class="trends-section">
          <h2>健康趋势</h2>
          
          <div v-if="trendsLoading" class="loading-container small"> 
              <div class="spinner"></div>
              <p>加载趋势图表中...</p>
          </div>
          <div v-else-if="trendsError" class="error-container small">
              <div class="error-icon">⚠️</div>
              <h3>趋势图表加载失败</h3>
              <p>{{ trendsError }}</p>
          </div>
          <div v-else class="charts-grid">
              <!-- Weight Chart -->
              <div class="chart-container" v-if="trendsData?.weight_kg?.length > 0">
                 <Line :data="weightChartData" :options="weightChartOptions" />
              </div>
              <p v-else class="no-chart-data">没有足够的体重数据来显示趋势。</p>
              
              <!-- Exercise Duration Chart -->
               <div class="chart-container" v-if="trendsData?.exercise_duration?.length > 0">
                 <Line :data="exerciseDurationChartData" :options="exerciseDurationChartOptions" />
              </div>
              <p v-else class="no-chart-data">没有足够的运动数据来显示趋势。</p>

              <!-- Mood Chart -->
              <div class="chart-container" v-if="trendsData?.mood?.length > 0">
                 <Bar :data="moodChartData" :options="moodChartOptions" />
              </div>
              <p v-else class="no-chart-data">没有足够的心情数据来显示趋势。</p>

          </div>
        </section>

         <!-- Auto-Suggestions Section -->
         <section class="auto-suggestions-section">
            <h2>智能建议 <span class="section-subtitle">(基于近14天数据)</span></h2>
            <ul v-if="autoSuggestions.length > 0" class="suggestions-list">
              <li v-for="(suggestion, index) in autoSuggestions" :key="index">
                {{ suggestion }}
              </li>
            </ul>
            <p v-else class="placeholder-text">暂无智能建议生成。</p>
         </section>

         <!-- Request Advice Section -->
         <section class="request-advice-section">
            <h2>咨询管理员</h2>
            <p>如果您对报告或建议有疑问，或者需要更个性化的指导，可以向管理员请求专业建议。</p>
            <button class="action-button" @click="openRequestModal">向管理员请求专业建议</button>
            
            <!-- Success message after submission -->
            <p v-if="adviceSubmitSuccess && !showRequestModal" class="success-message">
               您的建议请求已成功发送！管理员会尽快处理。
            </p>
         </section>

        <!-- Advice Request Modal -->
        <div v-if="showRequestModal" class="modal-overlay" @click.self="showRequestModal = false">
            <div class="modal-content">
                <h3>请求专业建议</h3>
                <p>请在此处简要说明您的问题或希望获得建议的方面（可选）：</p>
                <textarea 
                    v-model="requestText" 
                    rows="4" 
                    placeholder="例如：如何根据我的情况调整饮食计划？如何改善睡眠？"
                ></textarea>
                
                <div v-if="adviceSubmitError" class="error-message small">
                    {{ adviceSubmitError }}
                </div>
                 <div v-if="adviceSubmitSuccess" class="success-message small">
                    请求已发送！
                </div>

                <div class="modal-actions">
                    <button 
                        class="button secondary" 
                        @click="showRequestModal = false" 
                        :disabled="isSubmittingAdvice"
                    >
                        取消
                    </button>
                    <button 
                        class="button primary" 
                        @click="handleRequestSubmit" 
                        :disabled="isSubmittingAdvice"
                    >
                        {{ isSubmittingAdvice ? '提交中...' : '确认提交' }}
                    </button>
                </div>
            </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import useUserStore from '../stores/userStore'
import { getReportsSummary, getTrendsData } from '../api/reports'
import { submitAdviceRequest } from '../api/advice'
import { Line, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const router = useRouter()
const userStore = useUserStore()
const showUserMenu = ref(false)
const loading = ref(true)
const error = ref(null)
const userMenuRef = ref(null)
const refreshInterval = ref(null)

// --- State for Trends ---
const trendsLoading = ref(true)
const trendsError = ref(null)
const trendsData = ref(null) // Store raw trend data from API

// --- State for Advice Request ---
const showRequestModal = ref(false)
const requestText = ref('')
const isSubmittingAdvice = ref(false)
const adviceSubmitError = ref(null)
const adviceSubmitSuccess = ref(false)

// User information
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

// 开始自动刷新
const startAutoRefresh = () => {
  // 每5分钟刷新一次数据
  refreshInterval.value = setInterval(() => {
    console.log('自动刷新报告数据...')
    fetchReportData()
  }, 5 * 60 * 1000)
}

// 停止自动刷新
const stopAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

// 监听记录更新事件
const handleRecordUpdate = () => {
  console.log('收到记录更新事件，刷新报告数据...')
  fetchReportData()
}

// Analysis data
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
  dietStats: {
    totalRecords: 0,
    regularityRate: 0,
    mealDistribution: {
      breakfast: 25,
      lunch: 30,
      dinner: 30,
      snack: 15
    },
    categories: {
      staple: 30,
      protein: 25,
      vegetables: 35,
      snacks: 10
    }
  }
})

// Recommendations data
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

// --- Chart Data and Options ---
const weightChartData = computed(() => {
  if (!trendsData.value?.weight_kg || trendsData.value.weight_kg.length === 0) {
    return { labels: [], datasets: [] };
  }
  const labels = trendsData.value.weight_kg.map(item => item.date);
  const data = trendsData.value.weight_kg.map(item => item.value);
  
  return {
    labels,
    datasets: [
      {
        label: '体重 (kg)',
        backgroundColor: '#3b82f6', // Blue
        borderColor: '#3b82f6',
        data: data,
        tension: 0.1, // Makes the line slightly curved
        fill: false
      }
    ]
  };
});

// Basic chart options (can be customized further)
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: '数据趋势' // Default title, override per chart if needed
    }
  },
  scales: {
    y: {
      beginAtZero: false // Weight doesn't usually start at 0
    }
  }
});

const weightChartOptions = computed(() => ({
  ...chartOptions.value,
  plugins: {
     ...chartOptions.value.plugins,
     title: { display: true, text: '⚖️ 体重趋势' }
  },
   scales: {
    y: {
      beginAtZero: false,
      title: { display: true, text: '体重 (kg)' }
    }
  }
}));

// --- Exercise Duration Chart (Line) ---
const exerciseDurationChartData = computed(() => {
  if (!trendsData.value?.exercise_duration || trendsData.value.exercise_duration.length === 0) {
    return { labels: [], datasets: [] };
  }
  const labels = trendsData.value.exercise_duration.map(item => item.date);
  const data = trendsData.value.exercise_duration.map(item => item.value);

  return {
    labels,
    datasets: [
      {
        label: '运动时长 (分钟)',
        backgroundColor: '#10b981', // Green
        borderColor: '#10b981',
        data: data,
        tension: 0.1,
        fill: false
      }
    ]
  };
});

const exerciseDurationChartOptions = computed(() => ({
  ...chartOptions.value,
  plugins: {
     ...chartOptions.value.plugins,
     title: { display: true, text: '🏃 运动时长趋势' }
  },
   scales: {
    y: {
      beginAtZero: true,
      title: { display: true, text: '时长 (分钟)' }
    }
  }
}));

// --- Mood Chart (Bar) ---
const moodChartData = computed(() => {
  if (!trendsData.value?.mood || trendsData.value.mood.length === 0) {
    return { labels: [], datasets: [] };
  }
  
  // Count mood occurrences
  const moodCounts = trendsData.value.mood.reduce((acc, item) => {
      acc[item.value] = (acc[item.value] || 0) + 1;
      return acc;
  }, {});

  // Prepare labels and data for Bar chart
  const labels = Object.keys(moodCounts);
  const data = Object.values(moodCounts);
  
  // Define colors for different moods (optional, but nice)
  const moodColors = {
      happy: '#facc15', // Yellow
      calm: '#60a5fa', // Blue
      sad: '#9ca3af', // Gray
      angry: '#ef4444', // Red
      anxious: '#f97316', // Orange
      tired: '#6b7280', // Dark Gray
      excited: '#ec4899', // Pink
      bored: '#a78bfa'  // Purple
      // Add more if needed
  };
  const backgroundColors = labels.map(label => moodColors[label] || '#d1d5db'); // Default color if unknown

  return {
    labels,
    datasets: [
      {
        label: '心情次数',
        backgroundColor: backgroundColors,
        borderColor: backgroundColors, // Optional: border color same as background
        borderWidth: 1, // Optional
        data: data,
      }
    ]
  };
});

const moodChartOptions = computed(() => ({
  ...chartOptions.value,
   indexAxis: 'y',
   plugins: {
     ...chartOptions.value.plugins,
     legend: { display: false },
     title: { display: true, text: '😊 心情分布 (过去30天)' }
  },
   scales: {
    x: { 
      beginAtZero: true,
      title: { display: true, text: '记录次数' }
    },
    y: { 
       title: { display: false }
    }
  }
}));

// --- Auto Suggestions Logic ---

// Helper to filter data for the last N days
const filterLastNDays = (dataArray, days) => {
  if (!dataArray || dataArray.length === 0) return [];
  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - days);
  const cutoffDateStr = cutoffDate.toISOString().split('T')[0];
  return dataArray.filter(item => item.date >= cutoffDateStr);
};

const autoSuggestions = computed(() => {
  const suggestions = [];
  const days = 14;

  if (!trendsData.value) {
    return ['数据不足，无法生成建议。'];
  }

  // --- Exercise Suggestion ---
  const recentExercise = filterLastNDays(trendsData.value.exercise_duration, days);
  if (recentExercise.length > 0) {
    const totalDuration = recentExercise.reduce((sum, item) => sum + item.value, 0);
    const avgDuration = totalDuration / days;
    if (avgDuration < 20) {
      suggestions.push(`🏃 运动建议：过去 ${days} 天日均运动时长约 ${avgDuration.toFixed(0)} 分钟，尝试增加到每天 20-30 分钟的中等强度活动，如快走或骑行。`);
    } else if (avgDuration > 90) {
        suggestions.push(`🏃 运动很棒！过去 ${days} 天日均运动时长约 ${avgDuration.toFixed(0)} 分钟。注意劳逸结合，避免过度训练。`);
    } else {
        suggestions.push(`🏃 运动习惯保持得不错！过去 ${days} 天日均运动时长充足。`);
    }
  } else {
      suggestions.push(`🏃 运动建议：最近 ${days} 天缺少运动记录，尝试开始规律运动吧！即使每天散步 20 分钟也很有益。`);
  }

  // --- Mood Suggestion ---
  const recentMoods = filterLastNDays(trendsData.value.mood, days);
  if (recentMoods.length > 0) {
    const moodCounts = recentMoods.reduce((acc, item) => {
      acc[item.value] = (acc[item.value] || 0) + 1;
      return acc;
    }, {});
    const negativeMoodCount = (moodCounts.sad || 0) + (moodCounts.angry || 0) + (moodCounts.anxious || 0);
    if (negativeMoodCount > 3) { 
      suggestions.push(`😊 心情关怀：注意到您最近 ${days} 天记录到 ${negativeMoodCount} 次负面情绪。尝试通过放松练习、与人交流或培养兴趣爱好来调节心情。`);
    } else if (moodCounts.happy > recentMoods.length / 2) {
         suggestions.push(`😊 心情愉悦！过去 ${days} 天大部分时间心情都不错，继续保持好心态！`);
    }
    // Add more positive/neutral mood suggestions if needed
  }

  // --- Weight Suggestion ---
  const recentWeight = filterLastNDays(trendsData.value.weight_kg, days);
  if (recentWeight.length >= 2) { 
    const firstWeight = recentWeight[0].value;
    const lastWeight = recentWeight[recentWeight.length - 1].value;
    const weightChange = lastWeight - firstWeight;
    if (weightChange > 0.5) { 
      suggestions.push(`⚖️ 体重提示：最近 ${days} 天体重似乎有所增加 (${weightChange.toFixed(1)} kg)。请留意近期的饮食和运动情况。`);
    } else if (weightChange < -0.5) { 
      suggestions.push(`⚖️ 体重提示：最近 ${days} 天体重似乎有所下降 (${weightChange.toFixed(1)} kg)。如非目标减重，请确保营养摄入充足。`);
    } else {
        suggestions.push(`⚖️ 体重管理：最近 ${days} 天体重保持相对稳定。`);
    }
  }

  // --- Diet Suggestion (Placeholder - Requires Diet Data) ---
  // We currently don't fetch specific diet trend data (e.g., average calories, macro balance)
  // Add a placeholder or fetch diet data if available
  suggestions.push('🍽️ 饮食提醒：请记得记录您的饮食，以便获得更全面的分析和建议。');

  // Default suggestion
  if (suggestions.length <= 1) { // Adjust condition if diet placeholder added
    suggestions.push('✍️ 持续记录您的健康数据，有助于生成更准确的建议。');
  }

  return suggestions;
});

// --- Data Fetching ---
const fetchReportData = async () => {
  loading.value = true // Start overall loading
  trendsLoading.value = true // Start trends loading
  error.value = null
  trendsError.value = null

  try {
    if (!userStore.state.token) {
      console.log('未登录，跳转到登录页')
      // Redirect to login or show login message
      router.push('/login?redirect=/reports') 
      return
    }

    console.log('开始获取报告和趋势数据...')
    
    // Fetch summary and trends data in parallel
    const [summaryResponse, trendsResponse] = await Promise.allSettled([
      getReportsSummary(),
      // Fetch last 30 days of weight, mood, exercise duration
      getTrendsData(getPastDate(30), getCurrentDate(), ['weight_kg', 'mood', 'exercise_duration'])
    ]);

    // Handle Summary Data
    if (summaryResponse.status === 'fulfilled' && summaryResponse.value) {
       const summaryData = summaryResponse.value; // Use a shorter variable name
       console.log('报告摘要数据:', summaryData)
       
       // --- 恢复填充 analysisData --- 
       analysisData.value = {
         exerciseStats: {
           totalMinutes: summaryData.exerciseMinutes || 0,
           averagePerDay: summaryData.exerciseMinutes ? Math.round(summaryData.exerciseMinutes / (summaryData.days || 7)) : 0, // Use actual days if available
           mostFrequentType: summaryData.topExerciseType || '-',
           intensityDistribution: summaryData.intensityDistribution || { light: 0, medium: 0, high: 0 }
         },
         moodStats: {
           distribution: summaryData.moodDistribution || {},
           mostFrequent: summaryData.topMood || '-'
         },
         dietStats: {
           totalRecords: summaryData.foodCount || 0,
           regularityRate: summaryData.regularityRate || 0,
           mealDistribution: summaryData.mealDistribution || { breakfast: 0, lunch: 0, dinner: 0, snack: 0 },
           categories: summaryData.foodCategories || {}
         }
       };

       // --- 恢复填充 recommendationsData (只更新 healthTips 的第一条，保持其他不变) ---
       if (summaryData.healthTip) {
            // 创建一个新的 healthTips 数组，只修改第一项，保持其他默认项
            const updatedHealthTips = [...recommendationsData.value.healthTips]; 
            if (updatedHealthTips.length > 0) {
                updatedHealthTips[0] = { ...updatedHealthTips[0], content: summaryData.healthTip };
            } else {
                // 如果默认数组为空，则添加一项
                updatedHealthTips.push({ type: 'general', content: summaryData.healthTip });
            }
            recommendationsData.value = {
                ...recommendationsData.value, // 保留 personalizedRecommendations 等其他部分
                healthTips: updatedHealthTips
            };
       } else {
           // 如果 API 没有返回 healthTip，确保 recommendationsData 至少有默认值
           // (通常 ref 的默认值已经处理了这种情况，这里是双重保险)
           if (!recommendationsData.value) {
               recommendationsData.value = { healthTips: [], personalizedRecommendations: [] };
           }
       }
        console.log('填充后 analysisData:', analysisData.value);
        console.log('填充后 recommendationsData:', recommendationsData.value);

    } else {
        console.error('获取报告摘要失败:', summaryResponse.reason);
        error.value = '无法加载报告摘要信息。' 
        // 即使摘要失败，也给子组件提供默认空结构，避免它们出错
        analysisData.value = { exerciseStats: {}, moodStats: {}, dietStats: {} }; 
        recommendationsData.value = { healthTips: [], personalizedRecommendations: [] };
    }

    // Handle Trends Data
    if (trendsResponse.status === 'fulfilled' && trendsResponse.value) {
        console.log('趋势数据:', trendsResponse.value)
        trendsData.value = trendsResponse.value;
    } else {
        console.error('获取趋势数据失败:', trendsResponse.reason);
        trendsError.value = '无法加载趋势数据。' // Specific error for trends
        // Don't necessarily block the whole page if trends fail
    }

  } catch (err) { // Catch errors not handled by Promise.allSettled (e.g., network issues before requests)
    console.error('获取报告数据时发生意外错误:', err)
    error.value = '加载报告数据时出错，请稍后重试。'
    trendsError.value = '加载趋势数据时出错。'
  } finally {
    loading.value = false // Finish overall loading
    trendsLoading.value = false // Finish trends loading
  }
}

// Helper functions for dates
const getCurrentDate = () => {
  const today = new Date();
  return today.toISOString().split('T')[0]; // YYYY-MM-DD
};

const getPastDate = (daysAgo) => {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return date.toISOString().split('T')[0]; // YYYY-MM-DD
};

// Mock data function (keep or remove)
const useMockData = () => { 
    console.warn('使用模拟数据填充报告页！')
    // ... (populate analysisData and recommendationsData with mocks)
    trendsData.value = { // Add mock trend data if needed for testing
        weight_kg: [
            { date: '2024-04-20', value: 71.0 },
            { date: '2024-04-22', value: 70.5 },
            { date: '2024-04-25', value: 70.8 },
            { date: '2024-04-28', value: 70.2 },
        ]
    }
    loading.value = false
    trendsLoading.value = false
 }

// Method to open the advice request modal
const openRequestModal = () => {
    requestText.value = ''; // Clear previous text
    adviceSubmitError.value = null; // Clear previous errors
    adviceSubmitSuccess.value = false; // Reset success state
    showRequestModal.value = true;
};

// Method to handle the advice request submission
const handleRequestSubmit = async () => {
    isSubmittingAdvice.value = true;
    adviceSubmitError.value = null;
    adviceSubmitSuccess.value = false;

    try {
        const response = await submitAdviceRequest(requestText.value);
        console.log('建议请求提交成功:', response);
        adviceSubmitSuccess.value = true;
        // 可以在短暂延迟后关闭模态框，或让用户手动关闭
        setTimeout(() => {
            showRequestModal.value = false;
        }, 2000); // 2秒后自动关闭

    } catch (error) {
        console.error('提交建议请求失败:', error);
        adviceSubmitError.value = error.message || '提交请求时发生未知错误。';
    } finally {
        isSubmittingAdvice.value = false;
    }
};

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', (event) => {
    if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
      showUserMenu.value = false
    }
  })
  
  fetchReportData()
  
  // 开始自动刷新
  startAutoRefresh()
  
  // 监听记录更新事件
  window.addEventListener('recordUpdated', handleRecordUpdate)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', () => {})
  stopAutoRefresh()
  window.removeEventListener('recordUpdated', handleRecordUpdate)
})
</script>

<style scoped>
.reports-page {
  min-height: 100vh;
  background: #f8fafc;
}

.glass-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 0.75rem 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.main-nav {
  display: flex;
  gap: 1.5rem;
}

.nav-item {
  text-decoration: none;
  color: #64748b;
  font-size: 0.95rem;
  transition: color 0.2s;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
}

.nav-item:hover {
  color: #334155;
}

.nav-item.active {
  color: #3b82f6;
  font-weight: 500;
}

.user-menu {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.user-info:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.avatar {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.username {
  font-size: 0.95rem;
  color: #334155;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 0.7rem;
  color: #64748b;
  transition: transform 0.2s;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 0.25rem);
  right: 0;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 200px;
  overflow: hidden;
  z-index: 10;
}

.dropdown-header {
  padding: 0.75rem 1rem;
  background: #f8fafc;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.signed-in {
  font-size: 0.75rem;
  color: #64748b;
}

.dropdown-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.05);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #334155;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  cursor: pointer;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}

.dropdown-item:hover {
  background: #f1f5f9;
}

.item-icon {
  font-size: 1rem;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 1.75rem;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-container h3 {
  color: #ef4444;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.retry-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background: #2563eb;
}

.reports-content > * {
  margin-bottom: 1.5rem;
}

/* Trends Section Styles */
.trends-section {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-top: 2rem;
}

.trends-section h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.75rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.chart-container {
  position: relative; 
  min-height: 300px; /* Ensure container has height for chart */
  padding: 1rem;
  border: 1px solid #f1f5f9;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.no-chart-data {
    text-align: center;
    color: #64748b;
    padding: 2rem;
    font-style: italic;
}

.placeholder-text {
    text-align: center;
    color: #9ca3af;
    padding: 2rem;
}

/* Loading/Error states within section */
.loading-container.small,
.error-container.small {
    min-height: 150px;
    padding: 1rem;
}

/* Auto-Suggestions & Request Advice Sections */
.auto-suggestions-section,
.request-advice-section {
  background-color: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-top: 2rem;
}

.auto-suggestions-section h2,
.request-advice-section h2 {
   font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.75rem;
}

.action-button {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 1rem; /* Add some spacing if needed */
}

.action-button:hover {
    background-color: #2563eb;
}

/* Auto-Suggestions Section Styles */
.auto-suggestions-section h2 {
   /* Styles from previous edit */
   display: flex; /* Align subtitle */
   align-items: baseline;
}

.section-subtitle {
    font-size: 0.85rem;
    color: #64748b;
    font-weight: 400;
    margin-left: 0.75rem;
}

.suggestions-list {
  list-style: none; /* Remove default bullets */
  padding: 0;
  margin: 0;
}

.suggestions-list li {
  background-color: #f8f9fa; /* Light background for each suggestion */
  padding: 0.8rem 1.2rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
  color: #334155;
  border-left: 4px solid #3b82f6; /* Accent border */
  line-height: 1.5;
  display: flex; /* Align emoji and text */
  align-items: baseline;
  gap: 0.5em; /* Add space between emoji and text */
}

.suggestions-list li:last-child {
  margin-bottom: 0;
}

/* Request Advice Section Adjustments */
.request-advice-section p {
    color: #475569;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

.success-message {
  margin-top: 1rem;
  color: #059669; /* Green */
  font-weight: 500;
  font-size: 0.95rem;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #1e293b;
}

.modal-content p {
    color: #475569;
    margin-bottom: 1rem;
}

.modal-content textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.95rem;
  margin-bottom: 1rem;
  resize: vertical;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

/* General Button Styles (if not already defined globally) */
.button {
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.button.primary {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}
.button.primary:hover:not(:disabled) {
  background-color: #2563eb;
}

.button.secondary {
  background-color: #e2e8f0;
  color: #475569;
  border-color: #e2e8f0;
}
.button.secondary:hover:not(:disabled) {
  background-color: #cbd5e1;
}

.button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Smaller messages inside modal */
.error-message.small,
.success-message.small {
    font-size: 0.9rem;
    margin-top: 0.5rem;
    text-align: center;
}
</style> 
