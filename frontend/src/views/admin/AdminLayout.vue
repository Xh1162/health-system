<template>
  <div class="admin-layout">
    <header class="admin-header">
      <h1>管理后台</h1>
      <button @click="logout" class="logout-button">退出登录</button>
    </header>
    <main class="admin-main">
      <AdminSidebar />
      <div class="admin-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import AdminSidebar from '../../components/admin/AdminSidebar.vue';
import { useRouter } from 'vue-router';
import useUserStore from '../../stores/userStore';

const router = useRouter();
const userStore = useUserStore();

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
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  background-color: #343a40;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.admin-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.logout-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #c82333;
}

.admin-main {
  display: flex;
  flex-grow: 1;
}

.admin-content {
  flex-grow: 1;
  padding: 20px;
  background-color: #f8f9fa;
  overflow-y: auto;
}
</style> 