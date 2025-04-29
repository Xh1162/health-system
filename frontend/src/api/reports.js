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

/**
 * 获取指定时间范围和数据类型的趋势数据
 * @param {string} startDate - 开始日期 (YYYY-MM-DD)
 * @param {string} endDate - 结束日期 (YYYY-MM-DD)
 * @param {string[]} dataTypes - 需要的数据类型数组 (e.g., ['weight_kg', 'mood'])
 * @returns {Promise<object>} - 包含各种趋势数据的对象
 */
export const getTrendsData = async (startDate, endDate, dataTypes) => {
  try {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    if (dataTypes && dataTypes.length > 0) {
      params.append('data_types', dataTypes.join(','));
    }

    // 注意：我们新加的趋势接口在 records 蓝图下
    const response = await api.get('/records/trends', { params });
    
    // 检查 Flask 后端返回的格式
    if (response && response.success && response.data) {
       return response.data; // 直接返回 data 部分
    } else {
       // 如果后端没有返回 success: true，或者缺少 data，则抛出错误
       // 或者你可以根据需要返回一个空对象或特定错误结构
       console.error('获取趋势数据 API 响应格式无效:', response);
       throw new Error(response?.message || '获取趋势数据失败，响应格式无效');
    }

  } catch (error) {
    console.error('调用 getTrendsData API 失败:', error);
    // 将错误向上抛出，以便调用方可以处理 (例如在 UI 上显示错误信息)
    throw error;
  }
};