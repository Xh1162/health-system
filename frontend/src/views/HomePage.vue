<template>
  <div class="home-page">
    <!-- 欢迎页面 -->
    <div v-if="currentStep === 'welcome'" class="step-container">
      <header class="hero-section">
        <div class="hero-content">
          <h1>健康生活，从现在开始</h1>
          <p class="subtitle">记录、分析、改善您的生活方式</p>
          <div class="cta-buttons">
            <button @click="goToOnboarding" class="primary-btn">
              立即开始
            </button>
            <router-link to="/login" class="secondary-btn">
              登录
            </router-link>
          </div>
        </div>
      </header>

      <main>
        <section class="features-section">
          <h2>主要功能</h2>
          <div class="features-grid">
            <div class="feature-card">
              <div class="icon">🍎</div>
              <h3>饮食记录</h3>
              <p>记录每日饮食，追踪营养摄入</p>
            </div>
            <div class="feature-card">
              <div class="icon">🏃</div>
              <h3>运动追踪</h3>
              <p>记录运动数据，保持健康活力</p>
            </div>
            <div class="feature-card">
              <div class="icon">😊</div>
              <h3>心情日记</h3>
              <p>关注心理健康，记录情绪变化</p>
            </div>
            <div class="feature-card">
              <div class="icon">📊</div>
              <h3>健康报告</h3>
              <p>数据分析，提供健康建议</p>
            </div>
          </div>
        </section>

        <section class="how-it-works">
          <h2>使用流程</h2>
          <div class="steps">
            <div class="step">
              <div class="step-number">1</div>
              <h3>注册账号</h3>
              <p>创建您的个人账号，开始健康之旅</p>
            </div>
            <div class="step">
              <div class="step-number">2</div>
              <h3>记录数据</h3>
              <p>记录您的饮食、运动和心情数据</p>
            </div>
            <div class="step">
              <div class="step-number">3</div>
              <h3>查看报告</h3>
              <p>获取个性化的健康分析报告</p>
            </div>
          </div>
        </section>
      </main>
    </div>

    <!-- 选择原因页面 -->
    <div v-if="currentStep === 'reason'" class="step-container">
      <div class="question-card">
        <h2>为什么选择开始这段健康之旅？</h2>
        <p class="subtitle">选择最符合你心意的原因</p>
        
        <div class="options">
          <div 
            v-for="(option, index) in healthOptions" 
            :key="index"
            class="option-item"
            :class="{ 'selected': selectedReason === index }"
            @click="selectedReason = index"
          >
            <div class="option-content">
              <span class="option-icon">{{ option.icon }}</span>
              <span class="option-text">{{ option.text }}</span>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <button @click="currentStep = 'welcome'" class="back-btn">返回</button>
          <button 
            class="next-btn"
            :disabled="selectedReason === null"
            @click="currentStep = 'activity'"
          >
            继续
          </button>
        </div>
      </div>
    </div>

    <!-- 活动水平页面 -->
    <div v-if="currentStep === 'activity'" class="step-container">
      <div class="activity-card">
        <h2>您平时的运动量是？</h2>
        <p class="subtitle">选择最符合您日常情况的选项</p>
        
        <div class="options">
          <div 
            v-for="(level, index) in activityLevels" 
            :key="index"
            class="option-item"
            :class="{ 'selected': selectedActivity === index }"
            @click="selectedActivity = index"
          >
            <div class="option-content">
              <div class="option-header">
                <span class="option-icon">{{ level.icon }}</span>
                <span class="option-title">{{ level.title }}</span>
              </div>
              <p class="option-description">{{ level.description }}</p>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <button @click="currentStep = 'reason'" class="back-btn">返回</button>
          <button 
            class="next-btn"
            :disabled="selectedActivity === null"
            @click="currentStep = 'userInfo'"
          >
            继续
          </button>
        </div>
      </div>
    </div>

    <!-- 用户信息页面 -->
    <div v-if="currentStep === 'userInfo'" class="step-container">
      <div class="user-info-card">
        <h2>开始您的健康之旅</h2>
        <p class="subtitle">请告诉我们一些基本信息，以便为您提供个性化建议</p>
        
        <form @submit.prevent="goToAuth" class="user-info-form">
          <div class="form-group">
            <label for="height">身高 (cm)</label>
            <div class="number-input">
              <button type="button" @click="decreaseHeight" class="btn-effect">-</button>
              <input 
                type="number" 
                id="height"
                v-model="height"
                min="100"
                max="250"
              />
              <button type="button" @click="increaseHeight" class="btn-effect">+</button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="weight">体重 (kg)</label>
            <div class="number-input">
              <button type="button" @click="decreaseWeight" class="btn-effect">-</button>
              <input 
                type="number" 
                id="weight"
                v-model="weight"
                min="30"
                max="200"
                step="0.1"
              />
              <button type="button" @click="increaseWeight" class="btn-effect">+</button>
            </div>
          </div>
          
          <div class="form-group">
            <label for="birthdate">出生日期</label>
            <input 
              type="date" 
              id="birthdate"
              v-model="birthdate"
              :max="maxDate"
              placeholder="YYYY-MM-DD"
              required
            />
          </div>
          
          <div class="form-group">
            <label>性别</label>
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" v-model="gender" value="male" />
                <span>男</span>
              </label>
              <label class="radio-label">
                <input type="radio" v-model="gender" value="female" />
                <span>女</span>
              </label>
            </div>
          </div>
          
          <div class="form-group">
            <label for="goal">目标</label>
            <select id="goal" v-model="goal">
              <option value="maintain">保持健康</option>
              <option value="lose">健康减重</option>
              <option value="gain">增肌健体</option>
              <option value="balance">均衡营养</option>
            </select>
          </div>
          
          <div class="action-buttons">
            <button type="button" @click="currentStep = 'activity'" class="back-btn">返回</button>
            <button type="submit" class="next-btn">完成</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 账号访问页面 -->
    <div v-if="currentStep === 'auth'" class="step-container">
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
          <button @click="currentStep = 'userInfo'" class="back-btn">返回</button>
        </div>
        
        <div class="terms">
          <p>继续使用即表示您同意我们的<a href="#">服务条款</a>和<a href="#">隐私政策</a></p>
        </div>
      </div>
    </div>

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 健康生活. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = inject('userStore', { state: { isAuthenticated: false } })

