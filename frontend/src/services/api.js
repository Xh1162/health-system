import axios from 'axios'
import userStore from '../stores/userStore'

const api = axios.create({
    baseURL: 'http://localhost:5006/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 请求拦截器
api.interceptors.request.use(
    config => {
        console.log('发送请求:', {
            url: config.url,
            method: config.method,
            headers: config.headers,
            data: config.data
        })

        // 从 userStore 获取 token
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
        console.log('收到响应:', response.data)
        return response.data
    },
    error => {
        if (error.response) {
            console.error('响应错误:', {
                status: error.response.status,
                data: error.response.data
            })
        } else if (error.request) {
            console.error('请求未收到响应:', error.request)
        } else {
            console.error('请求配置错误:', error.message)
        }
        return Promise.reject(error)
    }
)

export const authApi = {
    login: async (username, password) => {
        const response = await api.post('/auth/login', { username, password })
        return response
    },
    
    register: async (userData) => {
        console.log('注册请求数据:', userData)
        const response = await api.post('/auth/register', userData)
        return response
    }
}

export const userApi = {
    updateAvatar: async (userId, file) => {
        try {
            // 检查文件类型
            const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']
            if (!allowedTypes.includes(file.type)) {
                throw new Error('不支持的文件类型，请上传 PNG、JPG、JPEG 或 GIF 格式的图片')
            }

            // 检查文件大小
            if (file.size > 2 * 1024 * 1024) {
                throw new Error('文件大小不能超过 2MB')
            }

            // 创建 FormData
            const formData = new FormData()
            formData.append('avatar', file)
            
            console.log('上传文件信息:', {
                name: file.name,
                type: file.type,
                size: file.size
            })
            
            // 检查token是否存在
            const token = userStore.state.token
            if (!token) {
                console.error('Token不存在，请先登录')
                throw new Error('请先登录')
            }
            
            console.log('使用的Token:', token)
            console.log('上传的用户ID:', userId)
            
            // 发送请求，使用原生fetch API
            const response = await fetch(`/api/auth/avatar/${userId}`, {
                method: 'POST',
                body: formData,
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            
            if (!response.ok) {
                const errorData = await response.json()
                console.error('上传失败:', errorData)
                throw new Error(errorData.message || `上传失败: ${response.status}`)
            }
            
            const data = await response.json()
            console.log('上传响应:', data)
            return data
        } catch (error) {
            console.error('头像上传错误:', error)
            throw error
        }
    },

    updateUsername: async (username) => {
        const response = await api.post('/auth/username', { username })
        return response
    },

    updatePassword: async (currentPassword, newPassword) => {
        const response = await api.post('/auth/password', { 
            currentPassword, 
            newPassword 
        })
        return response
    },

    sendPhoneCode: async (phone) => {
        const response = await api.post('/auth/phone/code', { phone })
        return response
    },

    bindPhone: async (phone, code) => {
        const response = await api.post('/auth/phone/bind', { phone, code })
        return response
    },

    sendEmailCode: async (email) => {
        const response = await api.post('/auth/email/code', { email })
        return response
    },

    bindEmail: async (email, code) => {
        const response = await api.post('/auth/email/bind', { email, code })
        return response
    }
}

export default api 