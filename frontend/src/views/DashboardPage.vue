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
            <UserAvatar
              :username="username"
              :showAdminBadge="isAdmin"
              :avatarUrl="avatarUrl"
              size="small"
            />
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
            <div class="dropdown-divider"></div>
            <button class="dropdown-item" @click="logout">
              <span class="item-icon">🚪</span>
              退出
            </button>
          </div>
        </div>
        <!-- Conditionally render Admin Button -->
        <div v-if="isAdmin" class="admin-entry">
          <router-link to="/admin" class="admin-link">
            <span class="admin-icon">⚙️</span>
            进入管理后台
          </router-link>
        </div>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="dashboard-content">
      <!-- 大标题区域 -->
      <div class="hero-section">
        <!-- Title might need adjustment later, keeping old one for now -->
        <h1 class="hero-title">今天过得怎么样？</h1> 
        <p class="hero-subtitle">{{ currentDate }} · {{ currentSeason }}</p>
      </div>

      <!-- ================================= -->
      <!-- ====== 食物推荐区域 (Moved Up) ====== -->
      <!-- ================================= -->
      <section class="food-recommendation glass-card">
          <div class="recommendation-header">
            <h3>智能饮食推荐</h3>
            <p>从您的健康数据获取均衡饮食方案</p>
          </div>
          <button @click="fetchRecommendations" class="recommend-btn" :disabled="isLoadingRecommendations">
            <span v-if="isLoadingRecommendations">
              <i class="fas fa-spinner fa-spin"></i> 正在加载...
            </span>
            <span v-else>
              <i class="fas fa-lightbulb"></i> 获取推荐
            </span>
          </button>
          <div v-if="recommendationError" class="error-message">
            <i class="fas fa-exclamation-triangle"></i> {{ recommendationError }}
          </div>
          <div v-if="!isLoadingRecommendations && recommendations.length > 0" class="recommendation-list">
             <h4>今日推荐食谱：</h4>
             <ul>
               <li v-for="(item, index) in recommendations" :key="index">
                  <strong>{{ item.meal_time }}:</strong> {{ item.content }}
                  <small v-if="item.calories"> (约 {{ item.calories }} kcal)</small>
               </li>
             </ul>
          </div>
          <div v-if="!isLoadingRecommendations && recommendations.length === 0 && !recommendationError && recommendationFetched" class="no-recommendations">
             <p><i class="fas fa-info-circle"></i> 暂时没有获取到推荐，请稍后再试或检查您的个人信息设置。</p>
           </div>
       </section>
       <!-- ====== 食物推荐区域结束 ====== -->

      <!-- 快捷记录区 (Moved Down) -->
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
        <div class="action-card" @click="(e) => showRecordDialog('body_status', e)">
          <div class="action-icon-wrapper">
            <span class="action-icon">⚖️</span>
          </div>
          <span class="action-text">身体状况记录</span>
        </div>
        <div class="action-card" @click="(e) => showRecordDialog('mood', e)">
          <div class="action-icon-wrapper">
            <span class="action-icon">😊</span>
          </div>
          <span class="action-text">心情记录</span>
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
            <!-- Old exercise form structure from e837098... -->
            <div class="form-group">
              <label for="exerciseType">运动类型</label>
              <select id="exerciseType" v-model="currentRecord.exerciseType" class="form-control">
                <option value="running">跑步</option>
                <option value="swimming">游泳</option>
                <option value="yoga">瑜伽</option>
                <option value="cycling">骑行</option>
                <option value="weightlifting">举重</option>
                <option value="other">其他</option>
              </select>
            </div>
            <div class="form-group">
              <label for="exerciseDuration">运动时长 (分钟)</label>
              <input type="number" id="exerciseDuration" v-model.number="currentRecord.duration" class="form-control" placeholder="例如: 30">
            </div>
            <div class="form-group">
              <label for="exerciseIntensity">运动强度</label>
              <select id="exerciseIntensity" v-model="currentRecord.intensity" class="form-control">
                <option value="low">低</option>
                <option value="medium">中</option>
                <option value="high">高</option>
              </select>
            </div>
            <div class="form-group">
              <label for="exerciseNotes">备注</label>
              <textarea id="exerciseNotes" v-model="currentRecord.notes" class="form-control" placeholder="可选"></textarea>
            </div>
          </div>

          <!-- 身体状况记录 -->
          <div v-if="recordType === 'body_status'" class="record-form">
            <!-- Section for Overall Feeling -->
            <div class="form-group">
              <label>整体感受</label>
              <div class="feeling-grid"> <!-- Or use a class similar to mood-options -->
                <button
                  v-for="feeling in feelings"
                  :key="feeling.type"
                  class="feeling-btn" 
                  :class="{ 'active': currentRecord.feelingType === feeling.type }"
                  @click="currentRecord.feelingType = feeling.type"
                >
                  <span class="feeling-icon">{{ feeling.icon }}</span> {{ feeling.label }}
                </button>
              </div>
            </div>
            
            <!-- RE-ADD Section for Weight -->
            <div class="form-group">
              <label for="weight">体重 (kg)</label>
              <input type="number" id="weight" v-model.number="currentRecord.weight" class="form-control" placeholder="例如: 65.5" step="0.1">
            </div>
            
            <!-- RE-ADD Section for Height -->
            <div class="form-group">
              <label for="height">身高 (cm)</label>
              <input type="number" id="height" v-model.number="currentRecord.height" class="form-control" placeholder="例如: 170">
            </div>

            <!-- Keep Section for Heart Rate -->
            <div class="form-group">
              <label for="heartRate">静息心率 (bpm)</label>
              <input type="number" id="heartRate" v-model.number="currentRecord.heartRate" class="form-control" placeholder="例如: 70">
            </div>
            
            <!-- Keep Section for Notes -->
            <div class="form-group">
              <label for="bodyStatusNotes">备注</label>
              <textarea id="bodyStatusNotes" v-model="currentRecord.notes" class="form-control" placeholder="可选"></textarea>
            </div>
            
            <!-- Blood Pressure sections are NOT included -->

          </div>

          <!-- 心情记录 -->
          <div v-if="recordType === 'mood'" class="record-form">
            <!-- Old mood form structure from e837098... -->
            <div class="form-group">
              <label>选择您的心情</label>
              <div class="mood-options">
                <button
                  v-for="mood in moods"
                  :key="mood.type" 
                  class="mood-option-btn"
                  :class="{ 'active': currentRecord.moodType === mood.type }"
                  @click="currentRecord.moodType = mood.type"
                >
                  <span class="mood-icon">{{ mood.icon }}</span> {{ mood.label }}
                </button>
              </div>
            </div>
            <div class="form-group">
              <label for="moodIntensity">心情强度 (1-5)</label>
              <input type="range" id="moodIntensity" v-model.number="currentRecord.moodIntensity" min="1" max="5" class="form-control-range">
              <p>当前强度: {{ currentRecord.moodIntensity }}</p>
            </div>
            <div class="form-group">
              <label for="moodNotes">备注</label>
              <textarea id="moodNotes" v-model="currentRecord.notes" class="form-control" placeholder="可选"></textarea>
            </div>
          </div>

          <div class="dialog-footer">
            <button class="cancel-btn" @click="closeDialog">取消</button>
            <button class="submit-btn" @click="submitRecord" :disabled="isSubmitting"> <!-- Add disabled state -->
                {{ isSubmitting ? '提交中...' : '记录' }}
            </button>
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
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick, reactive } from 'vue';
import { useRouter } from 'vue-router';
// IMPORTANT: Ensure the path to userStore is correct for your project structure
import useUserStore from '@/stores/userStore'; // Assuming src/stores/userStore.js or .ts
import UserAvatar from '@/components/user/UserAvatar.vue'; // Assuming src/components/user/UserAvatar.vue
// IMPORTANT: Ensure the path to api is correct
import { createExerciseRecord, createMoodRecord, createFoodRecord, getAllRecords } from '@/api/records'; // Assuming src/api/records.js or .ts
import { getUserDashboard } from '@/api/user'; // Assuming src/api/user.js or .ts
import axiosInstance from '@/api'; // Try importing from the api directory's index file

