<template>
  <div class="settings-page">
    <nav class="settings-nav">
      <router-link to="/dashboard" class="nav-back">
        <span class="back-icon">←</span>
        <span>返回仪表盘</span>
      </router-link>
      <h1>设置</h1>
    </nav>

    <div class="settings-container">
      <!-- 个人信息卡片 -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="profile-avatar">
            <img :src="userAvatar || 'https://via.placeholder.com/100'" :alt="username" />
            <div class="avatar-overlay">
              <label class="change-avatar">
                <span>更换头像</span>
                <input 
                  type="file" 
                  accept="image/*" 
                  @change="handleAvatarUpload" 
                  hidden 
                />
              </label>
            </div>
          </div>
          <div class="profile-info">
            <h2>{{ username }}</h2>
            <p class="profile-email">{{ email || '未绑定邮箱' }}</p>
          </div>
        </div>
      </div>

      <!-- 设置项列表 -->
      <div class="settings-sections">
        <!-- 账户安全 -->
        <section class="settings-section">
          <h3>
            <span class="section-icon">🔒</span>
            账户安全
          </h3>
          
          <div class="settings-items">
            <div class="settings-item" @click="toggleSection('password')">
              <div class="item-main">
                <div class="item-title">密码</div>
                <div class="item-subtitle">上次修改: {{ lastPasswordUpdate || '从未修改' }}</div>
              </div>
              <button class="item-action">修改</button>
            </div>

            <div v-if="activeSection === 'password'" class="item-detail">
              <form class="settings-form" @submit.prevent="updatePassword">
                <div class="form-group">
                  <input 
                    type="password" 
                    v-model="currentPassword" 
                    placeholder="当前密码"
                    required
                  />
                </div>
                <div class="form-group">
                  <input 
                    type="password" 
                    v-model="newPassword" 
                    placeholder="新密码"
                    required
                  />
                </div>
                <div class="form-group">
                  <input 
                    type="password" 
                    v-model="confirmPassword" 
                    placeholder="确认新密码"
                    required
                  />
                </div>
                <div class="form-actions">
                  <button type="button" class="btn-secondary" @click="closeSection">取消</button>
                  <button type="submit" class="btn-primary">保存更改</button>
                </div>
              </form>
            </div>
          </div>
        </section>

        <!-- 账户绑定 -->
        <section class="settings-section">
          <h3>
            <span class="section-icon">🔗</span>
            账户绑定
          </h3>
          
          <div class="settings-items">
            <div class="settings-item" @click="toggleSection('phone')">
              <div class="item-main">
                <div class="item-title">手机号码</div>
                <div class="item-subtitle">{{ phone || '未绑定手机号' }}</div>
              </div>
              <button class="item-action">{{ phone ? '更换' : '绑定' }}</button>
            </div>

            <div v-if="activeSection === 'phone'" class="item-detail">
              <form class="settings-form" @submit.prevent="updatePhone">
                <div class="form-group">
                  <input 
                    type="tel" 
                    v-model="newPhone" 
                    placeholder="请输入手机号"
                    required
                  />
                </div>
                <div class="form-group verify-group">
                  <input 
                    type="text" 
                    v-model="phoneCode" 
                    placeholder="验证码"
                    required
                  />
                  <button 
                    type="button" 
                    class="verify-btn" 
                    @click="handleSendPhoneCode"
                    :disabled="countdown > 0"
                  >
                    {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
                  </button>
                </div>
                <div class="form-actions">
                  <button type="button" class="btn-secondary" @click="closeSection">取消</button>
                  <button type="submit" class="btn-primary">确认绑定</button>
                </div>
              </form>
            </div>

            <div class="settings-item" @click="toggleSection('email')">
              <div class="item-main">
                <div class="item-title">邮箱地址</div>
                <div class="item-subtitle">{{ email || '未绑定邮箱' }}</div>
              </div>
              <button class="item-action">{{ email ? '更换' : '绑定' }}</button>
            </div>

            <div v-if="activeSection === 'email'" class="item-detail">
              <form class="settings-form" @submit.prevent="updateEmail">
                <div class="form-group">
                  <input 
                    type="email" 
                    v-model="newEmail" 
                    placeholder="请输入邮箱"
                    required
                  />
                </div>
                <div class="form-group verify-group">
                  <input 
                    type="text" 
                    v-model="emailCode" 
                    placeholder="验证码"
                    required
                  />
                  <button 
                    type="button" 
                    class="verify-btn"
                    @click="handleSendEmailCode"
                  >
                    获取验证码
                  </button>
                </div>
                <div class="form-actions">
                  <button type="button" class="btn-secondary" @click="closeSection">取消</button>
                  <button type="submit" class="btn-primary">确认绑定</button>
                </div>
              </form>
            </div>
          </div>
        </section>

        <!-- 个人资料 -->
        <section class="settings-section">
          <h3>
            <span class="section-icon">👤</span>
            个人资料
          </h3>
          
          <div class="settings-items">
            <div class="settings-item" @click="toggleSection('username')">
              <div class="item-main">
                <div class="item-title">用户名</div>
                <div class="item-subtitle">{{ username }}</div>
              </div>
              <button class="item-action">修改</button>
            </div>

            <div v-if="activeSection === 'username'" class="item-detail">
              <form class="settings-form" @submit.prevent="saveProfile">
                <div class="form-group">
                  <input 
                    type="text" 
                    v-model="newUsername" 
                    placeholder="请输入新用户名"
                    required
                  />
                </div>
                <div class="form-actions">
                  <button type="button" class="btn-secondary" @click="closeSection">取消</button>
                  <button type="submit" class="btn-primary">保存更改</button>
                </div>
              </form>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { sendPhoneCode, bindPhone, sendEmailCode, bindEmail, changePassword } from '../api/auth'
import { updateUsername } from '../api/user'

const router = useRouter()
const userStore = inject('userStore')
const username = ref(userStore.state.username || '')

// 添加更多关于头像的调试信息
console.log('账户设置页面加载，当前用户状态:', {
  username: userStore.state.username,
  avatar: userStore.state.userData?.avatar,
  userId: userStore.state.userData?.id
})

// 使用计算属性获取头像URL
const userAvatar = computed(() => {
  const avatar = userStore.state.userData?.avatar
  console.log('头像计算属性获取到的值:', avatar)
  return avatar || ''
})

// 用户数据
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const phone = ref('')
const phoneCode = ref('')
const email = ref('')
const emailCode = ref('')

// 新增状态管理
const activeSection = ref('')
const lastPasswordUpdate = ref('2024-01-01')
const newPhone = ref('')
const newEmail = ref('')
const newUsername = ref('')

const countdown = ref(0)

// 切换区域显示
const toggleSection = (section) => {
  activeSection.value = activeSection.value === section ? '' : section
}

// 保存个人资料
const saveProfile = async () => {
  try {
    await updateUsername(newUsername.value)
    userStore.updateUsername(newUsername.value)
    username.value = newUsername.value
    alert('用户名修改成功')
    activeSection.value = ''
    newUsername.value = ''
  } catch (error) {
    alert(error.response?.data?.message || '用户名修改失败')
  }
}

// 处理头像上传
const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) {
    return
  }

  console.log('选择的文件:', {
    name: file.name,
    type: file.type,
    size: file.size
  })

  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过 2MB')
    return
  }

  if (!userStore.state.userData?.id) {
    alert('请先登录')
    router.push('/login')
    return
  }

  console.log('当前用户ID:', userStore.state.userData?.id)
  console.log('当前Token:', userStore.state.token)

  try {
    // 显示上传中提示
    alert('头像上传中，请稍候...')
    
    // 使用原生fetch API上传
    const formData = new FormData()
    formData.append('avatar', file)
    
    // 确保token存在
    const token = userStore.state.token
    if (!token) {
      throw new Error('未找到认证令牌，请重新登录')
    }
    
    console.log('上传请求URL:', `/api/auth/avatar/${userStore.state.userData?.id}`)
    console.log('上传请求头:', {
      'Authorization': `Bearer ${token}`
    })
    
    // 构建完整的API URL
    const baseUrl = 'http://localhost:5007'; // 确保这个URL与你的后端匹配
    const apiUrl = `${baseUrl}/api/auth/avatar/${userStore.state.userData?.id}`;
    
    console.log('完整的API URL:', apiUrl);
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    console.log('上传响应状态:', response.status)
    
    const responseData = await response.json()
    console.log('上传响应数据:', responseData)
    console.log('上传响应数据类型:', typeof responseData)
    console.log('上传响应数据JSON格式:', JSON.stringify(responseData, null, 2))
    
    if (!response.ok) {
      throw new Error(responseData.message || `上传失败: ${response.status}`)
    }
    
    if (responseData.success) {
      // 检查avatar_url字段是否存在
      if (!responseData.data || !responseData.data.avatar_url) {
        console.error('响应数据中缺少avatar_url字段:', responseData)
        throw new Error('服务器返回的数据格式不正确')
      }
      
      const avatarUrl = responseData.data.avatar_url
      console.log('获取到的新头像URL:', avatarUrl)
      
      // 检查头像URL格式
      if (!avatarUrl.startsWith('http')) {
        console.log('头像URL不是绝对路径，将添加基础URL')
        const baseUrl = 'http://localhost:5007'
        const fullAvatarUrl = avatarUrl.startsWith('/') 
          ? `${baseUrl}${avatarUrl}` 
          : `${baseUrl}/${avatarUrl}`
        console.log('处理后的完整头像URL:', fullAvatarUrl)
        
        // 更新用户存储中的头像
        userStore.updateAvatar(fullAvatarUrl)
        
        // 更新本地组件状态
        userAvatar.value = fullAvatarUrl
      } else {
        console.log('头像URL已经是绝对路径:', avatarUrl)
        
        // 更新用户存储中的头像
        userStore.updateAvatar(avatarUrl)
        
        // 更新本地组件状态
        userAvatar.value = avatarUrl
      }
      
      alert('头像更新成功！')
    } else {
      throw new Error(responseData.message || '头像上传失败')
    }
  } catch (error) {
    console.error('头像上传错误:', error)
    alert('头像上传失败: ' + error.message)
  }
}

