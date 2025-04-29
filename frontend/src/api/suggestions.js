import api from './index'

// 获取用户的手动建议
export function getManualSuggestions(userId) {
  return api.get(`/suggestions/manual/${userId}`)
    .then(response => {
      if (response.success && response.data) {
        return response.data
      }
      return []
    })
}

// 添加手动建议
export function addManualSuggestion(userId, content) {
  return api.post(`/suggestions/manual/${userId}`, { content })
    .then(response => {
      if (response.success && response.data) {
        return response.data
      }
      throw new Error(response.message || '添加建议失败')
    })
}

// 删除手动建议
export function deleteManualSuggestion(suggestionId) {
  return api.delete(`/suggestions/manual/${suggestionId}`)
    .then(response => {
      if (response.success) {
        return true
      }
      throw new Error(response.message || '删除建议失败')
    })
}

export default {
  getManualSuggestions,
  addManualSuggestion,
  deleteManualSuggestion
} 