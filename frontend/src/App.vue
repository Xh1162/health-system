<template>
  <div class="app-container">
    <div v-if="error" class="error-message">
      <h2>出错了！</h2>
      <p>{{ error }}</p>
      <button @click="resetError">重试</button>
    </div>
    <router-view v-else @error="handleError"></router-view>
  </div>
</template>

<script setup>
import { ref, onMounted, onErrorCaptured } from 'vue'

const error = ref(null)

// 处理错误
const handleError = (err) => {
  console.error('应用捕获到错误:', err)
  error.value = err.message || '应用发生了未知错误'
}

// 重置错误状态
const resetError = () => {
  error.value = null
  window.location.reload()
}

// 全局错误捕获
onErrorCaptured((err) => {
  console.error('全局错误捕获:', err)
  handleError(err)
  return false // 阻止错误继续传播
})

onMounted(() => {
  console.log('App.vue已挂载')
})
</script>

<style>
:root {
  --primary-color: #3b82f6;
  --primary-light: #60a5fa;
  --text-color: #1e293b;
  --background-color: #f8fafc;
  --border-color: #e2e8f0;
}

body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--background-color);
  color: var(--text-color);
}

* {
  box-sizing: border-box;
}

button {
  font-family: inherit;
}

input, button {
  outline: none;
}

input:focus {
  border-color: var(--primary-color);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.error-message {
  padding: 20px;
  margin: 20px auto;
  max-width: 600px;
  background-color: #fee2e2;
  border: 1px solid #ef4444;
  border-radius: 8px;
  text-align: center;
}

.error-message h2 {
  color: #b91c1c;
  margin-top: 0;
}

.error-message button {
  margin-top: 15px;
  padding: 8px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-message button:hover {
  background-color: #2563eb;
}
</style> 