import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

export const userService = {
  // 更新头像
  updateAvatar: async (imageData) => {
    const formData = new FormData()
    formData.append('avatar', imageData)
    const response = await axios.post(`${API_URL}/user/avatar`, formData)
    return response.data
  },

  // 更新密码
  updatePassword: async (currentPassword, newPassword) => {
    const response = await axios.post(`${API_URL}/user/password`, {
      currentPassword,
      newPassword
    })
    return response.data
  },

  // 发送手机验证码
  sendPhoneCode: async (phone) => {
    const response = await axios.post(`${API_URL}/user/phone/code`, { phone })
    return response.data
  },

  // 绑定手机号
  bindPhone: async (phone, code) => {
    const response = await axios.post(`${API_URL}/user/phone/bind`, {
      phone,
      code
    })
    return response.data
  },

  // 发送邮箱验证码
  sendEmailCode: async (email) => {
    const response = await axios.post(`${API_URL}/user/email/code`, { email })
    return response.data
  },

  // 绑定邮箱
  bindEmail: async (email, code) => {
    const response = await axios.post(`${API_URL}/user/email/bind`, {
      email,
      code
    })
    return response.data
  },

  // 更新用户名
  updateUsername: async (username) => {
    const response = await axios.post(`${API_URL}/user/username`, { username })
    return response.data
  }
} 