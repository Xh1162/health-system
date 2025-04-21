<template>
  <div class="user-management">
    <h2 class="page-title">用户管理</h2>
    
    <div class="filters">
      <div class="search-box">
        <input v-model="searchTerm" placeholder="搜索用户名或邮箱..." />
      </div>
      
      <div class="filter-box">
        <select v-model="statusFilter">
          <option value="all">所有状态</option>
          <option value="active">活跃</option>
          <option value="inactive">禁用</option>
        </select>
      </div>
    </div>
    
    <div class="users-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>注册时间</th>
            <th>状态</th>
            <th width="200">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email || '未设置' }}</td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? '活跃' : '禁用' }}
              </span>
            </td>
            <td class="actions">
              <button 
                @click="toggleUserStatus(user)" 
                :class="user.is_active ? 'btn-danger' : 'btn-success'"
              >
                {{ user.is_active ? '禁用' : '启用' }}
              </button>
              <button @click="resetPassword(user)" class="btn-warning">重置密码</button>
              <button @click="viewDetails(user)" class="btn-info">详情</button>
            </td>
          </tr>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="6" class="empty-message">
              没有找到匹配的用户
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 用户详情弹窗 -->
    <div v-if="selectedUser" class="user-detail-modal">
      <div class="modal-backdrop" @click="selectedUser = null"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>用户详情</h3>
          <button @click="selectedUser = null" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="user-detail">
            <div class="detail-avatar">
              <img :src="selectedUser.avatar || '/default-avatar.png'" :alt="selectedUser.username">
            </div>
            <div class="detail-info">
              <div class="detail-item">
                <span class="detail-label">ID:</span>
                <span class="detail-value">{{ selectedUser.id }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">用户名:</span>
                <span class="detail-value">{{ selectedUser.username }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">邮箱:</span>
                <span class="detail-value">{{ selectedUser.email || '未设置' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">手机:</span>
                <span class="detail-value">{{ selectedUser.phone || '未设置' }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">注册时间:</span>
                <span class="detail-value">{{ formatDate(selectedUser.created_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">最后更新:</span>
                <span class="detail-value">{{ formatDate(selectedUser.updated_at) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">状态:</span>
                <span class="detail-value" :class="selectedUser.is_active ? 'status-active' : 'status-inactive'">
                  {{ selectedUser.is_active ? '活跃' : '禁用' }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="selectedUser = null" class="btn-secondary">关闭</button>
          <button 
            @click="toggleUserStatus(selectedUser); selectedUser = null;" 
            :class="selectedUser.is_active ? 'btn-danger' : 'btn-success'"
          >
            {{ selectedUser.is_active ? '禁用账户' : '启用账户' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// 状态变量
const users = ref([]);
const searchTerm = ref('');
const statusFilter = ref('all');
const selectedUser = ref(null);

// 过滤用户列表
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    // 状态过滤
    if (statusFilter.value !== 'all') {
      if (statusFilter.value === 'active' && !user.is_active) return false;
      if (statusFilter.value === 'inactive' && user.is_active) return false;
    }
    
    // 搜索过滤
    if (searchTerm.value) {
      const term = searchTerm.value.toLowerCase();
      return user.username.toLowerCase().includes(term) || 
             (user.email && user.email.toLowerCase().includes(term));
    }
    
    return true;
  });
});

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未知';
  const date = new Date(dateStr);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
};

// 切换用户状态
const toggleUserStatus = async (user) => {
  try {
    // 实际项目中应该调用后端API
    alert(`已${user.is_active ? '禁用' : '启用'}用户: ${user.username}`);
    user.is_active = !user.is_active;
  } catch (error) {
    console.error('更新用户状态失败:', error);
    alert('操作失败: ' + (error.response?.data?.message || error.message));
  }
};

// 重置密码
const resetPassword = async (user) => {
  if (!confirm(`确定要重置用户 ${user.username} 的密码吗？`)) return;
  
  try {
    // 实际项目中应该调用后端API
    const newPassword = Math.random().toString(36).slice(-8);
    alert(`密码已重置为: ${newPassword}\n\n提示：实际项目中，新密码应发送给用户邮箱而不是直接显示`);
  } catch (error) {
    console.error('重置密码失败:', error);
    alert('操作失败: ' + (error.response?.data?.message || error.message));
  }
};

// 查看用户详情
const viewDetails = (user) => {
  selectedUser.value = { ...user };
};

// 获取所有用户
const fetchUsers = async () => {
  try {
    // 实际项目中应该调用后端API
    // 这里使用模拟数据
    users.value = [
      {
        id: 1,
        username: 'admin',
        email: 'admin@example.com',
        phone: '13800138000',
        avatar: 'http://localhost:5008/default-avatar.png',
        role: 'admin',
        created_at: '2023-01-01T08:00:00Z',
        updated_at: '2023-06-15T10:30:00Z',
        is_active: true
      },
      {
        id: 2,
        username: 'user1',
        email: 'user1@example.com',
        phone: '13900139001',
        avatar: 'http://localhost:5008/default-avatar.png',
        role: 'user',
        created_at: '2023-02-15T09:20:00Z',
        updated_at: '2023-07-20T14:15:00Z',
        is_active: true
      },
      {
        id: 3,
        username: 'user2',
        email: 'user2@example.com',
        phone: null,
        avatar: 'http://localhost:5008/default-avatar.png',
        role: 'user',
        created_at: '2023-03-10T11:45:00Z',
        updated_at: '2023-05-05T16:30:00Z',
        is_active: true
      },
      {
        id: 4,
        username: 'inactive_user',
        email: 'inactive@example.com',
        phone: '13700137000',
        avatar: 'http://localhost:5008/default-avatar.png',
        role: 'user',
        created_at: '2023-04-05T15:10:00Z',
        updated_at: '2023-08-01T09:45:00Z',
        is_active: false
      }
    ];
  } catch (error) {
    console.error('获取用户列表失败:', error);
    alert('获取用户数据失败: ' + (error.response?.data?.message || error.message));
  }
};

onMounted(fetchUsers);
</script>

<style scoped>
.user-management {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-box input,
.filter-box select {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.search-box input {
  width: 250px;
}

.users-container {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #f1f5f9;
}

.users-table th {
  background: #f8fafc;
  font-weight: 500;
  color: #334155;
  font-size: 0.875rem;
}

.users-table tr:last-child td {
  border-bottom: none;
}

.status-active {
  color: #16a34a;
  font-weight: 500;
}

.status-inactive {
  color: #dc2626;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-success,
.btn-danger,
.btn-warning,
.btn-info,
.btn-secondary {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-success {
  background: #22c55e;
  color: white;
}

.btn-success:hover {
  background: #16a34a;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

.btn-warning {
  background: #f59e0b;
  color: white;
}

.btn-warning:hover {
  background: #d97706;
}

.btn-info {
  background: #3b82f6;
  color: white;
}

.btn-info:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #64748b;
  color: white;
}

.btn-secondary:hover {
  background: #475569;
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

/* 弹窗样式 */
.user-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
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
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.user-detail {
  display: flex;
  gap: 1.5rem;
}

.detail-avatar {
  flex-shrink: 0;
}

.detail-avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.detail-info {
  flex: 1;
}

.detail-item {
  margin-bottom: 0.5rem;
  display: flex;
}

.detail-label {
  width: 100px;
  color: #64748b;
  font-size: 0.875rem;
}

.detail-value {
  flex: 1;
  font-weight: 500;
}
</style> 