<template>
  <div class="register-page">
    <div class="register-card">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username"
            v-model="username"
            placeholder="请输入用户名"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            type="password" 
            id="password"
            v-model="password"
            placeholder="请输入密码（至少8位）"
            required
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input 
            type="password" 
            id="confirmPassword"
            v-model="confirmPassword"
            placeholder="请再次输入密码"
            required
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button type="submit" class="register-btn" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
        
        <p class="login-link">
          已有账号？
          <router-link to="/login">立即登录</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../api/auth'

const router = useRouter()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const loading = ref(false)

const handleRegister = async () => {
  try {
    // 验证密码
    if (password.value !== confirmPassword.value) {
      errorMessage.value = '两次输入的密码不一致'
      return
    }

    if (password.value.length < 8) {
      errorMessage.value = '密码长度必须至少为8位'
      return
    }

    loading.value = true
    errorMessage.value = ''
    
    const response = await register({
      username: username.value,
      password: password.value
    })
    
    if (response.success) {
      alert('注册成功！请登录')
      router.push('/login')
    } else {
      errorMessage.value = response.message || '注册失败'
    }
  } catch (error) {
    console.error('注册错误:', error)
    errorMessage.value = error.response?.data?.message || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--background-color);
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.register-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
}

.login-link a {
  color: var(--primary-color);
  text-decoration: none;
}

.error-message {
  color: #ef4444;
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
</style> 