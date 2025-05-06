<template>
  <div class="advice-management-page">
    <div class="page-header">
      <h2>咨询管理</h2>
      <p class="subtitle">查看并回复用户的建议请求</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载请求列表中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3>加载失败</h3>
      <p>{{ error }}</p>
      <button class="retry-button" @click="fetchRequests">重试</button>
    </div>

    <div v-else>
      <div class="filter-controls">
        <label for="status-filter">状态:</label>
        <select id="status-filter" v-model="currentStatusFilter" @change="fetchRequests(1)">
          <option value="pending">待处理</option>
          <option value="answered">已回复</option>
          <option value="all">所有</option>
        </select>
      </div>

      <div v-if="requests.length === 0" class="no-data">
        <p>没有找到符合条件的建议请求。</p>
      </div>

      <div v-else class="requests-list">
        <div v-for="request in requests" :key="request.id" class="request-card">
          <div class="request-header">
            <router-link 
              :to="`/admin/reports/user/${request.requester_id}`" 
              class="username-link"
              title="查看用户详细报告"
              v-if="request.requester_id" 
            >
              用户: {{ request.requester_username || '未知' }} (ID: {{ request.requester_id }})
            </router-link>
            <span v-else class="username">用户: {{ request.requester_username || '未知' }}</span>
            
            <span class="timestamp">{{ formatDate(request.requested_at) }}</span>
            <span :class="['status-badge', `status-${request.status}`]">{{ request.status }}</span>
          </div>
          <div class="request-body">
            <p v-if="request.request_text" class="request-text">{{ request.request_text }}</p>
            <p v-else class="request-text italic">用户未填写具体问题。</p>
          </div>
          
          <div v-if="request.status === 'answered'" class="response-section">
            <h4>管理员回复 ({{ request.responder_username || '未知' }}):</h4>
            <p class="response-text">{{ request.response_text }}</p>
            <span class="timestamp small">{{ formatDate(request.responded_at) }}</span>
          </div>
          
          <div v-else-if="request.status === 'pending'" class="action-section">
              <!-- 回复功能 -->
              <button @click="startReply(request)" class="button primary small">回复</button>
          </div>
        </div>
      </div>

      <!-- 分页控件 (如果需要) -->
      <div v-if="pagination && pagination.total_pages > 1" class="pagination-controls">
          <button @click="changePage(pagination.current_page - 1)" :disabled="!pagination.has_prev">上一页</button>
          <span>第 {{ pagination.current_page }} 页 / 共 {{ pagination.total_pages }} 页</span>
          <button @click="changePage(pagination.current_page + 1)" :disabled="!pagination.has_next">下一页</button>
      </div>

    </div>

    <!-- 回复模态框 -->
    <div v-if="showReplyModal" class="modal-overlay" @click.self="cancelReply">
        <div class="modal-content">
            <h3>回复 {{ replyingToRequest?.requester_username }} 的请求</h3>
            <p><strong>用户请求:</strong> {{ replyingToRequest?.request_text || '无' }}</p>
            <textarea 
                v-model="replyText" 
                rows="5" 
                placeholder="在此输入您的建议和回复..."
            ></textarea>
            <div v-if="replyError" class="error-message small">{{ replyError }}</div>
            <div class="modal-actions">
                <button class="button secondary" @click="cancelReply" :disabled="isReplying">取消</button>
                <button class="button primary" @click="submitReply" :disabled="isReplying || !replyText.trim()">
                    {{ isReplying ? '提交中...' : '确认回复' }}
                </button>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getAdminAdviceRequests, respondToAdviceRequest } from '../../api/admin'; // 从 admin.js 导入

const requests = ref([]);
const pagination = ref(null);
const loading = ref(true);
const error = ref(null);
const currentStatusFilter = ref('pending'); // 默认显示待处理

// 回复模态框状态
const showReplyModal = ref(false);
const replyingToRequest = ref(null); // 存储当前正在回复的请求对象
const replyText = ref('');
const isReplying = ref(false);
const replyError = ref(null);

// 获取数据函数
const fetchRequests = async (page = 1) => {
  loading.value = true;
  error.value = null;
  try {
    const response = await getAdminAdviceRequests(currentStatusFilter.value, page);
    requests.value = response.data;
    pagination.value = response.pagination;
  } catch (err) {
    console.error('获取建议请求失败:', err);
    error.value = err.message || '无法加载建议请求列表。';
    requests.value = []; // 清空列表以防显示旧数据
    pagination.value = null;
  } finally {
    loading.value = false;
  }
};

// 格式化日期 (与 ReportsPage 相同，可以考虑提取为公共 utils)
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('zh-CN', options);
  } catch (e) {
    return dateString;
  }
};

// 分页
const changePage = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.value.total_pages) {
        fetchRequests(newPage);
    }
};

// --- 回复逻辑 ---
const startReply = (request) => {
    replyingToRequest.value = request;
    replyText.value = ''; // 清空输入框
    replyError.value = null;
    showReplyModal.value = true;
};

const cancelReply = () => {
    showReplyModal.value = false;
    replyingToRequest.value = null;
    replyText.value = '';
    replyError.value = null;
};

