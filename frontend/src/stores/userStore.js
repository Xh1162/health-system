import { reactive, computed } from 'vue'

// 后端基础URL
const getApiBaseUrl = () => {
  return 'http://localhost:5007'
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
      
      // 更新头像URL的端口号
      if (parsedUserData.avatar && parsedUserData.avatar.includes('localhost:5000')) {
        parsedUserData.avatar = parsedUserData.avatar.replace('localhost:5000', 'localhost:5007')
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
  if (url.startsWith('http')) return url
  return `${getApiBaseUrl()}${url}`
}

const useUserStore = () => {
  const updateAvatar = (avatar) => {
    console.log('更新头像URL，原始值:', avatar)
    if (!state.userData) {
      console.error('无法更新头像：用户数据不存在')
      return
    }
    state.userData.avatar = ensureFullUrl(avatar)
    console.log('处理后的头像URL:', state.userData.avatar)
    // 更新localStorage中的用户数据
    updateLocalStorage()
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
      email: state.userData.email,
      avatar: state.userData.avatar
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
    state.userData = data.user
    
    console.log('登录后的用户状态:', { ...state })
    
    // 持久化到localStorage
    const userData = {
      id: data.user.id,
      username: data.user.username,
      email: data.user.email,
      avatar: ensureFullUrl(data.user.avatar)
    }
    
    console.log('保存到localStorage的用户数据:', userData)
    localStorage.setItem('token', data.token)
    localStorage.setItem('userData', JSON.stringify(userData))
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

  return {
    state,
    init,
    updateAvatar,
    updateUsername,
    login,
    logout
  }
}

// 创建全局单例
const userStore = useUserStore()

// 初始化用户状态
init()

export default userStore 