const router = useRouter()
const userStore = useUserStore()

// 用户信息
const username = computed(() => userStore.state.userData?.username || '用户')
const avatarUrl = computed(() => userStore.state.userData?.avatar || '')
const isAdmin = computed(() => userStore.state.userData?.role === 'admin')

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

// 记录对话框状态
const isDialogVisible = ref(false)
const recordType = ref('')
const isSubmitting = ref(false)

// 初始化 currentRecord，包含所有可能的字段
const currentRecord = ref({
  record_type: '',
  record_date: new Date().toISOString().split('T')[0], // 默认今天
  // Exercise specific
  exerciseType: '',       // 例如: 'running', 'swimming'
  duration: null,          // 例如: 30 (分钟)
  intensity: 'medium',     // 例如: 'low', 'medium', 'high'
  // Mood specific
  moodType: '',           // 例如: 'happy', 'sad'
  moodIntensity: 3,        // 例如: 1-5
  // Body Status specific (REVISED structure: Feeling, Weight, Height, HR, Notes)
  feelingType: '',        // 例如: 'energetic', 'tired'
  weight: null,            // RE-ADDED: 例如: 65.5 (kg)
  height: null,            // RE-ADDED: 例如: 170 (cm)
  heartRate: null,         // 例如: 70 (bpm)
  // bloodPressureSystolic: null, // REMOVED
  // bloodPressureDiastolic: null, // REMOVED
  notes: '' // 通用备注字段
});

// 选中状态 (这些很多会被 currentRecord 中的字段替代，但暂时保留以防万一)
const selectedExercise = ref('')
const exerciseDuration = ref('')
const selectedIntensity = ref('')
const selectedMood = ref('')
const moodNote = ref('')
const selectedFeeling = ref('')
const selectedStatus = ref([])
const healthNote = ref('') // This might be redundant if using the combined 'note' below
const note = ref('') // Consolidated note field

// 食物记录相关状态
const selectedMealTime = ref('')
const foodName = ref('')
const foodNote = ref('')

// 运动记录相关状态
const exerciseNote = ref('')

// 身体状况记录数据
const bodyStatusData = reactive({ weight_kg: null, bmi: null })
const foodData = reactive({ food_name: '', meal_time: '' }) // Keep reactive state for food form binding
const exerciseData = reactive({ exercise_type: '', duration: null, intensity: '' }) // Keep reactive state for exercise form binding
const moodData = reactive({ mood_type: '' }) // Keep reactive state for mood form binding
const healthData = reactive({ feeling: '', status: [] }) // Keep reactive state for health form binding (might be partially redundant)

// ============================================
// ====== 食物推荐逻辑 (恢复) ======
// ============================================
const recommendations = ref([]);
const isLoadingRecommendations = ref(false);
const recommendationError = ref(null);
const recommendationFetched = ref(false); // Track if fetch was attempted

const fetchRecommendations = async () => {
  isLoadingRecommendations.value = true;
  recommendationError.value = null;
  recommendationFetched.value = true; // Mark fetch as attempted
  recommendations.value = []; // Clear previous recommendations

  try {
    // Assume the backend endpoint is '/recommendations/food'
    const response = await axiosInstance.get('/recommendations/food');

    if (response.data && Array.isArray(response.data)) {
        recommendations.value = response.data;
        console.log("Fetched recommendations:", recommendations.value);
    } else {
        // Handle cases where response is valid but data format is unexpected
        console.warn("Received unexpected data format for recommendations:", response.data);
        recommendations.value = [];
        recommendationError.value = '无法解析推荐数据格式。';
    }

  } catch (error) {
    console.error("Error fetching food recommendations:", error);
    if (error.response) {
       recommendationError.value = `获取推荐失败: ${error.response.data.message || error.response.statusText || '服务器错误'}`;
    } else if (error.request) {
      recommendationError.value = '获取推荐失败: 无法连接到服务器。';
    } else {
      recommendationError.value = `获取推荐失败: ${error.message}`;
    }
    recommendations.value = []; // Ensure recommendations are empty on error
  } finally {
    isLoadingRecommendations.value = false;
  }
};
// ====== 食物推荐逻辑结束 ======

