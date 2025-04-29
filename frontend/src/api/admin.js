import api from './index'; // 导入配置好的 axios 实例

/**
 * 获取所有用户列表 (管理员权限)
 * @returns {Promise<Array<Object>>} 用户列表
 */
export const getAllUsers = async () => {
  try {
    const response = await api.get('/admin/users');
    return response; // axios 响应拦截器已经处理了 response.data
  } catch (error) {
    console.error('获取用户列表失败 (API):', error.response || error.message);
    throw error; // 将错误向上抛出，由调用方处理
  }
};

/**
 * 获取指定用户的健康报告 (管理员权限)
 * @param {string|number} userId 用户ID
 * @returns {Promise<Object>} 用户报告数据
 */
export const getUserReportById = async (userId) => {
  if (!userId) {
    throw new Error('获取用户报告需要提供用户ID');
  }
  try {
    const response = await api.get(`/admin/users/${userId}/report`);
    return response; // 响应拦截器处理了 response.data
  } catch (error) {
    console.error(`获取用户 ${userId} 报告失败 (API):`, error.response || error.message);
    throw error;
  }
};

/**
 * 提交管理员对用户报告的建议 (管理员权限)
 * @param {string|number} userId 用户ID
 * @param {string} recommendation 建议内容
 * @returns {Promise<Object>} 后端返回的确认信息
 */
export const submitAdminRecommendation = async (userId, recommendation) => {
  if (!userId) {
    throw new Error('提交建议需要提供用户ID');
  }
  if (recommendation === undefined || recommendation === null) {
     throw new Error('提交建议需要提供建议内容');
  }
  try {
    const response = await api.post(`/admin/users/${userId}/recommendation`, { recommendation });
    return response; // 响应拦截器处理了 response.data
  } catch (error) {
    console.error(`为用户 ${userId} 提交建议失败 (API):`, error.response || error.message);
    throw error;
  }
};

// 注意：这里还缺少 UserReportsPage.vue 中引用的 getAllUsers 函数，我们也一并加上
// (假设后端 API 路径为 /api/admin/users)
// 已在上面补充 getAllUsers 函数 

// --- 新增：管理员获取和回复建议请求的 API 函数 ---

/**
 * 管理员获取建议请求列表
 * @param {string} status - 筛选状态 (e.g., 'pending', 'answered', 'all')
 * @param {number} page - 页码
 * @param {number} perPage - 每页数量
 * @returns {Promise<object>} 包含请求列表和分页信息的对象
 */
export const getAdminAdviceRequests = async (status = 'pending', page = 1, perPage = 10) => {
  try {
    const params = new URLSearchParams({
      status: status,
      page: page.toString(),
      per_page: perPage.toString()
    });
    const response = await api.get('/admin/advice-requests', { params });
    if (response && response.success) {
      return response; // 返回包含 data 和 pagination 的完整响应
    } else {
      throw new Error(response?.message || '获取建议请求列表失败');
    }
  } catch (error) {
    console.error('调用 getAdminAdviceRequests API 失败:', error);
    throw error;
  }
};

/**
 * 管理员回复建议请求
 * @param {number|string} requestId - 请求 ID
 * @param {string} responseText - 回复内容
 * @returns {Promise<object>} 更新后的请求数据
 */
export const respondToAdviceRequest = async (requestId, responseText) => {
  if (!requestId || !responseText) {
      throw new Error('必须提供请求 ID 和回复内容');
  }
  try {
    const payload = { response_text: responseText };
    const response = await api.post(`/admin/advice-requests/${requestId}/respond`, payload);
    if (response && response.success && response.data) {
      return response.data; // 返回更新后的请求对象
    } else {
      throw new Error(response?.message || '回复建议请求失败');
    }
  } catch (error) {
    console.error(`调用 respondToAdviceRequest API (ID: ${requestId}) 失败:`, error);
     const errorMessage = error.response?.data?.message || error.message || '回复建议请求时发生网络或服务器错误';
    throw new Error(errorMessage);
  }
}; 