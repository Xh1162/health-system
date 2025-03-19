<template>
  <div class="dashboard-page">
    <!-- 导航栏 -->
    <header class="glass-header">
      <div class="header-content">
        <div class="logo">健康生活</div>
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-item active">首页</router-link>
          <router-link to="/records" class="nav-item">记录</router-link>
          <router-link to="/reports" class="nav-item">报告</router-link>
        </nav>
        <div class="user-menu" @click="toggleUserMenu" ref="userMenuRef">
          <div class="user-info">
            <div class="avatar">
              <img :src="avatarUrl" :alt="username" />
            </div>
            <span class="username">{{ username }}</span>
            <span class="dropdown-arrow" :class="{ 'rotated': showUserMenu }">▼</span>
          </div>
          
          <!-- 下拉菜单 -->
          <div v-if="showUserMenu" class="user-dropdown">
            <div class="dropdown-header">
              <div class="header-info">
                <span class="signed-in">登录为</span>
                <strong>{{ username }}</strong>
              </div>
            </div>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" class="dropdown-item">
              <span class="item-icon">👤</span>
              个人主页
            </router-link>
            <router-link to="/settings" class="dropdown-item">
              <span class="item-icon">⚙️</span>
              设置
            </router-link>
            <div class="dropdown-divider"></div>
            <button class="dropdown-item" @click="logout">
              <span class="item-icon">🚪</span>
              退出
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="dashboard-content">
      <!-- 大标题区域 -->
      <div class="hero-section">
        <div class="hero-avatar">
          <img :src="avatarUrl" :alt="username" />
        </div>
        <h1 class="hero-title">今天想吃点什么？</h1>
        <p class="hero-subtitle">{{ currentDate }} · {{ currentSeason }}</p>
      </div>

      <!-- 食物推荐区域 -->
      <section class="food-dice-section glass-card">
        <div class="dice-container" v-if="!diceResult">
          <div class="dice-placeholder" @click="rollDice">
            <div class="apple-style-icon">
              <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="40" r="40" fill="rgba(0, 113, 227, 0.08)"/>
                <circle cx="40" cy="40" r="32" fill="white"/>
                <path d="M52 28H28C26.9 28 26 28.9 26 30V50C26 51.1 26.9 52 28 52H52C53.1 52 54 51.1 54 50V30C54 28.9 53.1 28 52 28Z" fill="#0071E3" fill-opacity="0.1"/>
                <path d="M52 28H28C26.9 28 26 28.9 26 30V50C26 51.1 26.9 52 28 52H52C53.1 52 54 51.1 54 50V30C54 28.9 53.1 28 52 28ZM52 50H28V30H52V50Z" fill="#0071E3"/>
                <path d="M35 38C36.66 38 38 36.66 38 35C38 33.34 36.66 32 35 32C33.34 32 32 33.34 32 35C32 36.66 33.34 38 35 38Z" fill="#0071E3"/>
                <path d="M35 40C32.33 40 27 41.34 27 44V46H43V44C43 41.34 37.67 40 35 40Z" fill="#0071E3"/>
                <path d="M45 38C46.66 38 48 36.66 48 35C48 33.34 46.66 32 45 32C43.34 32 42 33.34 42 35C42 36.66 43.34 38 45 38Z" fill="#0071E3"/>
                <path d="M45 40C42.33 40 37 41.34 37 44V46H53V44C53 41.34 47.67 40 45 40Z" fill="#0071E3"/>
              </svg>
            </div>
            <h3 class="apple-style-title">今日饮食推荐</h3>
            <p class="apple-style-description">获取由AI生成的均衡健康饮食方案</p>
            <button class="apple-style-button">
              <span>获取推荐</span>
            </button>
          </div>
        </div>
        <div class="food-recommendation-layout" v-else>
          <h3 class="apple-style-title">今日饮食推荐</h3>
          <div class="apple-style-grid">
            <div class="apple-style-card">
              <div class="card-icon-container">
                <div class="food-svg-icon main-dish-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8.5 14L4 9.5L5.5 8L8.5 11L14.5 5L16 6.5L8.5 14Z" fill="#0071E3"/>
                    <path d="M19 17H5V19H19V17Z" fill="#0071E3"/>
                    <path d="M18 5H15V3H13V5H11V3H9V5H6C4.9 5 4 5.9 4 7V9.15C4 10.04 4.39 10.86 5.03 11.45L10.5 16.47V21H13.5V16.47L18.97 11.45C19.61 10.86 20 10.04 20 9.15V7C20 5.9 19.1 5 18 5Z" fill="#0071E3" fill-opacity="0.2"/>
                  </svg>
                </div>
                <span class="card-icon-text">{{ diceResult.mainDish.icon }}</span>
              </div>
              <div class="card-content">
                <span class="card-label">主菜</span>
                <span class="card-name">{{ diceResult.mainDish.name }}</span>
              </div>
            </div>
            <div class="apple-style-card">
              <div class="card-icon-container">
                <div class="food-svg-icon staple-food-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C8.43 2 5.23 3.54 3.01 6L12 22L20.99 6C18.78 3.55 15.57 2 12 2ZM12 17.92L5.51 6.36C7.32 4.85 9.62 4 12 4C14.38 4 16.68 4.85 18.49 6.36L12 17.92Z" fill="#0071E3" fill-opacity="0.2"/>
                    <path d="M7.5 10H16.5V12H7.5V10Z" fill="#0071E3"/>
                  </svg>
                </div>
                <span class="card-icon-text">{{ diceResult.stapleFood.icon }}</span>
              </div>
              <div class="card-content">
                <span class="card-label">主食</span>
                <span class="card-name">{{ diceResult.stapleFood.name }}</span>
              </div>
            </div>
            <div class="apple-style-card">
              <div class="card-icon-container">
                <div class="food-svg-icon vegetable-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M16.53 11.06L15.47 10L10.59 14.88L8.47 12.76L7.41 13.82L10.59 17L16.53 11.06Z" fill="#0071E3"/>
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#0071E3" fill-opacity="0.2"/>
                  </svg>
                </div>
                <span class="card-icon-text">{{ diceResult.vegetable.icon }}</span>
              </div>
              <div class="card-content">
                <span class="card-label">蔬菜</span>
                <span class="card-name">{{ diceResult.vegetable.name }}</span>
              </div>
            </div>
            <div class="apple-style-card">
              <div class="card-icon-container">
                <div class="food-svg-icon fruit-icon">
                  <svg viewBox="0 0 24 24" width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="#0071E3" fill-opacity="0.2"/>
                    <path d="M12 17L17 12H14V7H10V12H7L12 17Z" fill="#0071E3"/>
                  </svg>
                </div>
                <span class="card-icon-text">{{ diceResult.fruit.icon }}</span>
              </div>
              <div class="card-content">
                <span class="card-label">水果</span>
                <span class="card-name">{{ diceResult.fruit.name }}</span>
              </div>
            </div>
          </div>
          
          <!-- 健康提醒和小贴士轮流显示 -->
          <div class="apple-style-tips" v-if="diceResult">
            <div class="tips-header">
              <span class="tips-icon">{{ showHealthReminder ? '💡' : '✨' }}</span>
              <span class="tips-title">{{ showHealthReminder ? '健康提醒' : '今日小贴士' }}</span>
            </div>
            <p class="tips-content" v-if="showHealthReminder">
              在追求美食的同时，请珍爱健康：
              <br>• 均衡饮食是关键，多样化搭配更营养
              <br>• 适量进食，既不过量也不过度节食
              <br>• 细嚼慢咽，感受食物的真实味道
              <br>• 定时定量，建立健康的饮食习惯
            </p>
            <p class="tips-content" v-else>
              美食的快乐是生活中不可或缺的调味剂~ 
              <br>• 健康饮食≠苦行僧，偶尔放纵一下也是可以的！
              <br>• 不喜欢清淡？可以试试适量调味，让美味和健康达到平衡
              <br>• 想吃炸物的时候，选择空气炸锅会更健康一些哦
            </p>
          </div>
          
          <div class="apple-style-actions" v-if="diceResult">
            <button class="apple-secondary-button" @click="rollDice" :disabled="isRolling">
              {{ isRolling ? '生成中...' : '重新生成' }}
            </button>
            <button class="apple-primary-button" @click="confirmRecommendation">
              <span>添加到今日计划</span>
            </button>
          </div>
        </div>
      </section>

      <!-- 快捷记录区 -->
      <div class="quick-actions">
        <div class="action-card" @click="(e) => showRecordDialog('food', e)">
          <div class="action-icon-wrapper">
            <span class="action-icon">🍽️</span>
          </div>
          <span class="action-text">饮食记录</span>
        </div>
        <div class="action-card" @click="(e) => showRecordDialog('exercise', e)">
          <div class="action-icon-wrapper">
            <span class="action-icon">🏃</span>
          </div>
          <span class="action-text">运动记录</span>
        </div>
        <div class="action-card" @click="(e) => showRecordDialog('mood', e)">
          <div class="action-icon-wrapper">
            <span class="action-icon">😊</span>
          </div>
          <span class="action-text">心情记录</span>
        </div>
        <div class="action-card" @click="(e) => showRecordDialog('health', e)">
          <div class="action-icon-wrapper">
            <span class="action-icon">💪</span>
          </div>
          <span class="action-text">身体状况记录</span>
        </div>
      </div>

      <!-- 记录对话框 -->
      <div v-if="isDialogVisible" class="record-dialog-overlay" @click="closeDialogOnOverlayClick">
        <div class="record-dialog" @click.stop>
        <div class="dialog-content">
          <div class="dialog-header">
            <h3>{{ getDialogTitle() }}</h3>
            <button class="close-btn" @click="closeDialog">×</button>
          </div>

          <!-- 日期选择器 - 添加到所有记录表单的顶部 -->
          <div class="section-title">选择日期</div>
          <div class="date-selector">
            <input 
              type="date" 
              v-model="selectedDate"
              class="date-input"
              :max="maxDate"
            />
          </div>

          <!-- 食物记录 -->
          <div v-if="recordType === 'food'" class="record-form">
            <div class="section-title">用餐时间</div>
            <div class="meal-time-buttons">
              <button 
                v-for="meal in mealTimes" 
                :key="meal.value"
                class="meal-time-btn"
                :class="{ active: selectedMealTime === meal.value }"
                @click="selectMealTime(meal.value)"
              >
                <span class="meal-icon">{{ meal.icon }}</span>
                <span class="meal-label">{{ meal.label }}</span>
              </button>
            </div>

            <div class="section-title">食物名称</div>
            <input 
              type="text" 
              v-model="foodName"
              class="food-input"
              placeholder="输入食物名称"
            />

            <div class="section-title">常见食物</div>
            <div class="common-foods-grid">
              <button 
                v-for="food in currentCommonFoods" 
                :key="food.name"
                class="food-btn"
                @click="selectFood(food)"
              >
                <span class="food-icon">{{ food.icon }}</span>
                <span class="food-label">{{ food.name }}</span>
              </button>
            </div>

            <div class="section-title">备注</div>
            <textarea 
              v-model="foodNote"
              class="food-note"
              placeholder="添加备注..."
            ></textarea>
          </div>

          <!-- 运动记录 -->
          <div v-if="recordType === 'exercise'" class="record-form">
            <div class="section-title">运动类型</div>
            <div class="exercise-type-grid">
              <button 
                v-for="exercise in exerciseTypes" 
                :key="exercise.type"
                class="exercise-type-btn"
                :class="{ active: selectedExercise === exercise.type }"
                @click="selectExercise(exercise.type)"
              >
                <span class="exercise-icon">{{ exercise.icon }}</span>
                <span class="exercise-label">{{ exercise.label }}</span>
              </button>
            </div>

            <div class="section-title">运动时长</div>
            <div class="duration-input">
              <input 
                type="number" 
                v-model="exerciseDuration" 
                placeholder="输入时长"
                class="time-input"
              />
              <span class="time-unit">分钟</span>
            </div>

            <div class="section-title">运动强度</div>
            <div class="intensity-buttons">
              <button 
                v-for="intensity in intensityLevels" 
                :key="intensity.level"
                class="intensity-btn"
                :class="{ active: selectedIntensity === intensity.level }"
                @click="selectIntensity(intensity.level)"
              >
                <span class="intensity-icon">{{ intensity.icon }}</span>
                <span class="intensity-label">{{ intensity.label }}</span>
              </button>
            </div>
            
            <div class="section-title">备注</div>
            <textarea 
              v-model="exerciseNote"
              class="exercise-note"
              placeholder="添加备注..."
            ></textarea>
          </div>

          <!-- 心情记录 -->
          <div v-if="recordType === 'mood'" class="record-form">
            <div class="section-title">今日心情</div>
            <div class="mood-grid">
              <button 
                v-for="mood in moods" 
                :key="mood.type"
                class="mood-btn"
                :class="{ active: selectedMood === mood.type }"
                @click="selectMood(mood.type)"
              >
                <span class="mood-icon">{{ mood.icon }}</span>
                <span class="mood-label">{{ mood.label }}</span>
              </button>
            </div>

            <div class="section-title">心情小记</div>
            <textarea 
              v-model="moodNote"
              class="mood-note"
              :placeholder="'记录一下此刻的想法...\n\n可以写写：\n- 发生了什么事\n- 当下的感受\n- 想对自己说的话'"
            ></textarea>
          </div>

          <!-- 身体感受记录 -->
          <div v-if="recordType === 'health'" class="record-form">
            <div class="section-title">整体感受</div>
            <div class="feeling-grid">
              <button 
                v-for="feeling in feelings" 
                :key="feeling.type"
                class="feeling-btn"
                :class="{ active: selectedFeeling === feeling.type }"
                @click="selectFeeling(feeling.type)"
              >
                <span class="feeling-icon">{{ feeling.icon }}</span>
                <span class="feeling-label">{{ feeling.label }}</span>
              </button>
            </div>

            <div class="section-title">身体状态</div>
            <div class="status-tags">
              <button 
                v-for="status in healthStatus" 
                :key="status.type"
                class="status-tag"
                :class="{ active: selectedStatus.includes(status.type) }"
                @click="toggleStatus(status.type)"
              >
                {{ status.icon }} {{ status.label }}
              </button>
            </div>

            <div class="section-title">备注</div>
            <textarea 
              v-model="healthNote"
              class="health-note"
              placeholder="添加备注..."
            ></textarea>
          </div>

          <div class="dialog-footer">
            <button class="cancel-btn" @click="closeDialog">取消</button>
            <button class="submit-btn" @click="submitRecord">记录</button>
          </div>
        </div>
        </div>
      </div>

      <!-- 成功提示 -->
      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted, onUnmounted, nextTick, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { createExerciseRecord, createMoodRecord, createHealthRecord, createFoodRecord, getAllRecords } from '../api/records'