// 方法
const getDialogTitle = () => {
  const titles = {
    food: '记录饮食',
    exercise: '记录运动',
    mood: '记录心情',
    body_status: '身体感受记录' // Changed title slightly
  }
  return titles[recordType.value] || ''
}

// 日期选择器相关状态
const today = new Date()
const maxDate = ref(today.toISOString().split('T')[0]) // 今天的日期，格式为YYYY-MM-DD
const selectedDate = ref(today.toISOString().split('T')[0]) // 默认选择今天

const showRecordDialog = (type, event) => {
  event.stopPropagation();
  recordType.value = type;
  // Reset general fields first
  // note.value = ''; // Resetting currentRecord.notes below is sufficient
  selectedDate.value = new Date().toISOString().split('T')[0]; 
  currentRecord.value.record_date = selectedDate.value; // Correctly access .value

  // Reset specific form fields based on type
  if (type === 'food') {
    selectedMealTime.value = '';
    foodName.value = '';
    foodNote.value = '';
    // Reset potentially conflicting currentRecord fields if necessary
    currentRecord.value.notes = '';
  } else if (type === 'exercise') {
    currentRecord.value.exerciseType = '';
    currentRecord.value.duration = null;
    currentRecord.value.intensity = 'medium'; 
    currentRecord.value.notes = '';
  } else if (type === 'mood') {
    currentRecord.value.moodType = '';
    currentRecord.value.moodIntensity = 3;
    currentRecord.value.notes = '';
  } else if (type === 'body_status') {
    currentRecord.value.feelingType = ''; // Reset feeling
    currentRecord.value.weight = null;     // RE-ADDED: Reset weight
    currentRecord.value.height = null;     // RE-ADDED: Reset height
    currentRecord.value.heartRate = null;  // Reset heart rate
    currentRecord.value.notes = '';         // Reset notes
    // Ensure removed BP fields are null if they somehow linger
    // currentRecord.value.bloodPressureSystolic = null;
    // currentRecord.value.bloodPressureDiastolic = null;
  }

  // Clear potentially outdated separate state variables if they exist
  selectedExercise.value = '';
  exerciseDuration.value = '';
  selectedIntensity.value = '';
  exerciseNote.value = '';
  selectedMood.value = '';
  moodNote.value = '';
  selectedFeeling.value = ''; // Keep resetting this for now, might be used elsewhere or can be removed later
  selectedStatus.value = []; // Keep resetting this for now

  isDialogVisible.value = true;
};

const closeDialog = () => {
  isDialogVisible.value = false
  // Optionally reset fields again on close, although resetForm in showRecordDialog might be sufficient
}

const resetForm = () => { // Consolidate reset logic here
  selectedDate.value = today.toISOString().split('T')[0] 
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
  // healthNote.value = '' // Use consolidated 'note'
  note.value = '' 
  bodyStatusData.weight_kg = null
  bodyStatusData.bmi = null
}

const selectExercise = (type) => { selectedExercise.value = type }
const selectIntensity = (level) => { selectedIntensity.value = level }
const selectMood = (type) => { selectedMood.value = type }
const selectFeeling = (type) => { selectedFeeling.value = type }

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
  isSubmitting.value = true
  console.log('开始提交记录，类型:', recordType.value, '日期:', selectedDate.value)

  let data = { record_date: selectedDate.value }; 
  let apiCall = null;
  let successMsg = '';

  try {
    switch (recordType.value) {
      case 'food':
        if (!selectedMealTime.value || !foodName.value) {
          alert('请选择用餐时间并输入食物名称');
          isSubmitting.value = false;
          return;
        }
        data = { ...data, food_name: foodName.value, meal_time: selectedMealTime.value, note: foodNote.value };
        console.log('提交食物记录数据:', data)
        apiCall = createFoodRecord(data);
        successMsg = '饮食记录已保存';
        break;

      case 'exercise':
        if (!currentRecord.value.exerciseType || currentRecord.value.duration === null || currentRecord.value.duration <= 0) {
          alert('请选择运动类型并输入有效的运动时长');
          isSubmitting.value = false;
          return;
        }
        data = { 
          ...data, 
          exercise_type: currentRecord.value.exerciseType, 
          duration: parseInt(currentRecord.value.duration), 
          intensity: currentRecord.value.intensity, 
          note: currentRecord.value.notes 
        };
        console.log('提交运动记录数据:', data)
        apiCall = createExerciseRecord(data);
        successMsg = '运动记录已保存';
        break;

      case 'mood':
        if (!currentRecord.value.moodType) {
          alert('请选择心情类型');
          isSubmitting.value = false;
          return;
        }
        data = { 
          ...data, 
          mood_type: currentRecord.value.moodType, 
          intensity: currentRecord.value.moodIntensity, // Assuming API might take intensity
          note: currentRecord.value.notes 
        };
        console.log('提交心情记录数据:', data)
        apiCall = createMoodRecord(data);
        successMsg = '心情记录已保存';
        break;

      case 'body_status':
        // Using currentRecord fields for the REVISED simplified form (Feeling, W, H, HR, Notes)
        if (!currentRecord.value.feelingType && currentRecord.value.weight === null && currentRecord.value.height === null && currentRecord.value.heartRate === null && !currentRecord.value.notes) {
            alert('请输入至少一项身体状况信息');
            isSubmitting.value = false;
            return;
        }
        data = { 
             ...data, 
             feeling_type: currentRecord.value.feelingType, 
             weight_kg: currentRecord.value.weight, // RE-ADDED
             height_cm: currentRecord.value.height, // RE-ADDED (assuming API expects height_cm)
             heart_rate_bpm: currentRecord.value.heartRate, 
             note: currentRecord.value.notes
             // BP fields are not collected
        };
        console.log('提交身体记录数据:', data)
        // apiCall = createHealthRecord(data); // API call might need adjustment for new fields
        apiCall = null; 
        successMsg = '身体状况已记录 (模拟)'; 
        break;

      default:
        console.error('未知的记录类型:', recordType.value);
        isSubmitting.value = false;
        return;
    }

    if (apiCall) {
      await apiCall;
      showSuccessMessage(successMsg);
      closeDialog(); // Close dialog on success
    } else if (recordType.value === 'body_status') {
        // Handle the case where apiCall is null for body_status specifically
        // We still want to show success and close the dialog for now
        showSuccessMessage(successMsg);
        closeDialog();
    }

  } catch (error) {
    console.error('提交记录失败:', error);
    const errorMsg = error.response?.data?.message || error.message || '提交失败，请重试';
    alert(`提交失败: ${errorMsg}`);
  } finally {
    isSubmitting.value = false;
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

const toggleUserMenu = () => { showUserMenu.value = !showUserMenu.value }

const closeUserMenu = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

// 添加点击外部关闭用户菜单的事件监听
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    showUserMenu.value = false
  }
}

