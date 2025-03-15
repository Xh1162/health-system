<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>账号访问</h2>
      <p class="subtitle">选择登录或注册以继续</p>
      
      <div class="auth-options">
        <button @click="goToLogin" class="login-btn">
          <span class="icon">🔑</span>
          <div class="btn-content">
            <span class="btn-title">登录</span>
            <span class="btn-desc">已有账号，直接登录</span>
          </div>
        </button>
        
        <button @click="goToRegister" class="register-btn">
          <span class="icon">✨</span>
          <div class="btn-content">
            <span class="btn-title">注册</span>
            <span class="btn-desc">创建新账号开始健康之旅</span>
          </div>
        </button>
      </div>
      
      <div class="action-buttons">
        <button @click="goBack" class="back-btn">返回</button>
      </div>
      
      <div class="terms">
        <p>继续使用即表示您同意我们的<a href="#">服务条款</a>和<a href="#">隐私政策</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goBack = () => {
  router.push('/user-info')
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  padding: 1rem;
}

.auth-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  width: 90%;
  max-width: 500px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

h2 {
  color: #1e293b;
  margin-bottom: 0.5rem;
  text-align: center;
  font-size: 1.8rem;
}

.subtitle {
  color: #64748b;
  margin-bottom: 2.5rem;
  text-align: center;
  font-size: 1.1rem;
}

.auth-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.login-btn,
.register-btn {
  display: flex;
  align-items: center;
  padding: 1.25rem;
  border-radius: 1rem;
  border: 2px solid #e2e8f0;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.login-btn:hover,
.register-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
}

.login-btn:hover {
  background-color: #f0f9ff;
}

.register-btn:hover {
  background-color: #f0f9ff;
}

.icon {
  font-size: 1.75rem;
  margin-right: 1.25rem;
}

.btn-content {
  display: flex;
  flex-direction: column;
}

.btn-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.btn-desc {
  font-size: 0.9rem;
  color: #64748b;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.back-btn {
  padding: 0.75rem 2rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  background-color: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #f8fafc;
  color: #334155;
}

.terms {
  text-align: center;
  font-size: 0.875rem;
  color: #64748b;
}

.terms a {
  color: #3b82f6;
  text-decoration: none;
}

.terms a:hover {
  text-decoration: underline;
}

@media (max-width: 640px) {
  .auth-card {
    padding: 2rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .btn-title {
    font-size: 1rem;
  }
  
  .btn-desc {
    font-size: 0.875rem;
  }
}
</style> 