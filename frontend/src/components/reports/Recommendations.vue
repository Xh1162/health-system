<template>
  <div class="recommendations-section">
    <div class="section-header">
      <h2>健康建议</h2>
      <p class="subtitle">基于您的健康数据生成的个性化建议</p>
    </div>

    <!-- 健康总结 -->
    <section class="health-summary">
      <div class="summary-card">
        <div class="summary-content">
          <h3>健康状态总结</h3>
          <p>健康评分 <span class="highlight">{{ getHealthScore() }}分</span>，比上周{{ getScoreChangeText() }}。</p>
          <div class="progress-container">
            <div class="progress-bar" :style="{ width: `${getHealthScore()}%`, background: getHealthScoreColor() }"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- 健康建议卡片 -->
    <section class="health-tips">
      <h3>关键健康建议</h3>
      <div class="tips-grid">
        <div v-for="(tip, index) in recommendationsData.healthTips.slice(0, 3)" :key="index" class="tip-card">
          <h4>{{ getTipTitle(tip.type) }}</h4>
          <p>{{ tip.content }}</p>
        </div>
      </div>
    </section>

    <!-- 个性化推荐 -->
    <section class="personalized-recommendations">
      <h3>专属推荐</h3>
      <div class="recommendations-grid">
        <div v-for="(rec, index) in recommendationsData.personalizedRecommendations.slice(0, 2)" :key="index" class="recommendation-card">
          <div class="card-header" :class="`type-${rec.type}`">
            <h4>{{ rec.title }}</h4>
          </div>
          <div class="card-content">
            <ul class="recommendation-list">
              <li v-for="(item, itemIndex) in rec.items.slice(0, 3)" :key="itemIndex">
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  recommendationsData: {
    type: Object,
    default: () => ({
      healthTips: [],
      personalizedRecommendations: []
    })
  }
})

// 获取健康评分
const getHealthScore = () => {
  return 78
}

// 获取评分变化文本
const getScoreChangeText = () => {
  const change = 6
  return change > 0 ? `提升了${change}分` : change < 0 ? `下降了${Math.abs(change)}分` : '保持稳定'
}

// 获取健康评分颜色
const getHealthScoreColor = () => {
  const score = getHealthScore()
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#3b82f6'
  if (score >= 40) return '#f59e0b'
  return '#ef4444'
}

// 获取建议标题
const getTipTitle = (type) => {
  const titles = {
    exercise: '运动建议',
    diet: '饮食建议',
    sleep: '睡眠建议',
    mental: '心理建议'
  }
  return titles[type] || '健康建议'
}
</script>

<style scoped>
.recommendations-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
}

.section-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.875rem;
}

/* 健康总结 */
.health-summary {
  margin-bottom: 1.5rem;
}

.summary-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.25rem;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.summary-content h3 {
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.summary-content p {
  color: #475569;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0 0 0.75rem 0;
}

.highlight {
  color: #3b82f6;
  font-weight: 600;
}

.progress-container {
  width: 100%;
  height: 0.5rem;
  background: #e2e8f0;
  border-radius: 0.25rem;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 0.25rem;
  transition: width 1s ease;
}

/* 健康建议 */
.health-tips {
  margin-bottom: 1.5rem;
}

.health-tips h3 {
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.tip-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.25rem;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.tip-card h4 {
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
  margin: 0 0 0.75rem 0;
}

.tip-card p {
  color: #475569;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

/* 个性化推荐 */
.personalized-recommendations {
  margin-bottom: 1.5rem;
}

.personalized-recommendations h3 {
  color: #1e293b;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.recommendation-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.card-header {
  padding: 0.75rem 1.25rem;
  background: #f1f5f9;
}

.card-header h4 {
  color: #1e293b;
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.card-header.type-exercise {
  background: linear-gradient(to right, #bfdbfe, #93c5fd);
}

.card-header.type-diet {
  background: linear-gradient(to right, #bbf7d0, #86efac);
}

.card-header.type-knowledge {
  background: linear-gradient(to right, #fde68a, #fcd34d);
}

.card-header.type-lifestyle {
  background: linear-gradient(to right, #c4b5fd, #a78bfa);
}

.card-content {
  padding: 1.25rem;
}

.recommendation-list {
  padding-left: 1.25rem;
  margin: 0;
}

.recommendation-list li {
  color: #475569;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .recommendations-grid, .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style> 