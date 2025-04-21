<template>
  <div class="admin-dashboard">
    <h2 class="dashboard-title">管理员仪表盘</h2>
    
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon">👤</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.userCount }}</div>
          <div class="stat-label">用户总数</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🔄</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.activeUsers }}</div>
          <div class="stat-label">今日活跃用户</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.dataCount }}</div>
          <div class="stat-label">系统数据总量</div>
        </div>
      </div>
    </div>
    
    <div class="recent-section">
      <h3 class="section-title">最近活动</h3>
      <div class="activity-list">
        <div v-if="activities.length === 0" class="empty-message">
          暂无活动记录
        </div>
        <div v-for="(activity, index) in activities" :key="index" class="activity-item">
          <div class="activity-time">{{ formatTime(activity.time) }}</div>
          <div class="activity-content">
            <strong>{{ activity.username }}</strong> {{ activity.action }}
          </div>
        </div>
      </div>
    </div>
    
    <div class="admin-functions">
      <h3 class="section-title">快速操作</h3>
      <div class="function-cards">
        <router-link to="/admin/users" class="function-card">
          <div class="function-icon">👥</div>
          <div class="function-content">
            <h4>用户管理</h4>
            <p>查看、编辑和管理用户账户</p>
          </div>
        </router-link>
        
        <router-link to="/admin/announcements" class="function-card">
          <div class="function-icon">📢</div>
          <div class="function-content">
            <h4>公告管理</h4>
            <p>发布、编辑和删除系统公告</p>
          </div>
        </router-link>
        
        <router-link to="/admin/logs" class="function-card">
          <div class="function-icon">📝</div>
          <div class="function-content">
            <h4>系统日志</h4>
            <p>查看系统操作和用户活动日志</p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 系统统计数据
const stats = ref({
  userCount: '...',
  activeUsers: '...',
  dataCount: '...'
})

// 最近活动
const activities = ref([])

// 格式化时间
const formatTime = (time) => {
  if (!time) return '';
  const date = new Date(time);
  return date.toLocaleString();
}

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    // 这里实际项目中应该调用后端API获取数据
    // 示例数据
    stats.value = {
      userCount: 128,
      activeUsers: 43,
      dataCount: 1256
    }
    
    activities.value = [
      { time: new Date(Date.now() - 1000 * 60 * 5), username: '张三', action: '登录了系统' },
      { time: new Date(Date.now() - 1000 * 60 * 10), username: '李四', action: '更新了个人资料' },
      { time: new Date(Date.now() - 1000 * 60 * 15), username: '王五', action: '上传了新头像' },
      { time: new Date(Date.now() - 1000 * 60 * 30), username: '赵六', action: '记录了一条体重数据' },
      { time: new Date(Date.now() - 1000 * 60 * 45), username: '钱七', action: '注册了账户' }
    ]
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

onMounted(fetchDashboardData)
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 600;
  color: #1e40af;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
  margin-top: 0.5rem;
}

.section-title {
  font-size: 1.25rem;
  color: #334155;
  margin: 2rem 0 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.activity-list {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.activity-item {
  padding: 1rem 1.5rem;
  display: flex;
  border-bottom: 1px solid #f1f5f9;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  width: 150px;
  color: #64748b;
  font-size: 0.9rem;
}

.activity-content {
  flex: 1;
}

.function-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.function-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.function-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.function-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.function-content {
  flex: 1;
}

.function-content h4 {
  font-size: 1.1rem;
  margin: 0 0 0.3rem;
  color: #1e293b;
}

.function-content p {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
}

.empty-message {
  padding: 2rem;
  text-align: center;
  color: #64748b;
}
</style> 