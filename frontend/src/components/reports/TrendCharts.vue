<template>
  <div class="trend-charts-section">
    <div class="section-header">
      <h3>健康数据趋势</h3>
      <p class="subtitle">您的健康数据分析图表</p>
      
      <div class="period-selector">
        <button 
          v-for="option in periodOptions" 
          :key="option.value"
          :class="['period-button', { active: selectedPeriod === option.value }]"
          @click="changePeriod(option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载趋势数据中...</p>
    </div>

    <div v-else-if="!hasData" class="empty-state">
      <p>暂无足够的数据来生成趋势图表</p>
      <p class="suggestion">继续记录您的健康数据，以便查看详细的趋势分析</p>
    </div>

    <div v-else class="charts-container">
      <!-- 运动趋势图 -->
      <div class="chart-card" v-if="exerciseData.datasets[0].data.length > 0">
        <h4>运动趋势</h4>
        <div class="chart-wrapper">
          <LineChart 
            :chart-data="exerciseData" 
            :options="exerciseOptions" 
          />
        </div>
      </div>
      
      <!-- 心情趋势图 -->
      <div class="chart-card" v-if="moodData.datasets[0].data.length > 0">
        <h4>心情趋势</h4>
        <div class="chart-wrapper">
          <LineChart 
            :chart-data="moodData" 
            :options="moodOptions" 
          />
        </div>
      </div>
      
      <!-- 体重趋势图 (如果有数据) -->
      <div class="chart-card" v-if="weightData.datasets[0].data.length > 0">
        <h4>体重趋势</h4>
        <div class="chart-wrapper">
          <LineChart 
            :chart-data="weightData" 
            :options="weightOptions" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { Line as LineChart } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { getHealthTrends } from '../../api/reports'
import { useRouter } from 'vue-router'

// 注册Chart.js组件
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

const loading = ref(true)
const hasData = ref(false)
const selectedPeriod = ref('month')
const periodOptions = [
  { label: '周', value: 'week' },
  { label: '月', value: 'month' },
  { label: '年', value: 'year' }
]

const router = useRouter()

// 图表数据模板
const createChartData = () => ({
  labels: [],
  datasets: [
    {
      label: '',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      data: []
    }
  ]
})

// 初始化各图表数据
const exerciseData = ref(createChartData())
const moodData = ref(createChartData())
const weightData = ref(createChartData())

// 图表配置选项
const exerciseOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '运动时长(分钟)'
      }
    }
  }
}

const moodOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      min: 1,
      max: 5,
      title: {
        display: true,
        text: '心情评分'
      }
    }
  }
}

const weightOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      title: {
        display: true,
        text: '体重(kg)'
      }
    }
  }
}

// 加载趋势数据
const loadTrendsData = async () => {
  loading.value = true
  try {
    // 获取不同周期的天数
    const days = {
      week: 7,
      month: 30,
      year: 365
    }[selectedPeriod.value]
    
    const data = await getHealthTrends(days)
    
    if (!data || !data.exercise || !data.mood) {
      hasData.value = false
      return
    }
    
    hasData.value = true
    
    // 更新运动趋势数据
    if (data.exercise && data.exercise.dates && data.exercise.values) {
      exerciseData.value = {
        labels: data.exercise.dates,
        datasets: [{
          label: '运动时长(分钟)',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          data: data.exercise.values
        }]
      }
    }
    
    // 更新心情趋势数据
    if (data.mood && data.mood.dates && data.mood.values) {
      moodData.value = {
        labels: data.mood.dates,
        datasets: [{
          label: '心情评分',
          backgroundColor: 'rgba(255, 159, 64, 0.2)',
          borderColor: 'rgba(255, 159, 64, 1)',
          data: data.mood.values
        }]
      }
    }
    
    // 更新体重趋势数据 (如果有)
    if (data.weight && data.weight.dates && data.weight.values) {
      weightData.value = {
        labels: data.weight.dates,
        datasets: [{
          label: '体重(kg)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          data: data.weight.values
        }]
      }
    }
  } catch (err) {
    console.error('加载趋势数据失败:', err)
    hasData.value = false
  } finally {
    loading.value = false
  }
}

// 切换周期
const changePeriod = (period) => {
  selectedPeriod.value = period
}

// 监听周期变化，重新加载数据
watch(selectedPeriod, () => {
  loadTrendsData()
})

// 组件挂载时加载数据
onMounted(() => {
  loadTrendsData()
})

// 添加查看报告的方法
const viewUserReport = (user) => {
  router.push(`/admin/user-report/${user.id}`);
}

// 添加下面这个导航方法
const navigateToUserReports = () => {
  router.push('/admin/user-reports');
};
</script>

<style scoped>
.trend-charts-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.period-selector {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.period-button {
  background: #f1f5f9;
  border: none;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.period-button.active {
  background: #3b82f6;
  color: white;
}

.period-button:hover:not(.active) {
  background: #e2e8f0;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: #64748b;
}

.suggestion {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 0.5rem;
}

/* 图表容器 */
.charts-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 992px) {
  .charts-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

.chart-card {
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.chart-card h4 {
  font-size: 1rem;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.chart-wrapper {
  height: 250px;
}
</style> 