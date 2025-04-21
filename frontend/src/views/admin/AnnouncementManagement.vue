<template>
  <div class="announcement-management">
    <h2 class="page-title">公告管理</h2>
    
    <div class="action-bar">
      <button @click="showCreateModal = true" class="btn-primary">
        <span class="btn-icon">+</span> 创建新公告
      </button>
      <div class="filters">
        <select v-model="statusFilter" class="filter-select">
          <option value="all">所有状态</option>
          <option value="active">活跃</option>
          <option value="inactive">已归档</option>
        </select>
      </div>
    </div>
    
    <div class="announcements-list">
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载公告...</p>
      </div>
      
      <div v-else-if="filteredAnnouncements.length === 0" class="empty-list">
        <div class="empty-icon">📢</div>
        <p>暂无公告</p>
        <button @click="showCreateModal = true" class="btn-secondary">创建第一条公告</button>
      </div>
      
      <div v-else class="announcements-grid">
        <div 
          v-for="announcement in filteredAnnouncements" 
          :key="announcement.id" 
          class="announcement-card"
          :class="{ inactive: !announcement.is_active }"
        >
          <div class="card-header">
            <h3 class="card-title">{{ announcement.title }}</h3>
            <div class="card-status" :class="announcement.is_active ? 'status-active' : 'status-inactive'">
              {{ announcement.is_active ? '活跃' : '已归档' }}
            </div>
          </div>
          
          <div class="card-content">
            <p>{{ announcement.content }}</p>
          </div>
          
          <div class="card-footer">
            <div class="card-meta">
              <div class="meta-item">发布于: {{ formatDate(announcement.created_at) }}</div>
              <div class="meta-item">发布者: {{ announcement.admin_username || '管理员' }}</div>
            </div>
            <div class="card-actions">
              <button @click="editAnnouncement(announcement)" class="action-btn edit-btn">
                编辑
              </button>
              <button 
                @click="toggleAnnouncementStatus(announcement)" 
                class="action-btn"
                :class="announcement.is_active ? 'archive-btn' : 'activate-btn'"
              >
                {{ announcement.is_active ? '归档' : '激活' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 创建/编辑公告弹窗 -->
    <div v-if="showCreateModal || editingAnnouncement" class="modal">
      <div class="modal-backdrop" @click="cancelEdit"></div>
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editingAnnouncement ? '编辑公告' : '创建新公告' }}</h3>
          <button @click="cancelEdit" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="saveAnnouncement">
            <div class="form-group">
              <label for="title">标题 *</label>
              <input 
                id="title"
                v-model="announcementForm.title" 
                type="text" 
                placeholder="输入公告标题"
                required
              >
            </div>
            
            <div class="form-group">
              <label for="content">内容 *</label>
              <textarea 
                id="content"
                v-model="announcementForm.content" 
                placeholder="输入公告内容"
                rows="5"
                required
              ></textarea>
            </div>
            
            <div class="form-group">
              <div class="checkbox-wrapper">
                <input 
                  id="is_active"
                  v-model="announcementForm.is_active" 
                  type="checkbox"
                >
                <label for="is_active">立即发布</label>
              </div>
            </div>
            
            <div class="form-actions">
              <button type="button" @click="cancelEdit" class="btn-secondary">取消</button>
              <button type="submit" class="btn-primary">保存</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// 状态
const announcements = ref([]);
const isLoading = ref(true);
const statusFilter = ref('all');
const showCreateModal = ref(false);
const editingAnnouncement = ref(null);
const announcementForm = ref({
  title: '',
  content: '',
  is_active: true
});

// 计算属性: 过滤后的公告列表
const filteredAnnouncements = computed(() => {
  if (statusFilter.value === 'all') {
    return announcements.value;
  }
  return announcements.value.filter(a => 
    (statusFilter.value === 'active' && a.is_active) || 
    (statusFilter.value === 'inactive' && !a.is_active)
  );
});

// 获取公告列表
const fetchAnnouncements = async () => {
  try {
    isLoading.value = true;
    // 实际项目中应调用后端API
    // const response = await axios.get('/api/admin/announcements');
    // announcements.value = response.data;
    
    // 模拟数据
    await new Promise(resolve => setTimeout(resolve, 500));
    announcements.value = [
      {
        id: 1,
        title: '系统维护通知',
        content: '亲爱的用户，我们将于本周六凌晨2点至4点进行系统维护，届时系统将暂停服务。给您带来的不便，敬请谅解。',
        is_active: true,
        created_at: '2023-06-15T08:00:00Z',
        admin_username: '系统管理员'
      },
      {
        id: 2,
        title: '新功能上线预告',
        content: '我们即将推出全新的数据分析工具，帮助您更好地理解自己的健康状况。敬请期待！',
        is_active: true,
        created_at: '2023-06-10T14:30:00Z',
        admin_username: '产品经理'
      },
      {
        id: 3,
        title: '过时公告',
        content: '这是一个已经归档的公告示例，用户将不会看到这个公告。',
        is_active: false,
        created_at: '2023-05-20T10:15:00Z',
        admin_username: '系统管理员'
      }
    ];
    isLoading.value = false;
  } catch (error) {
    console.error('获取公告列表失败:', error);
    isLoading.value = false;
  }
};

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未知';
  const date = new Date(dateStr);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
};

