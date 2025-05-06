<template>
  <div class="user-report-detail-page">
    <div class="page-header">
      <h2>用户健康趋势</h2>
      <p class="subtitle">查看用户 {{ userId }} 的健康趋势数据</p>
      <button @click="goBack" class="back-button">返回用户列表</button>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载趋势数据中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3>加载趋势数据失败</h3>
      <p>{{ errorMessage }}</p>
      <button @click="fetchUserTrends" class="retry-button">
        重试加载
      </button>
    </div>

    <div v-else-if="trendsData" class="trends-content">
      
      <div class="trend-data-container">
        <h4>体重趋势 (kg)</h4>
        <ul v-if="formattedWeightData.datasets[0].data.length > 0" class="data-list">
          <li v-for="(label, index) in formattedWeightData.labels" :key="'weight-' + index">
            <span class="date">{{ formatDate(label) }}:</span> 
            <span class="value">{{ formattedWeightData.datasets[0].data[index] }} kg</span>
          </li>
        </ul>
        <p v-else class="no-data-small">无体重数据</p>
      </div>
      
      <div class="trend-data-container">
        <h4>运动时长趋势 (分钟)</h4>
        <ul v-if="formattedExerciseData.datasets[0].data.length > 0" class="data-list">
           <li v-for="(label, index) in formattedExerciseData.labels" :key="'exercise-' + index">
            <span class="date">{{ formatDate(label) }}:</span> 
            <span class="value">{{ formattedExerciseData.datasets[0].data[index] }} 分钟</span>
          </li>
        </ul>
        <p v-else class="no-data-small">无运动时长数据</p>
      </div>

      <div class="trend-data-container">
        <h4>心情分布 (最近30天)</h4>
        <div v-if="Object.keys(moodStatistics).length > 0" class="statistics-list">
          <div v-for="(count, mood) in moodStatistics" :key="mood" class="statistic-item">
            <span class="mood-label">{{ mood }}:</span> 
            <span class="mood-count">{{ count }} 次</span>
          </div>
        </div>
        <p v-else class="no-data-small">无心情数据</p>
      </div>

      <div class="admin-recommendations">
        <h4>管理员建议</h4>
        <textarea v-model="adminRecommendation" placeholder="为用户添加个性化建议..."></textarea>
        <button @click="submitRecommendation" :disabled="submittingRecommendation">
          {{ submittingRecommendation ? '提交中...' : '提交建议' }}
        </button>
        <p v-if="recommendationSuccess" class="success-message">建议提交成功！</p>
        <p v-if="recommendationError" class="error-message">{{ recommendationError }}</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getUserTrendsForAdmin, submitAdminRecommendation } from '../../api/admin';

const props = defineProps({
  userId: {
    type: [String, Number],
    required: true
  }
});

const router = useRouter();
const trendsData = ref(null);
const loading = ref(true);
const error = ref(null);
const errorCode = ref(null);
const adminRecommendation = ref('');
const submittingRecommendation = ref(false);
const recommendationSuccess = ref(false);
const recommendationError = ref(null);

const errorMessage = computed(() => {
  return error.value?.message || '加载趋势数据时发生未知错误。';
});

const fetchUserTrends = async () => {
  loading.value = true;
  error.value = null;
  errorCode.value = null;
  trendsData.value = null;
  try {
    const data = await getUserTrendsForAdmin(props.userId);
    trendsData.value = data;
  } catch (err) {
    console.error(`获取用户 ${props.userId} 的趋势数据失败:`, err);
    error.value = err;
    errorCode.value = err.response?.status;
  } finally {
    loading.value = false;
  }
};

const formatLineChartData = (rawData, label, color) => {
  const defaultDataset = { 
    label: label || '', 
    data: [], 
    borderColor: color || '#3b82f6', 
    backgroundColor: color ? `${color}33` : '#3b82f633', 
    tension: 0.1, 
    fill: false 
  };
  if (!rawData || !Array.isArray(rawData) || rawData.length === 0) {
      return { labels: [], datasets: [defaultDataset] }; 
  }
  try {
      const validData = rawData.filter(item => item && item.date !== undefined && item.value !== undefined);
      validData.sort((a, b) => new Date(a.date) - new Date(b.date));
      const labels = validData.map(item => item.date);
      const data = validData.map(item => item.value);
      return {
        labels,
        datasets: [{ ...defaultDataset, data }]
      };
  } catch (e) {
      console.error("Error formatting chart data:", e, rawData);
      return { labels: [], datasets: [defaultDataset] }; 
  }
};