// 食物相关方法 (Keep data definitions)
const mealTimes = [
  { value: 'breakfast', label: '早餐', icon: '🌅' },
  { value: 'lunch', label: '午餐', icon: '☀️' },
  { value: 'dinner', label: '晚餐', icon: '🌙' },
  { value: 'snack', label: '零食', icon: '🍪' }
]

const commonFoods = {
  breakfast: [
    { name: '牛奶', icon: '🥛' }, { name: '鸡蛋', icon: '🥚' }, { name: '面包', icon: '🍞' },
    { name: '燕麦', icon: '🥣' }, { name: '豆浆', icon: '🫖' }, { name: '包子', icon: '🧆' },
    { name: '粥', icon: '🍚' }, { name: '水果', icon: '🍎' }
  ],
  lunch: [
    { name: '米饭', icon: '🍚' }, { name: '面条', icon: '🍜' }, { name: '鸡肉', icon: '🍗' },
    { name: '牛肉', icon: '🥩' }, { name: '鱼', icon: '🐟' }, { name: '蔬菜', icon: '🥦' },
    { name: '沙拉', icon: '🥗' }, { name: '汤', icon: '🍲' }
  ],
  dinner: [
    { name: '米饭', icon: '🍚' }, { name: '面条', icon: '🍜' }, { name: '鸡肉', icon: '🍗' },
    { name: '牛肉', icon: '🥩' }, { name: '鱼', icon: '🐟' }, { name: '蔬菜', icon: '🥦' },
    { name: '豆腐', icon: '🧊' }, { name: '汤', icon: '🍲' }
  ],
  snack: [
    { name: '水果', icon: '🍎' }, { name: '坚果', icon: '🥜' }, { name: '酸奶', icon: '🥛' },
    { name: '饼干', icon: '��' }, { name: '巧克力', icon: '🍫' }, { name: '蛋糕', icon: '🍰' },
    { name: '薯片', icon: '🍟' }, { name: '冰淇淋', icon: '🍦' }
  ]
}

const currentCommonFoods = computed(() => {
  if (!selectedMealTime.value) return []
  return commonFoods[selectedMealTime.value] || []
})

const selectMealTime = (time) => { selectedMealTime.value = time }

const selectFood = (food) => {
  if (foodName.value) {
    foodName.value += '、'
  }
  foodName.value += food.name
}

// 运动类型 (Keep data definitions)
const exerciseTypes = [
  { type: 'walk', label: '步行', icon: '🚶' }, { type: 'run', label: '跑步', icon: '🏃' },
  { type: 'bike', label: '骑行', icon: '🚴' }, { type: 'swim', label: '游泳', icon: '🏊' },
  { type: 'yoga', label: '瑜伽', icon: '🧘' }, { type: 'gym', label: '健身', icon: '💪' },
  { type: 'ball', label: '球类', icon: '⚽' }, { type: 'other', label: '其他', icon: '✨' }
]

// 运动强度 (Keep data definitions)
const intensityLevels = [
  { level: 'light', label: '轻度', icon: '🌱' },
  { level: 'medium', label: '中度', icon: '🌿' },
  { level: 'high', label: '剧烈', icon: '🌳' }
]

// 心情类型 (Keep data definitions)
const moods = [
  { type: 'happy', label: '开心', icon: '😊' }, { type: 'calm', label: '平静', icon: '😌' },
  { type: 'sad', label: '难过', icon: '😔' }, { type: 'angry', label: '生气', icon: '😠' },
  { type: 'anxious', label: '焦虑', icon: '😰' }, { type: 'tired', label: '疲惫', icon: '😫' },
  { type: 'excited', label: '兴奋', icon: '🤩' }, { type: 'bored', label: '无聊', icon: '😑' }
]

// 身体感受 (Keep data definitions)
const feelings = [
  { type: 'energetic', label: '精力充沛', icon: '⚡️' },
  { type: 'good', label: '状态不错', icon: '👍' },
  { type: 'normal', label: '一般般', icon: '😐' },
  { type: 'tired', label: '有点累', icon: '😪' }
]

// 身体状态 (Keep data definitions)
const healthStatus = [
  { type: 'sleep_well', label: '睡眠充足', icon: '😴' }, { type: 'sleep_bad', label: '睡眠不足', icon: '🥱' },
  { type: 'appetite_good', label: '胃口好', icon: '😋' }, { type: 'appetite_bad', label: '没胃口', icon: '🤢' },
  { type: 'energetic', label: '精力充沛', icon: '💪' }, { type: 'fatigue', label: '疲劳乏力', icon: '😫' },
  { type: 'muscle_sore', label: '肌肉酸痛', icon: '🏋️' }, { type: 'headache', label: '头疼', icon: '🤕' },
  { type: 'throat', label: '咽喉不适', icon: '😷' }, { type: 'stomach', label: '胃部不适', icon: '🤮' },
  { type: 'cold', label: '感冒发烧', icon: '🤒' }, { type: 'allergy', label: '过敏', icon: '🤧' }
]

