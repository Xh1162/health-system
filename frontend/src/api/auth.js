import request from './request'
import userStore from '../stores/userStore'

// 登录
export function login(username, password) {
  console.log('调用登录API，用户名:', username)
  return request.post('/auth/login', { username, password })
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
  return request.post('/auth/register', userData)
}

// 更新用户信息
export function updateUserInfo(userId, data) {
  return request.put(`/user/${userId}`, data)
}

// 更新头像
export function updateAvatar(userId, avatarData) {
  const formData = new FormData()
  formData.append('avatar', avatarData)
  return request.post(`/auth/avatar/${userId}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 发送手机验证码
export function sendPhoneCode(phone) {
  return request.post('/user/phone/code', { phone })
}

// 绑定手机号
export function bindPhone(phone, code) {
  return request.post('/user/phone/bind', { phone, code })
}

// 发送邮箱验证码
export function sendEmailCode(email) {
  return request.post('/user/email/code', { email })
}

// 绑定邮箱
export function bindEmail(email, code) {
  return request.post('/user/email/bind', { email, code })
}

// 获取用户信息
export function getUserInfo() {
  return request.get('/user/info')
}

// 修改密码
export function changePassword(oldPassword, newPassword) {
  return request.post('/user/password', { oldPassword, newPassword })
}

// 重置密码
export function resetPassword(email, code, newPassword) {
  return request.post('/auth/reset-password', { email, code, newPassword })
} 