const submitReply = async () => {
    if (!replyText.value.trim() || !replyingToRequest.value) return;
    
    isReplying.value = true;
    replyError.value = null;
    try {
        const updatedRequest = await respondToAdviceRequest(replyingToRequest.value.id, replyText.value);
        
        // 更新列表中的请求状态 (或重新获取列表)
        const index = requests.value.findIndex(req => req.id === updatedRequest.id);
        if (index !== -1) {
            requests.value[index] = updatedRequest;
        }
        // 如果当前筛选的是 pending，回复后该项应消失，可以考虑重新获取当前页
        if (currentStatusFilter.value === 'pending') {
             fetchRequests(pagination.value?.current_page || 1);
        }

        cancelReply(); // 关闭模态框并重置状态
        
    } catch (err) {
        console.error('回复请求失败:', err);
        replyError.value = err.message || '回复失败，请重试。';
    } finally {
        isReplying.value = false;
    }
};

// 组件挂载时获取数据
onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
/* 与其他管理页面类似的样式 */
.advice-management-page {
  padding: 1.5rem;
  background-color: #f8f9fa;
  min-height: calc(100vh - 60px); /* Adjust based on header height */
}

.page-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.page-header h2 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.95rem;
}

.filter-controls {
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.filter-controls label {
    font-weight: 500;
    color: #334155;
}

.filter-controls select {
    padding: 0.4rem 0.8rem;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 0.9rem;
}

/* Loading and Error Styles */
.loading-container, .error-container, .no-data {
  /* Styles similar to UserReportDetailPage */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  text-align: center;
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  margin-top: 1rem;
}
.spinner { /* ... spinner styles ... */ width: 2.5rem; height: 2.5rem; border: 4px solid #f3f3f3; border-top: 4px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 1rem; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.error-icon { /* ... error icon styles ... */ font-size: 2rem; margin-bottom: 1rem; color: #ef4444; }
.error-container h3, .no-data h3 { /* ... error/no-data heading styles ... */ color: #ef4444; font-size: 1.2rem; margin-bottom: 0.5rem; }
.error-container p, .no-data p { /* ... error/no-data text styles ... */ color: #64748b; margin-bottom: 1.5rem; }
.retry-button { /* ... retry button styles ... */ background: #3b82f6; color: white; border: none; padding: 0.5rem 1.5rem; border-radius: 0.375rem; font-size: 0.9rem; cursor: pointer; transition: background-color 0.2s; }
.retry-button:hover { background: #2563eb; }

/* Request List Styles */
.requests-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.request-card {
    background: white;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    padding: 1rem 1.5rem;
}

.request-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #f1f5f9;
    font-size: 0.9rem;
}

.request-header .username-link {
    font-weight: 600;
    color: #1e293b;
}

.request-header .username {
    font-weight: 600;
    color: #1e293b;
}

.request-header .timestamp {
    color: #64748b;
    font-size: 0.85rem;
}

.status-badge {
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 500;
    text-transform: capitalize;
}

.status-pending {
    background-color: #fef9c3; /* Yellow */
    color: #a16207;
}

.status-answered {
    background-color: #dcfce7; /* Green */
    color: #15803d;
}

/* Add other statuses if needed */

.request-body {
    margin-bottom: 1rem;
}

.request-text {
    color: #334155;
    line-height: 1.5;
    white-space: pre-wrap; /* Preserve whitespace/newlines */
}

.request-text.italic {
    font-style: italic;
    color: #64748b;
}

.response-section {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin-top: 1rem;
}

.response-section h4 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    color: #475569;
    font-weight: 500;
}

.response-text {
    color: #1e293b;
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
    white-space: pre-wrap;
}

.response-section .timestamp.small {
    font-size: 0.8rem;
    color: #94a3b8;
}

.action-section {
    text-align: right;
    margin-top: 0.5rem;
}

.button.small {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
}

/* Pagination Styles */
.pagination-controls {
    margin-top: 1.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
}

.pagination-controls button {
    /* Basic button styles */
    padding: 0.4rem 0.8rem;
    border: 1px solid #cbd5e1;
    background-color: white;
    border-radius: 4px;
    cursor: pointer;
}

.pagination-controls button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-controls span {
    font-size: 0.9rem;
    color: #475569;
}

/* Modal Styles (Copied from ReportsPage, ensure consistency) */
.modal-overlay { /* ... modal overlay styles ... */ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { /* ... modal content styles ... */ background-color: white; padding: 2rem; border-radius: 8px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); width: 90%; max-width: 500px; }
.modal-content h3 { /* ... modal heading styles ... */ margin-top: 0; margin-bottom: 1rem; color: #1e293b; }
.modal-content p { /* ... modal text styles ... */ color: #475569; margin-bottom: 1rem; }
.modal-content textarea { /* ... modal textarea styles ... */ width: 100%; padding: 0.75rem; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.95rem; margin-bottom: 1rem; resize: vertical; }
.modal-actions { /* ... modal actions styles ... */ display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; }
.button { /* ... general button styles ... */ padding: 0.6rem 1.2rem; border-radius: 6px; font-size: 0.95rem; font-weight: 500; cursor: pointer; border: 1px solid transparent; transition: all 0.2s ease; }
.button.primary { /* ... primary button styles ... */ background-color: #3b82f6; color: white; border-color: #3b82f6; }
.button.primary:hover:not(:disabled) { background-color: #2563eb; }
.button.secondary { /* ... secondary button styles ... */ background-color: #e2e8f0; color: #475569; border-color: #e2e8f0; }
.button.secondary:hover:not(:disabled) { background-color: #cbd5e1; }
.button:disabled { opacity: 0.6; cursor: not-allowed; }
.error-message.small, .success-message.small { /* ... small message styles ... */ font-size: 0.9rem; margin-top: 0.5rem; text-align: center; }
.error-message { padding: 10px; background: #fee2e2; border-radius: 4px; color: #b91c1c; margin-bottom: 15px; font-size: 14px; }

</style> 