<template>
  <div class="trend-report">
    <div class="report-section">
      <div class="section-header">
        <h2>健康趋势分析</h2>
        <div class="time-filter">
          <button class="filter-btn active">周</button>
          <button class="filter-btn">月</button>
          <button class="filter-btn">年</button>
        </div>
      </div>

      <div class="trend-cards">
        <div class="trend-card">
          <div class="trend-header">
            <h3>健康评分趋势</h3>
            <span class="trend-indicator positive">↑ 5%</span>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">健康评分趋势图表</div>
          </div>
          <div class="trend-insights">
            <p>您的健康评分呈上升趋势，继续保持良好的生活习惯！</p>
          </div>
        </div>

        <div class="trend-card">
          <div class="trend-header">
            <h3>运动时长趋势</h3>
            <span class="trend-indicator positive">↑ 12%</span>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">运动时长趋势图表</div>
          </div>
          <div class="trend-insights">
            <p>您的运动时间逐渐增加，对健康大有帮助！</p>
          </div>
        </div>

        <div class="trend-card">
          <div class="trend-header">
            <h3>心情指数趋势</h3>
            <span class="trend-indicator neutral">→ 0%</span>
          </div>
          <div class="chart-container">
            <div class="chart-placeholder">心情指数趋势图表</div>
          </div>
          <div class="trend-insights">
            <p>您的心情保持稳定，建议多参与户外活动提升心情。</p>
          </div>
        </div>
      </div>
    </div>

    <div class="report-section">
      <div class="section-header">
        <h2>长期健康预测</h2>
      </div>
      <div class="prediction-content">
        <div class="prediction-card">
          <h3>健康风险评估</h3>
          <div class="risk-indicators">
            <div class="risk-item low">
              <span class="risk-label">心血管风险</span>
              <span class="risk-value">低</span>
            </div>
            <div class="risk-item medium">
              <span class="risk-label">亚健康风险</span>
              <span class="risk-value">中</span>
            </div>
            <div class="risk-item low">
              <span class="risk-label">营养风险</span>
              <span class="risk-value">低</span>
            </div>
          </div>
        </div>

        <div class="prediction-card">
          <h3>健康建议</h3>
          <ul class="health-suggestions">
            <li>保持规律运动习惯，每周至少运动3-4次</li>
            <li>注意作息时间，保证充足睡眠</li>
            <li>均衡饮食，增加蔬果摄入</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  trendData: {
    type: Object,
    default: () => ({})
  }
})
</script>

<style scoped>
.trend-report {
  padding: 1rem;
}

.report-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.time-filter {
  display: flex;
  gap: 0.5rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: #f8fafc;
}

.filter-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.trend-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.trend-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.trend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.trend-header h3 {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1e293b;
  margin: 0;
}

.trend-indicator {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

.trend-indicator.positive {
  background: #dcfce7;
  color: #16a34a;
}

.trend-indicator.negative {
  background: #fee2e2;
  color: #dc2626;
}

.trend-indicator.neutral {
  background: #f1f5f9;
  color: #64748b;
}

.chart-container {
  margin: 1rem 0;
}

.chart-placeholder {
  height: 200px;
  background: white;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.trend-insights {
  color: #64748b;
  font-size: 0.9rem;
}

.prediction-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.prediction-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
}

.prediction-card h3 {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.risk-indicators {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.risk-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.risk-item.low {
  background: #dcfce7;
}

.risk-item.medium {
  background: #fef3c7;
}

.risk-item.high {
  background: #fee2e2;
}

.risk-label {
  color: #1e293b;
  font-weight: 500;
}

.health-suggestions {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.health-suggestions li {
  padding: 0.75rem;
  background: white;
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
  color: #1e293b;
}

.health-suggestions li:last-child {
  margin-bottom: 0;
}

@media (max-width: 1024px) {
  .trend-cards,
  .prediction-content {
    grid-template-columns: 1fr;
  }
}
</style> 