import { getUserDashboard } from '../api/user'
import RecordForm from '../components/records/RecordForm.vue'

const router = useRouter()
const userStore = inject('userStore')

// 用户信息
const username = computed(() => userStore.state.username || '用户')
const avatarUrl = computed(() => {
  // 直接从userStore获取avatar，它已经在userStore中被处理成完整URL
  const avatar = userStore.state.userData?.avatar
  
  if (!avatar) {
    // 默认头像
    return 'http://localhost:5007/default-avatar.png'
  }
  
  console.log('使用头像URL:', avatar)
  return avatar
})

// 日期和季节
const now = new Date()
const currentDate = ref(now.toLocaleDateString('zh-CN', { 
  month: 'long', 
  day: 'numeric', 
  weekday: 'long' 
}))

const seasons = ['春季', '夏季', '秋季', '冬季']
const currentMonth = now.getMonth()
const currentSeason = ref(seasons[Math.floor(currentMonth / 3) % 4])

// 食物推荐
const isRolling = ref(false)
const diceResult = ref(null)
const showHealthReminder = ref(false)
const particleIcons = ['🍎', '🥦', '🍚', '🍗', '🥩', '🐟']
let tipsSwitchTimer = null // 定义定时器变量

// 食物数据库（示例）
const foodDatabase = {
  mainDish: [
    { name: '牛排', icon: '🥩' },
    { name: '三文鱼', icon: '🐟' },
    { name: '鸡胸肉', icon: '🍗' },
    { name: '带鱼', icon: '🐟' }
  ],
  stapleFood: [
    { name: '糙米饭', icon: '🍚' },
    { name: '全麦面包', icon: '🍞' },
    { name: '燕麦片', icon: '🥣' },
    { name: '红薯', icon: '🍠' },
    { name: '藜麦', icon: '🌾' }
  ],
  vegetables: [
    { name: '西兰花', icon: '🥦' },
    { name: '菠菜', icon: '🥬' },
    { name: '胡萝卜', icon: '🥕' },
    { name: '南瓜', icon: '🎃' }
  ],
  fruits: [
    { name: '苹果', icon: '🍎' },
    { name: '橙子', icon: '🍊' },
    { name: '香蕉', icon: '🍌' },
    { name: '蓝莓', icon: '🫐' }
  ]
}

