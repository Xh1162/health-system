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

/**
 * 触发后端为指定用户生成健康报告 (管理员权限)
 * @param {string|number} userId 用户ID
 * @returns {Promise<Object>} 后端返回的确认信息，可能包含新报告ID
 */
export const generateUserReport = async (userId) => {
  if (!userId) {
    throw new Error('生成报告需要提供用户ID');
  }
  try {
    // 调用 POST 请求来触发报告生成
    const response = await api.post(`/admin/users/${userId}/generate-report`);
    // 检查后端是否明确返回了成功状态和消息
    if (response && response.success) {
      return response; // 可以返回包含 report_id 的响应
    } else {
      // 如果后端没有返回标准的 success 字段，但状态码是 201，也认为成功
      // (axios 拦截器可能已经处理了数据，这里假设 response 是处理后的 data)
      // 更好的做法是确保后端总是返回一致的 { success: true, ... } 结构
      // 但为了兼容，我们先这样处理
      if (response && !response.success && response.message) { // 假设后端返回了 { message: '...' }
          console.warn('报告生成API未返回success=true，但有消息:', response.message);
          // 也可以根据具体情况决定是否抛出错误
          // throw new Error(response.message);
      } else if (!response) {
          console.warn('报告生成API未返回有效响应');
          // throw new Error('报告生成API未返回有效响应');
      }
      // 即使没有明确的 success: true，只要没抛出 http 错误，也暂时认为触发成功
      return response || { success: true, message: '报告生成请求已发送' }; 
    }
  } catch (error) {
    console.error(`为用户 ${userId} 生成报告失败 (API):`, error.response || error.message);
    // 抛出更具体的错误信息给前端组件
    const errorMessage = error.response?.data?.message || error.message || '生成报告时发生未知错误';
    throw new Error(errorMessage);
  }
};

/**
 * 管理员获取指定用户的健康趋势数据
 * @param {string|number} userId 用户ID
 * @param {object} params 查询参数 (可选, e.g., { data_types: 'weight_kg,mood', start_date: 'YYYY-MM-DD', end_date: 'YYYY-MM-DD' })
 * @returns {Promise<Object>} 包含趋势数据的对象
 */
export const getUserTrendsForAdmin = async (userId, params = {}) => {
  if (!userId) {
    throw new Error('获取用户趋势需要提供用户ID');
  }
  try {
    // 将 params 对象转换为 URL 查询参数
    const queryParams = new URLSearchParams(params).toString();
    const url = `/admin/users/${userId}/trends${queryParams ? '?' + queryParams : ''}`;
    const response = await api.get(url);
    // 假设响应拦截器已处理，直接返回数据部分
    if (response && response.success) {
        return response.data; 
    } else {
        throw new Error(response?.message || '获取用户趋势数据失败');
    }
  } catch (error) {
    console.error(`获取用户 ${userId} 趋势数据失败 (API):`, error.response || error.message);
    const errorMessage = error.response?.data?.message || error.message || '获取用户趋势数据时发生未知错误';
    throw new Error(errorMessage);
  }
};

/**
 * 获取食物推荐组合
 * GET /api/admin/food-recommendations
 */
export const getFoodRecommendations = async () => {
  try {
    // 注意：因为我们在 admin_api_bp 下添加了路由，所以路径是 /admin/food-recommendations
    // 如果您创建了独立的 food_api_bp (url_prefix='/api/foods'), 路径应改为 '/foods/recommendations'
    const response = await api.get('/admin/food-recommendations'); 
    if (response.data && response.data.success) {
      return response.data.data; // 返回 { mainDish: {name: ..., category: ...}, ... }
    } else {
      throw new Error(response.data?.message || '无法获取食物推荐');
    }
  } catch (error) {
    console.error('获取食物推荐API调用失败:', error.response?.data || error.message);
    // 将错误传递给调用者处理
    throw error;
  }
}; 