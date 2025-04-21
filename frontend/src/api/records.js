import api, { fetchApi } from './index'

// 创建食物记录
export function createFoodRecord(data) {
  console.log('创建食物记录，数据:', data)
  
  // 直接使用axios
  return api.post('/records', { type: 'food', ...data })
    .then(response => {
      console.log('创建食物记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('创建食物记录失败:', error)
      throw error
    })
}

// 创建运动记录
export function createExerciseRecord(data) {
  console.log('创建运动记录，数据:', data)
  
  // 直接使用axios
  return api.post('/records', { type: 'exercise', ...data })
    .then(response => {
      console.log('创建运动记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('创建运动记录失败:', error)
      throw error
    })
}

// 创建心情记录
export function createMoodRecord(data) {
  console.log('创建心情记录，数据:', data)
  
  // 直接使用axios
  return api.post('/records', { type: 'mood', ...data })
    .then(response => {
      console.log('创建心情记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('创建心情记录失败:', error)
      throw error
    })
}

// 创建健康状况记录
export function createHealthRecord(data) {
  console.log('创建健康状况记录，数据:', data)
  
  // 直接使用axios
  return api.post('/records', { type: 'health', ...data })
    .then(response => {
      console.log('创建健康状况记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('创建健康状况记录失败:', error)
      throw error
    })
}

// 获取所有记录
export function getAllRecords(days = 7) {
  console.log('获取所有记录，天数:', days)
  
  // 尝试使用fetch
  return fetchApi(`/records/all?days=${days}`, {
    method: 'GET'
  }).catch(error => {
    console.error('使用fetch获取记录失败，尝试使用axios:', error)
    // 如果fetch失败，回退到axios
    return api.get(`/records/all?days=${days}`)
  }).then(response => {
    console.log('获取所有记录成功:', response)
    return response
  }).catch(error => {
    console.error('获取所有记录失败:', error)
    throw error
  })
}

// 获取记录统计信息
export function getRecordsStats(days = 30) {
  console.log('获取记录统计，天数:', days)
  return api.get(`/records/stats?days=${days}`)
    .then(response => {
      console.log('获取记录统计成功:', response)
      return response
    })
    .catch(error => {
      console.error('获取记录统计失败:', error)
      throw error
    })
}

// 更新食物记录
export function updateFoodRecord(id, data) {
  console.log('更新食物记录，ID:', id, '数据:', data)
  return api.put(`/records/${id}`, { type: 'food', ...data })
    .then(response => {
      console.log('更新食物记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('更新食物记录失败:', error)
      throw error
    })
}

// 更新运动记录
export function updateExerciseRecord(id, data) {
  console.log('更新运动记录，ID:', id, '数据:', data)
  return api.put(`/records/${id}`, { type: 'exercise', ...data })
    .then(response => {
      console.log('更新运动记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('更新运动记录失败:', error)
      throw error
    })
}

// 更新心情记录
export function updateMoodRecord(id, data) {
  console.log('更新心情记录，ID:', id, '数据:', data)
  return api.put(`/records/${id}`, { type: 'mood', ...data })
    .then(response => {
      console.log('更新心情记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('更新心情记录失败:', error)
      throw error
    })
}

// 更新健康状况记录
export function updateHealthRecord(id, data) {
  console.log('更新健康状况记录，ID:', id, '数据:', data)
  return api.put(`/records/${id}`, { type: 'health', ...data })
    .then(response => {
      console.log('更新健康状况记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('更新健康状况记录失败:', error)
      throw error
    })
}

// 删除记录
export function deleteRecord(id) {
  console.log('删除记录，ID:', id)
  // 确保id是字符串类型
  const recordId = String(id);
  return api.delete(`/records/${recordId}`)
    .then(response => {
      console.log('删除记录成功:', response)
      return response
    })
    .catch(error => {
      console.error('删除记录失败:', error)
      throw error
    })
}