const closeDialogOnOverlayClick = (event) => {
  if (event.target.classList.contains('record-dialog-overlay')) {
    closeDialog()
  }
}

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    console.log('正在刷新仪表盘数据...')
    const response = await getUserDashboard()
    console.log('仪表盘数据已更新:', response)
    // Process dashboard data if needed
  } catch (error) {
    console.error('获取仪表盘数据失败:', error)
  }
}

// 查询用户记录
const queryRecords = async () => {
  try {
    console.log('正在查询用户记录...')
    // const response = await getAllRecords(7) // Fetch last 7 days?
    // Process records if needed
    // console.log('用户记录已更新:', response)
  } catch (error) {
    console.error('获取用户记录失败:', error)
  }
}

// 生命周期钩子
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  // queryRecords() // Decide if records need to be fetched on mount
  fetchDashboardData() // Fetch dashboard data on mount
  fetchRecommendations(); // Fetch recommendations on mount
  console.log("DashboardPage mounted");
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
  // Clear any timers if they were used
  // if (tipsSwitchTimer) {
  //   clearInterval(tipsSwitchTimer)
  // }
});


// ... (rest of script setup - ensure no dangling references)

</script>

<style scoped>
/* Keep all existing styles EXCEPT those related to the removed food dice section */

.dashboard-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
  padding-bottom: 2rem;
}

/* 毛玻璃效果导航栏 */
.glass-header {
  position: fixed; /* Changed from sticky to fixed for consistent behavior */
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px); /* For Safari */
  border-bottom: 1px solid rgba(229, 231, 235, 0.6); /* Adjusted border color */
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.8rem 2rem; /* Adjusted padding */
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
  /* Removed absolute positioning for simpler flow */
}

.nav-item {
  color: #334155; /* Adjusted color */
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  position: relative;
  transition: color 0.3s ease;
}
.nav-item:hover {
  color: #0071e3; /* Add hover effect */
}

.nav-item::after {
  content: '';
  position: absolute;
  bottom: -2px; /* Position slightly below text */
  left: 0;
  width: 0;
  height: 2px;
  background: #0071e3; /* Simpler underline */
  transition: width 0.3s ease;
}

.nav-item:hover::after,
.nav-item.active::after {
  width: 100%;
}
.nav-item.active {
    color: #0071e3; /* Ensure active color matches underline */
    font-weight: 600; /* Make active bolder */
}


/* 内容区域 */
.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 6rem 1.5rem 2rem; /* Increased top padding due to fixed header */
}

/* 英雄区域 */
.hero-section {
  text-align: center;
  margin-bottom: 3rem; /* Increased margin */
  display: flex;
  flex-direction: column;
  align-items: center;
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

/* 快捷记录区 */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 3rem; /* Increased margin */
}

.action-card {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); /* Smoother transition */
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06); /* Adjusted shadow */
  border: 1px solid #e2e8f0; /* Lighter border */
}

.action-card:hover {
  transform: translateY(-5px); /* Increased hover effect */
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.action-card:active {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
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
  transform: scale(1.1); /* Increased scale */
  background: #e0f2fe;
}

.action-icon {
  font-size: 1.8rem;
}

.action-text {
  font-size: 1rem;
  font-weight: 500;
  color: #334155; /* Adjusted color */
}


/* --- REMOVED food-dice-section and related styles --- */
/* --- REMOVED .apple-style-* styles --- */
/* --- REMOVED .dice-placeholder styles --- */
/* --- REMOVED .food-recommendation-layout (old) styles --- */
/* --- REMOVED related animation keyframes if ONLY used by dice --- */


/* 记录对话框样式 */
.record-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5); /* Slightly darker overlay */
  backdrop-filter: blur(5px); /* Increased blur */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: opacity 0.25s ease;
  overscroll-behavior: contain;
}

.record-dialog {
  background: white;
  border-radius: 16px; /* More rounded */
  width: 90%;
  max-width: 550px; /* Adjusted max-width */
  max-height: 85vh; /* Adjusted max-height */
  overflow-y: auto;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.2); /* Stronger shadow */
  transform: translateZ(0);
  animation: dialogShow 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards; /* Smoother animation */
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
  display: flex; /* Added */
  flex-direction: column; /* Added */
}

