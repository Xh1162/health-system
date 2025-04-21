import { reactive, computed } from 'vue'

// 简单的事件系统
const eventListeners = {
  avatarUpdate: []
}

// 事件相关函数
const emitEvent = (event, data) => {
  if (eventListeners[event]) {
    eventListeners[event].forEach(listener => listener(data))
  }
}

const onEvent = (event, callback) => {
  if (!eventListeners[event]) {
    eventListeners[event] = []
  }
  eventListeners[event].push(callback)
  
  // 返回取消监听的函数
  return () => {
    const index = eventListeners[event].indexOf(callback)
    if (index !== -1) {
      eventListeners[event].splice(index, 1)
    }
  }
}

// 后端基础URL
const getApiBaseUrl = () => {
  return 'http://localhost:5008'
}

const state = reactive({
  token: localStorage.getItem('token') || null,
  userData: null,
  isAuthenticated: false,
  // 添加计算属性的getter
  get avatar() {
    return this.userData?.avatar || ''
  },
  get username() {
    return this.userData?.username || ''
  }
})

// 初始化函数
const init = () => {
  // 从localStorage初始化用户状态
  const token = localStorage.getItem('token')
  const userData = localStorage.getItem('userData')
  
  console.log('初始化用户状态，从localStorage获取数据:', { token: !!token, userData })
  
  if (token && userData) {
    try {
      const parsedUserData = JSON.parse(userData)
      console.log('解析的用户数据:', parsedUserData)
      
      // Remove email from parsed data if it exists for backward compatibility
      if ('email' in parsedUserData) {
        delete parsedUserData.email;
        console.log('已移除旧的email字段');
      }
      
      // 更新头像URL的端口号
      if (parsedUserData.avatar && parsedUserData.avatar.includes('localhost:5000')) {
        parsedUserData.avatar = parsedUserData.avatar.replace('localhost:5000', 'localhost:5008')
      }
      
      state.isAuthenticated = true
      state.token = token
      state.userData = parsedUserData
      
      console.log('初始化后的用户状态:', { ...state })
    } catch (err) {
      console.error('解析用户数据失败:', err)
      logout() // 如果数据损坏，执行登出操作
    }
  }
}

// 确保URL是完整的URL
const ensureFullUrl = (url) => {
  if (!url) return ''
  
  // 如果已经是完整URL，直接返回
  if (url.startsWith('http')) return url
  
  // 处理开头有斜杠和没有斜杠的情况
  const baseUrl = getApiBaseUrl()
  return url.startsWith('/') ? `${baseUrl}${url}` : `${baseUrl}/${url}`
}

const useUserStore = () => {
  const updateAvatar = (avatar) => {
    console.log('更新头像URL，原始值:', avatar)
    if (!state.userData) {
      console.error('无法更新头像：用户数据不存在')
      return
    }
    
    try {
      // 处理可能的undefined或null值
      if (!avatar) {
        console.warn('收到空的头像URL，使用默认值')
        avatar = '/default-avatar.png'
      }
      
      // 确保头像URL是完整的
      state.userData.avatar = ensureFullUrl(avatar)
      console.log('处理后的头像URL:', state.userData.avatar)
      
      // 更新localStorage中的用户数据
      updateLocalStorage()
      
      // 触发头像更新事件
      emitEvent('avatarUpdate', state.userData.avatar)
    } catch (error) {
      console.error('更新头像时出错:', error)
    }
  }

  const updateUsername = (username) => {
    if (!state.userData) {
      console.error('无法更新用户名：用户数据不存在')
      return
    }
    state.userData.username = username
    // 更新localStorage中的用户数据
    updateLocalStorage()
  }

  const updateLocalStorage = () => {
    if (!state.userData) {
      console.error('无法更新localStorage：用户数据不存在')
      return
    }
    const userData = {
      id: state.userData.id,
      username: state.userData.username,
      avatar: state.userData.avatar,
      role: state.userData.role
    }
    console.log('更新localStorage中的用户数据:', userData)
    localStorage.setItem('userData', JSON.stringify(userData))
  }

  const login = (data) => {
    if (!data || !data.token || !data.user || !data.user.id) {
      console.error('登录数据无效:', data)
      throw new Error('无效的登录数据')
    }

    console.log('登录数据:', data)

    state.isAuthenticated = true
    state.token = data.token
    // Ensure email is not set on state.userData from login response
    const { email, ...userWithoutEmail } = data.user;
    state.userData = userWithoutEmail
    
    console.log('登录后的用户状态:', { ...state })
    
    // 持久化到localStorage (already handled by updateLocalStorage if called, 
    // but we do it explicitly here after login)
    const userDataToStore = {
      id: state.userData.id,
      username: state.userData.username,
      avatar: ensureFullUrl(state.userData.avatar), // Use state.userData.avatar
      role: state.userData.role
    }
    
    console.log('保存到localStorage的用户数据:', userDataToStore)
    localStorage.setItem('token', data.token)
    localStorage.setItem('userData', JSON.stringify(userDataToStore))
  }

  const logout = () => {
    console.log('执行登出操作')
    state.isAuthenticated = false
    state.token = null
    state.userData = null
    
    // 清除localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('userData')
  }

  // 执行初始化
  init()

  return {
    state,
    updateUsername,
    updateAvatar,
    login,
    logout,
    // 添加事件相关函数
    onAvatarUpdate: (callback) => onEvent('avatarUpdate', callback)
  }
}

export default useUserStore 