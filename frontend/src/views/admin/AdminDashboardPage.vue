<!-- frontend/src/views/admin/AdminDashboardPage.vue -->
<template>
  <div class="admin-dashboard">
    <h1>管理员仪表盘</h1>
    <p>欢迎来到管理员界面！</p>
    <!-- 这里将来会添加更多内容，如统计信息、快捷链接等 -->
    <div>
        <!-- 使用相对路径，因为现在是子路由 -->
        <router-link to="/admin/food-items" class="link-button">管理食物条目</router-link>
        <router-link to="/admin/users" class="link-button">管理用户账号</router-link>
    </div>
  </div>
</template>

<script setup>
// import { useRouter } from 'vue-router'; // 不再需要 useRouter

// const router = useRouter(); // 不再需要

// const logout = () => { // logout 函数移至 AdminLayout
//     localStorage.removeItem('admin_token');
//     localStorage.removeItem('admin_user');
//     router.push('/admin/login');
// }
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  background-color: #fff; /* Add white background */
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

h1 {
    color: #333;
    margin-bottom: 20px;
}

p {
    color: #555;
    margin-bottom: 30px;
}

.link-button {
    display: inline-block;
    margin-top: 10px; /* Adjusted margin */
    padding: 10px 15px;
    background-color: #007bff; /* Blue color */
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s ease;
    font-size: 1rem;
}

.link-button:hover {
    background-color: #0056b3;
}

/* Removed button styles */

/* Add some spacing between buttons if needed */
.link-button + .link-button {
  margin-left: 10px;
}
</style> 