// 密码更新
const updatePassword = async () => {
  try {
    if (newPassword.value !== confirmPassword.value) {
      alert('两次输入的密码不一致')
      return
    }
    await changePassword(currentPassword.value, newPassword.value)
    alert('密码修改成功')
    activeSection.value = ''
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (error) {
    alert(error.response?.data?.message || '密码修改失败')
  }
}

// 发送手机验证码
const handleSendPhoneCode = async () => {
  try {
    if (!newPhone.value) {
      alert('请输入手机号')
      return
    }
    
    // 验证手机号格式
    const phonePattern = /^1[3-9]\d{9}$/
    if (!phonePattern.test(newPhone.value)) {
      alert('请输入有效的手机号')
      return
    }

    await sendPhoneCode(newPhone.value)
    alert('验证码已发送')
    
    // 开始倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error) {
    alert(error.response?.data?.message || '验证码发送失败')
  }
}

// 绑定手机号
const updatePhone = async () => {
  try {
    await bindPhone(newPhone.value, phoneCode.value)
    alert('手机号绑定成功')
    phone.value = newPhone.value
    activeSection.value = ''
    newPhone.value = ''
    phoneCode.value = ''
  } catch (error) {
    alert(error.response?.data?.message || '手机号绑定失败')
  }
}

// 邮箱验证码
const handleSendEmailCode = async () => {
  try {
    if (!newEmail.value) {
      alert('请输入邮箱')
      return
    }
    await sendEmailCode(newEmail.value)
    alert('验证码已发送')
  } catch (error) {
    alert(error.response?.data?.message || '验证码发送失败')
  }
}

// 绑定邮箱
const updateEmail = async () => {
  try {
    await bindEmail(newEmail.value, emailCode.value)
    alert('邮箱绑定成功')
    email.value = newEmail.value
    activeSection.value = ''
    newEmail.value = ''
    emailCode.value = ''
  } catch (error) {
    alert(error.response?.data?.message || '邮箱绑定失败')
  }
}

// 关闭表单
const closeSection = () => {
  activeSection.value = ''
}
</script>

<style scoped>
.settings-page {
  min-height: 100vh;
  background-color: #f3f4f6;
}

.settings-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: #fff;
  display: flex;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.nav-back {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1f2937;
  font-weight: 500;
  margin-right: 24px;
  text-decoration: none;
}

.back-icon {
  font-size: 20px;
}

.settings-nav h1 {
  font-size: 20px;
  font-weight: 500;
  color: #111827;
  margin: 0;
}

.settings-container {
  max-width: 800px;
  margin: 88px auto 24px;
  padding: 0 24px;
}

.profile-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-avatar {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  overflow: hidden;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.profile-avatar:hover .avatar-overlay {
  opacity: 1;
}

.change-avatar {
  color: #fff;
  font-size: 14px;
  cursor: pointer;
}

.profile-info h2 {
  font-size: 24px;
  font-weight: 500;
  color: #111827;
  margin: 0 0 4px;
}

.profile-email {
  color: #6b7280;
  font-size: 14px;
}

.settings-section {
  background: #fff;
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.settings-section h3 {
  padding: 16px 24px;
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #e5e7eb;
}

.section-icon {
  font-size: 20px;
}

.settings-items {
  padding: 8px 0;
}

.settings-item {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.settings-item:hover {
  background-color: #f9fafb;
}

.item-main {
  flex: 1;
}

.item-title {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.item-subtitle {
  font-size: 13px;
  color: #6b7280;
  margin-top: 2px;
}

.item-action {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #3b82f6;
  background: transparent;
  border: 1px solid #e5e7eb;
  transition: all 0.2s;
}

.item-action:hover {
  background: #f0f9ff;
  border-color: #3b82f6;
}

.item-detail {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  background: #f9fafb;
}

.settings-form {
  max-width: 400px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  outline: none;
}

.verify-group {
  display: flex;
  gap: 12px;
}

.verify-group input {
  flex: 1;
}

.verify-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #3b82f6;
  background: transparent;
  border: 1px solid #e5e7eb;
  white-space: nowrap;
  transition: all 0.2s;
}

.verify-btn:hover:not(:disabled) {
  background: #f0f9ff;
  border-color: #3b82f6;
}

.verify-btn:disabled {
  color: #9ca3af;
  border-color: #e5e7eb;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.btn-primary {
  background: #3b82f6;
  color: #fff;
  border: none;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: transparent;
  color: #6b7280;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover {
  background: #f3f4f6;
}

@media (max-width: 640px) {
  .settings-container {
    padding: 0 16px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
  }

  .settings-item {
    padding: 12px 16px;
  }

  .item-detail {
    padding: 16px;
  }
}
</style> 