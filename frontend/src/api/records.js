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

// 创建食物记录
export function createFoodRecord(data) {
  return api.post('/records', { type: 'food', ...data })
}

// 创建运动记录
export function createExerciseRecord(data) {
  return api.post('/records', { type: 'exercise', ...data })
}

// 创建心情记录
export function createMoodRecord(data) {
  return api.post('/records', { type: 'mood', ...data })
}

// 创建健康状况记录
export function createHealthRecord(data) {
  return api.post('/records', { type: 'health', ...data })
}

// 获取所有记录
export function getAllRecords(days = 7) {
  return api.get(`/records/all?days=${days}`)
}

// 获取记录统计信息
export function getRecordsStats(days = 30) {
  return api.get(`/records/stats?days=${days}`)
}

// 更新食物记录
export function updateFoodRecord(id, data) {
  return api.put(`/records/${id}`, { type: 'food', ...data })
}

// 更新运动记录
export function updateExerciseRecord(id, data) {
  return api.put(`/records/${id}`, { type: 'exercise', ...data })
}

// 更新心情记录
export function updateMoodRecord(id, data) {
  return api.put(`/records/${id}`, { type: 'mood', ...data })
}

// 更新健康状况记录
export function updateHealthRecord(id, data) {
  return api.put(`/records/${id}`, { type: 'health', ...data })
}

// 删除记录
export function deleteRecord(id) {
  // 确保id是字符串类型
  const recordId = String(id);
  return api.delete(`/records/${recordId}`);
} 