// 步骤控制
const currentStep = ref('welcome')

// 健康原因选择
const selectedReason = ref(null)
const healthOptions = [
  { icon: '❤️', text: '为了健康更好的生活' },
  { icon: '💪', text: '想要增强体质' },
  { icon: '⚖️', text: '控制体重' },
  { icon: '🧠', text: '改善心理健康' },
  { icon: '🥗', text: '培养健康饮食习惯' },
  { icon: '🏃', text: '建立运动习惯' }
]

// 活动水平选择
const selectedActivity = ref(null)
const activityLevels = [
  {
    icon: '🧘',
    title: '几乎不运动',
    description: '大部分时间坐着或躺着，很少进行体力活动'
  },
  {
    icon: '🚶',
    title: '轻度活动',
    description: '偶尔散步或做轻度运动，每周1-2次'
  },
  {
    icon: '🏃',
    title: '中度活动',
    description: '定期进行中等强度运动，每周3-4次'
  },
  {
    icon: '🏋️',
    title: '高度活动',
    description: '频繁进行高强度运动，每周5-7次'
  },
  {
    icon: '🏆',
    title: '专业运动员',
    description: '每天进行高强度训练，或从事体力劳动工作'
  }
]

// 用户信息表单
const height = ref(170)
const weight = ref(65)
const birthdate = ref('')
const gender = ref('male')
const goal = ref('maintain')

// 计算最大日期（今天）
const maxDate = computed(() => {
  const today = new Date()
  return today.toISOString().split('T')[0]
})

const increaseHeight = () => {
  if (height.value < 250) height.value++
}

const decreaseHeight = () => {
  if (height.value > 100) height.value--
}

const increaseWeight = () => {
  if (weight.value < 200) weight.value = parseFloat((weight.value + 0.1).toFixed(1))
}

