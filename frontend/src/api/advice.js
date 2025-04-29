import api from './index'; // 导入配置好的 axios 实例

/**
 * 用户提交建议请求
 * @param {string} [requestText] - 用户可选填写的请求说明
 * @returns {Promise<object>} 后端返回的响应数据
 */
export const submitAdviceRequest = async (requestText) => {
  try {
    // 构造请求体，如果 requestText 为空或 undefined，则发送空对象或不发送 request_text
    const payload = requestText ? { request_text: requestText } : {};
    
    // 调用后端 API
    const response = await api.post('/advice-requests', payload);
    
    // 检查 Flask 后端返回的格式
    if (response && response.success) {
       return response; // 返回整个响应，可能包含 data 和 message
    } else {
       console.error('提交建议请求 API 响应格式无效或失败:', response);
       throw new Error(response?.message || '提交建议请求失败');
    }

  } catch (error) {
    console.error('调用 submitAdviceRequest API 失败:', error);
    // 将详细错误信息向上抛出
    const errorMessage = error.response?.data?.message || error.message || '提交建议请求时发生网络或服务器错误';
    throw new Error(errorMessage);
  }
}; 