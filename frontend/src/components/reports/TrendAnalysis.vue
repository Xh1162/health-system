<template>
  <div class="trend-analysis">
    <div class="trend-header">
      <h2>趋势分析</h2>
      <p class="subtitle">了解您的健康变化趋势</p>
    </div>

    <div class="trend-grid">
      <!-- 运动趋势 -->
      <div class="trend-card">
        <div class="card-header">
          <div class="header-icon">📈</div>
          <h3>运动趋势</h3>
        </div>
        <div class="trend-content">
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">每周运动时长</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ trendData.exerciseTrends.weeklyMinutes || 0 }}分钟</span>
                <span :class="['trend-change', getChangeClass(trendData.exerciseTrends.weeklyChange)]">
                  {{ formatChange(trendData.exerciseTrends.weeklyChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.exerciseTrends.weeklyChange)]" 
                   :style="{ width: getTrendWidth(trendData.exerciseTrends.weeklyChange) }"></div>
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">平均运动强度</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ formatTrend(trendData.exerciseTrends.intensityAvg) }}</span>
                <span :class="['trend-change', getChangeClass(trendData.exerciseTrends.intensityChange)]">
                  {{ formatChange(trendData.exerciseTrends.intensityChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.exerciseTrends.intensityChange)]" 
                   :style="{ width: getTrendWidth(trendData.exerciseTrends.intensityChange) }"></div>
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">运动频率</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ trendData.exerciseTrends.frequency || 0 }}次/周</span>
                <span :class="['trend-change', getChangeClass(trendData.exerciseTrends.frequencyChange)]">
                  {{ formatChange(trendData.exerciseTrends.frequencyChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.exerciseTrends.frequencyChange)]" 
                   :style="{ width: getTrendWidth(trendData.exerciseTrends.frequencyChange) }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 心情趋势 -->
      <div class="trend-card">
        <div class="card-header">
          <div class="header-icon">🧠</div>
          <h3>心情趋势</h3>
        </div>
        <div class="trend-content">
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">积极情绪比例</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ trendData.moodTrends.positiveRate || 0 }}%</span>
                <span :class="['trend-change', getChangeClass(trendData.moodTrends.positiveChange)]">
                  {{ formatChange(trendData.moodTrends.positiveChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.moodTrends.positiveChange)]" 
                   :style="{ width: getTrendWidth(trendData.moodTrends.positiveChange) }"></div>
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">情绪稳定性</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ formatTrend(trendData.moodTrends.stability) }}</span>
                <span :class="['trend-change', getChangeClass(trendData.moodTrends.stabilityChange)]">
                  {{ formatChange(trendData.moodTrends.stabilityChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.moodTrends.stabilityChange)]" 
                   :style="{ width: getTrendWidth(trendData.moodTrends.stabilityChange) }"></div>
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">主要情绪变化</span>
              <div class="trend-value-container">
                <span class="trend-value mood-change">
                  <span class="mood-icon">{{ getMoodIcon(trendData.moodTrends.previousMood) }}</span>
                  <span class="arrow">→</span>
                  <span class="mood-icon">{{ getMoodIcon(trendData.moodTrends.currentMood) }}</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 健康趋势 -->
      <div class="trend-card">
        <div class="card-header">
          <div class="header-icon">❤️</div>
          <h3>健康趋势</h3>
        </div>
        <div class="trend-content">
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">睡眠质量</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ formatTrend(trendData.healthTrends.sleepQuality) }}</span>
                <span :class="['trend-change', getChangeClass(trendData.healthTrends.sleepChange)]">
                  {{ formatChange(trendData.healthTrends.sleepChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.healthTrends.sleepChange)]" 
                   :style="{ width: getTrendWidth(trendData.healthTrends.sleepChange) }"></div>
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">健康问题频率</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ trendData.healthTrends.issueFrequency || 0 }}次/周</span>
                <span :class="['trend-change', getChangeClass(-trendData.healthTrends.issueChange)]">
                  {{ formatChange(-trendData.healthTrends.issueChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(-trendData.healthTrends.issueChange)]" 
                   :style="{ width: getTrendWidth(-trendData.healthTrends.issueChange) }"></div>
            </div>
          </div>
          <div class="trend-item">
            <div class="trend-info">
              <span class="trend-label">整体健康评分</span>
              <div class="trend-value-container">
                <span class="trend-value">{{ trendData.healthTrends.overallScore || 0 }}/100</span>
                <span :class="['trend-change', getChangeClass(trendData.healthTrends.scoreChange)]">
                  {{ formatChange(trendData.healthTrends.scoreChange) }}
                </span>
              </div>
            </div>
            <div class="trend-bar-container">
              <div :class="['trend-bar', getTrendClass(trendData.healthTrends.scoreChange)]" 
                   :style="{ width: getTrendWidth(trendData.healthTrends.scoreChange) }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 日期范围 -->
      <div class="date-range-card">
        <div class="card-header">
          <div class="header-icon">📅</div>
          <h3>数据范围</h3>
        </div>
        <div class="date-range-content">
          <div class="date-item">
            <span class="date-label">开始日期</span>
            <span class="date-value">{{ formatDate(trendData.dateRange?.start) }}</span>
          </div>
          <div class="date-divider"></div>
          <div class="date-item">
            <span class="date-label">结束日期</span>
            <span class="date-value">{{ formatDate(trendData.dateRange?.end) }}</span>
          </div>
          <div class="date-note">
            <p>数据基于过去30天的记录分析</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  trendData: {
    type: Object,
    required: true,
    default: () => ({
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
  }
})

// 确保数据结构完整
const safeTrendData = computed(() => {
  return {
    exerciseTrends: {
      weeklyMinutes: props.trendData?.exerciseTrends?.weeklyMinutes || 0,
      weeklyChange: props.trendData?.exerciseTrends?.weeklyChange || 0,
      intensityAvg: props.trendData?.exerciseTrends?.intensityAvg || 'medium',
      intensityChange: props.trendData?.exerciseTrends?.intensityChange || 0,
      frequency: props.trendData?.exerciseTrends?.frequency || 0,
      frequencyChange: props.trendData?.exerciseTrends?.frequencyChange || 0
    },
    moodTrends: {
      positiveRate: props.trendData?.moodTrends?.positiveRate || 0,
      positiveChange: props.trendData?.moodTrends?.positiveChange || 0,
      stability: props.trendData?.moodTrends?.stability || 'medium',
      stabilityChange: props.trendData?.moodTrends?.stabilityChange || 0,
      previousMood: props.trendData?.moodTrends?.previousMood || 'calm',
      currentMood: props.trendData?.moodTrends?.currentMood || 'calm'
    },
    healthTrends: {
      sleepQuality: props.trendData?.healthTrends?.sleepQuality || 'medium',
      sleepChange: props.trendData?.healthTrends?.sleepChange || 0,
      issueFrequency: props.trendData?.healthTrends?.issueFrequency || 0,
      issueChange: props.trendData?.healthTrends?.issueChange || 0,
      overallScore: props.trendData?.healthTrends?.overallScore || 0,
      scoreChange: props.trendData?.healthTrends?.scoreChange || 0
    },
    dateRange: {
      start: props.trendData?.dateRange?.start || new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      end: props.trendData?.dateRange?.end || new Date()
    }
  }
})

const getMoodIcon = (type) => {
  if (!type) return '😐'
  const icons = {
    happy: '😊',
    calm: '😌',
    sad: '😢',
    angry: '😠',
    anxious: '😰',
    tired: '😫',
    excited: '🤩',
    bored: '😑'
  }
  return icons[type] || '😐'
}

const getHealthIcon = (type) => {
  if (!type) return '🏥'
  const icons = {
    sleep_bad: '😴',
    appetite_bad: '🍽️',
    fatigue: '😫',
    headache: '🤕',
    muscle_sore: '💪',
    cold: '🤒'
  }
  return icons[type] || '🏥'
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

const formatDate = (date) => {
  if (!date) return '未知日期'
  if (typeof date === 'string') {
    date = new Date(date)
  }
  if (!(date instanceof Date) || isNaN(date)) {
    return '未知日期'
  }
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

const getChangeClass = (change) => {
  if (!change || isNaN(change)) return 'neutral'
  return change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral'
}

const formatChange = (change) => {
  if (!change || isNaN(change)) return '无变化'
  const prefix = change > 0 ? '+' : ''
  return `${prefix}${change}%`
}

const getTrendClass = (change) => {
  if (!change || isNaN(change)) return 'neutral'
  return change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral'
}

const getTrendWidth = (change) => {
  if (!change || isNaN(change)) return '50%'
  const absChange = Math.abs(change)
  const width = Math.min(100, 50 + absChange / 2)
  return `${width}%`
}

const formatTrend = (value) => {
  if (!value) return '中等'
  if (typeof value === 'number') {
    return value.toFixed(1)
  }
  const labels = {
    low: '低',
    medium: '中等',
    high: '高'
  }
  return labels[value] || '中等'
}
</script>

<style scoped>
.trend-analysis {
  padding: 1rem;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.trend-header {
  text-align: center;
  margin-bottom: 2rem;
}

.trend-header h2 {
  font-size: 1.75rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  color: #64748b;
  font-size: 1.1rem;
}

.trend-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.trend-card, .date-range-card {
  background: white;
  border-radius: 1.25rem;
  padding: 1.75rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
  transition: all 0.3s ease;
  border: 1px solid rgba(226, 232, 240, 0.8);
  animation: cardFadeIn 0.5s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

.trend-card:nth-child(1) { animation-delay: 0.1s; }
.trend-card:nth-child(2) { animation-delay: 0.2s; }
.trend-card:nth-child(3) { animation-delay: 0.3s; }
.date-range-card { animation-delay: 0.4s; }

@keyframes cardFadeIn {
  to { opacity: 1; transform: translateY(0); }
}

.trend-card:hover, .date-range-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.01);
  transform: translateY(-5px);
}

.card-header {
  margin-bottom: 1.75rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  font-size: 1.5rem;
  background: #f0f9ff;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.75rem;
}

.card-header h3 {
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.trend-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.trend-item {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.trend-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.trend-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.trend-value-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.trend-value {
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.trend-change {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
}

.trend-change.positive {
  color: #10b981;
  background: #ecfdf5;
}

.trend-change.negative {
  color: #ef4444;
  background: #fef2f2;
}

.trend-change.neutral {
  color: #6b7280;
  background: #f3f4f6;
}

.trend-bar-container {
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.trend-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;
  position: absolute;
  left: 0;
}

.trend-bar.positive {
  background: linear-gradient(to right, #34d399, #10b981);
}

.trend-bar.negative {
  background: linear-gradient(to right, #f87171, #ef4444);
}

.trend-bar.neutral {
  background: linear-gradient(to right, #9ca3af, #6b7280);
  width: 50%;
}

.mood-change {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  padding: 0.5rem 0.75rem;
  border-radius: 0.75rem;
}

.mood-icon {
  font-size: 1.25rem;
}

.arrow {
  color: #64748b;
  font-weight: 600;
}

/* 日期范围卡片样式 */
.date-range-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.date-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  padding: 1rem;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.date-item:hover {
  background: #f0f9ff;
  transform: translateY(-2px);
}

.date-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.date-value {
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
}

.date-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 0.5rem 0;
}

.date-note {
  text-align: center;
  color: #64748b;
  font-size: 0.875rem;
  font-style: italic;
  margin-top: 0.5rem;
}

@media (max-width: 1024px) {
  .trend-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .trend-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .trend-value-container {
    width: 100%;
    justify-content: space-between;
  }
  
  .trend-card, .date-range-card {
    padding: 1.25rem;
  }
  
  .card-header h3 {
    font-size: 1.1rem;
  }
}
</style> 