const decreaseWeight = () => {
  if (weight.value > 30) weight.value = parseFloat((weight.value - 0.1).toFixed(1))
}

// 保存用户信息并前往认证页面
const goToAuth = () => {
  // 保存所有收集的信息
  localStorage.setItem('healthReason', healthOptions[selectedReason.value].text)
  localStorage.setItem('activityLevel', activityLevels[selectedActivity.value].title)
  localStorage.setItem('userInfo', JSON.stringify({
    height: height.value,
    weight: weight.value,
    birthdate: birthdate.value,
    gender: gender.value,
    goal: goal.value
  }))
  
  // 前往认证页面
  currentStep.value = 'auth'
}

// 导航到登录/注册页面
const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goToOnboarding = () => {
  router.push('/onboarding')
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e0f7ff 100%);
  color: #0f172a;
  overflow-x: hidden;
}

.step-container {
  min-height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem 1rem;
  position: relative;
}

/* 欢迎页面样式 */
.hero-section {
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.05) 0%, rgba(255, 255, 255, 0) 70%);
  animation: rotate 30s linear infinite;
  z-index: 0;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-content {
  max-width: 800px;
  position: relative;
  z-index: 1;
}

h1 {
  font-size: 4.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e293b 0%, #3b82f6 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  padding-bottom: 0.5rem;
  line-height: 1.1;
  letter-spacing: -0.02em;
  animation: fadeInUp 1s ease-out;
}

.subtitle {
  font-size: 1.8rem;
  color: #64748b;
  margin-bottom: 3rem;
  font-weight: 300;
  animation: fadeInUp 1s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.cta-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  animation: fadeInUp 1s ease-out 0.4s both;
}

.primary-btn,
.secondary-btn,
.next-btn,
.back-btn {
  padding: 1rem 2.5rem;
  border-radius: 3rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 1.1rem;
  letter-spacing: 0.01em;
}

.primary-btn,
.next-btn {
  background: #3b82f6;
  color: white;
  border: none;
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
}

.primary-btn:hover,
.next-btn:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-3px);
  box-shadow: 0 15px 20px -3px rgba(59, 130, 246, 0.4);
}

.secondary-btn,
.back-btn {
  background: rgba(255, 255, 255, 0.8);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.3);
  backdrop-filter: blur(10px);
}

.secondary-btn:hover,
.back-btn:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.next-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
  box-shadow: none;
}

.features-section {
  padding: 8rem 2rem;
  background: white;
  position: relative;
  z-index: 1;
}

.features-section::before {
  content: '';
  position: absolute;
  top: -100px;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(to bottom, transparent, white);
  z-index: -1;
}

h2 {
  text-align: center;
  color: #1e293b;
  font-size: 3rem;
  margin-bottom: 4rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 3rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  text-align: center;
  padding: 3rem 2rem;
  border-radius: 1.5rem;
  background: #f8fafc;
  transition: all 0.5s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(255, 255, 255, 0) 100%);
  opacity: 0;
  transition: opacity 0.5s ease;
}

.feature-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.feature-card:hover::before {
  opacity: 1;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  display: inline-block;
  transition: transform 0.5s ease;
}

.feature-card:hover .icon {
  transform: scale(1.2);
}

.feature-card h3 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.feature-card p {
  color: #64748b;
  font-size: 1.1rem;
  line-height: 1.6;
}

.how-it-works {
  padding: 8rem 2rem;
  background: #f8fafc;
  position: relative;
}

.how-it-works::before {
  content: '';
  position: absolute;
  top: -100px;
  left: 0;
  right: 0;
  height: 200px;
  background: linear-gradient(to bottom, white, #f8fafc);
  z-index: 1;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 3rem;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.step {
  text-align: center;
  padding: 3rem 2rem;
  position: relative;
  transition: transform 0.5s ease;
}

.step:hover {
  transform: translateY(-5px);
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  font-weight: bold;
  font-size: 1.5rem;
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
}

.step h3 {
  color: #1e293b;
  margin-bottom: 1rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.step p {
  color: #64748b;
  font-size: 1.1rem;
  line-height: 1.6;
}

/* 问题卡片样式 */
.question-card,
.activity-card,
.user-info-card,
.auth-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 2rem;
  padding: 3rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  width: 90%;
  max-width: 650px;
  animation: fadeIn 0.8s ease-out;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.5);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-bottom: 3rem;
}

.option-item {
  padding: 1.5rem;
  border-radius: 1.2rem;
  border: 2px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.7);
}

