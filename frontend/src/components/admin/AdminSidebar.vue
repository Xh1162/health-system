<template>
  <aside class="admin-sidebar">
    <h2>侧边栏</h2>
    <nav>
      <ul>
        <li><router-link to="/admin/dashboard">仪表盘</router-link></li>
        <li><router-link to="/admin/users">用户管理</router-link></li>
        <li><router-link to="/admin/records">记录管理</router-link></li>
        <li><router-link to="/admin/reports">报告管理</router-link></li>
        <!-- 在这里添加更多侧边栏链接 -->
      </ul>
    </nav>
  </aside>
</template>

<script setup>
// 这里可以添加侧边栏相关的逻辑，如果需要的话
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.admin-sidebar {
  width: 220px;
  background-color: #495057;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 60px); /* 假设 header 高度为 60px */
  box-sizing: border-box;
}

.admin-sidebar h2 {
  margin-top: 0;
  margin-bottom: 20px;
  text-align: center;
  font-size: 1.3rem;
}

.admin-sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.admin-sidebar nav li {
  margin-bottom: 10px;
}

.admin-sidebar nav a {
  color: #dee2e6;
  text-decoration: none;
  display: block;
  padding: 8px 15px;
  border-radius: 4px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.admin-sidebar nav a:hover,
.admin-sidebar nav a.router-link-exact-active {
  background-color: #007bff;
  color: white;
}
</style>
