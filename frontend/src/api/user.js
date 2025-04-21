import api from './index'

// 获取用户信息
export function getUserInfo() {
  return api.get('/user/info')
}

// 获取用户个人资料
export function getUserProfile() {
  return api.get('/user/profile')
}

// 更新用户个人资料
export function updateUserProfile(data) {
  return api.put('/user/profile', data)
}

// 更新用户用户名
export function updateUsername(username) {
  console.log('调用updateUsername, 新用户名:', username);
  // 调用更新个人资料的接口，只传递username字段
  return api.put('/user/profile', { username })
    .then(response => {
      console.log('更新用户名响应:', response);
      // 可能需要从响应中提取更新后的用户数据
      return response;
    })
    .catch(error => {
      console.error('更新用户名失败:', error);
      throw error;
    });
}

// 上传用户头像
export function uploadAvatar(file) {
  const formData = new FormData()
  formData.append('avatar', file)
  
  return api.post('/user/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 获取用户仪表板数据
export function getUserDashboard() {
  return api.get('/user/dashboard')
}

// 获取公告
export function getAnnouncements() {
  return api.get('/user/announcements')
}

export default {
  getUserInfo,
  getUserProfile,
  updateUserProfile,
  updateUsername,
  uploadAvatar,
  getUserDashboard,
  getAnnouncements
} 