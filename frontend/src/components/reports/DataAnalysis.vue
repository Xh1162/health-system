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

      <!-- 健康状况分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>健康状况</h3>
        </div>
        <div class="health-stats">
          <div class="health-score-container">
            <h4>整体健康指数</h4>
            <div class="health-score-wrapper">
              <div class="health-gauge">
                <svg viewBox="0 0 120 120" class="gauge">
                  <circle class="gauge-bg" cx="60" cy="60" r="50" />
                  <circle class="gauge-value" cx="60" cy="60" r="50" 
                          :stroke="getHealthGaugeColor()" 
                          :stroke-dasharray="`${getHealthPercentage()}, 314`" />
                  <text x="60" y="65" class="gauge-text">{{ getHealthScore() }}</text>
                </svg>
                <div class="gauge-level">{{ getHealthLevel() }}</div>
              </div>
              <div class="health-factors">
                <div class="factor">
                  <span class="factor-label">活动指数</span>
                  <div class="factor-bar-container">
                    <div class="factor-bar" :style="{ width: '75%', background: 'linear-gradient(to right, #60a5fa, #3b82f6)' }"></div>
                  </div>
                </div>
                <div class="factor">
                  <span class="factor-label">情绪指数</span>
                  <div class="factor-bar-container">
                    <div class="factor-bar" :style="{ width: '82%', background: 'linear-gradient(to right, #34d399, #10b981)' }"></div>
                  </div>
                </div>
                <div class="factor">
                  <span class="factor-label">睡眠指数</span>
                  <div class="factor-bar-container">
                    <div class="factor-bar" :style="{ width: '68%', background: 'linear-gradient(to right, #60a5fa, #3b82f6)' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="common-issues">
            <h4>健康提示</h4>
            <div v-if="analysisData.healthStats.commonIssues && analysisData.healthStats.commonIssues.length > 0" class="issues-list">
              <div v-for="issue in analysisData.healthStats.commonIssues.slice(0, 2)" 
                   :key="issue.type" 
                   class="issue-item">
                <div class="issue-details">
                  <span class="issue-label">{{ getHealthLabel(issue.type) }}</span>
                  <span class="issue-suggestion">{{ getSimpleHealthSuggestion(issue.type) }}</span>
                </div>
                <span class="issue-count">{{ issue.count }}次</span>
              </div>
            </div>
            <div v-else class="empty-issues">
              <p>暂无健康问题记录，继续保持健康的生活方式！</p>
            </div>
          </div>
          
          <div class="data-insights">
            <p class="insight-text">{{ getSimpleHealthInsight() }}</p>
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
      healthStats: {
        commonIssues: []
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
    healthStats: {
      commonIssues: props.analysisData?.healthStats?.commonIssues || []
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

const getHealthLabel = (type) => {
  if (!type) return '未知'
  const labels = {
    sleep_bad: '睡眠不足',
    appetite_bad: '没有胃口',
    fatigue: '疲劳',
    headache: '头痛',
    muscle_sore: '肌肉酸痛',
    cold: '感冒'
  }
  return labels[type] || '未知'
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

// 获取健康评分
const getHealthScore = () => {
  return 78
}

// 获取健康仪表盘百分比
const getHealthPercentage = () => {
  const score = getHealthScore()
  return Math.round(score * 3.14)
}

// 获取健康仪表盘颜色
const getHealthGaugeColor = () => {
  const score = getHealthScore()
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#3b82f6'
  if (score >= 40) return '#f59e0b'
  return '#ef4444'
}

// 获取健康等级
const getHealthLevel = () => {
  const score = getHealthScore()
  if (score >= 80) return '优'
  if (score >= 60) return '良'
  if (score >= 40) return '中'
  return '差'
}

// 获取简化的健康建议
const getSimpleHealthSuggestion = (type) => {
  const suggestions = {
    sleep_bad: '尝试规律的睡眠时间',
    appetite_bad: '少量多餐，增加饮食多样性',
    fatigue: '保证足够休息，避免过度疲劳',
    headache: '注意用眼习惯，保持充分水分',
    muscle_sore: '运动后适当拉伸放松肌肉',
    cold: '保暖并增强免疫力'
  }
  return suggestions[type] || '关注身体状况变化'
}

// 获取简化的健康见解
const getSimpleHealthInsight = () => {
  const score = getHealthScore()
  
  if (score >= 80) {
    return "您的健康状况良好，继续保持健康的生活方式。"
  } else if (score >= 60) {
    return "您的健康状况总体不错，注意保持规律作息和适量运动。"
  } else {
    return "建议关注身体状况，增强锻炼并保持健康饮食习惯。"
  }
}

// 获取前几位的情绪类型
const getTopMoods = () => {
  const distribution = props.analysisData?.moodStats?.distribution || {}
  const moodsArray = Object.entries(distribution).map(([type, value]) => ({ type, value }))
  return moodsArray.sort((a, b) => b.value - a.value).slice(0, 3)
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

.intensity-distribution, .mood-distribution, .common-issues {
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.intensity-distribution h4, .mood-distribution h4, .common-issues h4, .emotion-balance-score h4 {
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

.health-score-container {
  margin-bottom: 1.5rem;
}

.health-score-wrapper {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.health-gauge {
  position: relative;
  width: 100px;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.gauge {
  transform: rotate(-90deg);
  overflow: visible;
}

.gauge-bg {
  fill: none;
  stroke: #f1f5f9;
  stroke-width: 6;
}

.gauge-value {
  fill: none;
  stroke-width: 6;
  stroke-linecap: round;
  transition: stroke-dasharray 1s ease;
}

.gauge-text {
  transform: rotate(90deg);
  font-size: 16px;
  font-weight: bold;
  fill: #1e293b;
  text-anchor: middle;
  dominant-baseline: middle;
}

.gauge-level {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

.health-factors {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.factor {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.factor-label {
  font-size: 0.75rem;
  color: #64748b;
}

.factor-bar-container {
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
}

.factor-bar {
  height: 100%;
  border-radius: 3px;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.issue-item {
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.25rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.issue-details {
  display: flex;
  flex-direction: column;
}

.issue-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #334155;
  margin-bottom: 0.125rem;
}

.issue-suggestion {
  font-size: 0.75rem;
  color: #64748b;
}

.issue-count {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  background: #f1f5f9;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
}

.empty-issues {
  text-align: center;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.25rem;
}

.empty-issues p {
  margin: 0;
  font-size: 0.8125rem;
  color: #64748b;
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
  .health-score-wrapper {
    flex-direction: column;
    gap: 1rem;
  }
  
  .stat-row {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .stat-item {
    min-width: auto;
  }
}
</style> 