// 随机选择食物
const rollDice = () => {
  if (isRolling.value) return;
  
  isRolling.value = true
  
  // 添加动画效果
  const animationDuration = 1500; // 1.5秒
  
  setTimeout(() => {
    diceResult.value = {
      mainDish: foodDatabase.mainDish[Math.floor(Math.random() * foodDatabase.mainDish.length)],
      stapleFood: foodDatabase.stapleFood[Math.floor(Math.random() * foodDatabase.stapleFood.length)],
      vegetable: foodDatabase.vegetables[Math.floor(Math.random() * foodDatabase.vegetables.length)],
      fruit: foodDatabase.fruits[Math.floor(Math.random() * foodDatabase.fruits.length)]
    }
    // 随机决定显示健康提醒还是小贴士
    showHealthReminder.value = Math.random() > 0.5
    isRolling.value = false
  }, animationDuration)
}

const getRecommendation = () => {
  // 这里可以根据用户的健康数据和偏好提供更个性化的推荐
  // 目前简单实现为重新随机
  rollDice()
}

const confirmRecommendation = () => {
  // 这里可以添加确认推荐的逻辑，例如保存到用户的饮食计划中
  showSuccessMessage('已将推荐添加到今日饮食计划')
}

// 记录对话框状态
const isDialogVisible = ref(false)
const recordType = ref('')
const isSubmitting = ref(false) // 添加提交状态变量

// 选中状态
const selectedExercise = ref('')
const exerciseDuration = ref('')
const selectedIntensity = ref('')
const selectedMood = ref('')
const moodNote = ref('')
const selectedFeeling = ref('')
const selectedStatus = ref([])
const healthNote = ref('')

// 食物记录相关状态
const selectedMealTime = ref('')
const foodName = ref('')
const foodNote = ref('')

// 运动记录相关状态
const exerciseNote = ref('')

// 方法
const getDialogTitle = () => {
  const titles = {
    food: '记录饮食',
    exercise: '记录运动',
    mood: '记录心情',
    health: '身体感受'
  }
  return titles[recordType.value] || ''
}

const showRecordDialog = (type) => {
  recordType.value = type
  resetForm() // 先重置表单
  nextTick(() => {
    isDialogVisible.value = true // 然后显示对话框
  })
}

const closeDialog = () => {
  isDialogVisible.value = false
  // 重置食物记录表单
  selectedMealTime.value = ''
  foodName.value = ''
  foodNote.value = ''
  // 重置其他表单数据
  selectedExercise.value = ''
  exerciseDuration.value = ''
  selectedIntensity.value = ''
  exerciseNote.value = ''
  selectedMood.value = ''
  moodNote.value = ''
  selectedFeeling.value = ''
  selectedStatus.value = []
  healthNote.value = ''
}

const resetForm = () => {
  // 重置表单状态
  selectedDate.value = today.toISOString().split('T')[0] // 重置为今天
  selectedMealTime.value = ''
  foodName.value = ''
  foodNote.value = ''
  selectedExercise.value = ''
  exerciseDuration.value = ''
  selectedIntensity.value = ''
  exerciseNote.value = ''
  selectedMood.value = ''
  moodNote.value = ''
  selectedFeeling.value = ''
  selectedStatus.value = []
  healthNote.value = ''
}

