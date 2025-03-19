<template>
  <div class="data-analysis">
    <div class="analysis-header">
      <h2>健康数据分析</h2>
      <p class="subtitle">您的关键健康指标</p>
    </div>

    <div class="analysis-grid">
      <!-- 运动分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>运动分析</h3>
        </div>
        <div class="exercise-stats">
          <div class="stat-row">
            <div class="stat-item">
              <span class="stat-label">总运动时长</span>
              <span class="stat-value highlight">{{ analysisData.exerciseStats.totalMinutes || 0 }}分钟</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">日均运动</span>
              <span class="stat-value highlight">{{ analysisData.exerciseStats.averagePerDay || 0 }}分钟</span>
              <span class="stat-recommendation" v-if="analysisData.exerciseStats.averagePerDay < 30">建议增加到30分钟/天</span>
              <span class="stat-achievement" v-else>达到推荐量</span>
            </div>
          </div>
          <div class="stat-row">
            <div class="stat-item">
              <span class="stat-label">最常见运动</span>
              <span class="stat-value">{{ getExerciseLabel(analysisData.exerciseStats.mostFrequentType) }}</span>
            </div>
          </div>
          <div class="intensity-distribution">
            <h4>运动强度分布</h4>
            <div class="distribution-bars">
              <div class="distribution-bar">
                <div class="bar-label">轻度</div>
                <div class="bar-container">
                  <div class="bar light" :style="{ width: getPercentage(analysisData.exerciseStats.intensityDistribution?.light) + '%' }"></div>
                </div>
                <div class="bar-value">{{ analysisData.exerciseStats.intensityDistribution?.light || 0 }}%</div>
              </div>
              <div class="distribution-bar">
                <div class="bar-label">中度</div>
                <div class="bar-container">
                  <div class="bar medium" :style="{ width: getPercentage(analysisData.exerciseStats.intensityDistribution?.medium) + '%' }"></div>
                </div>
                <div class="bar-value">{{ analysisData.exerciseStats.intensityDistribution?.medium || 0 }}%</div>
              </div>
              <div class="distribution-bar">
                <div class="bar-label">剧烈</div>
                <div class="bar-container">
                  <div class="bar high" :style="{ width: getPercentage(analysisData.exerciseStats.intensityDistribution?.high) + '%' }"></div>
                </div>
                <div class="bar-value">{{ analysisData.exerciseStats.intensityDistribution?.high || 0 }}%</div>
              </div>
            </div>
          </div>
          <div class="data-insights">
            <p class="insight-text">{{ getSimpleExerciseInsight() }}</p>
          </div>
        </div>
      </div>

      <!-- 心情分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>心情分析</h3>
        </div>
        <div class="mood-stats">
          <div class="emotion-balance-score">
            <h4>情绪健康评分</h4>
            <div class="balance-score">
              <div class="score-circle" :style="{ background: getMoodScoreColor() }">
                <span>{{ getMoodScore() }}</span>
              </div>
              <div class="score-label">{{ getMoodScoreLabel() }}</div>
            </div>
          </div>
          <div class="mood-distribution">
            <h4>主要心情</h4>
            <div class="mood-grid">
              <div v-for="(mood, index) in getTopMoods()" 
                   :key="index" 
                   class="mood-item">
                <span class="mood-label">{{ getMoodLabel(mood.type) }}</span>
                <span class="mood-value">{{ mood.value || 0 }}%</span>
              </div>
            </div>
          </div>
          <div class="data-insights">
            <p class="insight-text">{{ getSimpleMoodInsight() }}</p>
          </div>
        </div>
      </div>

      <!-- 饮食分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>饮食分析</h3>
        </div>
        <div class="diet-stats">
          <div class="diet-summary">
            <h4>饮食记录统计</h4>
            <div class="stat-row">
              <div class="stat-item">
                <span class="stat-label">记录总数</span>
                <span class="stat-value highlight">{{ analysisData.dietStats?.totalRecords || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">规律饮食率</span>
                <span class="stat-value highlight">{{ analysisData.dietStats?.regularityRate || 0 }}%</span>
              </div>
            </div>
          </div>
          
          <div class="meal-distribution">
            <h4>膳食分布</h4>
            <div class="meal-distribution-chart">
              <div v-for="(item, index) in getDietDistribution()" 
                   :key="index" 
                   class="meal-item">
                <div class="meal-label">{{ item.name }}</div>
                <div class="meal-bar-container">
                  <div class="meal-bar" :style="{ width: item.percentage + '%', background: getMealColor(item.name) }"></div>
                </div>
                <div class="meal-value">{{ item.value }}%</div>
              </div>
            </div>
          </div>
          
          <div class="food-categories">
            <h4>食物类别</h4>
            <div class="food-category-grid">
              <div class="food-category">
                <div class="category-icon">🍲</div>
                <div class="category-details">
                  <span class="category-name">主食</span>
                  <span class="category-percentage">{{ analysisData.dietStats?.categories?.staple || 30 }}%</span>
                </div>
              </div>
              <div class="food-category">
                <div class="category-icon">🥩</div>
                <div class="category-details">
                  <span class="category-name">蛋白质</span>
                  <span class="category-percentage">{{ analysisData.dietStats?.categories?.protein || 25 }}%</span>
                </div>
              </div>
              <div class="food-category">
                <div class="category-icon">🥗</div>
                <div class="category-details">
                  <span class="category-name">蔬果</span>
                  <span class="category-percentage">{{ analysisData.dietStats?.categories?.vegetables || 35 }}%</span>
                </div>
              </div>
              <div class="food-category">
                <div class="category-icon">🍭</div>
                <div class="category-details">
                  <span class="category-name">零食甜点</span>
                  <span class="category-percentage">{{ analysisData.dietStats?.categories?.snacks || 10 }}%</span>
                </div>
              </div>
            </div>
          </div>
          
          <div class="data-insights">
            <p class="insight-text">{{ getSimpleDietInsight() }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  analysisData: {
    type: Object,
    required: true,
    default: () => ({
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
  }
})

// 确保数据结构完整
const safeAnalysisData = computed(() => {
  return {
    exerciseStats: {
      totalMinutes: props.analysisData?.exerciseStats?.totalMinutes || 0,
      averagePerDay: props.analysisData?.exerciseStats?.averagePerDay || 0,
      mostFrequentType: props.analysisData?.exerciseStats?.mostFrequentType || 'walking',
      intensityDistribution: {
        light: props.analysisData?.exerciseStats?.intensityDistribution?.light || 0,
        medium: props.analysisData?.exerciseStats?.intensityDistribution?.medium || 0,
        high: props.analysisData?.exerciseStats?.intensityDistribution?.high || 0
      }
    },
    moodStats: {
      distribution: props.analysisData?.moodStats?.distribution || {
        happy: 0,
        calm: 0,
        sad: 0,
        angry: 0,
        anxious: 0,
        tired: 0,
        excited: 0,
        bored: 0
      },
      mostFrequent: props.analysisData?.moodStats?.mostFrequent || 'calm'
    },
    dietStats: {
      totalRecords: props.analysisData?.dietStats?.totalRecords || 0,
      regularityRate: props.analysisData?.dietStats?.regularityRate || 0,
      mealDistribution: props.analysisData?.dietStats?.mealDistribution || {
        breakfast: 25,
        lunch: 30,
        dinner: 30,
        snack: 15
      },
      categories: props.analysisData?.dietStats?.categories || {
        staple: 30,
        protein: 25,
        vegetables: 35,
        snacks: 10
      }
    }
  }
})

const getExerciseLabel = (type) => {
  if (!type) return '步行'
  const labels = {
    walking: '步行',
    running: '跑步',
    cycling: '骑行',
    swimming: '游泳',
    yoga: '瑜伽',
    gym: '健身',
    basketball: '篮球',
    football: '足球'
  }
  return labels[type] || '步行'
}

const getMoodLabel = (type) => {
  if (!type) return '平静'
  const labels = {
    happy: '开心',
    calm: '平静',
    sad: '难过',
    angry: '生气',
    anxious: '焦虑',
    tired: '疲惫',
    excited: '兴奋',
    bored: '无聊'
  }
  return labels[type] || '平静'
}

const getPercentage = (value) => {
  if (typeof value !== 'number' || isNaN(value)) return 0
  return Math.min(100, Math.max(0, value))
}

// 简化运动见解
const getSimpleExerciseInsight = () => {
  const avgPerDay = props.analysisData?.exerciseStats?.averagePerDay || 0
  const totalMinutes = props.analysisData?.exerciseStats?.totalMinutes || 0
  
  if (avgPerDay >= 30) {
    return "您的日均运动时间达到推荐水平，继续保持！"
  } else if (avgPerDay >= 15) {
    return "您的运动量接近推荐水平，可以适当增加运动时间。"
  } else {
    return "建议增加日常运动量，每天至少30分钟中等强度运动。"
  }
}

// 获取情绪评分
const getMoodScore = () => {
  const distribution = props.analysisData?.moodStats?.distribution || {}
  const positiveRatio = ((distribution.happy || 0) + (distribution.excited || 0) + (distribution.calm || 0)) / 100
  return Math.round(positiveRatio * 100)
}

// 获取情绪评分颜色
const getMoodScoreColor = () => {
  const score = getMoodScore()
  if (score >= 70) return '#10b981'
  if (score >= 50) return '#3b82f6'
  if (score >= 30) return '#f59e0b'
  return '#ef4444'
}

// 获取情绪评分等级
const getMoodScoreLabel = () => {
  const score = getMoodScore()
  if (score >= 70) return '良好'
  if (score >= 50) return '一般'
  if (score >= 30) return '需关注'
  return '需改善'
}

// 获取简化的情绪见解
const getSimpleMoodInsight = () => {
  const score = getMoodScore()
  const mostFrequent = props.analysisData?.moodStats?.mostFrequent || 'calm'
  
  if (score >= 70) {
    return "您的情绪状态良好，积极情绪占比高。"
  } else if (mostFrequent === 'anxious' || mostFrequent === 'tired') {
    return "您可能存在一些焦虑或疲劳，建议适当放松和休息。"
  } else if (mostFrequent === 'sad' || mostFrequent === 'angry') {
    return "您近期可能心情有些低落，建议找朋友交流或参与愉快的活动。"
  }
  
  return "您的情绪状态相对稳定，保持平衡的心态对健康有益。"
}

// 获取前几位的情绪类型
const getTopMoods = () => {
  const distribution = props.analysisData?.moodStats?.distribution || {}
  const moodsArray = Object.entries(distribution).map(([type, value]) => ({ type, value }))
  return moodsArray.sort((a, b) => b.value - a.value).slice(0, 3)
}

// 获取饮食分布数据
const getDietDistribution = () => {
  // 默认数据
  const defaultDistribution = [
    { name: '早餐', value: 25, percentage: 25 },
    { name: '午餐', value: 30, percentage: 30 },
    { name: '晚餐', value: 30, percentage: 30 },
    { name: '加餐', value: 15, percentage: 15 }
  ]
  
  // 如果有实际数据，使用实际数据
  if (props.analysisData?.dietStats?.mealDistribution) {
    return Object.entries(props.analysisData.dietStats.mealDistribution).map(([name, value]) => {
      return {
        name: getMealLabel(name),
        value,
        percentage: value
      }
    })
  }
  
  return defaultDistribution
}

// 获取膳食标签
const getMealLabel = (type) => {
  const labels = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐',
    snack: '加餐'
  }
  return labels[type] || type
}

// 获取膳食颜色
const getMealColor = (name) => {
  const colors = {
    '早餐': 'linear-gradient(to right, #60a5fa, #3b82f6)',
    '午餐': 'linear-gradient(to right, #34d399, #10b981)',
    '晚餐': 'linear-gradient(to right, #f59e0b, #d97706)',
    '加餐': 'linear-gradient(to right, #a78bfa, #8b5cf6)'
  }
  return colors[name] || 'linear-gradient(to right, #60a5fa, #3b82f6)'
}

// 饮食分析见解
const getSimpleDietInsight = () => {
  const totalRecords = props.analysisData?.dietStats?.totalRecords || 0
  const regularityRate = props.analysisData?.dietStats?.regularityRate || 0
  
  if (totalRecords < 5) {
    return "记录不足，建议坚持记录饮食习惯，有助于分析饮食模式。"
  }
  
  if (regularityRate >= 80) {
    return "您的饮食规律性良好，继续保持健康均衡的饮食习惯。"
  } else if (regularityRate >= 60) {
    return "您的饮食较为规律，建议更加注重三餐平衡和营养搭配。"
  } else {
    return "您的饮食规律性有待提高，建议规律进食，避免暴饮暴食。"
  }
}
</script>

<style scoped>
.data-analysis {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}

.analysis-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.analysis-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.875rem;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.analysis-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.25rem;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.analysis-card:hover {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
}

.card-header {
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-header h3 {
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
}

.stat-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-item {
  flex: 1;
  min-width: 120px;
}

.stat-label {
  display: block;
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.highlight {
  color: #3b82f6;
}

.stat-recommendation {
  display: block;
  font-size: 0.75rem;
  color: #f59e0b;
  margin-top: 0.25rem;
}

.stat-achievement {
  display: block;
  font-size: 0.75rem;
  color: #10b981;
  margin-top: 0.25rem;
}

.intensity-distribution, .mood-distribution {
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.intensity-distribution h4, .mood-distribution h4, .emotion-balance-score h4 {
  font-size: 0.9375rem;
  color: #334155;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.distribution-bars {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.distribution-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.bar-label {
  width: 40px;
  font-size: 0.75rem;
  color: #64748b;
}

.bar-container {
  flex: 1;
  height: 6px;
  background-color: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 3px;
}

.bar.light {
  background: linear-gradient(to right, #60a5fa, #3b82f6);
}

.bar.medium {
  background: linear-gradient(to right, #34d399, #10b981);
}

.bar.high {
  background: linear-gradient(to right, #f87171, #ef4444);
}

.bar-value {
  width: 30px;
  font-size: 0.75rem;
  color: #64748b;
  text-align: right;
}

.emotion-balance-score {
  margin-bottom: 1.5rem;
}

.balance-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.score-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.125rem;
  font-weight: 700;
}

.score-label {
  font-size: 0.875rem;
  color: #475569;
  font-weight: 500;
}

.mood-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 0.5rem;
}

.mood-item {
  background: #f8fafc;
  padding: 0.5rem;
  border-radius: 0.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.mood-label {
  font-size: 0.75rem;
  color: #475569;
  margin-bottom: 0.25rem;
}

.mood-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
}

.data-insights {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
}

.insight-text {
  color: #334155;
  font-size: 0.8125rem;
  line-height: 1.4;
  margin: 0;
}

@media (max-width: 768px) {
  .stat-row {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .stat-item {
    min-width: auto;
  }
}

/* 饮食分析样式 */
.diet-stats {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.diet-summary h4, 
.meal-distribution h4,
.food-categories h4 {
  color: #475569;
  font-size: 0.9rem;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.meal-distribution-chart {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.meal-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meal-label {
  width: 3rem;
  font-size: 0.875rem;
  color: #64748b;
}

.meal-bar-container {
  flex: 1;
  height: 0.75rem;
  background: #f1f5f9;
  border-radius: 1rem;
  overflow: hidden;
}

.meal-bar {
  height: 100%;
  border-radius: 1rem;
}

.meal-value {
  min-width: 2.5rem;
  text-align: right;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
}

.food-category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.food-category {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 0.75rem;
}

.category-icon {
  font-size: 1.25rem;
}

.category-details {
  display: flex;
  flex-direction: column;
}

.category-name {
  font-size: 0.875rem;
  color: #475569;
}

.category-percentage {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3b82f6;
}

.data-insights p {
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
  color: #334155;
}
</style> 