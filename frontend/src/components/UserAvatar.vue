<template>
  <div class="user-avatar">
    <div class="avatar-container">
      <img :src="avatarUrl" :alt="username" class="avatar-image" />
      <div class="avatar-overlay" v-if="editable">
        <label class="change-avatar">
          <span>更换头像</span>
          <input 
            type="file" 
            accept="image/*" 
            @change="handleAvatarChange" 
            hidden 
          />
        </label>
      </div>
    </div>
    <div class="user-info" v-if="showInfo">
      <span class="username">{{ username }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import useUserStore from '../stores/userStore'

const userStore = useUserStore()
const props = defineProps({
  editable: {
    type: Boolean,
    default: true
  },
  showInfo: {
    type: Boolean,
    default: true
  }
})

const username = computed(() => userStore.state.username)
const avatarUrl = computed(() => {
  if (!userStore.state.avatar) {
    return 'https://via.placeholder.com/100'
  }
  return userStore.state.avatar
})

const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  if (file.size > 2 * 1024 * 1024) {
    alert('图片大小不能超过 2MB')
    return
  }

  try {
    const formData = new FormData()
    formData.append('avatar', file)
    
    const response = await fetch(`/api/auth/avatar/${userStore.state.userData?.id}`, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${userStore.state.token}`
      }
    })
    
    const data = await response.json()
    
    if (data.success) {
      userStore.updateAvatar(data.data.avatar)
      alert('头像更新成功！')
    } else {
      throw new Error(data.message || '头像上传失败')
    }
  } catch (error) {
    console.error('头像上传错误:', error)
    alert('头像上传失败: ' + error.message)
  }
}
</script>

<style scoped>
.user-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.avatar-container {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
  cursor: pointer;
}

.avatar-container:hover .avatar-overlay {
  opacity: 1;
}

.change-avatar {
  color: white;
  font-size: 12px;
  cursor: pointer;
}

.user-info {
  text-align: center;
}

.username {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}
</style> 