<template>
  <div class="admin-layout">
    <header class="admin-header">
      <h1>健康系统管理后台</h1>
      <div class="admin-info">
        <div class="user-display">
          <UserAvatar 
            :username="username" 
            :showAdminBadge="true" 
            size="small" 
          />
          <span>管理员: {{ username }}</span>
        </div>
        <button @click="logout" class="logout-btn">退出</button>
      </div>
    </header>
    
    <div class="admin-content">
      <aside class="admin-sidebar">
        <nav>
          <router-link to="/admin" class="nav-item">仪表盘</router-link>
          <router-link to="/admin/users" class="nav-item">用户管理</router-link>
          <router-link to="/admin/announcements" class="nav-item">公告管理</router-link>
          <router-link to="/admin/logs" class="nav-item">系统日志</router-link>
          <div class="nav-divider"></div>
          <router-link to="/dashboard" class="nav-item back-link">返回前台</router-link>
        </nav>
      </aside>
      
      <main class="admin-main">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import useUserStore from '../../stores/userStore';
import UserAvatar from '../../components/user/UserAvatar.vue';

const router = useRouter();
const userStore = useUserStore();

const username = computed(() => userStore.state.userData?.username || '未知');

const logout = () => {
  userStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Arial', sans-serif;
}

.admin-header {
  background: #1e40af;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logout-btn {
  padding: 0.4rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.admin-content {
  display: flex;
  flex: 1;
}

.admin-sidebar {
  width: 220px;
  background: #f8fafc;
  box-shadow: 1px 0 3px rgba(0, 0, 0, 0.1);
}

.admin-sidebar nav {
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
}

.nav-item {
  padding: 0.75rem 1rem;
  color: #334155;
  text-decoration: none;
  font-weight: 500;
  border-radius: 6px;
  margin-bottom: 0.25rem;
  transition: all 0.2s;
}

.nav-item:hover, .router-link-active {
  background: #e2e8f0;
  color: #1e40af;
}

.nav-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 1rem 0;
}

.back-link {
  color: #64748b;
  font-size: 0.9rem;
}

.admin-main {
  flex: 1;
  padding: 2rem;
  background: #f1f5f9;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .admin-content {
    flex-direction: column;
  }
  
  .admin-sidebar {
    width: 100%;
  }
  
  .admin-sidebar nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 0.5rem;
  }
  
  .nav-divider {
    display: none;
  }
}
</style> 