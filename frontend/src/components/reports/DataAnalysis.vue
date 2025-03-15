<template>
  <div class="data-analysis">
    <div class="analysis-header">
      <h2>数据分析</h2>
      <p class="subtitle">深入了解您的健康数据</p>
    </div>

    <div class="analysis-grid">
      <!-- 运动分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <div class="header-icon">🏃</div>
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
        </div>
      </div>

      <!-- 心情分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <div class="header-icon">😊</div>
          <h3>心情分析</h3>
        </div>
        <div class="mood-stats">
          <div class="mood-distribution">
            <h4>心情分布</h4>
            <div class="mood-grid">
              <div v-for="(value, mood) in analysisData.moodStats.distribution" 
                   :key="mood" 
                   class="mood-item">
                <span class="mood-icon">{{ getMoodIcon(mood) }}</span>
                <span class="mood-label">{{ getMoodLabel(mood) }}</span>
                <span class="mood-value">{{ value || 0 }}%</span>
              </div>
            </div>
          </div>
          <div class="most-frequent">
            <h4>最常见心情</h4>
            <div class="frequent-mood">
              <span class="mood-icon large">{{ getMoodIcon(analysisData.moodStats.mostFrequent) }}</span>
              <span class="mood-label">{{ getMoodLabel(analysisData.moodStats.mostFrequent) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 健康状况分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <div class="header-icon">💪</div>
          <h3>健康状况分析</h3>
        </div>
        <div class="health-stats">
          <div class="common-issues">
            <h4>常见问题</h4>
            <div v-if="analysisData.healthStats.commonIssues && analysisData.healthStats.commonIssues.length > 0" class="issues-list">
              <div v-for="issue in analysisData.healthStats.commonIssues" 
                   :key="issue.type" 
                   class="issue-item">
                <span class="issue-icon">{{ getHealthIcon(issue.type) }}</span>
                <span class="issue-label">{{ getHealthLabel(issue.type) }}</span>
                <span class="issue-count">{{ issue.count }}次</span>
              </div>
            </div>
            <div v-else class="empty-issues">
              <p>暂无健康问题记录</p>
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

const getPercentage = (value) => {
  if (typeof value !== 'number' || isNaN(value)) return 0
  return Math.min(100, Math.max(0, value))
}
</script>

<style scoped>
.data-analysis {
  padding: 1rem;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.analysis-header {
  text-align: center;
  margin-bottom: 2rem;
}

.analysis-header h2 {
  font-size: 1.75rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  color: #64748b;
  font-size: 1.1rem;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.analysis-card {
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

.analysis-card:nth-child(1) { animation-delay: 0.1s; }
.analysis-card:nth-child(2) { animation-delay: 0.2s; }
.analysis-card:nth-child(3) { animation-delay: 0.3s; }

@keyframes cardFadeIn {
  to { opacity: 1; transform: translateY(0); }
}

.analysis-card:hover {
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

/* 运动分析样式 */
.exercise-stats {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: #f8fafc;
  padding: 1rem;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: #f0f9ff;
  transform: translateY(-2px);
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.stat-value {
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.stat-value.highlight {
  color: #3b82f6;
  font-size: 1.5rem;
}

.intensity-distribution h4 {
  color: #1e293b;
  font-size: 1.1rem;
  margin-bottom: 1.25rem;
  font-weight: 600;
}

.distribution-bars {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.distribution-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.bar-label {
  width: 60px;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
}

.bar-container {
  flex: 1;
  height: 10px;
  background: #f1f5f9;
  border-radius: 5px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 5px;
  transition: width 1s ease;
}

.bar.light {
  background: linear-gradient(to right, #60a5fa, #3b82f6);
}

.bar.medium {
  background: linear-gradient(to right, #34d399, #10b981);
}

.bar.high {
  background: linear-gradient(to right, #f97316, #ea580c);
}

.bar-value {
  width: 40px;
  color: #64748b;
  font-size: 0.875rem;
  text-align: right;
  font-weight: 600;
}

/* 心情分析样式 */
.mood-stats {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.mood-distribution h4,
.most-frequent h4 {
  color: #1e293b;
  font-size: 1.1rem;
  margin-bottom: 1.25rem;
  font-weight: 600;
}

.mood-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.mood-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.mood-item:hover {
  background: #f0f9ff;
  transform: translateY(-2px);
}

.mood-icon {
  font-size: 1.5rem;
}

.mood-icon.large {
  font-size: 3rem;
}

.mood-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
  flex: 1;
}

.mood-value {
  color: #1e293b;
  font-weight: 600;
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  min-width: 2.5rem;
  text-align: center;
}

.frequent-mood {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: #f8fafc;
  padding: 1.25rem;
  border-radius: 0.75rem;
  justify-content: center;
}

/* 健康状况分析样式 */
.health-stats {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.common-issues h4 {
  color: #1e293b;
  font-size: 1.1rem;
  margin-bottom: 1.25rem;
  font-weight: 600;
}

.issues-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.issue-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  transition: all 0.3s ease;
}

.issue-item:hover {
  background: #f0f9ff;
  transform: translateY(-2px);
}

.issue-icon {
  font-size: 1.5rem;
}

.issue-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
  flex: 1;
}

.issue-count {
  color: #1e293b;
  font-weight: 600;
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  min-width: 2.5rem;
  text-align: center;
}

.empty-issues {
  padding: 1.5rem;
  text-align: center;
  color: #64748b;
  background: #f8fafc;
  border-radius: 0.75rem;
  font-size: 0.875rem;
}

@media (max-width: 1024px) {
  .analysis-grid {
    grid-template-columns: 1fr;
  }
  
  .mood-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stat-row {
    flex-direction: column;
  }
  
  .analysis-card {
    padding: 1.25rem;
  }
  
  .card-header h3 {
    font-size: 1.1rem;
  }
}
</style> 