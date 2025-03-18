<template>
  <div class="records-page">
    <header class="glass-header">
      <div class="header-content">
        <div class="logo">健康生活</div>
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-item">首页</router-link>
          <router-link to="/records" class="nav-item active">记录</router-link>
          <router-link to="/reports" class="nav-item">报告</router-link>
        </nav>
        <div class="user-menu" @click="toggleDropdown" ref="userMenuRef">
          <div class="user-info">
            <div class="avatar">
              <UserAvatar />
            </div>
            <span class="username">{{ username }}</span>
            <span class="dropdown-arrow" :class="{ 'rotated': isDropdownVisible }">▼</span>
          </div>
          
          <!-- 下拉菜单 -->
          <div v-if="isDropdownVisible" class="user-dropdown">
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
            <button class="dropdown-item" @click="handleLogout">
              <span class="item-icon">🚪</span>
              退出
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="main-content">
      <!-- 页面标题区域 -->
      <div class="page-header">
        <div class="title-section">
          <h1>健康生活</h1>
          <p class="subtitle">生活记录</p>
          <button class="add-record-btn" @click="showAddRecordDialog">
            <span class="plus-icon">+</span>
            添加记录
          </button>
        </div>
        
        <!-- 记录类型过滤器 -->
        <div class="record-types">
          <button
            v-for="type in recordTypes"
            :key="type.value"
            :class="['type-btn', { active: selectedTypes.includes(type.value) }]"
            @click="toggleType(type.value)"
          >
            <span class="icon">{{ type.icon }}</span>
            {{ type.label }}
          </button>
        </div>

        <!-- 搜索和时间过滤器 -->
        <div class="filters">
          <select v-model="selectedDays" @change="changeTimeRange(selectedDays)" class="time-select">
            <option v-for="option in timeOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>

          <input
            type="search"
            v-model="searchQuery"
            placeholder="搜索记录..."
            class="search-input"
          />
        </div>
      </div>

      <div class="records-list">
        <template v-if="Object.keys(groupedByDateRecords).length > 0">
          <div v-for="(dateGroup, date) in groupedByDateRecords" :key="date" class="date-group">
            <div class="date-header">{{ formatDateHeader(date) }}</div>
            
            <div class="date-records">
              <!-- 食物记录 -->
              <div v-if="dateGroup.food && selectedTypes.includes('food')" class="record-section">
                <h3>饮食记录</h3>
                <div v-for="record in dateGroup.food" :key="record.id" class="record-item">
                  <div class="record-content">
                    <span class="meal-time">{{ getMealTimeLabel(record.meal_time) }}</span>
                    <span class="food-name">{{ record.food_name }}</span>
                    <span v-if="record.note" class="note">{{ record.note }}</span>
                  </div>
                  <div class="record-actions">
                    <button @click="editRecord(record, 'food')" class="edit-btn">✏️</button>
                    <button @click="confirmDelete(record.id, 'food')" class="delete-btn">🗑️</button>
                  </div>
                </div>
              </div>

              <!-- 运动记录 -->
              <div v-if="dateGroup.exercise && selectedTypes.includes('exercise')" class="record-section">
                <h3>运动记录</h3>
                <div v-for="record in dateGroup.exercise" :key="record.id" class="record-item">
                  <div class="record-content">
                    <span class="exercise-type">{{ getExerciseLabel(record.exercise_type) }}</span>
                    <span class="duration">{{ record.duration }}分钟</span>
                    <span class="intensity">{{ getIntensityLabel(record.intensity) }}</span>
                    <span v-if="record.note" class="note">{{ record.note }}</span>
                  </div>
                  <div class="record-actions">
                    <button @click="editRecord(record, 'exercise')" class="edit-btn">✏️</button>
                    <button @click="confirmDelete(record.id, 'exercise')" class="delete-btn">🗑️</button>
                  </div>
                </div>
              </div>

              <!-- 心情记录 -->
              <div v-if="dateGroup.mood && selectedTypes.includes('mood')" class="record-section">
                <h3>心情记录</h3>
                <div v-for="record in dateGroup.mood" :key="record.id" class="record-item">
                  <div class="record-content">
                    <span class="mood-type">{{ getMoodLabel(record.mood_type) }}</span>
                    <span v-if="record.note" class="note">{{ record.note }}</span>
                  </div>
                  <div class="record-actions">
                    <button @click="editRecord(record, 'mood')" class="edit-btn">✏️</button>
                    <button @click="confirmDelete(record.id, 'mood')" class="delete-btn">🗑️</button>
                  </div>
                </div>
              </div>

              <!-- 身体状况记录 -->
              <div v-if="dateGroup.health && selectedTypes.includes('health')" class="record-section">
                <h3>身体状况</h3>
                <div v-for="record in dateGroup.health" :key="record.id" class="record-item">
                  <div class="record-content">
                    <span class="feeling">{{ getFeelingLabel(record.feeling) }}</span>
                    <div class="status-list">
                      <span v-for="status in record.status" :key="status" class="status-tag">
                        {{ getStatusLabel(status) }}
                      </span>
                    </div>
                    <span v-if="record.note" class="note">{{ record.note }}</span>
                  </div>
                  <div class="record-actions">
                    <button @click="editRecord(record, 'health')" class="edit-btn">✏️</button>
                    <button @click="confirmDelete(record.id, 'health')" class="delete-btn">🗑️</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
        
        <div v-else class="empty-state">
          <p>暂无记录</p>
        </div>
      </div>

      <!-- 编辑对话框 -->
      <div v-if="isEditDialogVisible" class="edit-dialog-overlay" @click="isEditDialogVisible = false">
        <div class="edit-dialog" @click.stop>
          <div class="dialog-header">
            <h3>编辑{{ getRecordTypeLabel(editingType) }}记录</h3>
            <button class="close-btn" @click="isEditDialogVisible = false">×</button>
          </div>

          <div class="dialog-content">
            <!-- 食物记录编辑表单 -->
            <template v-if="editingType === 'food'">
              <div class="form-group">
                <label>用餐时间</label>
                <div class="meal-time-buttons">
                  <button 
                    v-for="meal in mealTimes" 
                    :key="meal.value"
                    :class="['meal-time-btn', { active: editingRecord.meal_time === meal.value }]"
                    @click="editingRecord.meal_time = meal.value"
                  >
                    <span class="meal-icon">{{ meal.icon }}</span>
                    <span class="meal-label">{{ meal.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>食物名称</label>
                <input 
                  type="text" 
                  v-model="editingRecord.food_name"
                  class="form-input"
                  placeholder="输入食物名称"
                />
              </div>
              <div class="form-group">
                <label>备注</label>
                <textarea 
                  v-model="editingRecord.note"
                  class="form-textarea"
                  placeholder="添加备注..."
                ></textarea>
              </div>
            </template>

            <!-- 运动记录编辑表单 -->
            <template v-if="editingType === 'exercise'">
              <div class="form-group">
                <label>运动类型</label>
                <div class="exercise-grid">
                  <button 
                    v-for="exercise in exerciseTypes" 
                    :key="exercise.type"
                    :class="['exercise-btn', { active: editingRecord.exercise_type === exercise.type }]"
                    @click="editingRecord.exercise_type = exercise.type"
                  >
                    <span class="exercise-icon">{{ exercise.icon }}</span>
                    <span class="exercise-label">{{ exercise.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>运动时长（分钟）</label>
                <input 
                  type="number" 
                  v-model="editingRecord.duration"
                  class="form-input"
                  min="1"
                />
              </div>
              <div class="form-group">
                <label>运动强度</label>
                <div class="intensity-buttons">
                  <button 
                    v-for="intensity in intensityLevels" 
                    :key="intensity.level"
                    :class="['intensity-btn', { active: editingRecord.intensity === intensity.level }]"
                    @click="editingRecord.intensity = intensity.level"
                  >
                    <span class="intensity-icon">{{ intensity.icon }}</span>
                    <span class="intensity-label">{{ intensity.label }}</span>
                  </button>
                </div>
              </div>
            </template>

            <!-- 心情记录编辑表单 -->
            <template v-if="editingType === 'mood'">
              <div class="form-group">
                <label>心情</label>
                <div class="mood-grid">
                  <button 
                    v-for="mood in moods" 
                    :key="mood.type"
                    :class="['mood-btn', { active: editingRecord.mood_type === mood.type }]"
                    @click="editingRecord.mood_type = mood.type"
                  >
                    <span class="mood-icon">{{ mood.icon }}</span>
                    <span class="mood-label">{{ mood.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>心情小记</label>
                <textarea 
                  v-model="editingRecord.note"
                  class="form-textarea"
                  placeholder="记录一下此刻的想法..."
                ></textarea>
              </div>
            </template>

            <!-- 身体状况记录编辑表单 -->
            <template v-if="editingType === 'health'">
              <div class="form-group">
                <label>整体感受</label>
                <div class="feeling-grid">
                  <button 
                    v-for="feeling in feelings" 
                    :key="feeling.type"
                    :class="['feeling-btn', { active: editingRecord.feeling === feeling.type }]"
                    @click="editingRecord.feeling = feeling.type"
                  >
                    <span class="feeling-icon">{{ feeling.icon }}</span>
                    <span class="feeling-label">{{ feeling.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>身体状态</label>
                <div class="status-tags">
                  <button 
                    v-for="status in healthStatus" 
                    :key="status.type"
                    :class="['status-tag', { active: editingRecord.status.includes(status.type) }]"
                    @click="toggleStatus(status.type)"
                  >
                    {{ status.icon }} {{ status.label }}
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>备注</label>
                <textarea 
                  v-model="editingRecord.note"
                  class="form-textarea"
                  placeholder="添加备注..."
                ></textarea>
              </div>
            </template>
          </div>

          <div class="dialog-footer">
            <button class="cancel-btn" @click="isEditDialogVisible = false">取消</button>
            <button class="submit-btn" @click="saveEdit">保存</button>
          </div>
        </div>
      </div>

      <!-- 添加记录对话框 -->
      <div v-if="isAddDialogVisible" class="dialog-overlay" @click="closeAddDialog">
        <div class="dialog-content" @click.stop>
          <div class="dialog-header">
            <h3>添加记录</h3>
            <button class="close-btn" @click="closeAddDialog">×</button>
          </div>
          
          <div class="dialog-body">
            <!-- 记录类型选择 -->
            <div v-if="!selectedRecordType" class="record-type-grid">
              <button 
                v-for="type in recordTypes" 
                :key="type.value"
                class="record-type-btn"
                @click="selectRecordType(type.value)"
              >
                <span class="type-icon">{{ type.icon }}</span>
                <span class="type-label">{{ type.label }}</span>
              </button>
            </div>

            <!-- 食物记录表单 -->
            <template v-if="selectedRecordType === 'food'">
              <div class="form-group">
                <label>用餐时间</label>
                <div class="meal-time-buttons">
                  <button 
                    v-for="meal in mealTimes" 
                    :key="meal.value"
                    :class="['meal-time-btn', { active: editingRecord.meal_time === meal.value }]"
                    @click="editingRecord.meal_time = meal.value"
                  >
                    <span class="meal-icon">{{ meal.icon }}</span>
                    <span class="meal-label">{{ meal.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>食物名称</label>
                <input 
                  type="text" 
                  v-model="editingRecord.food_name"
                  class="form-input"
                  placeholder="输入食物名称"
                />
              </div>
              <div class="form-group">
                <label>备注</label>
                <textarea 
                  v-model="editingRecord.note"
                  class="form-textarea"
                  placeholder="添加备注..."
                ></textarea>
              </div>
              <div class="form-group">
                <label>日期</label>
                <input 
                  type="date" 
                  v-model="editingRecord.record_date"
                  class="form-input date-input"
                  :max="today"
                  :min="oneMonthAgo"
                />
              </div>
            </template>

            <!-- 运动记录表单 -->
            <template v-if="selectedRecordType === 'exercise'">
              <div class="form-group">
                <label>运动类型</label>
                <div class="exercise-grid">
                  <button 
                    v-for="exercise in exerciseTypes" 
                    :key="exercise.type"
                    :class="['exercise-btn', { active: editingRecord.exercise_type === exercise.type }]"
                    @click="editingRecord.exercise_type = exercise.type"
                  >
                    <span class="exercise-icon">{{ exercise.icon }}</span>
                    <span class="exercise-label">{{ exercise.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>运动时长（分钟）</label>
                <input 
                  type="number" 
                  v-model="editingRecord.duration"
                  class="form-input"
                  min="1"
                />
              </div>
              <div class="form-group">
                <label>运动强度</label>
                <div class="intensity-buttons">
                  <button 
                    v-for="intensity in intensityLevels" 
                    :key="intensity.level"
                    :class="['intensity-btn', { active: editingRecord.intensity === intensity.level }]"
                    @click="editingRecord.intensity = intensity.level"
                  >
                    <span class="intensity-icon">{{ intensity.icon }}</span>
                    <span class="intensity-label">{{ intensity.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>日期</label>
                <input 
                  type="date" 
                  v-model="editingRecord.record_date"
                  class="form-input date-input"
                  :max="today"
                  :min="oneMonthAgo"
                />
              </div>
            </template>

            <!-- 心情记录表单 -->
            <template v-if="selectedRecordType === 'mood'">
              <div class="form-group">
                <label>心情</label>
                <div class="mood-grid">
                  <button 
                    v-for="mood in moods" 
                    :key="mood.type"
                    :class="['mood-btn', { active: editingRecord.mood_type === mood.type }]"
                    @click="editingRecord.mood_type = mood.type"
                  >
                    <span class="mood-icon">{{ mood.icon }}</span>
                    <span class="mood-label">{{ mood.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>心情小记</label>
                <textarea 
                  v-model="editingRecord.note"
                  class="form-textarea"
                  placeholder="记录一下此刻的想法..."
                ></textarea>
              </div>
              <div class="form-group">
                <label>日期</label>
                <input 
                  type="date" 
                  v-model="editingRecord.record_date"
                  class="form-input date-input"
                  :max="today"
                  :min="oneMonthAgo"
                />
              </div>
            </template>

            <!-- 身体状况记录表单 -->
            <template v-if="selectedRecordType === 'health'">
              <div class="form-group">
                <label>整体感受</label>
                <div class="feeling-grid">
                  <button 
                    v-for="feeling in feelings" 
                    :key="feeling.type"
                    :class="['feeling-btn', { active: editingRecord.feeling === feeling.type }]"
                    @click="editingRecord.feeling = feeling.type"
                  >
                    <span class="feeling-icon">{{ feeling.icon }}</span>
                    <span class="feeling-label">{{ feeling.label }}</span>
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>身体状态</label>
                <div class="status-tags">
                  <button 
                    v-for="status in healthStatus" 
                    :key="status.type"
                    :class="['status-tag', { active: editingRecord.status.includes(status.type) }]"
                    @click="toggleStatus(status.type)"
                  >
                    {{ status.icon }} {{ status.label }}
                  </button>
                </div>
              </div>
              <div class="form-group">
                <label>备注</label>
                <textarea 
                  v-model="editingRecord.note"
                  class="form-textarea"
                  placeholder="添加备注..."
                ></textarea>
              </div>
              <div class="form-group">
                <label>日期</label>
                <input 
                  type="date" 
                  v-model="editingRecord.record_date"
                  class="form-input date-input"
                  :max="today"
                  :min="oneMonthAgo"
                />
              </div>
            </template>
          </div>

          <div class="dialog-footer">
            <button v-if="selectedRecordType" class="back-btn" @click="backToTypeSelection">返回</button>
            <button class="cancel-btn" @click="closeAddDialog">取消</button>
            <button v-if="selectedRecordType" class="submit-btn" @click="saveNewRecord">保存</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { getAllRecords, updateFoodRecord, updateExerciseRecord, updateMoodRecord, updateHealthRecord, deleteRecord, createFoodRecord, createExerciseRecord, createMoodRecord, createHealthRecord } from '../api/records'
import { useRouter } from 'vue-router'
import UserAvatar from '../components/UserAvatar.vue'
import useUserStore from '../stores/userStore'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const records = ref({
  food: [],
  exercise: [],
  mood: [],
  health: []
})

const selectedDays = ref(7)
const timeOptions = [
  { label: '最近7天', value: 7 },
  { label: '最近14天', value: 14 },
  { label: '最近30天', value: 30 },
  { label: '最近60天', value: 60 },
  { label: '最近90天', value: 90 }
]

// 搜索和筛选状态
const searchQuery = ref('')
const selectedTypes = ref(['food', 'exercise', 'mood', 'health'])

const recordTypes = [
  { value: 'food', label: '饮食', icon: '🍽️' },
  { value: 'exercise', label: '运动', icon: '🏃' },
  { value: 'mood', label: '心情', icon: '😊' },
  { value: 'health', label: '身体状况', icon: '💪' }
]

// 过滤记录
const filteredRecords = computed(() => {
  const result = {}
  const query = searchQuery.value.toLowerCase()

  selectedTypes.value.forEach(type => {
    if (!records.value[type]) return

    result[type] = records.value[type].filter(record => {
      switch (type) {
        case 'food':
          return record.food_name.toLowerCase().includes(query) ||
                 record.note?.toLowerCase().includes(query)
        case 'exercise':
          return getExerciseLabel(record.exercise_type).toLowerCase().includes(query) ||
                 record.note?.toLowerCase().includes(query)
        case 'mood':
          return getMoodLabel(record.mood_type).toLowerCase().includes(query) ||
                 record.note?.toLowerCase().includes(query)
        case 'health':
          return getFeelingLabel(record.feeling).toLowerCase().includes(query) ||
                 record.status.some(s => getStatusLabel(s).toLowerCase().includes(query)) ||
                 record.note?.toLowerCase().includes(query)
        default:
          return false
      }
    })
  })

  return result
})

// 按日期分组记录
const groupedByDateRecords = computed(() => {
  const groupedRecords = {}
  
  // 合并所有记录并按日期分组
  Object.entries(filteredRecords.value).forEach(([type, typeRecords]) => {
    typeRecords.forEach(record => {
      const date = record.record_date || record.created_at.split('T')[0]
      if (!groupedRecords[date]) {
        groupedRecords[date] = {
          food: [],
          exercise: [],
          mood: [],
          health: []
        }
      }
      
      groupedRecords[date][type].push(record)
    })
  })

  // 按日期降序排序
  return Object.entries(groupedRecords)
    .sort(([dateA], [dateB]) => new Date(dateB) - new Date(dateA))
    .reduce((acc, [date, records]) => {
      acc[date] = records
      return acc
    }, {})
})

// 格式化日期头部
const formatDateHeader = (date) => {
  const today = new Date().toLocaleDateString('zh-CN')
  const yesterday = new Date(Date.now() - 86400000).toLocaleDateString('zh-CN')
  
  if (date === today) {
    return '今天'
  } else if (date === yesterday) {
    return '昨天'
  }
  
  // 将日期字符串转换为Date对象
  const dateObj = new Date(date)
  // 格式化为"年-月-日"格式
  return dateObj.getFullYear() + '年' + (dateObj.getMonth() + 1) + '月' + dateObj.getDate() + '日'
}

// 获取用餐时间标签
const getMealTimeLabel = (mealTime) => {
  const labels = {
    breakfast: '早餐',
    lunch: '午餐',
    dinner: '晚餐',
    snack: '零食'
  }
  return labels[mealTime] || mealTime
}

// 获取运动类型标签
const getExerciseLabel = (type) => {
  const labels = {
    walk: '步行',
    run: '跑步',
    bike: '骑行',
    swim: '游泳',
    yoga: '瑜伽',
    gym: '健身',
    ball: '球类',
    other: '其他'
  }
  return labels[type] || type
}

// 获取运动强度标签
const getIntensityLabel = (intensity) => {
  const labels = {
    light: '轻度',
    medium: '中度',
    high: '剧烈'
  }
  return labels[intensity] || intensity
}

// 获取心情标签
const getMoodLabel = (type) => {
  const labels = {
    happy: '开心',
    calm: '平静',
    sad: '难过',
    angry: '生气',
    anxious: '焦虑',
    tired: '疲惫',
    excited: '兴奋',
    bored: '无聊'
  }
  return labels[type] || type
}

// 获取身体感受标签
const getFeelingLabel = (feeling) => {
  const labels = {
    energetic: '精力充沛',
    good: '状态不错',
    normal: '一般般',
    tired: '有点累'
  }
  return labels[feeling] || feeling
}

// 获取身体状态标签
const getStatusLabel = (status) => {
  const labels = {
    sleep_well: '睡眠充足',
    sleep_bad: '睡眠不足',
    appetite_good: '胃口好',
    appetite_bad: '没胃口',
    energetic: '精力充沛',
    fatigue: '疲劳乏力',
    muscle_sore: '肌肉酸痛',
    headache: '头疼',
    throat: '咽喉不适',
    stomach: '胃部不适',
    cold: '感冒发烧',
    allergy: '过敏'
  }
  return labels[status] || status
}

// 切换记录类型
const toggleType = (type) => {
  const index = selectedTypes.value.indexOf(type)
  if (index === -1) {
    selectedTypes.value.push(type)
  } else if (selectedTypes.value.length > 1) {
    selectedTypes.value.splice(index, 1)
  }
}

// 切换时间范围
const changeTimeRange = (days) => {
  selectedDays.value = days
  fetchRecords(days)
}

// 获取记录
const fetchRecords = async (days) => {
  try {
    const response = await getAllRecords(days)
    
    // 初始化记录对象
    const recordsByType = {
      food: [],
      exercise: [],
      mood: [],
      health: []
    }
    
    // 将数组数据按类型分组
    if (Array.isArray(response)) {
      response.forEach(record => {
        // 确保记录有正确的日期
        if (!record.record_date && record.created_at) {
          if (typeof record.created_at === 'string') {
            record.record_date = record.created_at.split('T')[0]
          } else if (record.created_at instanceof Date) {
            record.record_date = record.created_at.toISOString().split('T')[0]
          }
        }
        
        if (record.type && recordsByType[record.type]) {
          recordsByType[record.type].push(record)
        }
      })
    } else if (response.data && Array.isArray(response.data)) {
      // 如果响应包装在data字段中
      response.data.forEach(record => {
        // 确保记录有正确的日期
        if (!record.record_date && record.created_at) {
          if (typeof record.created_at === 'string') {
            record.record_date = record.created_at.split('T')[0]
          } else if (record.created_at instanceof Date) {
            record.record_date = record.created_at.toISOString().split('T')[0]
          }
        }
        
        if (record.type && recordsByType[record.type]) {
          recordsByType[record.type].push(record)
        }
      })
    }
    
    // 更新记录状态
    records.value = recordsByType
    
    console.log('获取到的记录:', records.value)
  } catch (error) {
    console.error('获取记录失败:', error)
  }
}

// 编辑记录相关状态
const isEditDialogVisible = ref(false)
const editingRecord = ref(null)
const editingType = ref('')

// 编辑记录
const editRecord = (record, type) => {
  editingRecord.value = { ...record }
  
  // 使用created_at作为record_date
  if (record.created_at) {
    editingRecord.value.record_date = record.created_at.split('T')[0]
  } else {
    editingRecord.value.record_date = formatDateForInput(new Date())
  }
  
  editingType.value = type
  isEditDialogVisible.value = true
}

// 保存编辑
const saveEdit = async () => {
  try {
    const recordToSave = { ...editingRecord.value }
    if (recordToSave.record_date) {
      recordToSave.record_date = recordToSave.record_date.split('T')[0]
    }
    
    const updateFunctions = {
      food: updateFoodRecord,
      exercise: updateExerciseRecord,
      mood: updateMoodRecord,
      health: updateHealthRecord
    }
    
    const updateFunction = updateFunctions[editingType.value]
    if (!updateFunction) {
      throw new Error(`Unknown record type: ${editingType.value}`)
    }
    
    const response = await updateFunction(recordToSave.id, recordToSave)
    if (response.status === 200) {
      alert('记录已更新')
      isEditDialogVisible.value = false
      fetchRecords(selectedDays.value)
    }
  } catch (error) {
    console.error('更新记录失败:', error)
    alert('更新记录失败，请重试')
  }
}

// 删除确认
const confirmDelete = (id, type) => {
  if (confirm('确定要删除这条记录吗？')) {
    handleDelete(id, type)
  }
}

// 删除记录
const handleDelete = async (id, type) => {
  try {
    // 只传递ID参数
    await deleteRecord(id)
    alert('记录已删除')
    fetchRecords(selectedDays.value)
  } catch (error) {
    console.error('删除记录失败:', error)
    alert('删除记录失败，请重试')
  }
}

// 获取记录类型标签
const getRecordTypeLabel = (type) => {
  const labels = {
    food: '饮食',
    exercise: '运动',
    mood: '心情',
    health: '身体状况'
  }
  return labels[type] || type
}

// 切换身体状态
const toggleStatus = (type) => {
  if (!editingRecord.value.status) {
    editingRecord.value.status = []
  }
  const index = editingRecord.value.status.indexOf(type)
  if (index === -1) {
    editingRecord.value.status.push(type)
  } else {
    editingRecord.value.status.splice(index, 1)
  }
}

// 添加记录相关状态
const isAddDialogVisible = ref(false)
const selectedRecordType = ref(null)

// 显示添加记录对话框
const showAddRecordDialog = () => {
  isAddDialogVisible.value = true
}

// 选择记录类型
const selectRecordType = (type) => {
  selectedRecordType.value = type
  // 初始化编辑记录对象
  if (type === 'health') {
    editingRecord.value = { status: [], record_date: formatDateForInput(new Date()) }
  } else if (type === 'exercise') {
    editingRecord.value = { duration: 30, intensity: 'medium', record_date: formatDateForInput(new Date()) }
  } else if (type === 'food') {
    editingRecord.value = { meal_time: 'lunch', record_date: formatDateForInput(new Date()) }
  } else if (type === 'mood') {
    editingRecord.value = { mood_type: 'happy', record_date: formatDateForInput(new Date()) }
  } else {
    editingRecord.value = { record_date: formatDateForInput(new Date()) }
  }
}

// 返回记录类型选择
const backToTypeSelection = () => {
  selectedRecordType.value = null
  editingRecord.value = {}
}

// 关闭添加记录对话框
const closeAddDialog = () => {
  isAddDialogVisible.value = false
  selectedRecordType.value = null
  editingRecord.value = {}
}

const mealTimes = [
  { value: 'breakfast', label: '早餐', icon: '🌅' },
  { value: 'lunch', label: '午餐', icon: '🌞' },
  { value: 'dinner', label: '晚餐', icon: '🌙' },
  { value: 'snack', label: '零食', icon: '🍪' }
]

const exerciseTypes = [
  { type: 'walking', label: '步行', icon: '🚶' },
  { type: 'running', label: '跑步', icon: '🏃' },
  { type: 'cycling', label: '骑行', icon: '🚴' },
  { type: 'swimming', label: '游泳', icon: '🏊' },
  { type: 'yoga', label: '瑜伽', icon: '🧘' },
  { type: 'gym', label: '健身', icon: '💪' },
  { type: 'basketball', label: '篮球', icon: '🏀' },
  { type: 'football', label: '足球', icon: '⚽' }
]

const intensityLevels = [
  { level: 'light', label: '轻度', icon: '🌱' },
  { level: 'medium', label: '中度', icon: '🌿' },
  { level: 'high', label: '剧烈', icon: '🌳' }
]

const moods = [
  { type: 'happy', label: '开心', icon: '😊' },
  { type: 'calm', label: '平静', icon: '😌' },
  { type: 'sad', label: '难过', icon: '😢' },
  { type: 'angry', label: '生气', icon: '😠' },
  { type: 'anxious', label: '焦虑', icon: '😰' },
  { type: 'tired', label: '疲惫', icon: '😫' },
  { type: 'excited', label: '兴奋', icon: '🤩' },
  { type: 'bored', label: '无聊', icon: '😑' }
]

const feelings = [
  { type: 'energetic', label: '精力充沛', icon: '⚡' },
  { type: 'good', label: '状态不错', icon: '👍' },
  { type: 'normal', label: '一般般', icon: '😐' },
  { type: 'tired', label: '有点累', icon: '😪' }
]

const healthStatus = [
  { type: 'sleep_well', label: '睡眠充足', icon: '😴' },
  { type: 'sleep_bad', label: '睡眠不足', icon: '🥱' },
  { type: 'appetite_good', label: '胃口好', icon: '🍽️' },
  { type: 'appetite_bad', label: '没胃口', icon: '🤢' },
  { type: 'energetic', label: '精力充沛', icon: '💪' },
  { type: 'fatigue', label: '疲劳乏力', icon: '😫' },
  { type: 'muscle_sore', label: '肌肉酸痛', icon: '🦴' },
  { type: 'headache', label: '头疼', icon: '🤕' },
  { type: 'throat', label: '咽喉不适', icon: '😷' },
  { type: 'stomach', label: '胃部不适', icon: '🤢' },
  { type: 'cold', label: '感冒发烧', icon: '🤒' },
  { type: 'allergy', label: '过敏', icon: '🤧' }
]

// 保存新记录
const saveNewRecord = async () => {
  try {
    let isValid = true
    let errorMessage = ''

    // 验证表单
    if (selectedRecordType.value === 'food') {
      if (!editingRecord.value.food_name) {
        isValid = false
        errorMessage = '请输入食物名称'
      }
      if (!editingRecord.value.meal_time) {
        isValid = false
        errorMessage = '请选择用餐时间'
      }
    } else if (selectedRecordType.value === 'exercise') {
      if (!editingRecord.value.exercise_type) {
        isValid = false
        errorMessage = '请选择运动类型'
      } else if (!editingRecord.value.duration) {
        isValid = false
        errorMessage = '请输入运动时长'
      } else if (!editingRecord.value.intensity) {
        isValid = false
        errorMessage = '请选择运动强度'
      }
    } else if (selectedRecordType.value === 'mood') {
      if (!editingRecord.value.mood_type) {
        isValid = false
        errorMessage = '请选择心情类型'
      }
    } else if (selectedRecordType.value === 'health') {
      if (!editingRecord.value.feeling) {
        isValid = false
        errorMessage = '请选择身体感受'
      }
    }

    if (!isValid) {
      alert(errorMessage)
      return
    }

    // 将record_date转换为created_at
    const recordToSave = { ...editingRecord.value }
    if (recordToSave.record_date) {
      recordToSave.record_date = recordToSave.record_date.split('T')[0]
    }

    console.log('保存记录，类型:', selectedRecordType.value, '数据:', recordToSave)
    
    let response
    
    // 尝试使用fetch直接提交
    try {
      const token = userStore.state.token
      console.log('使用fetch直接提交，token:', token)
      
      // 使用相对路径，避免硬编码端口
      const fetchResponse = await fetch('/api/records', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token ? `Bearer ${token}` : ''
        },
        body: JSON.stringify({ 
          type: selectedRecordType.value, 
          ...recordToSave 
        })
      })
      
      if (!fetchResponse.ok) {
        throw new Error(`HTTP错误: ${fetchResponse.status}`)
      }
      
      response = await fetchResponse.json()
      console.log('fetch响应:', response)
    } catch (fetchError) {
      console.error('fetch错误:', fetchError)
      
      // 如果fetch失败，尝试使用API函数
      console.log('尝试使用API函数')
      const createFunctions = {
        food: createFoodRecord,
        exercise: createExerciseRecord,
        mood: createMoodRecord,
        health: createHealthRecord
      }
      
      response = await createFunctions[selectedRecordType.value](recordToSave)
    }
    
    console.log('保存记录响应:', response)
    
    // 检查响应是否有效
    if (response && (response.id || response.success)) {
      // 先显示提醒
      alert('记录添加成功！')
      // 然后刷新数据
      await fetchRecords(selectedDays.value)
      // 最后关闭对话框
      isAddDialogVisible.value = false
      selectedRecordType.value = null
      editingRecord.value = {}
    } else {
      alert(response?.message || '保存记录失败')
    }
  } catch (error) {
    console.error('保存记录失败:', error)
    alert('保存记录失败，请重试: ' + (error.message || '未知错误'))
  }
}

// 日期相关计算
const today = computed(() => formatDateForInput(new Date()))
const oneMonthAgo = computed(() => {
  const date = new Date()
  date.setMonth(date.getMonth() - 1)
  return formatDateForInput(date)
})

// 格式化日期为 input[type=date] 所需的格式 (YYYY-MM-DD)
const formatDateForInput = (date) => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const isDropdownVisible = ref(false)
const userMenuRef = ref(null)

const toggleDropdown = () => {
  isDropdownVisible.value = !isDropdownVisible.value
}

const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    isDropdownVisible.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

const username = computed(() => userStore.state.username)

onMounted(() => {
  fetchRecords(selectedDays.value)
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.records-page {
  min-height: 100vh;
  background: #f1f5f9;
  padding-top: 4rem; /* 为固定导航栏留出空间 */
}

.glass-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.5);
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
  margin: 0;
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

.user-menu {
  position: relative;
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
}

.username {
  font-weight: 500;
  color: #1e293b;
}

.dropdown-arrow {
  font-size: 0.75rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  background: white;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  min-width: 160px;
  z-index: 1000;
}

.dropdown-header {
  padding: 1rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.signed-in {
  font-size: 0.875rem;
  color: #64748b;
}

.dropdown-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 1rem 0;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 0.75rem 1rem;
  text-align: left;
  color: #1e293b;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.item-icon {
  margin-right: 0.5rem;
}

.main-content {
  max-width: 1280px;
  margin: 2rem auto;
  padding: 0 2rem;
}

/* 页面标题区域 */
.page-header {
  margin-bottom: 3rem;
  text-align: center;
}

.title-section {
  margin-bottom: 2rem;
  position: relative;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  padding-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #64748b;
  margin: 0;
}

.add-record-btn {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  background: #3b82f6;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-record-btn:hover {
  background: #2563eb;
  transform: translateY(-50%) scale(1.05);
}

.plus-icon {
  font-size: 1.25rem;
  font-weight: bold;
}

/* 记录类型过滤器 */
.record-types {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 2rem 0;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.type-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0;
  background: transparent;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.type-btn:hover {
  color: #3b82f6;
}

.type-btn.active {
  background: transparent;
  color: #3b82f6;
}

.type-btn::after {
  content: '';
  position: absolute;
  bottom: -1rem;
  left: 0;
  width: 0;
  height: 2px;
  background: #3b82f6;
  transition: width 0.3s ease;
}

.type-btn:hover::after,
.type-btn.active::after {
  width: 100%;
}

.type-btn .icon {
  font-size: 1.25rem;
}

/* 搜索和时间过滤器 */
.filters {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.time-select {
  padding: 0.75rem 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  min-width: 150px;
}

.search-input {
  padding: 0.75rem 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #1e293b;
  width: 300px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 记录列表样式 */
.records-list {
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.date-group {
  border-bottom: 1px solid #e2e8f0;
}

.date-group:last-child {
  border-bottom: none;
}

.date-header {
  padding: 1.5rem 2rem;
  background: #f8fafc;
  font-weight: 600;
  color: #1e293b;
}

.record-section {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.record-section:last-child {
  border-bottom: none;
}

.record-section h3 {
  color: #64748b;
  font-size: 1rem;
  margin: 0 0 1rem 0;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  margin-bottom: 0.75rem;
}

.record-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.meal-time, .exercise-type, .mood-type, .feeling {
  font-weight: 500;
  color: #333;
}

.duration, .intensity {
  color: #666;
}

.status-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.status-tag {
  padding: 2px 8px;
  background: #e9ecef;
  border-radius: 12px;
  font-size: 0.875rem;
  color: #495057;
}

.note {
  color: #666;
  font-style: italic;
}

.record-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.5rem;
  border: none;
  background: none;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.3s ease;
  border-radius: 0.5rem;
}

.edit-btn:hover, .delete-btn:hover {
  opacity: 1;
  background: #f1f5f9;
}

.empty-state {
  padding: 4rem 2rem;
  text-align: center;
  color: #64748b;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .header-content {
    padding: 1rem;
  }

  .main-nav {
    gap: 0.5rem;
  }

  .nav-item {
    padding: 0.5rem;
  }

  .main-content {
    padding: 0 1rem;
  }
}

/* 对话框样式 */
.dialog-overlay, .edit-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-content, .edit-dialog {
  position: relative;
  z-index: 1001;
  background: rgba(255, 255, 255, 0.98);
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  width: 480px;
  max-width: 95vw;
  max-height: 90vh;
  overflow-y: auto;
  animation: dialogShow 0.3s ease-out;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

@keyframes dialogShow {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 20px 20px 0 20px;
}

.dialog-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #1d1d1f;
  margin: 0;
}

.close-btn {
  font-size: 28px;
  line-height: 1;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #1e293b;
}

.dialog-body {
  padding: 0 20px 20px 20px;
}

/* 记录类型选择网格 */
.record-type-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.record-type-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  background: white;
  transition: all 0.3s ease;
  cursor: pointer;
}

.record-type-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  border-color: #3b82f6;
}

.type-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.type-label {
  font-size: 16px;
  font-weight: 500;
  color: #1e293b;
}

/* 表单样式 */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #1e293b;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 16px;
  min-height: 100px;
  resize: vertical;
  transition: all 0.3s ease;
}

.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 按钮网格 */
.meal-time-buttons,
.exercise-grid,
.mood-grid,
.feeling-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.meal-time-btn,
.exercise-btn,
.mood-btn,
.feeling-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  transition: all 0.3s ease;
  cursor: pointer;
}

.meal-time-btn:hover,
.exercise-btn:hover,
.mood-btn:hover,
.feeling-btn:hover {
  border-color: #3b82f6;
}

.meal-time-btn.active,
.exercise-btn.active,
.mood-btn.active,
.feeling-btn.active {
  background: #ebf5ff;
  border-color: #3b82f6;
  color: #3b82f6;
}

.meal-icon,
.exercise-icon,
.mood-icon,
.feeling-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.meal-label,
.exercise-label,
.mood-label,
.feeling-label {
  font-size: 14px;
}

/* 强度按钮 */
.intensity-buttons {
  display: flex;
  gap: 12px;
}

.intensity-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  transition: all 0.3s ease;
  cursor: pointer;
}

.intensity-btn:hover {
  border-color: #3b82f6;
}

.intensity-btn.active {
  background: #ebf5ff;
  border-color: #3b82f6;
  color: #3b82f6;
}

/* 健康状态标签 */
.status-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.status-tag {
  padding: 8px 12px;
  border: 2px solid #e2e8f0;
  border-radius: 20px;
  background: white;
  font-size: 14px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.status-tag:hover {
  border-color: #3b82f6;
}

.status-tag.active {
  background: #ebf5ff;
  border-color: #3b82f6;
  color: #3b82f6;
}

/* 对话框底部按钮 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 0 0 20px 20px;
}

.back-btn,
.cancel-btn,
.submit-btn {
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

.back-btn:hover {
  background: #e2e8f0;
}

.cancel-btn {
  background: white;
  border: 1px solid #e2e8f0;
  color: #64748b;
}

.cancel-btn:hover {
  background: #f1f5f9;
}

.submit-btn {
  background: #3b82f6;
  border: none;
  color: white;
}

.submit-btn:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(37, 99, 235, 0.2);
}

/* 响应式调整 */
@media (max-width: 480px) {
  .record-type-grid,
  .meal-time-buttons,
  .exercise-grid,
  .mood-grid,
  .feeling-grid {
    grid-template-columns: 1fr;
  }
  
  .intensity-buttons {
    flex-direction: column;
  }
  
  .dialog-footer {
    flex-direction: column-reverse;
  }
  
  .back-btn,
  .cancel-btn,
  .submit-btn {
    width: 100%;
    margin-bottom: 8px;
  }
}
</style> 