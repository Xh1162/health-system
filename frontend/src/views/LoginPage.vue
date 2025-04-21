<template>
  <div class="login-container">
    <div class="login-form">
      <h2>用户登录</h2>
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <div class="form-group">
        <label for="username">用户名</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          placeholder="请输入用户名"
          autocomplete="username"
        />
      </div>
      
      <div class="form-group">
        <label for="password">密码</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          placeholder="请输入密码"
          autocomplete="current-password"
        />
      </div>
      
      <button 
        class="login-button" 
        @click="login" 
        :disabled="isLoading"
      >
        {{ isLoading ? '登录中...' : '登录' }}
      </button>
      
      <div class="register-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>

      <div class="admin-tip">
        提示：管理员账户 - 用户名：admin，密码：admin123
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const userStore = inject('userStore')

// 表单数据
const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

const login = async () => {
  try {
    error.value = ''
    
    if (!username.value || !password.value) {
      error.value = '请输入用户名和密码'
      return
    }
    
    isLoading.value = true
    
    // 调用登录API
    const apiBaseUrl = 'http://localhost:5008'
    const response = await axios.post(`${apiBaseUrl}/api/auth/login`, {
      username: username.value,
      password: password.value
    })
    
    if (response.data.success) {
      // 登录成功，更新用户状态
      userStore.login(response.data.data)
      
      // 检查是否有重定向路径
      const redirectPath = route.query.redirect || '/dashboard'
      router.push(redirectPath)
    } else {
      error.value = response.data.message || '登录失败'
    }
  } catch (err) {
    if (err.response) {
      error.value = err.response.data?.message || '登录失败，请检查您的用户名和密码'
    } else if (err.request) {
      error.value = '服务器无响应，请检查网络连接'
    } else {
      error.value = err.message || '登录时发生错误'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  padding: 20px;
}

.login-form {
  width: 100%;
  max-width: 360px;
  background: white;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

h2 {
  text-align: center;
  margin: 0 0 24px 0;
  color: #333;
  font-weight: 500;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 400;
  color: #333;
}

input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #666;
}

.login-button {
  width: 100%;
  padding: 10px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 10px;
}

.login-button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.register-link {
  margin-top: 15px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #3b82f6;
  text-decoration: none;
}

.error-message {
  padding: 10px;
  background: #fee2e2;
  border-radius: 4px;
  color: #b91c1c;
  margin-bottom: 15px;
  font-size: 14px;
}

.admin-tip {
  margin-top: 15px;
  text-align: center;
  font-size: 14px;
  color: #666;
}
</style> 