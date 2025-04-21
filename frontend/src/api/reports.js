import api from './index'

// 获取报告摘要
export function getReportsSummary() {
  return api.get('/reports/summary')
    .then(response => {
      // 适配Flask后端的响应格式
      if (response.success && response.data) {
        return response.data
      }
      return response
    })
}

// 获取健康趋势
export function getHealthTrends(days = 30) {
  return api.get(`/reports/trends?days=${days}`)
    .then(response => {
      // 适配Flask后端的响应格式
      if (response.success && response.data) {
        return response.data
      }
      return response
    })
}

// // 获取个性化建议 - 已移除，将采用新的动态生成方式
// export function getRecommendations() {
//   return api.get('/reports/recommendations')
//     .then(response => {
//       // 适配Flask后端的响应格式
//       if (response.success && response.data) {
//         return response.data
//       }
//       return response
//     })
// }

export default {
  getReportsSummary,
  getHealthTrends
  // getRecommendations // - 已移除
}