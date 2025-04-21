<template>
  <div class="avatar-container" :class="{ 'with-badge': showAdminBadge }">
    <img 
      v-if="avatarUrl" 
      :src="avatarUrl" 
      :alt="username || 'User avatar'" 
      class="avatar-image"
      @error="handleImageError"
    />
    <div v-else class="avatar-placeholder">
      {{ userInitial }}
    </div>
    <div v-if="showAdminBadge" class="admin-badge" title="Administrator">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import useUserStore from '../../stores/userStore'

const props = defineProps({
  username: {
    type: String,
    default: ''
  },
  avatarUrl: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'medium'
  },
  showAdminBadge: {
    type: Boolean,
    default: false
  }
})

const userStore = useUserStore()
const localAvatarUrl = ref('')

const avatarUrl = computed(() => {
  return props.avatarUrl || localAvatarUrl.value || ''
})

const userInitial = computed(() => {
  if (props.username && props.username.length > 0) {
    return props.username.charAt(0).toUpperCase()
  }
  return 'U'
})

const handleImageError = () => {
  console.warn('Avatar image failed to load')
  localAvatarUrl.value = ''
}

onMounted(() => {
  if (!props.avatarUrl && !props.username) {
    // If no props are provided, try to get from user store
    const userData = userStore.userData
    if (userData) {
      localAvatarUrl.value = userData.avatar || ''
    }
  } else {
    localAvatarUrl.value = props.avatarUrl
  }
})

defineExpose({
  updateAvatar(url) {
    localAvatarUrl.value = url
  }
})
</script>

<style scoped>
.avatar-container {
  position: relative;
  display: inline-block;
}

.avatar-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #f0f0f0;
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
}

.avatar-container.with-badge {
  margin-right: 4px;
}

.admin-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  background-color: #f1c40f;
  color: #fff;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  border: 1px solid white;
}

/* Size variants */
.avatar-container.small .avatar-image,
.avatar-container.small .avatar-placeholder {
  width: 24px;
  height: 24px;
  font-size: 12px;
}

.avatar-container.large .avatar-image,
.avatar-container.large .avatar-placeholder {
  width: 64px;
  height: 64px;
  font-size: 24px;
}
</style> 