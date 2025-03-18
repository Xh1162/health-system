<template>
  <div class="login-container">
    <div class="debug-info">
      <h3>调试信息</h3>
      <div>
        <strong>认证状态:</strong> {{ userStore.state.isAuthenticated ? '已登录' : '未登录' }}
      </div>
      <div>
        <strong>用户数据:</strong> {{ userStore.state.userData ? '已加载' : '未加载' }}
      </div>
      <pre v-if="userStore.state.userData">{{ JSON.stringify(userStore.state.userData, null, 2) }}</pre>
    </div>
    
    <div class="login-form">
      <h2>健康生活系统登录</h2>
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

// 仅用于测试：自动填入测试凭据
username.value = 'testuser'
password.value = 'password123'

const login = async () => {
  try {
    error.value = ''
    
    if (!username.value || !password.value) {
      error.value = '请输入用户名和密码'
      return
    }
    
    isLoading.value = true
    
    console.log('登录请求:', { username: username.value, password: password.value })
    
    // 调用登录API
    const apiBaseUrl = 'http://localhost:5007'
    const response = await axios.post(`${apiBaseUrl}/api/auth/login`, {
      username: username.value,
      password: password.value
    })
    
    console.log('登录响应:', response.data)
    
    if (response.data.success) {
      // 登录成功，更新用户状态
      userStore.login(response.data.data)
      
      console.log('登录后用户状态:', userStore.state)
      
      // 检查是否有重定向路径
      const redirectPath = route.query.redirect || '/dashboard'
      router.push(redirectPath)
    } else {
      error.value = response.data.message || '登录失败'
    }
  } catch (err) {
    console.error('登录错误:', err)
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

// 调试函数：模拟登录
const simulateLogin = () => {
  const mockData = {
    success: true,
    data: {
      token: 'mock-token-123',
      user: {
        id: '1',
        username: 'testuser',
        email: 'test@example.com',
        avatar: '/uploads/avatars/default.png'
      }
    }
  }
  
  try {
    userStore.login(mockData.data)
    console.log('模拟登录成功!')
    router.push('/dashboard')
  } catch (err) {
    console.error('模拟登录失败:', err)
    error.value = '模拟登录失败: ' + err.message
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-form {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #334155;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #475569;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.login-button {
  width: 100%;
  padding: 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover:not(:disabled) {
  background: #2563eb;
}

.login-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.register-link {
  margin-top: 16px;
  text-align: center;
  font-size: 14px;
  color: #475569;
}

.register-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.register-link a:hover {
  text-decoration: underline;
}

.error-message {
  padding: 12px;
  background: #fee2e2;
  border-radius: 6px;
  color: #b91c1c;
  margin-bottom: 20px;
  font-size: 14px;
}

.debug-info {
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.8);
  padding: 15px;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: auto;
}

.debug-info h3 {
  margin-top: 0;
  color: #334155;
}

.debug-info pre {
  margin: 10px 0 0;
  white-space: pre-wrap;
  word-break: break-all;
  background: #f1f5f9;
  padding: 10px;
  border-radius: 4px;
  font-size: 12px;
  max-height: 200px;
  overflow: auto;
}
</style> 