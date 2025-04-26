<!-- frontend/src/views/admin/AdminLoginPage.vue -->
<template>
  <div class="admin-login-page">
    <div class="login-container">
      <h2>管理员登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../api'; // Assuming your API client setup is in /src/api/index.js or similar

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await api.post('/auth/login', {
      username: username.value,
      password: password.value,
    });

    console.log("Login response:", response.data); // Debugging

    if (response.data.success && response.data.user) {
        // 检查用户角色
        if (response.data.user.role === 'admin') {
            // 存储Token (注意：实际项目中推荐使用更安全的方式如 HttpOnly Cookie 或 状态管理库 Pinia/Vuex)
            localStorage.setItem('admin_token', response.data.access_token);
            localStorage.setItem('admin_user', JSON.stringify(response.data.user)); // 可选，存储用户信息

            // 跳转到管理员主页
            router.push('/admin/dashboard'); // 或者 '/admin'
        } else {
            error.value = '您没有管理员权限。';
        }
    } else {
      error.value = response.data.message || '登录失败，请检查用户名和密码。';
    }
  } catch (err) {
    console.error("Login error:", err); // Debugging
    error.value = '登录请求失败，请稍后重试。';
    if (err.response && err.response.data && err.response.data.message) {
        error.value = err.response.data.message;
    } else if (err.message) {
        error.value = err.message;
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.admin-login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f4f7f6;
}

.login-container {
  background-color: #fff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h2 {
  margin-bottom: 25px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Important for width */
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #5cb85c; /* Green color */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

button:not(:disabled):hover {
  background-color: #4cae4c;
}

.error-message {
  margin-top: 15px;
  color: #d9534f; /* Red color */
  font-weight: bold;
}
</style> 