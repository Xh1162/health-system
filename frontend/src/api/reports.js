import axios from 'axios'
import userStore from '../stores/userStore'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从userStore获取token
    const token = userStore.state.token
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

// 获取报告数据
export function getReportData(period = 'week') {
  return api.get(`/reports/data?period=${period}`)
}

// 获取摘要数据
export function getReportSummary(period = 'week') {
  return api.get(`/reports/summary?period=${period}`)
} 