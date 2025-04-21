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
                <span class="info-label">邮箱</span>
                <div class="info-value-container">
                  <span v-if="!editMode.email" class="info-value">
                    {{ email || '未设置' }}
                    <span v-if="email && emailVerified" class="verified-badge">已验证</span>
                    <span v-else-if="email && !emailVerified" class="unverified-badge">未验证</span>
                  </span>
                  <div v-else class="edit-container">
                    <input v-model="editValues.email" class="edit-input" type="email" />
                  </div>
                  <button 
                    v-if="!editMode.email" 
                    @click="startEdit('email')" 
                    class="edit-btn"
                  >
                    {{ email ? '更换' : '添加' }}
                  </button>
                  <div v-else class="action-btns">
                    <button @click="saveEdit('email')" class="save-btn">保存</button>
                    <button @click="cancelEdit('email')" class="cancel-btn">取消</button>
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
            <div class="info-grid">
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
                  {{ gender ? (gender === 'male' ? '男' : gender === 'female' ? '女' : gender) : '未设置' }}
                </span>
              </div>

              <div class="info-item">
                <span class="info-label">活动水平</span>
                <span class="info-value">
                  {{ getActivityLevelText(activityLevel) }}
                </span>
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
        <div class="modal-footer">
          <button @click="showPasswordModal = false" class="cancel-btn">取消</button>
          <button @click="changePassword" class="save-btn">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import * as authApi from '../api/auth'
import { useRouter } from 'vue-router'
import useUserStore from '../stores/userStore'
import { ElMessage } from 'element-plus'
import { uploadAvatar } from '../api/user'

const userStore = useUserStore()
// 用户基本信息
const username = ref(userStore.state.username || '')
const email = ref('')
const phone = ref('')
const emailVerified = ref(false)
const phoneVerified = ref(false)
const userCreatedAt = ref(new Date())
const passwordLastChanged = ref(new Date())
// 添加身体信息
const height = ref(null)
const weight = ref(null)
const birthDate = ref(null)
const gender = ref('')
const activityLevel = ref('')

// 编辑状态
const editMode = ref({
  username: false,
  email: false,
  phone: false
})

// 编辑值
const editValues = ref({
  username: '',
  email: '',
  phone: ''
})