.option-item:hover {
  border-color: #3b82f6;
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.option-item.selected {
  border-color: #3b82f6;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.8) 100%);
  box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);
}

.option-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.option-icon {
  font-size: 2rem;
}

.option-text {
  font-size: 1.2rem;
  color: #1e293b;
  font-weight: 500;
}

.option-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.option-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.option-description {
  color: #64748b;
  font-size: 1rem;
  margin-left: 3.5rem;
  line-height: 1.6;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
}

/* 用户信息表单样式 */
.user-info-form {
  width: 100%;
}

.form-group {
  margin-bottom: 2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.8rem;
  color: #1e293b;
  font-weight: 600;
  font-size: 1.1rem;
}

.number-input {
  display: flex;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border-radius: 0.8rem;
  overflow: hidden;
}

.number-input button {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  border: none;
  width: 4rem;
  height: 3.5rem;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.number-input button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
}

.number-input input {
  flex: 1;
  height: 3.5rem;
  text-align: center;
  border: 1px solid #e2e8f0;
  border-left: none;
  border-right: none;
  font-size: 1.2rem;
  font-weight: 500;
}

input[type="date"],
select {
  width: 100%;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.8rem;
  font-size: 1.1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

input[type="date"]:focus,
select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.radio-group {
  display: flex;
  gap: 3rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  font-size: 1.1rem;
}

.radio-label input[type="radio"] {
  width: 1.2rem;
  height: 1.2rem;
  accent-color: #3b82f6;
}

/* 认证页面样式 */
.auth-options {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.login-btn,
.register-btn {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  border-radius: 1.2rem;
  border: 2px solid #e2e8f0;
  background: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  width: 100%;
}

.login-btn:hover,
.register-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(255, 255, 255, 0.8) 100%);
}

.btn-content {
  display: flex;
  flex-direction: column;
  margin-left: 1.5rem;
}

.btn-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.3rem;
}

.btn-desc {
  font-size: 1rem;
  color: #64748b;
}

.terms {
  text-align: center;
  font-size: 0.95rem;
  color: #64748b;
  margin-top: 2.5rem;
}

.terms a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
}

.terms a:hover {
  text-decoration: underline;
}

.footer {
  background: #1e293b;
  color: white;
  padding: 2rem;
  text-align: center;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  font-size: 1rem;
  letter-spacing: 0.01em;
}

@media (max-width: 768px) {
  h1 {
    font-size: 3rem;
  }
  
  .subtitle {
    font-size: 1.4rem;
  }
  
  .features-grid,
  .steps {
    grid-template-columns: 1fr;
  }
  
  .hero-section {
    height: auto;
    padding-top: 6rem;
    padding-bottom: 6rem;
  }
  
  .question-card,
  .activity-card,
  .user-info-card,
  .auth-card {
    padding: 2.5rem;
  }
  
  .action-buttons {
    flex-direction: column-reverse;
  }
  
  .action-buttons button {
    width: 100%;
  }
  
  h2 {
    font-size: 2.5rem;
  }
  
  .features-section,
  .how-it-works {
    padding: 5rem 2rem;
  }
}

@media (max-width: 480px) {
  h1 {
    font-size: 2.5rem;
  }
  
  .subtitle {
    font-size: 1.2rem;
  }
  
  .primary-btn,
  .secondary-btn,
  .next-btn,
  .back-btn {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
  }
  
  .question-card,
  .activity-card,
  .user-info-card,
  .auth-card {
    padding: 2rem;
  }
  
  .option-text,
  .option-title {
    font-size: 1.1rem;
  }
  
  .option-description {
    font-size: 0.9rem;
  }
  
  .radio-group {
    gap: 1.5rem;
  }
}
</style> 