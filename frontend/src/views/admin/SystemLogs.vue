<template>
  <div class="system-logs">
    <h2 class="page-title">系统日志</h2>
    
    <div class="filters-bar">
      <div class="search-box">
        <input 
          v-model="searchTerm" 
          type="text" 
          placeholder="搜索用户名、操作或IP..." 
          class="search-input"
        />
      </div>
      
      <div class="filters">
        <div class="filter-group">
          <label>操作类型:</label>
          <select v-model="actionFilter" class="filter-select">
            <option value="all">所有操作</option>
            <option value="login">登录</option>
            <option value="logout">登出</option>
            <option value="register">注册</option>
            <option value="update">更新</option>
            <option value="admin">管理操作</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>时间段:</label>
          <select v-model="timeFilter" class="filter-select">
            <option value="all">所有时间</option>
            <option value="today">今天</option>
            <option value="week">本周</option>
            <option value="month">本月</option>
          </select>
        </div>
      </div>
    </div>
    
    <div class="logs-content">
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载日志数据...</p>
      </div>
      
      <div v-else-if="filteredLogs.length === 0" class="empty-logs">
        <div class="empty-icon">📋</div>
        <p>无符合条件的日志记录</p>
      </div>
      
      <div v-else class="logs-table-container">
        <table class="logs-table">
          <thead>
            <tr>
              <th class="column-time">时间</th>
              <th class="column-user">用户</th>
              <th class="column-action">操作</th>
              <th class="column-ip">IP地址</th>
              <th class="column-details">详情</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in paginatedLogs" :key="log.id" class="log-row">
              <td class="column-time">{{ formatDateTime(log.created_at) }}</td>
              <td class="column-user">{{ log.username || log.user_id }}</td>
              <td class="column-action">
                <span class="action-badge" :class="getActionClass(log.action)">
                  {{ formatAction(log.action) }}
                </span>
              </td>
              <td class="column-ip">{{ log.ip_address || '-' }}</td>
              <td class="column-details">
                <button 
                  v-if="log.details" 
                  @click="viewLogDetails(log)" 
                  class="details-btn"
                >
                  查看详情
                </button>
                <span v-else>-</span>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- 分页控件 -->
        <div class="pagination">
          <div class="pagination-info">
            显示 {{ startIndex + 1 }}-{{ endIndex }} 条，共 {{ filteredLogs.length }} 条
          </div>
          <div class="pagination-controls">
            <button 
              @click="currentPage--" 
              :disabled="currentPage === 1" 
              class="pagination-btn"
            >
              上一页
            </button>
            <span class="page-indicator">{{ currentPage }} / {{ totalPages }}</span>
            <button 
              @click="currentPage++" 
              :disabled="currentPage === totalPages" 
              class="pagination-btn"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 日志详情弹窗 -->
    <div v-if="selectedLog" class="log-details-modal">
      <div class="modal-backdrop" @click="selectedLog = null"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>日志详情</h3>
          <button @click="selectedLog = null" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="detail-item">
            <div class="detail-label">ID:</div>
            <div class="detail-value">{{ selectedLog.id }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">用户:</div>
            <div class="detail-value">{{ selectedLog.username || selectedLog.user_id }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">操作:</div>
            <div class="detail-value">
              <span class="action-badge" :class="getActionClass(selectedLog.action)">
                {{ formatAction(selectedLog.action) }}
              </span>
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-label">时间:</div>
            <div class="detail-value">{{ formatDateTime(selectedLog.created_at) }}</div>
          </div>
          <div class="detail-item">
            <div class="detail-label">IP地址:</div>
            <div class="detail-value">{{ selectedLog.ip_address || '-' }}</div>
          </div>
          <div class="detail-item detail-json">
            <div class="detail-label">详细信息:</div>
            <pre class="detail-value detail-json">{{ formatJSON(selectedLog.details) }}</pre>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="selectedLog = null" class="btn-primary">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

// 状态
const logs = ref([]);
const isLoading = ref(true);
const searchTerm = ref('');
const actionFilter = ref('all');
const timeFilter = ref('all');
const currentPage = ref(1);
const itemsPerPage = 20;
const selectedLog = ref(null);

// 计算过滤后的日志
const filteredLogs = computed(() => {
  return logs.value
    .filter(log => {
      // 搜索条件过滤
      if (searchTerm.value) {
        const term = searchTerm.value.toLowerCase();
        return (
          (log.username && log.username.toLowerCase().includes(term)) ||
          (log.action && log.action.toLowerCase().includes(term)) ||
          (log.ip_address && log.ip_address.includes(term))
        );
      }
      return true;
    })
    .filter(log => {
      // 操作类型过滤
      if (actionFilter.value === 'all') return true;
      if (actionFilter.value === 'admin') {
        return log.action.startsWith('admin_');
      }
      return log.action === actionFilter.value;
    })
    .filter(log => {
      // 时间过滤
      if (timeFilter.value === 'all') return true;
      
      const logDate = new Date(log.created_at);
      const now = new Date();
      
      if (timeFilter.value === 'today') {
        return logDate.toDateString() === now.toDateString();
      }
      
      if (timeFilter.value === 'week') {
        const weekStart = new Date(now);
        weekStart.setDate(now.getDate() - now.getDay());
        weekStart.setHours(0, 0, 0, 0);
        return logDate >= weekStart;
      }
      
      if (timeFilter.value === 'month') {
        return (
          logDate.getMonth() === now.getMonth() && 
          logDate.getFullYear() === now.getFullYear()
        );
      }
      
      return true;
    });
});

// 计算分页日志
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage);
const endIndex = computed(() => {
  const end = startIndex.value + itemsPerPage;
  return end > filteredLogs.value.length ? filteredLogs.value.length : end;
});

const paginatedLogs = computed(() => {
  return filteredLogs.value.slice(startIndex.value, endIndex.value);
});

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredLogs.value.length / itemsPerPage));
});

