import axios from 'axios'
import userStore from '../stores/userStore'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',  // 使用相对URL，让vite代理处理
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
    // 从userStore获取token
    const token = userStore.state.token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    
    console.log('API请求:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    })
    
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
    console.log('API响应成功:', {
      url: response.config.url,
      status: response.status,
      data: response.data
    })
    return response.data
  },
  error => {
    console.error('API响应错误:', {
      url: error.config?.url,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message
    })
    
    // 处理401未授权错误
    if (error.response && error.response.status === 401) {
      console.log('授权失败，清除token')
      userStore.logout()
      // 可以在这里添加重定向到登录页面的逻辑
    }
    
    return Promise.reject(error)
  }
)

// 提供一个使用fetch的备选方法
export async function fetchApi(endpoint, options = {}) {
  const url = `/api${endpoint}`;
  const token = userStore.state.token;
  
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
  
  console.log('Fetch请求:', {
    url,
    ...fetchOptions
  });
  
  try {
    console.log(`开始发送请求到: ${url}`);
    const response = await fetch(url, fetchOptions);
    console.log(`收到响应，状态码: ${response.status}`);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`HTTP错误 ${response.status}: ${errorText}`);
      throw new Error(`HTTP错误: ${response.status}, ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Fetch响应:', data);
    return data;
  } catch (error) {
    console.error('Fetch错误:', error);
    throw error;
  }
}

export default api 