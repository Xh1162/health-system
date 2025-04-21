import axios from 'axios'
import useUserStore from '../stores/userStore'

// 创建userStore实例
const userStore = useUserStore()

// 判断是否为开发环境
const isDev = import.meta.env.DEV

// 获取token的函数
const getToken = () => {
  return localStorage.getItem('token') || userStore?.state?.token || null
}

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5008/api',  // 使用完整URL，修改端口为5008
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false,
  maxRedirects: 0
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 获取token
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    // 只在开发环境中记录详细日志
    if (isDev) {
      console.log('API请求:', {
        url: config.url,
        method: config.method,
        headers: { ...config.headers, Authorization: token ? '已设置' : '未设置' },
        data: config.data
      })
    }
    
    return config
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 只在开发环境中记录详细日志
    if (isDev) {
      console.log('API响应成功:', {
        url: response.config.url,
        status: response.status,
        data: response.data
      })
    }
    return response.data
  },
  error => {
    // 错误日志在所有环境中都记录，但可以简化
    console.error('API响应错误:', error.message)
    
    // 处理401未授权错误
    if (error.response && error.response.status === 401) {
      console.log('授权失败，清除token')
      // 直接清除localStorage中的token
      localStorage.removeItem('token')
      localStorage.removeItem('userData')
      
      // 如果userStore可用，也调用logout方法
      if (userStore && userStore.logout) {
        try {
          userStore.logout()
        } catch (e) {
          console.error('清除userStore失败:', e)
        }
      }
    }
    
    return Promise.reject(error)
  }
)

// 提供一个使用fetch的备选方法
export async function fetchApi(endpoint, options = {}) {
  const url = `http://localhost:5008/api${endpoint}`; // 使用完整URL，修改端口为5008
  const token = getToken();
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    },
    redirect: 'follow',
    mode: 'cors'
  };
  
  const fetchOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  };
  
  // 只在开发环境中记录详细日志
  if (isDev) {
    console.log('Fetch请求:', { 
      url, 
      ...fetchOptions, 
      headers: { ...fetchOptions.headers, Authorization: token ? '已设置' : '未设置' } 
    });
  }
  
  try {
    const response = await fetch(url, fetchOptions);
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP错误: ${response.status}, ${errorText}`);
    }
    
    const data = await response.json();
    
    // 只在开发环境中记录详细日志
    if (isDev) {
      console.log('Fetch响应:', data);
    }
    
    return data;
  } catch (error) {
    console.error('Fetch错误:', error.message);
    throw error;
  }
}

export default api 