// 密码修改
const showPasswordModal = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

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

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const response = await authApi.getUserInfo()
    
    if (response.data) {
      const userData = response.data
      username.value = userData.username
      email.value = userData.email
      phone.value = userData.phone
      emailVerified.value = userData.email_verified
      phoneVerified.value = userData.phone_verified
      userCreatedAt.value = userData.created_at
      passwordLastChanged.value = userData.password_last_changed || userData.created_at
      
      // 更新编辑值
      editValues.value.username = userData.username
      editValues.value.email = userData.email || ''
      editValues.value.phone = userData.phone || ''
      
      // 获取用户个人资料
      try {
        const profileResponse = await axios.get('http://localhost:5008/api/user/profile', {
          headers: {
            'Authorization': `Bearer ${userStore.state.token}`
          }
        })
        
        if (profileResponse.data && profileResponse.data.profile) {
          const profile = profileResponse.data.profile
          height.value = profile.height
          weight.value = profile.weight
          birthDate.value = profile.birth_date
          gender.value = profile.gender
          activityLevel.value = profile.activity_level
        }
      } catch (profileError) {
        console.error('获取用户个人资料失败:', profileError)
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 开始编辑
const startEdit = (field) => {
  editMode.value[field] = true
}

// 取消编辑
const cancelEdit = (field) => {
  editMode.value[field] = false
  
  // 重置编辑值
  if (field === 'username') {
    editValues.value.username = username.value
  } else if (field === 'email') {
    editValues.value.email = email.value || ''
  } else if (field === 'phone') {
    editValues.value.phone = phone.value || ''
  }
}

// 保存编辑
const saveEdit = async (field) => {
  try {
    if (field === 'username') {
      // 验证用户名
      if (!editValues.value.username.trim()) {
        alert('用户名不能为空')
        return
      }
      
      await authApi.updateUserInfo(userStore.state.userId, {
        username: editValues.value.username
      })
      
      username.value = editValues.value.username
      userStore.updateUsername(editValues.value.username)
    } else if (field === 'email') {
      // 验证邮箱
      if (!editValues.value.email.trim()) {
        alert('邮箱不能为空')
        return
      }
      
      // 这里应该有发送验证码的逻辑
      alert('邮箱更新功能需要后端支持，暂未实现')
      return
    } else if (field === 'phone') {
      // 验证手机号
      if (!editValues.value.phone.trim()) {
        alert('手机号不能为空')
        return
      }
      
      // 这里应该有发送验证码的逻辑
      alert('手机号更新功能需要后端支持，暂未实现')
      return
    }
    
    editMode.value[field] = false
  } catch (error) {
    console.error(`保存${field}失败:`, error)
    alert(error.response?.data?.message || `保存${field}失败`)
  }
}

// 修改密码
const changePassword = async () => {
  try {
    // 验证密码
    if (!passwordForm.value.currentPassword) {
      alert('请输入当前密码')
      return
    }
    
    if (!passwordForm.value.newPassword) {
      alert('请输入新密码')
      return
    }
    
    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      alert('两次输入的新密码不一致')
      return
    }
    
    await authApi.changePassword(
      passwordForm.value.currentPassword,
      passwordForm.value.newPassword
    )
    
    alert('密码修改成功')
    showPasswordModal.value = false
    
    // 清空表单
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
    
    // 更新密码修改时间
    passwordLastChanged.value = new Date()
  } catch (error) {
    console.error('修改密码失败:', error)
    alert(error.response?.data?.message || '修改密码失败')
  }
}

// 打开头像上传
const openAvatarUpload = () => {
  avatarInput.value.click()
}

// 处理头像变更
const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  // 验证文件类型
  if (!file.type.startsWith('image/')) {
    alert('请上传图片文件')
    return
  }
  
  // 验证文件大小
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过2MB')
    return
  }
  
  try {
    // 显示上传中提示
    alert('头像上传中，请稍候...')
    
    // 构建FormData对象
    const formData = new FormData()
    formData.append('avatar', file)
    
    // 构建请求URL
    const apiBaseUrl = 'http://localhost:5008'
    const apiUrl = `${apiBaseUrl}/api/auth/avatar/${userStore.state.userData.id}`
    
    // 发送请求
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${userStore.state.token}`
      }
    })
    
    // 解析响应
    const result = await response.json()
    console.log('上传响应数据:', result)
    
    if (result.success) {
      // 确保返回的数据包含avatar字段
      const avatarUrl = result.data?.avatar
      
      if (avatarUrl) {
        console.log('头像上传成功，URL:', avatarUrl)
        
        // 确保URL是完整路径
        const fullAvatarUrl = avatarUrl.startsWith('http') 
          ? avatarUrl 
          : avatarUrl.startsWith('/') 
            ? `${apiBaseUrl}${avatarUrl}` 
            : `${apiBaseUrl}/${avatarUrl}`
        
        // 更新状态
        userStore.updateAvatar(fullAvatarUrl)
        alert('头像更新成功')
        
        // 强制刷新头像
        const avatarImg = document.querySelector('.avatar')
        if (avatarImg) {
          avatarImg.src = fullAvatarUrl + '?t=' + new Date().getTime()
        }
      } else {
        throw new Error('服务器返回的数据缺少avatar字段')
      }
    } else {
      throw new Error(result.message || '头像上传失败')
    }
  } catch (error) {
    console.error('上传头像失败:', error)
    alert('头像上传失败: ' + (error.message || '未知错误'))
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchUserInfo()
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
</style> 