const selectExercise = (type) => {
  selectedExercise.value = type
}

const selectIntensity = (level) => {
  selectedIntensity.value = level
}

const selectMood = (type) => {
  selectedMood.value = type
}

const selectFeeling = (type) => {
  selectedFeeling.value = type
}

const toggleStatus = (type) => {
  const index = selectedStatus.value.indexOf(type)
  if (index === -1) {
    selectedStatus.value.push(type)
  } else {
    selectedStatus.value.splice(index, 1)
  }
}

// 提交记录
const submitRecord = async () => {
  try {
    isSubmitting.value = true
    console.log('开始提交记录，类型:', recordType.value)
    
    // 验证表单
    if (recordType.value === 'food') {
      if (!selectedMealTime.value) {
        alert('请选择用餐时间')
        return
      }
      if (!foodName.value) {
        alert('请输入食物名称')
        return
      }
      
      // 准备数据
      const data = {
        food_name: foodName.value,
        meal_time: selectedMealTime.value,
        note: foodNote.value,
        record_date: selectedDate.value // 添加选择的日期
      }
      
      console.log('提交食物记录数据:', data)
      
      // 使用API模块提交
      await createFoodRecord(data)
      showSuccessMessage('饮食记录已保存')
    } else if (recordType.value === 'exercise') {
      if (!selectedExercise.value) {
        alert('请选择运动类型')
        return
      }
      if (!exerciseDuration.value) {
        alert('请输入运动时长')
        return
      }
      
      // 准备数据
      const data = {
        exercise_type: selectedExercise.value,
        duration: parseInt(exerciseDuration.value),
        intensity: selectedIntensity.value || 'medium',
        note: exerciseNote.value,
        record_date: selectedDate.value // 添加选择的日期
      }
      
      console.log('提交运动记录数据:', data)
      
      // 使用API模块提交
      await createExerciseRecord(data)
      showSuccessMessage('运动记录已保存')
    } else if (recordType.value === 'mood') {
      if (!selectedMood.value) {
        alert('请选择心情类型')
        return
      }
      
      // 准备数据
      const data = {
        mood_type: selectedMood.value,
        note: moodNote.value,
        record_date: selectedDate.value // 添加选择的日期
      }
      
      console.log('提交心情记录数据:', data)
      
      // 使用API模块提交
      await createMoodRecord(data)
      showSuccessMessage('心情记录已保存')
    } else if (recordType.value === 'health') {
      if (!selectedFeeling.value) {
        alert('请选择身体感受')
        return
      }
      
      // 准备数据
      const data = {
        feeling: selectedFeeling.value,
        status: selectedStatus.value,
        note: healthNote.value,
        record_date: selectedDate.value // 添加选择的日期
      }
      
      console.log('提交健康记录数据:', data)
      
      // 使用API模块提交
      await createHealthRecord(data)
      showSuccessMessage('身体状况已记录')
    }
    
    // 成功提交后清空表单
    resetForm()
    closeDialog()
  } catch (error) {
    console.error('提交记录失败:', error)
    if (error.response) {
      alert(`提交失败: ${error.response.data?.message || '请重试'}`)
    } else if (error.request) {
      alert('服务器无响应，请检查网络连接')
    } else {
      alert(`提交失败: ${error.message || '未知错误'}`)
    }
  } finally {
    isSubmitting.value = false
  }
}

// 成功提示
const successMessage = ref('')
const showSuccessMessage = (message) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

// 登出功能
const logout = () => {
  userStore.logout()
  router.push('/login')
}