// 重置页码当过滤条件变化时
watch([searchTerm, actionFilter, timeFilter], () => {
  currentPage.value = 1;
});

// 格式化日期时间
const formatDateTime = (dateStr) => {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toLocaleString();
};

// 获取操作类名
const getActionClass = (action) => {
  if (!action) return '';
  if (action === 'login') return 'action-login';
  if (action === 'logout') return 'action-logout';
  if (action === 'register') return 'action-register';
  if (action.includes('update')) return 'action-update';
  if (action.startsWith('admin_')) return 'action-admin';
  return '';
};

// 格式化操作名称
const formatAction = (action) => {
  if (!action) return '-';
  
  const actionMap = {
    login: '登录',
    logout: '登出',
    register: '注册',
    update_profile: '更新资料',
    update_password: '修改密码',
    update_avatar: '更新头像',
    admin_user_update: '管理员更新用户',
    admin_announcement_create: '创建公告',
    admin_announcement_update: '更新公告'
  };
  
  return actionMap[action] || action;
};

// 格式化JSON对象
const formatJSON = (obj) => {
  if (!obj) return '-';
  if (typeof obj === 'string') {
    try {
      return JSON.stringify(JSON.parse(obj), null, 2);
    } catch (e) {
      return obj;
    }
  }
  return JSON.stringify(obj, null, 2);
};

// 查看日志详情
const viewLogDetails = (log) => {
  selectedLog.value = log;
};

