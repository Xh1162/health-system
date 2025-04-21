<template>
  <div class="profile-page">
    <header class="glass-header">
      <div class="header-content">
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-item">首页</router-link>
          <router-link to="/records" class="nav-item">记录</router-link>
          <router-link to="/reports" class="nav-item">报告</router-link>
        </nav>
      </div>
    </header>

    <main class="profile-content">
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar-section">
            <div class="avatar-container">
              <img :src="avatarUrl" :alt="username" class="avatar" />
              <div class="avatar-overlay" @click="openAvatarUpload">
                <span class="change-avatar-text">更换头像</span>
                <input 
                  type="file" 
                  ref="avatarInput" 
                  @change="handleAvatarChange" 
                  accept="image/*" 
                  class="avatar-input" 
                />
              </div>
            </div>
          </div>
          <div class="user-info">
            <h1>{{ username }}</h1>
            <p class="join-date">注册于 {{ formatDate(userCreatedAt) }}</p>
          </div>
        </div>

        <div class="profile-body">
          <div class="info-section">
            <h2>个人信息</h2>
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">用户名</span>
                <div class="info-value-container">
                  <span v-if="!editMode.username" class="info-value">{{ username }}</span>
                  <div v-else class="edit-container">
                    <input v-model="editValues.username" class="edit-input" />
                  </div>
                  <button 
                    v-if="!editMode.username" 
                    @click="startEdit('username')" 
                    class="edit-btn"
                  >
                    编辑
                  </button>
                  <div v-else class="action-btns">
                    <button @click="saveEdit('username')" class="save-btn">保存</button>
                    <button @click="cancelEdit('username')" class="cancel-btn">取消</button>
                  </div>
                </div>
              </div>

              <div class="info-item">
                <span class="info-label">手机</span>
                <div class="info-value-container">
                  <span v-if="!editMode.phone" class="info-value">
                    {{ phone || '未设置' }}
                    <span v-if="phone && phoneVerified" class="verified-badge">已验证</span>
                    <span v-else-if="phone && !phoneVerified" class="unverified-badge">未验证</span>
                  </span>
                  <div v-else class="edit-container">
                    <input v-model="editValues.phone" class="edit-input" type="tel" />
                  </div>
                  <button 
                    v-if="!editMode.phone" 
                    @click="startEdit('phone')" 
                    class="edit-btn"
                  >
                    {{ phone ? '更换' : '添加' }}
                  </button>
                  <div v-else class="action-btns">
                    <button @click="saveEdit('phone')" class="save-btn">保存</button>
                    <button @click="cancelEdit('phone')" class="cancel-btn">取消</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="physical-section">
            <h2>身体信息</h2>
            <div v-if="!editMode.physical" class="info-grid">
              <div class="info-item">
                <span class="info-label">身高</span>
                <span class="info-value">{{ height ? `${height} cm` : '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">体重</span>
                <span class="info-value">{{ weight ? `${weight} kg` : '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">出生日期</span>
                <span class="info-value">{{ birthDate ? formatDate(birthDate) : '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">性别</span>
                <span class="info-value">
                  {{ gender ? getGenderText(gender) : '未设置' }}
                </span>
              </div>
              <div class="info-item">
                <span class="info-label">活动水平</span>
                <span class="info-value">
                  {{ getActivityLevelText(activityLevel) }}
                </span>
              </div>
              <div class="info-item edit-action-item">
                <button @click="startEdit('physical')" class="edit-btn full-width-btn">编辑身体信息</button>
              </div>
            </div>
            <div v-else class="edit-form">
              <div class="form-group">
                <label for="edit-height">身高 (cm)</label>
                <input id="edit-height" type="number" v-model.number="editValues.height" class="edit-input" placeholder="例如 175" />
              </div>
              <div class="form-group">
                <label for="edit-weight">体重 (kg)</label>
                <input id="edit-weight" type="number" step="0.1" v-model.number="editValues.weight" class="edit-input" placeholder="例如 68.5" />
              </div>
              <div class="form-group">
                <label for="edit-birthDate">出生日期</label>
                <input id="edit-birthDate" type="date" v-model="editValues.birthDate" class="edit-input" />
              </div>
              <div class="form-group">
                <label for="edit-gender">性别</label>
                <select id="edit-gender" v-model="editValues.gender" class="edit-input">
                  <option value="">请选择</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label for="edit-activityLevel">活动水平</label>
                <select id="edit-activityLevel" v-model="editValues.activityLevel" class="edit-input">
                  <option value="">请选择</option>
                  <option value="low">几乎不运动</option>
                  <option value="medium">适量运动（每周1-3次）</option>
                  <option value="high">经常运动（每周4-5次）</option>
                  <option value="very_high">专业运动员（每天运动）</option>
                </select>
              </div>
              <div class="action-btns physical-action-btns">
                <button @click="saveEdit('physical')" class="save-btn">保存</button>
                <button @click="cancelEdit('physical')" class="cancel-btn">取消</button>
              </div>
            </div>
          </div>

          <div class="security-section">
            <h2>账号安全</h2>
            <div class="security-item">
              <div class="security-info">
                <span class="security-label">密码</span>
                <span class="security-value">上次修改: {{ formatDate(passwordLastChanged) }}</span>
              </div>
              <button @click="showPasswordModal = true" class="change-btn">修改密码</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 密码修改弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay">
      <div class="modal-container">
        <div class="modal-header">
          <h3>修改密码</h3>
          <button @click="showPasswordModal = false" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>当前密码</label>
            <input 
              type="password" 
              v-model="passwordForm.currentPassword" 
              placeholder="请输入当前密码"
            />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input 
              type="password" 
              v-model="passwordForm.newPassword" 
              placeholder="请输入新密码"
            />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input 
              type="password" 
              v-model="passwordForm.confirmPassword" 
              placeholder="请再次输入新密码"
            />
          </div>
        </div>
        <!-- Add error display element here -->
        <div v-if="passwordError" class="modal-error-message">
          {{ passwordError }}
        </div>
        <div class="modal-footer">
          <button @click="showPasswordModal = false" class="cancel-btn">取消</button>
          <button @click="changePasswordHandler" class="save-btn">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { getUserProfile, updateUserProfile, uploadAvatar as userUploadAvatar } from '../api/user'
import { changePassword } from '../api/auth'
import { useRouter } from 'vue-router'
import useUserStore from '../stores/userStore'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
// 用户基本信息
const username = ref(userStore.state.username || '')
const phone = ref('')
const phoneVerified = ref(false)
const userCreatedAt = ref(new Date())
const passwordLastChanged = ref(new Date())
// 身体信息
const height = ref(null)
const weight = ref(null)
const birthDate = ref(null)
const gender = ref('')
const activityLevel = ref('')

// 编辑状态
const editMode = ref({
  username: false,
  phone: false,
  physical: false
})

// 编辑值 - Initialize with correct types
const editValues = ref({
  username: '',
  phone: '',
  height: null,
  weight: null,
  birthDate: null,
  gender: '',
  activityLevel: ''
})

// 密码修改
const showPasswordModal = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordError = ref(''); // Add ref for password error message

// 头像上传
const avatarInput = ref(null)
const loading = ref(false)
const router = useRouter()

// 计算头像URL
const avatarUrl = computed(() => {
  if (!userStore.state.avatar) {
    return 'https://via.placeholder.com/150'
  }
  return userStore.state.avatar
})

// 格式化日期
const formatDate = (date) => {
  if (!date) return '未知'
  
  const d = new Date(date)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// 获取活动水平文本描述
const getActivityLevelText = (level) => {
  if (!level) return '未设置'
  
  const activityTexts = {
    'low': '几乎不运动',
    'medium': '适量运动（每周1-3次）',
    'high': '经常运动（每周4-5次）',
    'very_high': '专业运动员（每天运动）'
  }
  
  return activityTexts[level] || level
}

// 添加 getGenderText 函数
const getGenderText = (value) => {
  if (value === 'male') return '男'
  if (value === 'female') return '女'
  if (value === 'other') return '其他'
  return '未设置'
}

// 获取用户信息和资料
const fetchProfileData = async () => {
  try {
    const data = await getUserProfile() // Use the new API function
    
    username.value = data.username || ''
    phone.value = data.phone || ''
    // phoneVerified logic might need backend support
    userCreatedAt.value = data.created_at ? new Date(data.created_at) : new Date()
    // passwordLastChanged needs a dedicated field from backend
    passwordLastChanged.value = data.password_last_changed || data.updated_at ? new Date(data.updated_at) : new Date()
    
    if (data.profile) {
      height.value = data.profile.height
      weight.value = data.profile.weight
      birthDate.value = data.profile.birth_date // Keep as YYYY-MM-DD string
      gender.value = data.profile.gender
      activityLevel.value = data.profile.activity_level
    }
    
    resetEditValues() // Initialize editValues after fetching
    
  } catch (error) {
    console.error("获取用户资料失败:", error)
    ElMessage.error(error.response?.data?.message || '获取用户资料失败')
  }
}

// 重置编辑值
const resetEditValues = () => {
  editValues.value.username = username.value
  editValues.value.phone = phone.value
  editValues.value.height = height.value
  editValues.value.weight = weight.value
  editValues.value.birthDate = birthDate.value // Keep as string
  editValues.value.gender = gender.value
  editValues.value.activityLevel = activityLevel.value
}

// 开始编辑
const startEdit = (field) => {
  resetEditValues() // Reset all fields first
  Object.keys(editMode.value).forEach(key => {
    editMode.value[key] = (key === field) // Set only the target field to true
  })
}

// 取消编辑
const cancelEdit = (field) => {
  editMode.value[field] = false
  resetEditValues() // Reset values on cancel
}

// 保存编辑
const saveEdit = async (field) => {
  try {
    let updateData = {}
    
    if (field === 'username' || field === 'phone') {
      // Basic info update
      if (field === 'username' && !editValues.value.username.trim()) {
        ElMessage.error('用户名不能为空'); return;
      }
      // Phone validation could be added here if needed
      updateData[field] = editValues.value[field]
    } else if (field === 'physical') {
      // Physical info update - construct the nested 'profile' object
      // Basic validation
      if (editValues.value.height === null || editValues.value.height === '') { ElMessage.error('请输入身高'); return; }
      if (editValues.value.weight === null || editValues.value.weight === '') { ElMessage.error('请输入体重'); return; }
      if (!editValues.value.birthDate) { ElMessage.error('请选择出生日期'); return; }
      if (!editValues.value.gender) { ElMessage.error('请选择性别'); return; }
      if (!editValues.value.activityLevel) { ElMessage.error('请选择活动水平'); return; }
      
      updateData.profile = {
        height: parseFloat(editValues.value.height) || null,
        weight: parseFloat(editValues.value.weight) || null,
        birth_date: editValues.value.birthDate, // Send as YYYY-MM-DD string
        gender: editValues.value.gender,
        activity_level: editValues.value.activityLevel
      }
    }
    
    console.log('更新数据:', updateData)
    
    // Call the unified update API
    const updatedProfile = await updateUserProfile(updateData)
    
    // Update local state from the response
    username.value = updatedProfile.username
    phone.value = updatedProfile.phone
    if (updatedProfile.profile) {
      height.value = updatedProfile.profile.height
      weight.value = updatedProfile.profile.weight
      birthDate.value = updatedProfile.profile.birth_date
      gender.value = updatedProfile.profile.gender
      activityLevel.value = updatedProfile.profile.activity_level
    }
    
    // Update store if username changed
    if (field === 'username') {
      userStore.updateUsername(updatedProfile.username)
    }

    editMode.value[field] = false
    ElMessage.success('信息更新成功')

  } catch (error) {
    console.error("更新失败:", error)
    ElMessage.error(error.response?.data?.message || '更新失败，请重试')
    cancelEdit(field) // Revert changes on error
  }
}

// 修改密码
const changePasswordHandler = async () => {
  passwordError.value = ''; // Clear previous error on new attempt
  try {
    if (!passwordForm.value.currentPassword) { passwordError.value = '请输入当前密码'; return; }
    if (!passwordForm.value.newPassword) { passwordError.value = '请输入新密码'; return; }
    if (passwordForm.value.newPassword.length < 8) { passwordError.value = '新密码至少需要8位'; return; }
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      passwordError.value = '两次输入的新密码不一致';
      return;
    }
    
    await changePassword({
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword
    }) // Use the imported auth API function
    
    ElMessage.success('密码修改成功')
    showPasswordModal.value = false
    passwordForm.value = { currentPassword: '', newPassword: '', confirmPassword: '' }
    passwordLastChanged.value = new Date() // Update timestamp locally
  } catch (error) {
    console.error('修改密码失败:', error)
    // Set the local error message to be displayed in the modal
    passwordError.value = error.response?.data?.message || '修改密码失败，请重试';
    // Optionally keep ElMessage for a toast notification as well
    // ElMessage.error(passwordError.value);
  }
}

// 打开头像上传
const openAvatarUpload = () => {
  avatarInput.value.click()
}

// 处理头像变更 - Use imported userUploadAvatar
const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  if (!file.type.startsWith('image/')) { ElMessage.error('请上传图片文件'); return; }
  if (file.size > 2 * 1024 * 1024) { ElMessage.error('图片大小不能超过2MB'); return; }
  
  loading.value = true
  ElMessage.info('头像上传中...')
  
  try {
    const formData = new FormData()
    formData.append('avatar', file)
    
    const data = await userUploadAvatar(formData) // Use the API function
    
    if (data.avatar) {
        userStore.updateAvatar(data.avatar) // updateAvatar ensures full URL
        ElMessage.success('头像更新成功')
    } else {
        throw new Error('服务器未返回头像地址')
    }
  } catch (error) {
    console.error('上传头像失败:', error)
    ElMessage.error(error.response?.data?.message || '头像上传失败')
  } finally {
      loading.value = false
      // Reset file input to allow uploading the same file again if needed
      if (avatarInput.value) {
          avatarInput.value.value = ''
      }
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchProfileData()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
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
  justify-content: center;
  align-items: center;
}

.main-nav {
  display: flex;
  gap: 2rem;
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

.profile-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 5rem 1.5rem 2rem;
}

.profile-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.profile-header {
  display: flex;
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-bottom: 1px solid #e2e8f0;
}

.avatar-section {
  margin-right: 2rem;
}

.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  cursor: pointer;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.change-avatar-text {
  color: white;
  font-size: 0.875rem;
}

.avatar-input {
  display: none;
}

.user-info {
  flex: 1;
}

.user-info h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem;
}

.join-date {
  color: #64748b;
  font-size: 0.875rem;
}

.profile-body {
  padding: 2rem;
}

.info-section,
.security-section {
  margin-bottom: 2rem;
}

h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.info-item {
  margin-bottom: 1rem;
}

.info-label {
  display: block;
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.info-value-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.info-value {
  font-size: 1rem;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.verified-badge,
.unverified-badge {
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
}

.verified-badge {
  background: #dcfce7;
  color: #166534;
}

.unverified-badge {
  background: #fee2e2;
  color: #991b1b;
}

.edit-container {
  flex: 1;
  margin-right: 0.5rem;
}

.edit-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.edit-btn,
.change-btn,
.save-btn,
.cancel-btn {
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-btn {
  background: transparent;
  color: #3b82f6;
  border: 1px solid #e2e8f0;
}

.edit-btn:hover {
  background: #f0f9ff;
  border-color: #3b82f6;
}

.action-btns {
  display: flex;
  gap: 0.5rem;
}

.save-btn {
  background: #3b82f6;
  color: white;
  border: none;
}

.save-btn:hover {
  background: #2563eb;
}

.cancel-btn {
  background: transparent;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

.cancel-btn:hover {
  background: #f1f5f9;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.security-info {
  display: flex;
  flex-direction: column;
}

.security-label {
  font-size: 1rem;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.security-value {
  font-size: 0.875rem;
  color: #64748b;
}

.change-btn {
  background: #3b82f6;
  color: white;
  border: none;
}

.change-btn:hover {
  background: #2563eb;
}

/* 密码修改弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background: white;
  border-radius: 0.5rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: #64748b;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .avatar-section {
    margin-right: 0;
    margin-bottom: 1.5rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}

.physical-section .info-grid {
  /* Adjust grid for physical info if needed, maybe fewer columns */
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); 
}

.edit-action-item {
  grid-column: 1 / -1; /* Make edit button span full width */
  margin-top: 1rem;
}

.full-width-btn {
  width: 100%;
  justify-content: center;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.875rem;
  color: #64748b;
}

.physical-action-btns {
  margin-top: 1rem;
  justify-content: flex-end; /* Align buttons to the right */
}

/* Comment out the problematic style for the date picker indicator */
/*
.edit-input[type="date"]::-webkit-calendar-picker-indicator {
    background: transparent;
    bottom: 0;
    color: transparent;
    cursor: pointer;
    height: auto;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
    width: auto;
}
*/

select.edit-input {
  /* Style select elements similarly to inputs */
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background-color: white; 
  width: 100%;
}

/* Add styles for the modal error message */
.modal-error-message {
  color: #ef4444; /* Red color for errors */
  background-color: #fee2e2; /* Light red background */
  border: 1px solid #fca5a5; /* Red border */
  border-radius: 0.375rem; /* Rounded corners */
  padding: 0.75rem; /* Padding */
  margin-top: 1rem; /* Space above the footer */
  margin-bottom: -0.5rem; /* Adjust spacing if needed before footer */
  font-size: 0.875rem; /* Font size */
  text-align: center;
}
</style> 