const userMenuRef = ref(null)
const showUserMenu = ref(false)

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const closeUserMenu = (event) => {
  // 如果点击的不是用户菜单区域，则关闭菜单
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

// 添加全局点击事件监听器
onMounted(() => {
  // 查询记录数据
  queryRecords()
  
  // 生成随机的食物推荐
  generateFoodRecommendation()
  
  // 获取仪表盘数据
  fetchDashboardData()
})

onBeforeUnmount(() => {
  // 清除定时器
  if (tipsSwitchTimer) {
    clearInterval(tipsSwitchTimer)
  }
  
  // 移除事件监听
  document.removeEventListener('click', handleClickOutside)
})

// 食物相关方法
const mealTimes = [
  { value: 'breakfast', label: '早餐', icon: '🌅' },
  { value: 'lunch', label: '午餐', icon: '☀️' },
  { value: 'dinner', label: '晚餐', icon: '🌙' },
  { value: 'snack', label: '零食', icon: '🍪' }
]

const commonFoods = {
  breakfast: [
    { name: '牛奶', icon: '🥛' },
    { name: '鸡蛋', icon: '🥚' },
    { name: '面包', icon: '🍞' },
    { name: '燕麦', icon: '🥣' },
    { name: '豆浆', icon: '🫖' },
    { name: '包子', icon: '🧆' },
    { name: '粥', icon: '🍚' },
    { name: '水果', icon: '🍎' }
  ],
  lunch: [
    { name: '米饭', icon: '🍚' },
    { name: '面条', icon: '🍜' },
    { name: '鸡肉', icon: '🍗' },
    { name: '牛肉', icon: '🥩' },
    { name: '鱼', icon: '🐟' },
    { name: '蔬菜', icon: '🥦' },
    { name: '沙拉', icon: '🥗' },
    { name: '汤', icon: '🍲' }
  ],
  dinner: [
    { name: '米饭', icon: '🍚' },
    { name: '面条', icon: '🍜' },
    { name: '鸡肉', icon: '🍗' },
    { name: '牛肉', icon: '🥩' },
    { name: '鱼', icon: '🐟' },
    { name: '蔬菜', icon: '🥦' },
    { name: '豆腐', icon: '🧊' },
    { name: '汤', icon: '🍲' }
  ],
  snack: [
    { name: '水果', icon: '🍎' },
    { name: '坚果', icon: '🥜' },
    { name: '酸奶', icon: '🥛' },
    { name: '饼干', icon: '🍪' },
    { name: '巧克力', icon: '🍫' },
    { name: '蛋糕', icon: '🍰' },
    { name: '薯片', icon: '🍟' },
    { name: '冰淇淋', icon: '🍦' }
  ]
}

const currentCommonFoods = computed(() => {
  if (!selectedMealTime.value) return []
  return commonFoods[selectedMealTime.value] || []
})

const selectMealTime = (time) => {
  selectedMealTime.value = time
}

const selectFood = (food) => {
  if (foodName.value) {
    foodName.value += '、'
  }
  foodName.value += food.name
}

// 运动类型
const exerciseTypes = [
  { type: 'walk', label: '步行', icon: '🚶' },
  { type: 'run', label: '跑步', icon: '🏃' },
  { type: 'bike', label: '骑行', icon: '🚴' },
  { type: 'swim', label: '游泳', icon: '🏊' },
  { type: 'yoga', label: '瑜伽', icon: '🧘' },
  { type: 'gym', label: '健身', icon: '💪' },
  { type: 'ball', label: '球类', icon: '⚽' },
  { type: 'other', label: '其他', icon: '✨' }
]

// 运动强度
const intensityLevels = [
  { level: 'light', label: '轻度', icon: '🌱' },
  { level: 'medium', label: '中度', icon: '🌿' },
  { level: 'high', label: '剧烈', icon: '🌳' }
]

// 心情类型
const moods = [
  { type: 'happy', label: '开心', icon: '😊' },
  { type: 'calm', label: '平静', icon: '😌' },
  { type: 'sad', label: '难过', icon: '😔' },
  { type: 'angry', label: '生气', icon: '😠' },
  { type: 'anxious', label: '焦虑', icon: '😰' },
  { type: 'tired', label: '疲惫', icon: '😫' },
  { type: 'excited', label: '兴奋', icon: '🤩' },
  { type: 'bored', label: '无聊', icon: '😑' }
]

const feelings = [
  { type: 'energetic', label: '精力充沛', icon: '⚡️', description: '活力满满，可以开始运动或工作' },
  { type: 'good', label: '状态不错', icon: '👍', description: '身体机能正常，没有不适' },
  { type: 'normal', label: '一般般', icon: '😐', description: '基本正常，有轻微疲劳' },
  { type: 'tired', label: '有点累', icon: '😪', description: '需要休息，注意补充能量' }
]

const healthStatus = [
  { type: 'sleep_well', label: '睡眠充足', icon: '😴', category: 'sleep' },
  { type: 'sleep_bad', label: '睡眠不足', icon: '🥱', category: 'sleep' },
  { type: 'appetite_good', label: '胃口好', icon: '😋', category: 'appetite' },
  { type: 'appetite_bad', label: '没胃口', icon: '🤢', category: 'appetite' },
  { type: 'energetic', label: '精力充沛', icon: '💪', category: 'energy' },
  { type: 'fatigue', label: '疲劳乏力', icon: '😫', category: 'energy' },
  { type: 'muscle_sore', label: '肌肉酸痛', icon: '🏋️', category: 'body' },
  { type: 'headache', label: '头疼', icon: '🤕', category: 'body' },
  { type: 'throat', label: '咽喉不适', icon: '😷', category: 'body' },
  { type: 'stomach', label: '胃部不适', icon: '🤮', category: 'body' },
  { type: 'cold', label: '感冒发烧', icon: '🤒', category: 'body' },
  { type: 'allergy', label: '过敏', icon: '🤧', category: 'body' }
]

const closeDialogOnOverlayClick = (event) => {
  // 只有当点击的是遮罩层本身时才关闭对话框
  if (event.target.classList.contains('record-dialog-overlay')) {
    closeDialog()
  }
}

// 生命周期钩子
onMounted(() => {
  // 查询记录数据
  queryRecords()
  
  // 生成随机的食物推荐
  generateFoodRecommendation()
  
  // 获取仪表盘数据
  fetchDashboardData()
})

onBeforeUnmount(() => {
  // 清除定时器
  if (tipsSwitchTimer) {
    clearInterval(tipsSwitchTimer)
  }
  
  // 移除事件监听
  document.removeEventListener('click', handleClickOutside)
})

// 添加点击外部关闭用户菜单的事件监听
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

// 生成随机的食物推荐
const generateFoodRecommendation = () => {
  // 这里可以添加生成食物推荐的逻辑
  console.log('生成随机的食物推荐')
}

// 获取用户信息
const fetchUserInfo = () => {
  // 这里可以添加获取用户信息的逻辑
  console.log('获取用户信息')
}

// 获取记录统计
const fetchRecordsStats = () => {
  // 这里可以添加获取记录统计的逻辑
  console.log('获取记录统计')
}

// 获取最近记录
const fetchRecentRecords = () => {
  // 这里可以添加获取最近记录的逻辑
  console.log('获取最近记录')
}

// 获取公告
const fetchAnnouncements = () => {
  // 这里可以添加获取公告的逻辑
  console.log('获取公告')
}

// 日期选择器相关状态
const today = new Date()
const maxDate = ref(today.toISOString().split('T')[0]) // 今天的日期，格式为YYYY-MM-DD
const selectedDate = ref(today.toISOString().split('T')[0]) // 默认选择今天

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    console.log('正在刷新仪表盘数据...')
    const response = await getUserDashboard()
    // 处理仪表盘数据
    console.log('仪表盘数据已更新:', response)
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

// 查询用户记录
const queryRecords = async () => {
  try {
    console.log('正在查询用户记录...')
    const response = await getAllRecords(7) // 获取最近7天的记录
    // 处理记录数据
    console.log('用户记录已更新:', response)
  } catch (error) {
    console.error('获取用户记录失败:', error)
  }
}
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  padding-bottom: 2rem;
}

/* 毛玻璃效果导航栏 */
.glass-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.main-nav {
  display: flex;
  gap: 2rem;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.nav-item {
  color: #1e293b;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  position: relative;
  transition: all 0.3s ease;
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  transition: width 0.3s ease;
}

.nav-item:hover::after,
.nav-item.active::after {
  width: 100%;
}

/* 内容区域 */
.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 1.5rem 2rem;
}

/* 英雄区域 */
.hero-section {
  text-align: center;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 1.5rem;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.hero-avatar:hover {
  transform: scale(1.05);
}

.hero-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1rem;
  color: #64748b;
}

/* 主要功能卡片区域 */
.dashboard-section {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1e293b;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.exercise-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.2s;
  cursor: pointer;
}

.exercise-btn.active {
  background: #f5f5f7;
  border-color: #0066cc;
  color: #0066cc;
}

.exercise-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.exercise-label {
  font-size: 14px;
}

/* 时长输入 */
.duration-input {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.time-input {
  flex: 1;
  padding: 12px 16px;
  font-size: 17px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
}

.time-unit {
  font-size: 17px;
  color: #86868b;
}

/* 强度按钮 */
.intensity-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.intensity-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.2s;
  cursor: pointer;
}

.intensity-btn.active {
  background: #f5f5f7;
  border-color: #0066cc;
  color: #0066cc;
}

/* 心情网格 */
.mood-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.mood-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.mood-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d0d0d5;
}

.mood-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.15);
}

.mood-icon {
  font-size: 28px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.mood-btn:hover .mood-icon,
.mood-btn.active .mood-icon {
  transform: scale(1.1);
}

.mood-label {
  font-size: 14px;
  font-weight: 500;
}

/* 身体感受网格 */
.feeling-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.feeling-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.feeling-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d0d0d5;
}

