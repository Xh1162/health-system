import axios from 'axios'

// 根据环境设置不同的 baseURL
const baseURL = import.meta.env.PROD 
  ? 'https://你的域名/api'  // 生产环境 API 地址
  : 'http://localhost:5000/api' // 开发环境 API 地址

const api = axios.create({
  baseURL,
  timeout: 5000
})

export default api 