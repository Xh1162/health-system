<template>
  <div class="login-page">
    <div class="login-card">
      <h2>欢迎回来</h2>
      <p class="subtitle">登录您的健康助手账号</p>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input 
            type="text" 
            v-model="username"
            placeholder="请输入用户名"
            required
          />
        </div>
        
        <div class="form-group">
          <label>密码</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="password"
              placeholder="请输入密码"
              required
            />
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
            >
              <span class="icon">{{ showPassword ? '⊙' : '⊗' }}</span>
            </button>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" />
            <span>记住我</span>
          </label>
          <a href="#" class="forgot-password">忘记密码?</a>
        </div>

        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        
        <div class="register-link">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import * as authApi from '../api/auth'
import userStore from '../stores/userStore'

const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  error.value = ''

  try {
    console.log('登录请求数据:', { username: username.value, password: '******' })
    
    const response = await authApi.login(username.value, password.value)
    console.log('登录响应:', response)
    
    if (response.success) {
      console.log('登录成功，保存用户信息:', {
        token: response.data.token,
        user: response.data.user
      })
      
      // 保存用户信息
      userStore.login({
        token: response.data.token,
        user: response.data.user
      })
      
      // 检查token是否正确保存
      console.log('登录后localStorage中的token:', localStorage.getItem('token'))
      console.log('登录后userStore中的token:', userStore.state.token)
      console.log('登录后localStorage中的userData:', localStorage.getItem('userData'))
      
      // 如果选择记住我，保存用户名
      if (rememberMe.value) {
        localStorage.setItem('rememberedUsername', username.value)
      } else {
        localStorage.removeItem('rememberedUsername')
      }
      
      // 跳转到仪表板
      console.log('准备跳转到仪表板页面')
      setTimeout(() => {
        router.push('/dashboard')
      }, 500) // 延迟500毫秒，确保数据已保存
    } else {
      console.error('登录失败，服务器返回失败状态:', response)
      error.value = response.message || '登录失败'
    }
  } catch (err) {
    console.error('登录错误:', err)
    if (err.response) {
      console.error('错误响应:', err.response.data)
      error.value = err.response.data.message || '登录失败，请检查用户名和密码'
    } else if (err.request) {
      console.error('未收到响应:', err.request)
      error.value = '服务器无响应，请检查网络连接'
    } else {
      console.error('请求配置错误:', err.message)
      error.value = '登录失败，请检查网络连接'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #64748b;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.password-input {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input input {
  flex: 1;
  padding-right: 4rem;
}

.toggle-password {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  color: #64748b;
  padding: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.toggle-password:hover {
  opacity: 1;
}

.toggle-password .icon {
  display: block;
  line-height: 1;
}

.error-message {
  color: #ef4444;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0 1.5rem;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  cursor: pointer;
}

.remember-me input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.remember-me span {
  user-select: none;
}

.forgot-password {
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover {
  background: #2563eb;
}

.login-button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #64748b;
}

.register-link a {
  color: #3b82f6;
  text-decoration: none;
  margin-left: 0.5rem;
}

.register-link a:hover {
  text-decoration: underline;
}
</style> 