.feeling-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.15);
}

.feeling-icon {
  font-size: 28px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.feeling-btn:hover .feeling-icon,
.feeling-btn.active .feeling-icon {
  transform: scale(1.1);
}

.feeling-label {
  font-size: 14px;
  font-weight: 500;
}

/* 身体状态标签 */
.status-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 24px;
}

.status-tag {
  padding: 8px 16px;
  border-radius: 100px;
  background: #f5f5f7;
  border: 1px solid #e5e5e7;
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.status-tag:hover {
  background: #f0f0f2;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.status-tag.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.15);
}

/* 对话框底部按钮 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn, .submit-btn {
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  border: none;
}

.cancel-btn {
  background: #f5f5f7;
  color: #1a1a1a;
}

.cancel-btn:hover {
  background: #e5e5e7;
}

.submit-btn {
  background: #0071e3;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.25);
}

.submit-btn:hover {
  background: #0077ed;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 113, 227, 0.3);
}

.submit-btn:active, .cancel-btn:active {
  transform: scale(0.98);
}

/* 成功提示 */
.success-message {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(52, 199, 89, 0.9);
  color: white;
  padding: 12px 24px;
  border-radius: 100px;
  font-size: 16px;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1100;
  animation: messageSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1), messageFadeOut 0.3s ease 2.7s forwards;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

@keyframes messageSlideUp {
  from {
    opacity: 0;
    transform: translate(-50%, 20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

@keyframes messageFadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .food-recommendation-layout {
    grid-template-columns: 1fr;
  }
  
  .tip-reminder {
    grid-column: 1;
    grid-row: 2;
    margin-top: 1rem;
    padding: 1rem;
  }
}

@media (max-width: 768px) {
  .food-categories {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .category-icon {
    font-size: 2rem;
  }
  
  .category-name {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .food-categories {
    grid-template-columns: 1fr;
  }
  
  .food-category {
    padding: 1.2rem;
  }
}

@media (max-width: 768px) {
  .food-categories {
    grid-template-columns: 1fr;
  }
  
  .food-recommendation-layout {
    gap: 1rem;
  }
  
  .quick-actions {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .dashboard-content {
    padding: 4rem 1rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .food-categories {
    grid-template-columns: 1fr;
  }
  
  .exercise-type-grid,
  .mood-grid,
  .feeling-grid,
  .meal-time-buttons,
  .common-foods-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dialog-content {
    padding: 20px;
  }
  
  .section-title {
    font-size: 16px;
  }
  
  .record-dialog {
    width: 95vw;
    max-height: 80vh;
  }
}

/* 快捷记录区 */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-card {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: all 0.3s ease;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #f5f5f7;
}

.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.action-card:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.action-icon-wrapper {
  width: 56px;
  height: 56px;
  margin: 0 auto 0.75rem;
  background: #f0f7ff;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-card:hover .action-icon-wrapper {
  transform: scale(1.05);
  background: #e0f2fe;
}

.action-icon {
  font-size: 1.8rem;
}

.action-text {
  font-size: 1rem;
  font-weight: 500;
  color: #1d1d1f;
}

/* 按钮样式优化 */
.primary-btn, .confirm-btn {
  padding: 0.6rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn {
  background: #3b82f6;
  color: white;
  border: none;
}

.primary-btn:hover {
  background: #2563eb;
}

.primary-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.confirm-btn {
  background: #10b981;
  color: white;
  border: none;
}

.confirm-btn:hover {
  background: #059669;
}

/* 食物推荐区域样式 */
.food-dice-section {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  border: none;
  margin-bottom: 2rem;
}

.dice-container {
  padding: 2rem;
}

.dice-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
}

.apple-style-icon {
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease;
}

.dice-placeholder:hover .apple-style-icon {
  transform: scale(1.05);
}

.apple-style-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 0.75rem;
  letter-spacing: -0.02em;
}

.apple-style-description {
  font-size: 1.1rem;
  color: #86868b;
  margin-bottom: 2rem;
  max-width: 400px;
}

.apple-style-button {
  background: #0071e3;
  color: white;
  border: none;
  padding: 0.85rem 2rem;
  border-radius: 980px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.apple-style-button:hover {
  background: #0077ed;
  transform: scale(1.02);
}

.food-recommendation-layout {
  padding: 2rem;
}

.apple-style-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.apple-style-card {
  background: #f5f5f7;
  border-radius: 12px;
  padding: 1.2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.apple-style-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
}

.card-icon-container {
  width: 48px;
  height: 48px;
  background: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
}

.food-svg-icon {
  position: absolute;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon-text {
  font-size: 1.8rem;
  position: relative;
  z-index: 2;
}

.main-dish-icon svg {
  fill: #0071E3;
}

.staple-food-icon svg {
  fill: #0071E3;
}

.vegetable-icon svg {
  fill: #0071E3;
}

.fruit-icon svg {
  fill: #0071E3;
}

.card-content {
  display: flex;
  flex-direction: column;
}

.card-label {
  font-size: 0.8rem;
  color: #86868b;
  margin-bottom: 0.25rem;
}

.card-name {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1d1d1f;
}

.apple-style-tips {
  background: #f5f5f7;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.tips-header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.tips-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

.tips-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1d1d1f;
}

.tips-content {
  line-height: 1.6;
  color: #515154;
  font-size: 0.95rem;
}

.apple-style-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.apple-primary-button {
  background: #0071e3;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 980px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.apple-primary-button:hover {
  background: #0077ed;
  transform: scale(1.02);
}

.apple-secondary-button {
  background: #f5f5f7;
  color: #1d1d1f;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 980px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.apple-secondary-button:hover {
  background: #e8e8ed;
  transform: scale(1.02);
}

.apple-secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .apple-style-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .apple-style-title {
    font-size: 1.5rem;
  }
  
  .apple-style-description {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .apple-style-grid {
    grid-template-columns: 1fr;
  }
  
  .apple-style-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .apple-primary-button,
  .apple-secondary-button {
    width: 100%;
  }
}

.dice-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  animation: fadeIn 0.6s ease-out;
}

.primary-btn, .secondary-btn {
  padding: 0.85rem 1.5rem;
  border-radius: 100px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.primary-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.35);
}

.secondary-btn {
  background: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
}

.secondary-btn:hover {
  background: #f8fafc;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.secondary-btn:disabled {
  background: #f1f5f9;
  color: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-icon {
  font-size: 1rem;
}

@keyframes floatAnimation {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulseAnimation {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.5;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.8;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 记录对话框样式 */
.record-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  will-change: opacity;
  transition: opacity 0.25s ease;
  overscroll-behavior: contain;
}

.record-dialog {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  transform: translateZ(0);
  will-change: transform, opacity;
  animation: dialogShow 0.25s ease-out forwards;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

@keyframes dialogShow {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.dialog-content {
  padding: 20px;
  contain: content;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.dialog-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #64748b;
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #1a1a1a;
}

/* 食物记录表单样式 */
.meal-time-buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.meal-time-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.meal-time-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d0d0d5;
}

.meal-time-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.15);
}

.meal-icon {
  font-size: 28px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.meal-time-btn:hover .meal-icon,
.meal-time-btn.active .meal-icon {
  transform: scale(1.1);
}

.meal-label {
  font-size: 14px;
  font-weight: 500;
}

.food-input {
  width: 100%;
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  margin-bottom: 24px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.food-input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
}

.common-foods-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.food-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.food-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d0d0d5;
}

.food-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
}

.food-icon {
  font-size: 28px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.food-btn:hover .food-icon {
  transform: scale(1.1);
}

.food-label {
  font-size: 14px;
  font-weight: 500;
  text-align: center;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .meal-time-buttons,
  .common-foods-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 运动类型网格 */
.exercise-type-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.exercise-type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.exercise-type-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d0d0d5;
}

.exercise-type-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.15);
}

.exercise-icon {
  font-size: 28px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.exercise-type-btn:hover .exercise-icon,
.exercise-type-btn.active .exercise-icon {
  transform: scale(1.1);
}

.exercise-label {
  font-size: 14px;
  font-weight: 500;
}

/* 时长输入 */
.duration-input {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.time-input {
  flex: 1;
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
}

.time-input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
}

.time-unit {
  font-size: 16px;
  color: #64748b;
  font-weight: 500;
}

/* 强度按钮 */
.intensity-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.intensity-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.intensity-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #d0d0d5;
}

.intensity-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.15);
}

.intensity-icon {
  font-size: 24px;
  margin-bottom: 8px;
  transition: transform 0.3s ease;
}

.intensity-btn:hover .intensity-icon,
.intensity-btn.active .intensity-icon {
  transform: scale(1.1);
}

.intensity-label {
  font-size: 14px;
  font-weight: 500;
}

/* 备注文本框 */
.exercise-note, .food-note, .mood-note, .health-note {
  width: 100%;
  height: 100px;
  padding: 14px 16px;
  font-size: 16px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  resize: vertical;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

.exercise-note:focus, .food-note:focus, .mood-note:focus, .health-note:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
}

/* 按钮点击动画 */
@keyframes buttonPulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.98);
  }
  100% {
    transform: scale(1);
  }
}

