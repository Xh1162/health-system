<template>
  <div class="recommendations-section">
    <div class="section-header">
      <h2>健康建议</h2>
      <p class="subtitle">根据您的健康数据为您提供的个性化建议</p>
    </div>

    <!-- 健康建议卡片 -->
    <section class="health-tips">
      <h3>今日健康建议</h3>
      <div class="tips-grid">
        <div class="tip-card">
          <div class="tip-icon">💪</div>
          <h4>运动建议</h4>
          <p>根据您的运动记录，建议今天进行30分钟的中等强度运动，如快走或游泳。</p>
        </div>
        <div class="tip-card">
          <div class="tip-icon">🍽️</div>
          <h4>饮食建议</h4>
          <p>保持均衡饮食，多吃蔬菜水果，适量摄入蛋白质，避免过度加工食品。</p>
        </div>
        <div class="tip-card">
          <div class="tip-icon">😴</div>
          <h4>睡眠建议</h4>
          <p>保持规律的作息时间，确保7-8小时的优质睡眠，睡前避免使用电子设备。</p>
        </div>
        <div class="tip-card">
          <div class="tip-icon">🧘</div>
          <h4>心理建议</h4>
          <p>保持积极乐观的心态，适当进行冥想或深呼吸练习，缓解压力。</p>
        </div>
      </div>
    </section>

    <!-- 个性化推荐 -->
    <section class="personalized-recommendations">
      <h3>为您推荐</h3>
      <div class="recommendations-grid">
        <div class="recommendation-card">
          <div class="card-header">
            <span class="card-icon">🏃</span>
            <h4>运动计划</h4>
          </div>
          <div class="card-content">
            <ul class="recommendation-list">
              <li>周一：30分钟快走</li>
              <li>周三：45分钟游泳</li>
              <li>周五：60分钟瑜伽</li>
              <li>周日：40分钟骑行</li>
            </ul>
          </div>
        </div>
        <div class="recommendation-card">
          <div class="card-header">
            <span class="card-icon">🥗</span>
            <h4>营养食谱</h4>
          </div>
          <div class="card-content">
            <ul class="recommendation-list">
              <li>早餐：全麦面包 + 鸡蛋 + 牛奶</li>
              <li>午餐：糙米饭 + 鸡胸肉 + 西兰花</li>
              <li>晚餐：三文鱼 + 藜麦 + 沙拉</li>
              <li>加餐：水果 + 坚果</li>
            </ul>
          </div>
        </div>
        <div class="recommendation-card">
          <div class="card-header">
            <span class="card-icon">📚</span>
            <h4>健康知识</h4>
          </div>
          <div class="card-content">
            <ul class="recommendation-list">
              <li>了解运动强度与心率的关系</li>
              <li>学习营养均衡的饮食搭配</li>
              <li>掌握压力管理技巧</li>
              <li>了解睡眠质量的影响因素</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  recommendationsData: {
    type: Object,
    default: () => ({
      healthTips: [],
      personalizedRecommendations: []
    })
  }
})
</script>

<style scoped>
.recommendations-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #64748b;
  font-size: 1rem;
}

.health-tips h3,
.personalized-recommendations h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.tip-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.25rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
}

.tip-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.tip-card h4 {
  font-size: 1.1rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.tip-card p {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.5;
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.recommendation-card {
  background: #f8fafc;
  border-radius: 0.75rem;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.recommendation-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.05);
}

.card-header {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-icon {
  font-size: 1.5rem;
}

.card-header h4 {
  font-size: 1.1rem;
  margin: 0;
}

.card-content {
  padding: 1.25rem;
}

.recommendation-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.recommendation-list li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #e2e8f0;
  color: #334155;
  font-size: 0.9rem;
}

.recommendation-list li:last-child {
  border-bottom: none;
}

@media (max-width: 768px) {
  .tips-grid,
  .recommendations-grid {
    grid-template-columns: 1fr;
  }
}
</style> 