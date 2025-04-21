import api from './index'
import useUserStore from '../stores/userStore'

const userStore = useUserStore()

// 登录
export function login(username, password) {
  console.log('调用登录API，用户名:', username)
  return api.post('/auth/login', { username, password })
    .then(response => {
      console.log('登录API响应:', response)
      if (response.success && response.data && response.data.user) {
        console.log('登录成功，用户数据:', response.data.user)
        console.log('头像URL:', response.data.user.avatar)
      }
      return response
    })
}

// 注册
export function register(userData) {
  return api.post('/auth/register', userData)
}

// 更新用户信息
export function updateUserInfo(userId, data) {
  return api.put(`/user/${userId}`, data)
}

// 发送手机验证码
export function sendPhoneCode(phone) {
  return api.post('/user/phone/code', { phone })
}

// 绑定手机号
export function bindPhone(phone, code) {
  return api.post('/user/phone/bind', { phone, code })
}

// 发送邮箱验证码 (不再需要)
export function sendEmailCode(email) {
  console.warn('该功能已弃用：系统不再依赖邮箱')
  return Promise.reject(new Error('该功能已弃用：系统不再依赖邮箱'))
}

// 绑定邮箱 (不再需要)
export function bindEmail(email, code) {
  console.warn('该功能已弃用：系统不再依赖邮箱')
  return Promise.reject(new Error('该功能已弃用：系统不再依赖邮箱'))
}

// 获取用户信息
export function getUserInfo() {
  return api.get('/user/info')
}

// 修改密码 (修正以匹配后端)
export function changePassword(passwordData) {
  // passwordData should be an object like { current_password: '...', new_password: '...' }
  return api.put('/auth/password/change', passwordData)
}

// 重置密码 (修改为使用用户名)
export function resetPassword(username, code, newPassword) {
  return api.post('/auth/reset-password', { username, code, newPassword })
}

export default {
  login,
  register,
  updateUserInfo,
  sendPhoneCode,
  bindPhone,
  sendEmailCode,
  bindEmail,
  getUserInfo,
  changePassword,
  resetPassword
} 