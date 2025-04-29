<template>
  <div class="user-reports-page">
    <div class="page-header">
      <h2>用户健康报告</h2>
      <p class="subtitle">选择用户查看健康报告并添加个性化建议</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载用户列表中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-icon">❌</div>
      <h3>加载用户列表失败</h3>
      <p>{{ error }}</p>
      <button class="retry-button" @click="loadUsers">重试</button>
    </div>

    <div v-else class="users-grid">
      <div v-for="user in users" :key="user.id" class="user-card">
        <div class="user-info">
          <div class="avatar">
            <img :src="user.avatar || '/default-avatar.png'" :alt="user.username">
          </div>
          <div class="user-details">
            <h3>{{ user.username }}</h3>
            <p>{{ user.email || '无邮箱信息' }}</p>
          </div>
        </div>
        <button class="view-report-button" @click="viewUserReport(user.id)">
          查看健康报告
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
// 确保你有一个可以获取所有用户的API函数
import { getAllUsers } from '../../api/admin';

const router = useRouter();
const users = ref([]);
const loading = ref(true);
const error = ref(null);

// 加载用户列表的函数
const loadUsers = async () => {
  loading.value = true;
  error.value = null; // 重置错误状态
  try {
    // 调用API获取用户数据
    const userList = await getAllUsers(); // 确保这个API函数存在且正确工作
    users.value = userList;
  } catch (err) {
    console.error('获取用户列表失败:', err);
    error.value = err.message || '无法连接到服务器或加载数据时出错。';
  } finally {
    loading.value = false;
  }
};

// 导航到特定用户的报告页面
const viewUserReport = (userId) => {
  // 使用我们在路由中定义的名称或路径
  router.push({ name: 'UserReport', params: { userId: userId } });
  // 或者 router.push(`/admin/user-report/${userId}`);
};

// 组件挂载时加载用户数据
onMounted(() => {
  loadUsers();
});

// Add this new function
const navigateToUserReports = () => {
  router.push('/admin/user-reports'); // Navigates to the new user list page we defined
};
</script>

<style scoped>
.user-reports-page {
  padding: 1.5rem;
  background-color: #f8f9fa; /* 淡灰色背景 */
  min-height: calc(100vh - 60px); /* 减去可能的头部高度 */
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

/* 加载和错误状态 */
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  text-align: center;
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

/* 用户卡片网格 */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); /* 响应式网格 */
  gap: 1.5rem; /* 卡片间距 */
}

.user-card {
  background: white;
  border-radius: 0.75rem; /* 更圆润的边角 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* 更柔和的阴影 */
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.avatar {
  width: 50px; /* 头像尺寸 */
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 1rem;
  flex-shrink: 0; /* 防止头像被压缩 */
  border: 2px solid #e2e8f0; /* 头像边框 */
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  overflow: hidden; /* 防止长文本溢出 */
}

.user-details h3 {
  margin: 0 0 0.25rem 0;
  font-size: 1.1rem;
  color: #1e293b;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* 用户名过长时显示省略号 */
}

.user-details p {
  margin: 0;
  color: #64748b;
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* 邮箱过长时显示省略号 */
}

.view-report-button {
  background: #4f46e5; /* 换个颜色试试 */
  color: white;
  border: none;
  padding: 0.6rem 0; /* 调整内边距 */
  border-radius: 0.5rem;
  margin-top: auto; /* 将按钮推到底部 */
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  text-align: center;
  transition: background-color 0.3s ease;
}

.view-report-button:hover {
  background: #4338ca;
}
</style>



