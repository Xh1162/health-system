<template>
  <div class="health-summary">
    <div class="summary-header">
      <h2>健康数据总览</h2>
      <p class="subtitle">您的健康记录概要</p>
    </div>

    <div class="summary-grid">
      <!-- 记录统计 -->
      <div class="summary-card">
        <div class="card-header">
          <h3>记录统计</h3>
        </div>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-icon">📝</span>
            <span class="stat-value">{{ summaryData.totalRecords }}</span>
            <span class="stat-label">总记录</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">🍽️</span>
            <span class="stat-value">{{ summaryData.foodRecords }}</span>
            <span class="stat-label">饮食记录</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">🏃</span>
            <span class="stat-value">{{ summaryData.exerciseRecords }}</span>
            <span class="stat-label">运动记录</span>
          </div>
          <div class="stat-item">
            <span class="stat-icon">😊</span>
            <span class="stat-value">{{ summaryData.moodRecords }}</span>
            <span class="stat-label">心情记录</span>
          </div>
        </div>
      </div>

      <!-- 运动概览 -->
      <div class="summary-card">
        <div class="card-header">
          <h3>运动概览</h3>
        </div>
        <div class="exercise-summary">
          <div class="total-minutes">
            <span class="big-number">{{ summaryData.exerciseMinutes }}</span>
            <span class="unit">分钟</span>
          </div>
          <p class="description">本周累计运动时长</p>
        </div>
      </div>

      <!-- 睡眠质量 -->
      <div class="summary-card">
        <div class="card-header">
          <h3>睡眠质量</h3>
        </div>
        <div class="sleep-quality">
          <div class="quality-item">
            <span class="quality-icon">😴</span>
            <span class="quality-value">{{ summaryData.sleepQuality.good }}</span>
            <span class="quality-label">睡眠充足</span>
          </div>
          <div class="quality-item">
            <span class="quality-icon">😫</span>
            <span class="quality-value">{{ summaryData.sleepQuality.bad }}</span>
            <span class="quality-label">睡眠不足</span>
          </div>
        </div>
      </div>

      <!-- 最近心情 -->
      <div class="summary-card">
        <div class="card-header">
          <h3>最近心情</h3>
        </div>
        <div class="mood-list">
          <div v-for="mood in summaryData.recentMoods" :key="mood.date" class="mood-item">
            <span class="mood-icon">{{ getMoodIcon(mood.type) }}</span>
            <span class="mood-date">{{ formatDate(mood.date) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  summaryData: {
    type: Object,
    required: true
  }
})

const getMoodIcon = (type) => {
  const moodIcons = {
    happy: '😊',
    calm: '😌',
    sad: '😢',
    angry: '😠',
    anxious: '😰',
    tired: '😫',
    excited: '🤩',
    bored: '😑'
  }
  return moodIcons[type] || '😐'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}
</script>

<style scoped>
.health-summary {
  padding: 1rem;
}

.summary-header {
  text-align: center;
  margin-bottom: 2rem;
}

.summary-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #64748b;
  font-size: 1rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.summary-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
  margin-bottom: 1rem;
}

.card-header h3 {
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
}

.exercise-summary {
  text-align: center;
}

.total-minutes {
  margin-bottom: 0.5rem;
}

.big-number {
  font-size: 2rem;
  font-weight: 700;
  color: #3b82f6;
}

.unit {
  font-size: 1rem;
  color: #64748b;
  margin-left: 0.25rem;
}

.description {
  color: #64748b;
  font-size: 0.875rem;
}

.sleep-quality {
  display: flex;
  justify-content: space-around;
}

.quality-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.quality-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.quality-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
}

.quality-label {
  font-size: 0.875rem;
  color: #64748b;
}

.mood-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.mood-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mood-icon {
  font-size: 1.25rem;
}

.mood-date {
  color: #64748b;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style> 