const formattedWeightData = computed(() => {
  if (!trendsData.value) {
      return { labels: [], datasets: [{ label: '体重 (kg)', data: [] }] };
  }
  return formatLineChartData(trendsData.value.weight_kg, '体重 (kg)', '#3b82f6');
});

const formattedExerciseData = computed(() => {
  if (!trendsData.value) {
      return { labels: [], datasets: [{ label: '运动时长 (分钟)', data: [] }] };
  }
  return formatLineChartData(trendsData.value.exercise_duration, '运动时长 (分钟)', '#10b981');
});

const moodStatistics = computed(() => {
  if (!trendsData.value || !trendsData.value.mood || trendsData.value.mood.length === 0) {
    return {};
  }
  
  return trendsData.value.mood.reduce((stats, moodEntry) => {
    const moodValue = moodEntry.value;
    if (moodValue) {
      stats[moodValue] = (stats[moodValue] || 0) + 1;
    }
    return stats;
  }, {});
});

const submitRecommendation = async () => {
  submittingRecommendation.value = true;
  recommendationSuccess.value = false;
  recommendationError.value = null;
  try {
    await submitAdminRecommendation(props.userId, adminRecommendation.value);
    recommendationSuccess.value = true;
  } catch (err) {
    console.error(`为用户 ${props.userId} 提交建议失败:`, err);
    recommendationError.value = err.response?.data?.message || err.message || '提交建议时发生未知错误。';
  } finally {
    submittingRecommendation.value = false;
  }
};

const goBack = () => {
  router.push({ name: 'AdminUserReports' });
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' }; 
    return new Date(dateString).toLocaleDateString('zh-CN', options);
  } catch (e) {
    console.error('日期格式化错误:', e);
    return dateString;
  }
};

onMounted(() => {
  fetchUserTrends();
});
</script>

<style scoped>
.user-report-detail-page {
  padding: 1.5rem;
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.page-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
  flex-grow: 1;
  margin-left: 1rem;
}

.back-button {
  background: #64748b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.back-button:hover {
  background: #475569;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  text-align: center;
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin-top: 1rem;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #ef4444;
}

.error-container h3 {
  color: #ef4444;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.error-container p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.retry-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.retry-button:hover {
  background: #2563eb;
}

.trends-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-top: 1rem;
}

.trend-data-container {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
  display: flex; 
  flex-direction: column;
}

.trend-data-container h4 {
  font-size: 1.1rem;
  color: #334155;
  margin-top: 0;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.data-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 300px;
  overflow-y: auto;
  font-size: 0.9rem;
}

.data-list li {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem 0.2rem;
  border-bottom: 1px solid #f1f5f9;
}

.data-list li:last-child {
  border-bottom: none;
}

.data-list .date {
  color: #64748b;
  margin-right: 1rem;
}

.data-list .value {
  color: #1e293b;
  font-weight: 500;
}

.no-data-small {
  font-size: 0.9rem;
  color: #64748b;
  text-align: center;
  padding: 1rem 0;
}

.statistics-list {
  padding: 0.5rem 0.2rem;
  font-size: 0.9rem;
}

.statistic-item {
  display: flex;
  justify-content: space-between;
  padding: 0.4rem 0;
  border-bottom: 1px solid #f1f5f9;
}

.statistic-item:last-child {
  border-bottom: none;
}

.mood-label {
  color: #475569;
  text-transform: capitalize;
}

.mood-count {
  color: #1e293b;
  font-weight: 500;
}

.admin-recommendations {
  grid-column: 1 / -1;
  margin-top: 1.5rem;
  padding: 1.5rem;
  border-top: none;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
}

.admin-recommendations h4 {
  font-size: 1.1rem;
  color: #334155;
  margin-bottom: 1rem;
}

.admin-recommendations textarea {
  width: 100%;
  min-height: 100px;
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  resize: vertical;
}

.admin-recommendations button {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.admin-recommendations button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.admin-recommendations button:hover:not(:disabled) {
  background: #059669;
}

.success-message {
  color: #10b981;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.error-message {
  color: #ef4444;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

@media (min-width: 768px) {
  .trends-content {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .trends-content {
    grid-template-columns: repeat(3, 1fr);
  }
  .admin-recommendations {
      grid-column: 1 / -1;
  }
}
</style> 