.exercise-type-btn:active,
.intensity-btn:active,
.mood-btn:active,
.feeling-btn:active,
.status-tag:active,
.meal-time-btn:active,
.food-btn:active {
  animation: buttonPulse 0.2s ease;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .exercise-type-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .intensity-buttons {
    flex-direction: column;
  }
  
  .intensity-btn {
    margin-bottom: 8px;
  }
}

/* 优化按钮样式和动画 - 减少不必要的效果 */
.exercise-type-btn,
.intensity-btn,
.mood-btn,
.feeling-btn,
.status-tag,
.meal-time-btn,
.food-btn {
  transform: translateZ(0);
  will-change: transform;
  transition: transform 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.exercise-type-btn:hover,
.intensity-btn:hover,
.mood-btn:hover,
.feeling-btn:hover,
.status-tag:hover,
.meal-time-btn:hover,
.food-btn:hover {
  transform: translateY(-1px);
}

.exercise-type-btn.active,
.intensity-btn.active,
.mood-btn.active,
.feeling-btn.active,
.status-tag.active,
.meal-time-btn.active,
.food-btn.active {
  background: #f0f7ff;
  border-color: #0071e3;
  color: #0071e3;
}

/* 优化图标 - 移除不必要的动画 */
.exercise-icon,
.intensity-icon,
.mood-icon,
.feeling-icon,
.meal-icon,
.food-icon {
  display: inline-block;
}

/* 优化表单输入 - 简化过渡效果 */
.time-input,
.food-input,
.exercise-note,
.food-note,
.mood-note,
.health-note {
  transition: border-color 0.15s ease;
}

.time-input:focus,
.food-input:focus,
.exercise-note:focus,
.food-note:focus,
.mood-note:focus,
.health-note:focus {
  outline: none;
  border-color: #0071e3;
}

/* 优化提交和取消按钮 - 简化效果 */
.submit-btn, 
.cancel-btn {
  transition: background-color 0.15s ease;
}

/* 添加性能优化的CSS变量 */
:root {
  --animation-speed: 0.15s;
  --transition-timing: ease;
}

/* 优化网格布局 */
.exercise-type-grid,
.mood-grid,
.feeling-grid,
.meal-time-buttons,
.common-foods-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
  contain: layout style;
}

@media (max-width: 480px) {
  .exercise-type-grid,
  .mood-grid,
  .feeling-grid,
  .meal-time-buttons,
  .common-foods-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 优化对话框内容 */
.dialog-content {
  padding: 20px;
  contain: content;
}

/* 简化按钮点击效果 */
.exercise-type-btn:active,
.intensity-btn:active,
.mood-btn:active,
.feeling-btn:active,
.status-tag:active,
.meal-time-btn:active,
.food-btn:active,
.submit-btn:active, 
.cancel-btn:active {
  opacity: 0.9;
}

.food-category {
  background: white;
  border-radius: 16px;
  padding: 1.2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
  border: 1px solid #f5f5f7;
}

.food-category:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.category-icon {
  font-size: 2rem;
  background: #f5f5f7;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.category-info {
  display: flex;
  flex-direction: column;
}

.category-label {
  font-size: 0.8rem;
  color: #86868b;
  letter-spacing: 0.02em;
  margin-bottom: 0.25rem;
}

.category-name {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1d1d1f;
}

.tip-reminder {
  background: #f5f5f7;
  border-radius: 16px;
  padding: 1.2rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  animation: fadeIn 0.4s ease-out;
}

.tip-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
}

.tip-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

.tip-title {
  font-size: 1.1rem;
  font-weight: 500;
  color: #1d1d1f;
}

.tip-content {
  line-height: 1.6;
  color: #515154;
  font-size: 0.95rem;
}

