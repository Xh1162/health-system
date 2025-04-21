<template>
  <div class="avatar-test">
    <h2>头像测试组件</h2>
    <div class="avatar-section">
      <h3>UserStore Avatar</h3>
      <div class="avatar">
        <img :src="userStoreAvatar" alt="User Avatar from Store" />
        <div class="avatar-info">
          <p>Avatar URL: {{ userStoreAvatar }}</p>
        </div>
      </div>
    </div>
    
    <div class="avatar-section">
      <h3>Computed Avatar</h3>
      <div class="avatar">
        <img :src="computedAvatarUrl" alt="Computed Avatar URL" />
        <div class="avatar-info">
          <p>Avatar URL: {{ computedAvatarUrl }}</p>
        </div>
      </div>
    </div>
    
    <div class="avatar-section">
      <h3>Raw Avatar</h3>
      <div class="avatar">
        <img :src="rawAvatarUrl" alt="Raw Avatar URL" />
        <div class="avatar-info">
          <p>Avatar URL: {{ rawAvatarUrl }}</p>
        </div>
      </div>
    </div>
    
    <div class="avatar-section">
      <h3>Upload New Avatar</h3>
      <input type="file" accept="image/*" @change="handleFileChange" />
      <button @click="uploadAvatar" :disabled="!selectedFile">上传</button>
      <div v-if="uploadStatus" class="upload-status">
        {{ uploadStatus }}
      </div>
    </div>
    
    <div class="user-data">
      <h3>用户数据</h3>
      <pre>{{ JSON.stringify(userStore.state.userData, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, inject, computed, onMounted } from 'vue'

const userStore = inject('userStore')
const selectedFile = ref(null)
const uploadStatus = ref('')

// 直接从userStore获取头像URL
const userStoreAvatar = computed(() => userStore.state.userData?.avatar || '')

// 计算属性生成头像URL
const computedAvatarUrl = computed(() => {
  const avatar = userStore.state.userData?.avatar
  if (!avatar) return 'http://localhost:5008/default-avatar.png'
  
  // 确保是完整URL
  if (avatar.startsWith('http')) return avatar
  return avatar.startsWith('/') 
    ? `http://localhost:5008${avatar}` 
    : `http://localhost:5008/${avatar}`
})

// 原始头像URL，不做任何处理
const rawAvatarUrl = computed(() => {
  const avatar = userStore.state.userData?.avatar || ''
  console.log('Raw Avatar URL:', avatar)
  return avatar
})

// 处理文件选择
const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0]
  if (selectedFile.value) {
    console.log('已选择文件:', {
      name: selectedFile.value.name,
      size: selectedFile.value.size,
      type: selectedFile.value.type
    })
  }
}

// 上传头像
const uploadAvatar = async () => {
  if (!selectedFile.value) {
    uploadStatus.value = '请先选择文件'
    return
  }
  
  try {
    uploadStatus.value = '上传中...'
    
    const formData = new FormData()
    formData.append('avatar', selectedFile.value)
    
    if (!userStore.state.userData?.id) {
      uploadStatus.value = '用户未登录'
      return
    }
    
    const baseUrl = 'http://localhost:5008'
    const url = `${baseUrl}/api/auth/avatar/${userStore.state.userData.id}`
    
    console.log('上传URL:', url)
    console.log('Token:', userStore.state.token)
    
    const response = await fetch(url, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${userStore.state.token}`
      }
    })
    
    const data = await response.json()
    console.log('上传响应:', data)
    
    if (response.ok && data.success) {
      uploadStatus.value = '上传成功'
      
      // 更新头像
      if (data.data?.avatar) {
        const avatarUrl = data.data.avatar
        
        // 处理相对路径
        const fullAvatarUrl = avatarUrl.startsWith('http') 
          ? avatarUrl 
          : avatarUrl.startsWith('/') 
            ? `${baseUrl}${avatarUrl}` 
            : `${baseUrl}/${avatarUrl}`
        
        console.log('新头像URL:', fullAvatarUrl)
        userStore.updateAvatar(fullAvatarUrl)
      } else {
        console.error('响应中缺少avatar:', data)
        uploadStatus.value = '上传成功但未获取到新头像URL'
      }
    } else {
      uploadStatus.value = '上传失败: ' + (data.message || '未知错误')
    }
  } catch (error) {
    console.error('上传出错:', error)
    uploadStatus.value = '上传出错: ' + error.message
  }
}

onMounted(() => {
  console.log('AvatarTest组件已挂载')
  console.log('当前用户数据:', userStore.state.userData)
})
</script>

<style scoped>
.avatar-test {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.avatar-section {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  background: #f9f9f9;
}

.avatar {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ddd;
}

.avatar-info {
  flex: 1;
}

.user-data {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  overflow: auto;
  max-height: 300px;
}

pre {
  margin: 0;
  white-space: pre-wrap;
}

button {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.upload-status {
  margin-top: 10px;
  padding: 8px;
  border-radius: 4px;
  background: #f8f8f8;
}
</style> 