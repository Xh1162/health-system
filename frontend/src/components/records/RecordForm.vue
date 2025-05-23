<template>
  <div class="record-form">
    <!-- 记录类型选择 -->
    <div class="record-types">
      <button
        v-for="type in recordTypes"
        :key="type.value"
        :class="['type-btn', { active: recordType === type.value }]"
        @click="setRecordType(type.value)"
      >
        <span class="icon">{{ type.icon }}</span>
        {{ type.label }}
      </button>
    </div>

    <!-- 食物记录表单 -->
    <div v-if="recordType === 'food'" class="form-container">
      <div class="form-group">
        <label>用餐时间</label>
        <div class="meal-time-buttons">
          <button 
            v-for="meal in mealTimes" 
            :key="meal.value"
            :class="['meal-time-btn', { active: selectedMealTime === meal.value }]"
            @click="selectedMealTime = meal.value"
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
          v-model="foodName"
          class="form-input"
          placeholder="输入食物名称"
        />
      </div>
      <div class="form-group">
        <label>备注</label>
        <textarea 
          v-model="foodNote"
          class="form-textarea"
          placeholder="添加备注..."
        ></textarea>
      </div>
    </div>

    <!-- 运动记录表单 -->
    <div v-if="recordType === 'exercise'" class="form-container">
      <div class="form-group">
        <label>运动类型</label>
        <div class="exercise-grid">
          <button 
            v-for="exercise in exerciseTypes" 
            :key="exercise.type"
            :class="['exercise-btn', { active: selectedExercise === exercise.type }]"
            @click="selectedExercise = exercise.type"
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
          v-model="exerciseDuration"
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
            :class="['intensity-btn', { active: selectedIntensity === intensity.level }]"
            @click="selectedIntensity = intensity.level"
          >
            <span class="intensity-icon">{{ intensity.icon }}</span>
            <span class="intensity-label">{{ intensity.label }}</span>
          </button>
        </div>
      </div>
      <div class="form-group">
        <label>备注</label>
        <textarea 
          v-model="exerciseNote"
          class="form-textarea"
          placeholder="添加备注..."
        ></textarea>
      </div>
    </div>

    <!-- 心情记录表单 -->
    <div v-if="recordType === 'mood'" class="form-container">
      <div class="form-group">
        <label>心情</label>
        <div class="mood-grid">
          <button 
            v-for="mood in moods" 
            :key="mood.type"
            :class="['mood-btn', { active: selectedMood === mood.type }]"
            @click="selectedMood = mood.type"
          >
            <span class="mood-icon">{{ mood.icon }}</span>
            <span class="mood-label">{{ mood.label }}</span>
          </button>
        </div>
      </div>
      <div class="form-group">
        <label>心情小记</label>
        <textarea 
          v-model="moodNote"
          class="form-textarea"
          placeholder="记录一下此刻的想法..."
        ></textarea>
      </div>
    </div>

    <!-- 身体状况记录表单 -->
    <div v-if="recordType === 'body_status'" class="form-container">
      <div class="form-group">
        <label>整体感受</label>
        <div class="feeling-grid">
          <button 
            v-for="feeling in feelings" 
            :key="feeling.type"
            :class="['feeling-btn', { active: selectedFeeling === feeling.type }]"
            @click="selectedFeeling = feeling.type"
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
            :class="['status-tag', { active: selectedStatus.includes(status.type) }]"
            @click="toggleStatus(status.type)"
          >
            {{ status.icon }} {{ status.label }}
          </button>
        </div>
      </div>
      <div class="form-group">
        <label>身体数据</label>
        <div class="body-data-grid">
          <div class="body-data-item">
            <label for="weight">体重 (kg)</label>
            <input type="number" id="weight" class="form-input" v-model.number="bodyStatusData.weight_kg" placeholder="例如: 70.5" step="0.1" min="0" />
          </div>
          <div class="body-data-item">
            <label for="bmi">BMI (可选)</label>
            <input type="number" id="bmi" class="form-input" v-model.number="bodyStatusData.bmi" placeholder="例如: 22.5" step="0.1" min="0" />
          </div>
        </div>
      </div>
      <div class="form-group">
        <label>备注 (可选)</label>
        <textarea 
          v-model="note" 
          class="form-textarea"
          placeholder="记录一些额外信息..."
        ></textarea>
      </div>
    </div>

    <!-- 日期选择 -->
    <div class="form-group">
      <label>日期</label>
      <input 
        type="date" 
        v-model="selectedDate"
        class="form-input date-input"
        :max="today"
      />
    </div>

    <!-- 提交按钮 -->
    <button 
      class="submit-btn" 
      @click="submitRecord"
      :disabled="isSubmitting"
    >
      {{ isSubmitting ? '提交中...' : '记录' }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { createFoodRecord, createExerciseRecord, createMoodRecord } from '../../api/records'
import api from '../../api/index'
import { ElMessage } from 'element-plus'

// 记录类型
const recordType = ref('food')
const recordTypes = [
  { value: 'food', label: '饮食', icon: '🍽️' },
  { value: 'exercise', label: '运动', icon: '🏃' },
  { value: 'mood', label: '心情', icon: '😊' },
  { value: 'body_status', label: '身体状况', icon: '⚖️' }
]

// 食物记录表单
const selectedMealTime = ref('')
const foodName = ref('')
const foodNote = ref('')

// 运动记录表单
const selectedExercise = ref('')
const exerciseDuration = ref(30)
const selectedIntensity = ref('medium')
const exerciseNote = ref('')

// 心情记录表单
const selectedMood = ref('')
const moodNote = ref('')

// 身体状况表单
const selectedFeeling = ref('')
const selectedStatus = ref([])
const bodyStatusData = reactive({ weight_kg: null, bmi: null })
const note = ref('')

// 日期选择
const selectedDate = ref(new Date().toISOString().split('T')[0])
const today = computed(() => new Date().toISOString().split('T')[0])

// 提交状态
const isSubmitting = ref(false)

// 选项数据
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

// 设置记录类型
const setRecordType = (type) => {
  recordType.value = type
}

// 切换健康状态
const toggleStatus = (type) => {
  const index = selectedStatus.value.indexOf(type)
  if (index === -1) {
    selectedStatus.value.push(type)
  } else {
    selectedStatus.value.splice(index, 1)
  }
}

// 显示成功消息
const showSuccessMessage = (message) => {
  ElMessage({
    message,
    type: 'success',
    duration: 2000
  })
}

// 提交记录
const submitRecord = async () => {
  isSubmitting.value = true
  try {
    let payload = {
      record_date: selectedDate.value,
      type: recordType.value
    };
    let apiCallPromise = null;

    if (recordType.value === 'food') {
      if (!selectedMealTime.value || !foodName.value) {
        ElMessage.warning('请填写用餐时间和食物名称')
        return;
      }
      payload = { 
        ...payload,
        meal_time: selectedMealTime.value,
        food_name: foodName.value,
        note: foodNote.value // Assuming food has its own note
      };
      // Use specific function or generic call
      // apiCallPromise = createFoodRecord(payload);
      // Let's switch to generic for consistency
      apiCallPromise = api.post('/records', payload);
      
    } else if (recordType.value === 'exercise') {
      if (!selectedExercise.value || !exerciseDuration.value) {
        ElMessage.warning('请选择运动类型并填写时长')
        return;
      }
       payload = { 
         ...payload,
         exercise_type: selectedExercise.value,
         duration: parseInt(exerciseDuration.value),
         intensity: selectedIntensity.value || 'medium',
         note: exerciseNote.value // Assuming exercise has its own note
       };
      // apiCallPromise = createExerciseRecord(payload);
      apiCallPromise = api.post('/records', payload);

    } else if (recordType.value === 'mood') {
      if (!selectedMood.value) {
        ElMessage.warning('请选择心情')
        return;
      }
      payload = {
        ...payload,
        mood_type: selectedMood.value,
        note: moodNote.value // Assuming mood has its own note
      };
      // apiCallPromise = createMoodRecord(payload);
      apiCallPromise = api.post('/records', payload);

    } else if (recordType.value === 'body_status') {
      if (!selectedFeeling.value) {
        // Maybe allow submitting without feeling/status?
        // ElMessage.warning('请选择整体感受')
        // return;
      }
      // Construct payload for body_status
      payload = {
        ...payload,
        feeling: selectedFeeling.value || null, // Send null if empty
        status: selectedStatus.value.length > 0 ? selectedStatus.value : null, // Send null if empty
        note: note.value // Use general note
      };
      // Add weight and BMI if present
      const weight = parseFloat(bodyStatusData.weight_kg);
      const bmi = parseFloat(bodyStatusData.bmi);
      if (!isNaN(weight)) {
        payload.weight_kg = weight;
      }
      if (!isNaN(bmi)) {
        payload.bmi = bmi;
      }
      
      // Use the generic api.post call directly, no need for createHealthRecord
      apiCallPromise = api.post('/records', payload); 
    }

    if (apiCallPromise) {
       await apiCallPromise;
       showSuccessMessage(` ${recordTypes.find(t => t.value === recordType.value)?.label || ''}记录已保存`);
       resetForm(recordType.value);
       resetForm('all'); // Also reset general note and date
    } else {
        console.error("No valid record type selected or API call promise not set.");
        ElMessage.error('无效的记录类型');
    }

  } catch (error) {
    console.error('Error submitting record:', error)
    ElMessage.error(error.response?.data?.message || '保存记录失败')
  } finally {
    isSubmitting.value = false
  }
}

// 重置表单
const resetForm = (type) => {
  if (type === 'food' || type === 'all') {
    selectedMealTime.value = ''
    foodName.value = ''
    foodNote.value = ''
  }
  
  if (type === 'exercise' || type === 'all') {
    selectedExercise.value = ''
    exerciseDuration.value = 30
    selectedIntensity.value = 'medium'
    exerciseNote.value = ''
  }
  
  if (type === 'mood' || type === 'all') {
    selectedMood.value = ''
    moodNote.value = ''
  }
  
  if (type === 'body_status' || type === 'all') {
    selectedFeeling.value = ''
    selectedStatus.value = []
    bodyStatusData.weight_kg = null
    bodyStatusData.bmi = null
  }
  
  if (type === 'all') {
    note.value = ''
    selectedDate.value = new Date().toISOString().split('T')[0]
  }
}

// 定义事件
const emit = defineEmits(['record-submitted'])
</script>

<style scoped>
.record-form {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.record-types {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.type-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: white;
  color: #64748b;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.type-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.type-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.form-container {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #1e293b;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
}

.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  min-height: 100px;
  resize: vertical;
}

.meal-time-buttons,
.exercise-grid,
.mood-grid,
.feeling-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.meal-time-btn,
.exercise-btn,
.mood-btn,
.feeling-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
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

.intensity-buttons {
  display: flex;
  gap: 0.5rem;
}

.intensity-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
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

.status-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.status-tag {
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  background: white;
  font-size: 0.875rem;
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

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  background: #3b82f6;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  background: #2563eb;
}

.submit-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .meal-time-buttons,
  .exercise-grid,
  .mood-grid,
  .feeling-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .intensity-buttons {
    flex-direction: column;
  }
}

.body-data-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  align-items: end;
}

.body-data-item label {
  display: block;
  margin-bottom: 0.3rem;
  font-size: 0.9em;
  color: #666;
}

.body-data-item input {
  width: 100%;
}
</style> 