<template>
  <div class="user-report-detail-page">
    <div class="page-header">
      <h2>用户健康报告详情</h2>
      <p class="subtitle">查看用户 {{ userId }} 的详细健康报告</p>
      <button @click="goBack" class="back-button">返回用户列表</button>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载报告中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3>加载报告失败</h3>
      <p>{{ error }}</p>
      <button class="retry-button" @click="fetchUserReport">重试</button>
    </div>

    <div v-else-if="reportData" class="report-content">
      <h3>{{ reportData.userName || '用户' }} 的健康报告</h3>
      <p class="report-meta">报告 ID: {{ reportData.report_id || 'N/A' }} | 生成时间: {{ formatDate(reportData.generated_at) }}</p>

      <div class="report-grid">
        <!-- Key Metrics Card -->
        <div class="report-card">
          <h4>关键指标</h4>
          <div class="metric-item">
            <span class="metric-label">BMI:</span>
            <span class="metric-value">{{ reportData.bmi || 'N/A' }}</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">目标热量:</span>
            <span class="metric-value">{{ reportData.calorie_goal || 'N/A' }} kcal</span>
          </div>
          <div class="metric-item">
            <span class="metric-label">平均摄入:</span>
            <span class="metric-value">{{ reportData.average_intake || 'N/A' }} kcal</span>
          </div>
        </div>

        <!-- Macros Card -->
        <div class="report-card">
          <h4>宏量营养素 (平均)</h4>
          <div v-if="reportData.macros" class="macros-details">
            <div class="metric-item">
              <span class="metric-label">蛋白质:</span>
              <span class="metric-value">{{ reportData.macros.protein || 'N/A' }} g</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">碳水化合物:</span>
              <span class="metric-value">{{ reportData.macros.carbs || 'N/A' }} g</span>
            </div>
            <div class="metric-item">
              <span class="metric-label">脂肪:</span>
              <span class="metric-value">{{ reportData.macros.fat || 'N/A' }} g</span>
            </div>
          </div>
          <p v-else class="no-data-small">无宏量营养素数据</p>
        </div>

        <!-- Key Findings Card -->
        <div class="report-card full-width">
          <h4>主要发现</h4>
          <ul v-if="reportData.key_findings && reportData.key_findings.length > 0" class="findings-list">
            <li v-for="(finding, index) in reportData.key_findings" :key="index">{{ finding }}</li>
          </ul>
          <p v-else class="no-data-small">无主要发现</p>
        </div>
      </div>

      <!-- 在这里添加更详细的报告展示逻辑 -->
      <!-- 例如：图表等 -->

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

    <div v-else class="no-data">
      <p>未能找到该用户的报告数据。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// 假设有一个获取特定用户报告的API函数
import { getUserReportById, submitAdminRecommendation } from '../../api/admin'; // 需要创建这些API函数

const props = defineProps({
  userId: {
    type: [String, Number],
    required: true
  }
});

const router = useRouter();
const reportData = ref(null);
const loading = ref(true);
const error = ref(null);
const adminRecommendation = ref('');
const submittingRecommendation = ref(false);
const recommendationSuccess = ref(false);
const recommendationError = ref(null);

const fetchUserReport = async () => {
  loading.value = true;
  error.value = null;
  try {
    // 调用API获取特定用户的报告数据
    // 注意：getUserReportById 需要在后端实现，并在 frontend/src/api/admin.js 中定义
    const data = await getUserReportById(props.userId);
    reportData.value = data;
    // 从获取的数据中加载已有的管理员建议到 textarea
    adminRecommendation.value = data.admin_recommendation || '';
  } catch (err) {
    console.error(`获取用户 ${props.userId} 的报告失败:`, err);
    error.value = err.response?.data?.message || err.message || '加载报告时发生未知错误。';
  } finally {
    loading.value = false;
  }
};

const submitRecommendation = async () => {
  submittingRecommendation.value = true;
  recommendationSuccess.value = false;
  recommendationError.value = null;
  try {
    // 调用API提交管理员建议
    // 注意：submitAdminRecommendation 需要在后端实现，并在 frontend/src/api/admin.js 中定义
    await submitAdminRecommendation(props.userId, adminRecommendation.value);
    recommendationSuccess.value = true;
    // 可选：提交成功后重新获取报告数据以更新显示
    // await fetchUserReport();
  } catch (err) {
    console.error(`为用户 ${props.userId} 提交建议失败:`, err);
    recommendationError.value = err.response?.data?.message || err.message || '提交建议时发生未知错误。';
  } finally {
    submittingRecommendation.value = false;
  }
};

const goBack = () => {
  // 返回到之前的用户列表页面
  router.push({ name: 'AdminUserReports' });
};

// 新增日期格式化函数
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('zh-CN', options);
  } catch (e) {
    console.error('日期格式化错误:', e);
    return dateString; // 返回原始字符串以防出错
  }
};

onMounted(() => {
  fetchUserReport();
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
  margin: 0; /* Removed default margin */
  flex-grow: 1; /* Allow subtitle to take space */
  margin-left: 1rem; /* Add some space from title */
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

/* Loading and Error Styles (similar to UserReportsPage) */
.loading-container, .error-container, .no-data {
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

.error-container h3, .no-data h3 {
  color: #ef4444;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.error-container p, .no-data p {
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

/* Report Content */
.report-content {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  margin-top: 1rem;
}

.report-content h3 {
  font-size: 1.4rem; /* Slightly larger title */
  color: #1e293b;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.75rem;
}

.report-meta {
  font-size: 0.85rem;
  color: #64748b;
  margin-bottom: 1.5rem;
}

.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.report-card {
  background-color: #ffffff;
  border-radius: 0.5rem;
  padding: 1.25rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #e2e8f0;
}

.report-card.full-width {
  grid-column: 1 / -1; /* Make findings card span full width */
}

.report-card h4 {
  font-size: 1.1rem;
  color: #334155;
  margin-top: 0;
  margin-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.5rem;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.6rem;
  font-size: 0.95rem;
}

.metric-label {
  color: #475569;
  font-weight: 500;
}

.metric-value {
  color: #1e293b;
  font-weight: 600;
}

.macros-details .metric-item:last-child,
.metric-item:last-child {
  margin-bottom: 0;
}

.findings-list {
  list-style: disc;
  padding-left: 1.5rem;
  margin: 0;
  color: #334155;
  font-size: 0.95rem;
}

.findings-list li {
  margin-bottom: 0.5rem;
}

.no-data-small {
  font-size: 0.9rem;
  color: #64748b;
  text-align: center;
  padding: 1rem 0;
}

/* Admin Recommendations Section */
.admin-recommendations {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
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
  resize: vertical; /* Allow vertical resizing */
}

.admin-recommendations button {
  background: #10b981; /* Green color for submit */
  color: white;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.admin-recommendations button:disabled {
  background-color: #9ca3af; /* Gray out when disabled */
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
</style> 