// 获取系统日志
const fetchLogs = async () => {
  try {
    isLoading.value = true;
    // 实际项目中应调用后端API
    // const response = await axios.get('/api/admin/logs');
    // logs.value = response.data;
    
    // 模拟数据
    await new Promise(resolve => setTimeout(resolve, 500));
    
    logs.value = Array.from({ length: 100 }, (_, i) => {
      const date = new Date();
      date.setHours(date.getHours() - Math.floor(Math.random() * 72));
      
      const actions = [
        'login', 'logout', 'register', 'update_profile', 
        'update_avatar', 'admin_user_update', 'admin_announcement_create'
      ];
      const action = actions[Math.floor(Math.random() * actions.length)];
      
      const usernames = ['admin', '张三', '李四', '王五', '赵六'];
      const username = usernames[Math.floor(Math.random() * usernames.length)];
      
      let details = null;
      if (Math.random() > 0.5) {
        if (action === 'login') {
          details = { browser: 'Chrome', device: 'Desktop', os: 'Windows 10' };
        } else if (action === 'update_profile') {
          details = { changed_fields: ['username', 'phone'] };
        } else if (action.startsWith('admin_')) {
          details = { affected_id: Math.floor(Math.random() * 100) + 1 };
        }
      }
      
      return {
        id: 1000 + i,
        user_id: Math.floor(Math.random() * 10) + 1,
        username,
        action,
        ip_address: `192.168.1.${Math.floor(Math.random() * 255)}`,
        details,
        created_at: date.toISOString()
      };
    }).sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    isLoading.value = false;
  } catch (error) {
    console.error('获取系统日志失败:', error);
    isLoading.value = false;
  }
};

// 页面加载时获取日志
onMounted(fetchLogs);
</script>

<style scoped>
.system-logs {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.filters-bar {
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-size: 0.875rem;
  color: #64748b;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #334155;
}

.logs-content {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.loading-container, .empty-logs {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #94a3b8;
}

.logs-table-container {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table th, .logs-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
}

.logs-table th {
  background: #f8fafc;
  color: #334155;
  font-weight: 600;
  font-size: 0.875rem;
}

.logs-table tr:last-child td {
  border-bottom: none;
}

.log-row:hover {
  background-color: #f8fafc;
}

.column-time {
  width: 180px;
  white-space: nowrap;
}

.column-user {
  width: 120px;
}

.column-action {
  width: 120px;
}

.column-ip {
  width: 120px;
  white-space: nowrap;
}

.action-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.action-login {
  background: #dbeafe;
  color: #2563eb;
}

.action-logout {
  background: #fef3c7;
  color: #d97706;
}

.action-register {
  background: #dcfce7;
  color: #16a34a;
}

.action-update {
  background: #e0e7ff;
  color: #4f46e5;
}

.action-admin {
  background: #fae8ff;
  color: #a21caf;
}

.details-btn {
  padding: 0.25rem 0.5rem;
  background: #f1f5f9;
  border: none;
  border-radius: 0.25rem;
  color: #475569;
  font-size: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.details-btn:hover {
  background: #e2e8f0;
}

.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-top: 1px solid #f1f5f9;
  font-size: 0.875rem;
  color: #64748b;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pagination-btn {
  padding: 0.375rem 0.75rem;
  background: #f1f5f9;
  border: none;
  border-radius: 0.25rem;
  color: #475569;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background: #e2e8f0;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 模态框样式 */
.log-details-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 600px;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
}

.modal-body {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-footer {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  border-top: 1px solid #e2e8f0;
}

.detail-item {
  margin-bottom: 1rem;
  display: flex;
}

.detail-label {
  width: 100px;
  color: #64748b;
  font-weight: 500;
}

.detail-value {
  flex: 1;
}

.detail-json {
  display: block;
}

.detail-json .detail-label {
  margin-bottom: 0.5rem;
}

.detail-json .detail-value {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 0.375rem;
  border: 1px solid #e2e8f0;
  overflow-x: auto;
  white-space: pre-wrap;
  font-family: monospace;
  font-size: 0.875rem;
  color: #334155;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #2563eb;
}

@media (max-width: 768px) {
  .filters-bar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .column-time, .column-ip {
    display: none;
  }
}
</style> 