@keyframes dialogShow {
  from {
    opacity: 0;
    transform: translateY(15px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.dialog-content {
  padding: 24px; /* Adjusted padding */
  flex-grow: 1; /* Allow content to take space */
  overflow-y: auto; /* Ensure content scrolls */
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px; /* Adjusted margin */
  padding-bottom: 16px; /* Added padding */
  border-bottom: 1px solid #e5e7eb; /* Added border */
}

.dialog-header h3 {
  font-size: 1.25rem; /* Adjusted size */
  font-weight: 600;
  color: #1f2937; /* Adjusted color */
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem; /* Adjusted size */
  color: #9ca3af; /* Adjusted color */
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6; /* Light background on hover */
  color: #4b5563;
}

/* Section Title Style */
.section-title {
  font-weight: 600;
  color: #374151; /* Adjusted color */
  margin-bottom: 12px;
  font-size: 1rem; /* Adjusted size */
  padding-bottom: 8px; /* Added padding */
  border-bottom: 1px solid #f3f4f6; /* Light border */
}

/* Date Selector */
.date-selector {
  margin-bottom: 24px; /* Ensure consistent spacing */
}

.date-input {
  width: 100%; /* Make date input full width */
  padding: 12px 16px;
  font-size: 1rem; /* Adjusted size */
  border: 1px solid #d1d5db; /* Adjusted border */
  border-radius: 8px; /* Adjusted radius */
  background: #fff;
  color: #1f2937;
  font-family: inherit;
  box-sizing: border-box; /* Include padding in width */
}

.date-input:focus {
  outline: none;
  border-color: #3b82f6; /* Blue focus */
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}


/* Button Grids */
.meal-time-buttons,
.exercise-type-grid,
.mood-grid,
.feeling-grid,
.common-foods-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

/* Shared Button Style (for grids) */
.meal-time-btn,
.exercise-type-btn,
.mood-btn,
.feeling-btn,
.food-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* Center content */
  padding: 12px 8px; /* Adjusted padding */
  border: 1px solid #e5e7eb; /* Lighter border */
  border-radius: 12px;
  background: #fff;
  transition: all 0.2s ease; /* Faster transition */
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  text-align: center; /* Ensure text centers */
  min-height: 80px; /* Ensure consistent height */
}

.meal-time-btn:hover,
.exercise-type-btn:hover,
.mood-btn:hover,
.feeling-btn:hover,
.food-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
}

.meal-time-btn.active,
.exercise-type-btn.active,
.mood-btn.active,
.feeling-btn.active {
  background: #eef2ff; /* Lighter active blue */
  border-color: #6366f1; /* Indigo border */
  color: #4338ca; /* Darker indigo text */
  transform: translateY(0px); /* Reset transform on active */
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.05); /* Inset shadow */
}

/* Icons within buttons */
.meal-icon,
.exercise-icon,
.mood-icon,
.feeling-icon,
.food-icon {
  font-size: 1.75rem; /* Slightly smaller icons */
  margin-bottom: 6px;
  transition: transform 0.2s ease;
  line-height: 1; /* Ensure proper vertical alignment */
}

.meal-time-btn:hover .meal-icon, /* Remove hover scale */
.exercise-type-btn:hover .exercise-icon,
.mood-btn:hover .mood-icon,
.feeling-btn:hover .feeling-icon,
.food-btn:hover .food-icon {
  transform: scale(1); 
}
.meal-time-btn.active .meal-icon, /* Add active scale */
.exercise-type-btn.active .exercise-icon,
.mood-btn.active .mood-icon,
.feeling-btn.active .feeling-icon {
   transform: scale(1.05);
}


/* Labels within buttons */
.meal-label,
.exercise-label,
.mood-label,
.feeling-label,
.food-label {
  font-size: 0.8rem; /* Smaller labels */
  font-weight: 500;
  color: #4b5563; /* Adjusted color */
  line-height: 1.2; /* Improve readability */
}
.meal-time-btn.active .meal-label, /* Active label style */
.exercise-type-btn.active .exercise-label,
.mood-btn.active .mood-label,
.feeling-btn.active .feeling-label {
  color: #4338ca; 
  font-weight: 600;
}


/* Input Fields (Food Name, Duration) */
.food-input,
.time-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  margin-bottom: 20px; /* Consistent margin */
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-sizing: border-box;
}
.food-input:focus,
.time-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* Duration Input Specifics */
.duration-input {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.time-unit {
  font-size: 1rem;
  color: #6b7280;
  font-weight: 500;
}

/* Intensity Buttons */
.intensity-buttons {
  display: flex; /* Use flex for intensity */
  gap: 10px;
  margin-bottom: 20px;
}
.intensity-btn {
  flex: 1; /* Make buttons equal width */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px 8px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #fff;
  transition: all 0.2s ease;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  text-align: center;
  min-height: 80px;
}
.intensity-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  border-color: #d1d5db;
}
.intensity-btn.active {
  background: #eef2ff;
  border-color: #6366f1;
  color: #4338ca;
  transform: translateY(0px);
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
}
.intensity-icon { font-size: 1.5rem; margin-bottom: 6px; }
.intensity-label { font-size: 0.8rem; font-weight: 500; }
.intensity-btn.active .intensity-label { color: #4338ca; font-weight: 600; }
.intensity-btn.active .intensity-icon { transform: scale(1.05); }


/* Status Tags (Body Status) */
.status-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px; /* Reduced gap */
  margin-bottom: 20px;
}
.status-tag {
  padding: 6px 14px; /* Adjusted padding */
  border-radius: 100px;
  background: #f3f4f6; /* Lighter background */
  border: 1px solid transparent; /* Transparent border */
  font-size: 0.85rem; /* Adjusted size */
  font-weight: 500;
  color: #4b5563; /* Adjusted color */
  cursor: pointer;
  transition: all 0.2s ease;
}
.status-tag:hover {
  background: #e5e7eb; /* Slightly darker hover */
}
.status-tag.active {
  background: #eef2ff;
  border-color: #a5b4fc; /* Lighter indigo border */
  color: #4f46e5; /* Indigo text */
  box-shadow: none; /* Remove shadow */
}

/* Form Grid (Body Status) */
.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 20px; /* Consistent margin */
}
.form-group label {
    display: block;
    margin-bottom: 4px; /* Reduced margin */
    font-size: 0.85rem; /* Adjusted size */
    color: #4b5563; /* Adjusted color */
    font-weight: 500;
}
.form-group input[type="number"] {
    width: 100%;
    padding: 10px 14px; /* Adjusted padding */
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 0.95rem;
    box-sizing: border-box;
}
.form-group input[type="number"]:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* Textarea (Notes) */
.exercise-note, .food-note, .mood-note, .health-note, /* Added .health-note for consistency */
textarea[v-model="note"] /* Target consolidated note */
 {
  width: 100%;
  min-height: 80px; /* Reduced min-height */
  padding: 12px 16px;
  font-size: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  resize: vertical;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-shadow: none; /* Remove default shadow */
  margin-bottom: 20px; /* Consistent margin */
  box-sizing: border-box;
}
.exercise-note:focus, .food-note:focus, .mood-note:focus, .health-note:focus,
textarea[v-model="note"]:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}