// 编辑公告
const editAnnouncement = (announcement) => {
  editingAnnouncement.value = announcement;
  announcementForm.value = {
    title: announcement.title,
    content: announcement.content,
    is_active: announcement.is_active
  };
};

// 切换公告状态
const toggleAnnouncementStatus = async (announcement) => {
  try {
    // 实际项目中应调用后端API
    // await axios.put(`/api/admin/announcements/${announcement.id}/status`, {
    //   is_active: !announcement.is_active
    // });
    
    // 模拟操作
    announcement.is_active = !announcement.is_active;
    alert(`公告已${announcement.is_active ? '激活' : '归档'}`);
  } catch (error) {
    console.error('更新公告状态失败:', error);
    alert('操作失败，请重试');
  }
};

// 保存公告
const saveAnnouncement = async () => {
  try {
    if (editingAnnouncement.value) {
      // 编辑现有公告
      // 实际项目中应调用后端API
      // await axios.put(`/api/admin/announcements/${editingAnnouncement.value.id}`, announcementForm.value);
      
      // 模拟操作
      const index = announcements.value.findIndex(a => a.id === editingAnnouncement.value.id);
      if (index !== -1) {
        announcements.value[index] = {
          ...editingAnnouncement.value,
          ...announcementForm.value,
          updated_at: new Date().toISOString()
        };
      }
      alert('公告已更新');
    } else {
      // 创建新公告
      // 实际项目中应调用后端API
      // const response = await axios.post('/api/admin/announcements', announcementForm.value);
      // announcements.value.unshift(response.data);
      
      // 模拟操作
      const newAnnouncement = {
        id: Date.now(),
        ...announcementForm.value,
        created_at: new Date().toISOString(),
        admin_username: '当前管理员'
      };
      announcements.value.unshift(newAnnouncement);
      alert('公告已创建');
    }
    
    // 重置表单并关闭模态框
    cancelEdit();
  } catch (error) {
    console.error('保存公告失败:', error);
    alert('保存失败，请重试');
  }
};

// 取消编辑
const cancelEdit = () => {
  editingAnnouncement.value = null;
  showCreateModal.value = false;
  announcementForm.value = {
    title: '',
    content: '',
    is_active: true
  };
};

// 页面加载时获取公告列表
onMounted(fetchAnnouncements);
</script>

<style scoped>
.announcement-management {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  font-size: 1.5rem;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #2563eb;
}

.btn-secondary {
  background-color: #e2e8f0;
  color: #475569;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #cbd5e1;
}

.btn-icon {
  margin-right: 0.5rem;
  font-weight: bold;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  color: #475569;
}

.announcements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.announcement-card {
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}

.announcement-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.announcement-card.inactive {
  opacity: 0.7;
}

.card-header {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #f1f5f9;
}

.card-title {
  margin: 0;
  font-size: 1.1rem;
  color: #1e293b;
}

.card-status {
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: #dcfce7;
  color: #16a34a;
}

.status-inactive {
  background: #f1f5f9;
  color: #64748b;
}

.card-content {
  padding: 1rem;
  flex: 1;
}

.card-content p {
  margin: 0;
  color: #475569;
  line-height: 1.5;
}

.card-footer {
  padding: 1rem;
  border-top: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.card-meta {
  font-size: 0.8rem;
  color: #64748b;
}

.meta-item {
  margin-bottom: 0.25rem;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.action-btn {
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn {
  background: #e2e8f0;
  color: #334155;
}

.edit-btn:hover {
  background: #cbd5e1;
}

.archive-btn {
  background: #fecaca;
  color: #b91c1c;
}

.archive-btn:hover {
  background: #fca5a5;
}

.activate-btn {
  background: #d1fae5;
  color: #047857;
}

.activate-btn:hover {
  background: #a7f3d0;
}

.loading-container, .empty-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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
}

/* 模态框样式 */
.modal {
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
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #334155;
}

.form-group input[type="text"],
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
}

.checkbox-wrapper input[type="checkbox"] {
  margin-right: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style> 