.apple-primary-btn, .apple-secondary-btn {
  padding: 0.6rem 1.2rem;
  border-radius: 980px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.apple-primary-btn {
  background: #0071e3;
  color: white;
}

.apple-primary-btn:hover {
  background: #0077ed;
  transform: scale(1.02);
}

.apple-primary-btn:active {
  background: #0068d1;
  transform: scale(0.98);
}

.apple-secondary-btn {
  background: #f5f5f7;
  color: #1d1d1f;
}

.apple-secondary-btn:hover {
  background: #e8e8ed;
  transform: scale(1.02);
}

.apple-secondary-btn:active {
  background: #dedee3;
  transform: scale(0.98);
}

.apple-secondary-btn:disabled {
  background: #f5f5f7;
  color: #86868b;
  cursor: not-allowed;
  transform: none;
}

.dice-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 苹果风格的食物推荐区域 */
.apple-style-animation {
  position: relative;
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.animation-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid rgba(0, 0, 0, 0.1);
  border-top: 2px solid #0071e3;
  animation: appleRing 1.5s linear infinite;
  will-change: transform;
}

.animation-icon {
  font-size: 2rem;
  opacity: 0.9;
}

@keyframes appleRing {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.dice-text {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.dice-description {
  font-size: 1rem;
  color: #86868b;
  margin-bottom: 1.5rem;
  max-width: 280px;
  margin-left: auto;
  margin-right: auto;
}

.apple-style-button {
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 980px;
  padding: 0.6rem 1.2rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: none;
}

.apple-style-button:hover {
  background: #0077ed;
  transform: scale(1.02);
}

.apple-style-button:active {
  background: #0068d1;
  transform: scale(0.98);
}

.dice-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  border-radius: 18px;
}

.food-recommendation-layout {
  padding: 1.5rem;
}

.recommendation-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
  text-align: center;
}

.food-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

/* 科技风格的食物推荐区域 */
.tech-dice-animation {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tech-dice-outer {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(0, 113, 227, 0.1) 0%, rgba(0, 113, 227, 0.05) 100%);
  border: 1px solid rgba(0, 113, 227, 0.2);
  animation: rotateDice 10s linear infinite;
  will-change: transform;
}

.tech-dice-inner {
  position: absolute;
  width: 70%;
  height: 70%;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(0, 113, 227, 0.15) 0%, rgba(0, 113, 227, 0.1) 100%);
  border: 1px solid rgba(0, 113, 227, 0.3);
  animation: rotateDice 8s linear infinite reverse;
  will-change: transform;
}

.tech-dice-core {
  position: absolute;
  width: 50%;
  height: 50%;
  border-radius: 12px;
  background: #0071e3;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(0, 113, 227, 0.5);
  animation: pulseDice 2s ease-in-out infinite;
  will-change: transform, opacity;
}

.tech-dice-icon {
  font-size: 1.5rem;
  color: white;
}

.tech-particles {
  position: absolute;
  width: 100%;
  height: 100%;
  animation: rotateParticles 15s linear infinite;
  will-change: transform;
}

.tech-particle {
  position: absolute;
  display: block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #0071e3;
  transform-origin: 50px 50px;
  transform: rotate(calc(60deg * var(--i))) translateX(50px);
  animation: particleGlow 3s ease-in-out infinite;
  animation-delay: calc(0.5s * var(--i));
  will-change: opacity, box-shadow;
}

@keyframes rotateDice {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulseDice {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.9;
  }
}

@keyframes rotateParticles {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}

@keyframes particleGlow {
  0%, 100% {
    opacity: 0.5;
    box-shadow: 0 0 4px rgba(0, 113, 227, 0.5);
  }
  50% {
    opacity: 1;
    box-shadow: 0 0 8px rgba(0, 113, 227, 0.8);
  }
}

.tech-style-button {
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.4rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.25);
}

.tech-style-button:hover {
  background: #0077ed;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 113, 227, 0.35);
}

.tech-style-button:active {
  background: #0068d1;
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2);
}

.button-icon {
  font-size: 0.9rem;
  transition: transform 0.3s ease;
}

.tech-style-button:hover .button-icon {
  transform: translateX(3px);
}

.dice-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  border-radius: 18px;
}

.dice-placeholder:hover {
  background: #f9f9fb;
}

/* 平衡设计的食物推荐区域 */
.balanced-animation {
  position: relative;
  width: 90px;
  height: 90px;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.balanced-circle {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #e0f2fe;
  animation: rotateCircle 12s linear infinite;
  will-change: transform;
}

.balanced-icon {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #f0f7ff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0, 113, 227, 0.15);
  z-index: 2;
}

.balanced-icon span {
  font-size: 2rem;
}

.balanced-dots {
  position: absolute;
  width: 100%;
  height: 100%;
  animation: rotateDots 20s linear infinite;
  will-change: transform;
}

.dot {
  position: absolute;
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #0071e3;
  transform-origin: 45px 45px;
  transform: rotate(calc(90deg * var(--i))) translateX(45px);
  opacity: 0.7;
}

@keyframes rotateCircle {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes rotateDots {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}

.balanced-button {
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.7rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2);
}

.balanced-button:hover {
  background: #0077ed;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.25);
}

.balanced-button:active {
  background: #0068d1;
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 113, 227, 0.15);
}

.dice-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  border-radius: 18px;
}

.dice-placeholder:hover {
  background: #f9f9fb;
}

/* 简约温馨的食物推荐区域 */
.simple-animation {
  margin: 0 auto 1.5rem;
}

.food-icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  animation: gentlePulse 3s infinite ease-in-out;
}

.dice-placeholder:hover .food-icon-wrapper {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.food-icon {
  font-size: 2.5rem;
}

@keyframes gentlePulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.simple-button {
  background: #0071e3;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.7rem 1.8rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 113, 227, 0.2);
}

.simple-button:hover {
  background: #0077ed;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.25);
}

.simple-button:active {
  background: #0068d1;
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 113, 227, 0.15);
}

.user-menu {
  position: relative;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 100px;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(0, 0, 0, 0.05);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.username {
  font-size: 0.9rem;
  font-weight: 500;
  color: #1e293b;
}

.dropdown-arrow {
  font-size: 0.7rem;
  color: #64748b;
  transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 220px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 1000;
  animation: dropdownFadeIn 0.3s ease-out forwards;
  transform-origin: top right;
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.dropdown-header {
  padding: 12px 16px;
  background: #f8fafc;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.signed-in {
  font-size: 0.8rem;
  color: #64748b;
}

.dropdown-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 4px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  color: #1e293b;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f1f5f9;
}

.item-icon {
  font-size: 1.1rem;
}

.date-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 24px;
}

.date-input {
  flex: 1;
  padding: 12px 16px;
  font-size: 17px;
  border: 1px solid #e5e5e7;
  border-radius: 12px;
  background: #fff;
  color: #1d1d1f;
  font-family: inherit;
}

.date-input:focus {
  outline: none;
  border-color: #0071e3;
  box-shadow: 0 0 0 3px rgba(0, 113, 227, 0.15);
}

.section-title {
  font-weight: 600;
  color: #1d1d1f;
  margin-bottom: 12px;
  font-size: 17px;
}

/* 记录卡片样式 */
.record-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #f5f5f7;
  margin-bottom: 2rem;
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #f5f5f7;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: #1d1d1f;
}
</style> 