/* Dialog Footer Buttons */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px; /* Space above footer */
  padding-top: 20px; /* Space */
  border-top: 1px solid #e5e7eb; /* Separator */
}

.cancel-btn, .submit-btn {
  padding: 10px 20px; /* Adjusted padding */
  border-radius: 8px; /* Adjusted radius */
  font-size: 0.95rem; /* Adjusted size */
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.cancel-btn {
  background: #f3f4f6; /* Light gray */
  color: #4b5563; /* Dark gray text */
  border: 1px solid #d1d5db; /* Add subtle border */
}
.cancel-btn:hover { background: #e5e7eb; }

.submit-btn {
  background: #3b82f6; /* Primary blue */
  color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.submit-btn:hover { background: #2563eb; }
.submit-btn:active { background: #1d4ed8; transform: scale(0.98); }
.submit-btn:disabled { background: #93c5fd; cursor: not-allowed; box-shadow: none; }


/* Success Message */
.success-message {
  position: fixed;
  bottom: 20px; /* Adjusted position */
  left: 50%;
  transform: translateX(-50%);
  background: rgba(16, 185, 129, 0.9); /* Emerald green */
  color: white;
  padding: 10px 20px; /* Adjusted padding */
  border-radius: 8px; /* Less rounded */
  font-size: 0.95rem; /* Adjusted size */
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 1100;
  animation: messageSlideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1), messageFadeOut 0.3s ease 2.7s forwards;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}
/* Keyframes remain the same */


/* User Menu & Dropdown */
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
  transition: background-color 0.2s ease;
}
.user-info:hover { background: rgba(0, 0, 0, 0.05); }
.username { font-size: 0.9rem; font-weight: 500; color: #1f2937; }
.dropdown-arrow { font-size: 0.7rem; color: #6b7280; transition: transform 0.3s ease; }
.dropdown-arrow.rotated { transform: rotate(180deg); }

.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 200px; /* Adjusted width */
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1); /* Adjusted shadow */
  overflow: hidden;
  z-index: 1000;
  animation: dropdownFadeIn 0.2s ease-out forwards; /* Faster animation */
  transform-origin: top right;
}
@keyframes dropdownFadeIn { /* Keep */ }
.dropdown-header { padding: 10px 14px; background: #f9fafb; } /* Adjusted padding */
.header-info { display: flex; flex-direction: column; gap: 2px; }
.signed-in { font-size: 0.75rem; color: #6b7280; } /* Adjusted size */
.dropdown-divider { height: 1px; background: #e5e7eb; margin: 4px 0; }
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px; /* Adjusted padding */
  color: #374151; /* Adjusted color */
  text-decoration: none;
  transition: background-color 0.2s ease;
  cursor: pointer;
  background: none; /* Ensure button is transparent */
  border: none; /* Ensure button has no border */
  width: 100%; /* Ensure button takes full width */
  text-align: left; /* Align text left */
  font-size: 0.9rem; /* Ensure consistent font size */
  font-family: inherit; /* Ensure consistent font */
}
.dropdown-item:hover { background: #f3f4f6; }
.item-icon { font-size: 1rem; width: 16px; text-align: center; color: #6b7280; } /* Adjusted icon styles */


/* Admin Entry */
.admin-entry { margin-left: 1rem; /* Add space */ }
.admin-link {
  background: #4f46e5; /* Indigo */
  color: white;
  padding: 0.6rem 1.2rem; /* Adjusted padding */
  border-radius: 8px; /* Adjusted radius */
  text-decoration: none;
  transition: all 0.2s ease;
  display: inline-flex; /* Use inline-flex */
  align-items: center; /* Align icon */
  gap: 0.5rem; /* Add gap */
  font-size: 0.9rem; /* Adjusted size */
  font-weight: 500;
}
.admin-link:hover { background: #4338ca; transform: translateY(-1px); box-shadow: 0 2px 6px rgba(79, 70, 229, 0.2); }
.admin-icon { font-size: 1rem; }


/* General Responsive */
@media (max-width: 768px) {
  .main-nav { display: none; } /* Hide nav on smaller screens for simplicity, or implement mobile menu */
  .header-content { padding: 0.8rem 1rem; }
  .dashboard-content { padding: 5rem 1rem 1.5rem; }
  .hero-title { font-size: 2rem; }
  .quick-actions { grid-template-columns: repeat(2, 1fr); gap: 0.8rem; }
  .action-card { padding: 1.2rem 0.8rem; }
  .record-dialog { max-width: 95%; max-height: 90vh; }
  .meal-time-buttons, .common-foods-grid, .exercise-type-grid, .mood-grid, .feeling-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; } /* Adjust grids */
  .intensity-buttons { flex-direction: column; gap: 8px; } /* Stack intensity */
  .intensity-btn { margin-bottom: 0; }
}

/* ======================================== */
/* ====== 食物推荐区域样式 (新增) ====== */
/* ======================================== */
.food-recommendation {
  background-color: white; /* Or use existing glass-card style if preferred */
  border-radius: 16px; /* Match other cards */
  padding: 1.5rem 2rem; /* Consistent padding */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06); /* Match other cards */
  border: 1px solid #e2e8f0; /* Match other cards */
  margin-bottom: 3rem; /* Space below */
}

.recommendation-header {
  margin-bottom: 1.5rem;
  text-align: center; /* Center header text */
}

.recommendation-header h3 {
  font-size: 1.4rem; /* Slightly larger title */
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.3rem 0;
}

.recommendation-header p {
  font-size: 0.95rem;
  color: #6b7280;
  margin: 0;
}

.recommend-btn {
  background-color: #3b82f6; /* Primary blue */
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  display: block; /* Make button block level */
  margin: 0 auto 1.5rem; /* Center button and add space below */
  min-width: 150px; /* Give button some width */
}
.recommend-btn i { margin-right: 0.5rem; }
.recommend-btn:disabled {
  background-color: #9ca3af; /* Gray when disabled */
  cursor: not-allowed;
}
.recommend-btn:not(:disabled):hover { background-color: #2563eb; } /* Darker blue on hover */
.recommend-btn:not(:disabled):active { transform: scale(0.98); }

.recommendation-list {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6; /* Light separator */
}
.recommendation-list h4 {
   font-size: 1.1rem;
   font-weight: 600;
   color: #374151;
   margin-bottom: 1rem;
}

.recommendation-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendation-list li {
  background-color: #f9fafb; /* Very light background for list items */
  padding: 0.8rem 1.2rem;
  border-radius: 8px;
  margin-bottom: 0.8rem;
  font-size: 0.95rem;
  color: #1f2937;
  border: 1px solid #f3f4f6;
}
.recommendation-list li strong {
    color: #3b82f6; /* Highlight meal time */
    margin-right: 0.5rem;
    font-weight: 600;
}
.recommendation-list li small {
    color: #6b7280;
    margin-left: 0.5rem;
    font-size: 0.85rem;
}

.error-message {
  color: #ef4444; /* Red */
  background-color: #fee2e2; /* Light red background */
  border: 1px solid #fecaca; /* Lighter red border */
  padding: 0.8rem 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.9rem;
  text-align: center;
}
.error-message i { margin-right: 0.5rem; }

.no-recommendations {
   color: #6b7280; /* Gray text */
   background-color: #f3f4f6; /* Light gray background */
   border: 1px solid #e5e7eb; /* Gray border */
   padding: 1rem 1.2rem;
   border-radius: 8px;
   margin-top: 1rem;
   font-size: 0.95rem;
   text-align: center;
 }
.no-recommendations i { margin-right: 0.5rem; color: #9ca3af; }

/* Styles from e837098 for the dialog forms - ensuring these are present */
.record-dialog .form-group {
  margin-bottom: 1rem; /* Increased spacing */
}

.record-dialog .form-group label {
  display: block;
  margin-bottom: 0.5rem; /* Increased spacing */
  color: #4a5568; /* Darker label color for better contrast */
  font-weight: 600; /* Slightly bolder labels */
}

.record-dialog .form-control,
.record-dialog .form-control-range {
  width: 100%;
  padding: 0.75rem 1rem; /* Larger padding */
  border: 1px solid #cbd5e0; /* Softer border color */
  border-radius: 0.375rem; /* Standard border radius */
  background-color: #fff; /* Explicit white background */
  color: #2d3748; /* Darker text color */
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.record-dialog .form-control:focus,
.record-dialog .form-control-range:focus {
  border-color: #4299e1; /* Focus border color (blue) */
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(66, 153, 225, 0.25); /* Focus shadow */
}

.record-dialog .form-control::placeholder {
  color: #a0aec0; /* Lighter placeholder text */
}

/* Mood options specific styling from e837098 */
.mood-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem; /* Spacing between mood buttons */
  margin-bottom: 1rem;
}

.mood-option-btn {
  padding: 0.75rem 1rem; /* Comfortable padding */
  border: 1px solid #cbd5e0; /* Consistent border */
  border-radius: 0.375rem;
  background-color: #f7fafc; /* Light background */
  color: #4a5568; /* Default text color */
  cursor: pointer;
  transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
  font-size: 0.9rem; /* Slightly smaller font for buttons */
  display: flex;
  align-items: center;
  gap: 0.5rem; /* Space between icon and text */
}

.mood-option-btn .mood-icon {
  font-size: 1.2rem; /* Larger icon */
}

.mood-option-btn:hover {
  background-color: #e2e8f0; /* Hover background */
  border-color: #a0aec0; /* Hover border */
}

.mood-option-btn.active {
  background-color: #4299e1; /* Active background (blue) */
  color: #fff; /* White text for active */
  border-color: #4299e1; /* Active border */
  font-weight: 600; /* Bolder text for active */
}

.record-dialog .form-control-range {
  padding: 0; /* Reset padding for range input if needed */
}

.record-dialog p { /* For mood intensity display */
  font-size: 0.875rem;
  color: #718096; /* Subdued text color */
  margin-top: 0.25rem;
}

/* Ensure submit button has good contrast and styling if it was part of the old form's look */
.submit-record-btn {
  background-color: #4CAF50; /* Green */
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
  width: 100%; /* Make button full width */
  margin-top: 1rem; /* Space above the button */
}

.submit-record-btn:hover {
  background-color: #45a049; /* Darker green on hover */
}

.submit-record-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* Adjustments if the old dialog had a different footer structure or button alignment */
.dialog-footer {
  display: flex;
  justify-content: flex-end; /* Align buttons to the right */
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0; /* Separator line */
  margin-top: 1.5rem; /* Space above footer */
}

/* Add specific styles for .exercise-type-grid, .duration-input, .intensity-buttons if they were distinct in the old version and different from current */
/* For now, assuming .form-group and .form-control cover most needs, but if specific layouts like grids were different, those styles would go here */

/* The following are generic styles from the old commit that might affect form inputs,
   if they were not already covered or if they are preferred over the current ones for these specific forms.
   Be cautious about overriding too broadly.
*/
.record-form input[type="text"],
.record-form input[type="number"],
.record-form input[type="date"],
.record-form select,
.record-form textarea {
  display: block;
  width: 100%;
  padding: 10px;
  margin-bottom: 15px; /* Increased margin from old style */
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1rem;
}

.record-form textarea {
  min-height: 80px; /* Slightly taller textarea */
  resize: vertical;
}

.record-form button { /* Generic button style within forms if needed */
  /* background-color: #5cb85c; */ /* Example, might conflict with specific buttons */
  /* color: white; */
  /* padding: 10px 15px; */
  /* border: none; */
  /* border-radius: 4px; */
  /* cursor: pointer; */
}

/* .record-form button:hover { */
  /* background-color: #4cae4c; */
/* } */

/* End of specific styles from e837098 for the dialog forms */
</style>
