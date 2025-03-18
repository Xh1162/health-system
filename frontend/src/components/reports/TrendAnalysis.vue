<template>
  <div class="trend-analysis">
    <div class="trend-header">
      <h2>健康趋势</h2>
      <p class="subtitle">您的关键健康数据变化</p>
    </div>

    <div class="trend-grid">
      <!-- 运动趋势 -->
      <div class="trend-card">
        <div class="card-header">
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
          
          <div class="trend-insight simple">
            <p class="insight-text">{{ getSimpleExerciseInsight() }}</p>
          </div>
        </div>
      </div>

      <!-- 心情趋势 -->
      <div class="trend-card">
        <div class="card-header">
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
              <span class="trend-label">主要情绪变化</span>
              <div class="trend-value-container">
                <span class="trend-value mood-change">
                  <span class="prev-mood">{{ getMoodLabel(trendData.moodTrends.previousMood) }}</span>
                  <span class="arrow">→</span>
                  <span class="curr-mood">{{ getMoodLabel(trendData.moodTrends.currentMood) }}</span>
                </span>
              </div>
            </div>
          </div>
          
          <div class="trend-insight simple">
            <p class="insight-text">{{ getSimpleMoodInsight() }}</p>
          </div>
        </div>
      </div>

      <!-- 健康趋势 -->
      <div class="trend-card">
        <div class="card-header">
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
          
          <div class="trend-insight simple">
            <p class="insight-text">{{ getSimpleHealthInsight() }}</p>
          </div>
        </div>
      </div>

      <!-- 数据范围 -->
      <div class="date-range-card">
        <div class="card-header">
          <h3>数据范围</h3>
        </div>
        <div class="date-range-content">
          <div class="date-range">
            <span>{{ formatDate(trendData.dateRange?.start) }} - {{ formatDate(trendData.dateRange?.end) }}</span>
          </div>
          <div class="summary-box">
            <div class="summary-content">
              <button class="action-button primary">查看完整健康报告</button>
            </div>
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

// 获取简化的运动趋势见解
const getSimpleExerciseInsight = () => {
  const weeklyChange = props.trendData?.exerciseTrends?.weeklyChange || 0
  const frequencyChange = props.trendData?.exerciseTrends?.frequencyChange || 0
  
  if (weeklyChange > 10 && frequencyChange > 5) {
    return '您的运动量持续增加，继续保持这个良好趋势。'
  } else if (weeklyChange < -10) {
    return '建议尝试增加每周运动时间，保持规律运动习惯。'
  }
  
  return '您的运动数据相对稳定，坚持规律运动有助于健康。'
}

// 获取简化的心情趋势见解
const getSimpleMoodInsight = () => {
  const positiveChange = props.trendData?.moodTrends?.positiveChange || 0
  const currentMood = props.trendData?.moodTrends?.currentMood || 'calm'
  
  if (positiveChange > 10) {
    return '您的积极情绪比例在提升，这对健康非常有益。'
  } else if (positiveChange < -10) {
    return '建议尝试一些能提升心情的活动，如户外运动或社交活动。'
  } else if (currentMood === 'anxious' || currentMood === 'tired') {
    return '近期可能有些焦虑或疲劳，建议适当休息和放松。'
  }
  
  return '您的情绪状态稳定，这是健康的积极信号。'
}

// 获取简化的健康趋势见解
const getSimpleHealthInsight = () => {
  const sleepChange = props.trendData?.healthTrends?.sleepChange || 0
  const scoreChange = props.trendData?.healthTrends?.scoreChange || 0
  
  if (scoreChange > 5) {
    return '您的健康评分有提升，继续保持良好的健康习惯。'
  } else if (scoreChange < -5) {
    return '留意您的健康状况变化，合理调整生活作息。'
  } else if (sleepChange < -10) {
    return '您的睡眠质量有所下降，建议调整睡眠习惯。'
  }
  
  return '整体健康趋势稳定，维持健康生活方式是关键。'
}
</script>

<style scoped>
.trend-analysis {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}

.trend-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.trend-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.875rem;
}

.trend-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.trend-card, .date-range-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.25rem;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.trend-card:hover, .date-range-card:hover {
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

.trend-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.trend-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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
  gap: 0.5rem;
}

.trend-value {
  color: #1e293b;
  font-size: 0.875rem;
  font-weight: 600;
}

.trend-change {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.15rem 0.35rem;
  border-radius: 0.25rem;
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
  height: 6px;
  background: #f1f5f9;
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}

.trend-bar {
  height: 100%;
  border-radius: 3px;
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
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.prev-mood, .curr-mood {
  font-size: 0.75rem;
  font-weight: 500;
}

.arrow {
  color: #64748b;
  font-weight: 600;
}

.date-range-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.date-range {
  text-align: center;
  padding: 0.5rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #1e293b;
  font-weight: 500;
}

.trend-insight.simple {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
}

.insight-text {
  color: #334155;
  font-size: 0.8125rem;
  line-height: 1.4;
  margin: 0;
}

.summary-box {
  margin-top: 1rem;
}

.summary-content {
  display: flex;
  justify-content: center;
}

.action-button {
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  font-size: 0.875rem;
}

.action-button.primary {
  background: #3b82f6;
  color: white;
}

.action-button.primary:hover {
  background: #2563eb;
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
    gap: 0.25rem;
  }
  
  .trend-value-container {
    width: 100%;
    justify-content: space-between;
  }
  
  .trend-card, .date-range-card {
    padding: 1rem;
  }
  
  .card-header h3 {
    font-size: 1rem;
  }
}
</style> 