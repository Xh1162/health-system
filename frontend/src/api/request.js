import axios from 'axios'

// 创建axios实例
const request = axios.create({
  baseURL: 'http://localhost:5000',  // 修改为不包含/api的路径
  timeout: 10000,  // 增加超时时间到10秒
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      console.log('添加Authorization头:', `Bearer ${token}`)
      config.headers['Authorization'] = `Bearer ${token}`
    } else {
      console.log('未找到token，请求将不包含Authorization头')
    }
    
    // 如果URL已经包含/api，则不再添加
    if (!config.url.startsWith('/api') && !config.url.startsWith('http')) {
      config.url = `/api${config.url}`
      console.log('修正后的URL:', config.url)
    }
    
    // 打印完整请求信息
    console.log('发送请求配置:', {
      url: config.url,
      method: config.method,
      headers: JSON.stringify(config.headers),
      data: config.data
    })
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    console.log('收到响应:', response.data)
    // 直接返回响应数据部分
    return response.data
  },
  error => {
    if (error.response) {
      console.error('响应错误状态:', error.response.status)
      console.error('响应错误数据:', error.response.data)
      
      switch (error.response.status) {
        case 401:
          // token过期或无效，清除用户信息并跳转到登录页
          console.error('认证失败，清除token并跳转到登录页')
          localStorage.removeItem('token')
          localStorage.removeItem('userData')
          window.location.href = '/login'
          break
        case 403:
          console.error('没有权限访问该资源')
          break
        case 404:
          console.error('请求的资源不存在')
          break
        case 422:
          console.error('请求数据验证失败:', error.response.data)
          break
        case 500:
          console.error('服务器错误')
          break
        default:
          console.error('发生错误:', error.response.data)
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      console.error('未收到响应:', error.request)
      alert('服务器无响应，请检查网络连接')
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message)
    }
    return Promise.reject(error)
  }
)

export default request 