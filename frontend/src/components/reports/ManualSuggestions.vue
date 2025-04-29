<template>
  <div class="manual-suggestions-section">
    <div class="section-header">
      <h3>健康建议</h3>
      <p class="subtitle">为您量身定制的专业建议</p>
    </div>

    <!-- 建议列表 -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="suggestions.length === 0" class="empty-state">
      <p>暂无个性化建议</p>
    </div>
    
    <div v-else class="suggestions-list">
      <div 
        v-for="suggestion in suggestions" 
        :key="suggestion.id" 
        class="suggestion-item"
      >
        <div class="suggestion-content">{{ suggestion.content }}</div>
        <div class="suggestion-meta">
          <span class="suggestion-date">{{ formatDate(suggestion.created_at) }}</span>
          <span v-if="isAdmin" class="suggestion-admin">- {{ suggestion.admin_name || '系统' }}</span>
        </div>
        <button 
          v-if="isAdmin" 
          class="delete-button" 
          @click="confirmDelete(suggestion.id)"
        >
          删除
        </button>
      </div>
    </div>

    <!-- 管理员添加建议表单 -->
    <div v-if="isAdmin" class="add-suggestion-form">
      <h4>添加新建议</h4>
      <textarea 
        v-model="newSuggestion" 
        placeholder="输入对该用户的健康建议..."
        rows="4"
      ></textarea>
      <div class="form-actions">
        <button 
          class="submit-button" 
          :disabled="!newSuggestion.trim() || submitting" 
          @click="addSuggestion"
        >
          {{ submitting ? '提交中...' : '添加建议' }}
        </button>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteConfirm" class="delete-confirm-modal">
      <div class="modal-content">
        <h4>确认删除</h4>
        <p>确定要删除这条建议吗？此操作无法撤销。</p>
        <div class="modal-actions">
          <button class="cancel-button" @click="showDeleteConfirm = false">取消</button>
          <button class="delete-button" @click="deleteSuggestion">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getManualSuggestions, addManualSuggestion, deleteManualSuggestion } from '../../api/suggestions'
import useUserStore from '../../stores/userStore'

const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

const userStore = useUserStore()
const isAdmin = computed(() => userStore.state.userData?.role === 'admin')

const suggestions = ref([])
const loading = ref(true)
const newSuggestion = ref('')
const submitting = ref(false)
const showDeleteConfirm = ref(false)
const deletingId = ref(null)

// 加载建议列表
const loadSuggestions = async () => {
  loading.value = true
  try {
    const data = await getManualSuggestions(props.userId)
    suggestions.value = data
  } catch (err) {
    console.error('加载建议失败:', err)
  } finally {
    loading.value = false
  }
}

// 添加新建议
const addSuggestion = async () => {
  if (!newSuggestion.value.trim() || submitting.value) return
  
  submitting.value = true
  try {
    await addManualSuggestion(props.userId, newSuggestion.value.trim())
    // 重新加载建议列表
    await loadSuggestions()
    // 清空表单
    newSuggestion.value = ''
  } catch (err) {
    console.error('添加建议失败:', err)
    alert(`添加建议失败: ${err.message || '未知错误'}`)
  } finally {
    submitting.value = false
  }
}

// 确认删除
const confirmDelete = (id) => {
  deletingId.value = id
  showDeleteConfirm.value = true
}

// 执行删除
const deleteSuggestion = async () => {
  if (!deletingId.value) return
  
  try {
    await deleteManualSuggestion(deletingId.value)
    // 本地更新列表
    suggestions.value = suggestions.value.filter(item => item.id !== deletingId.value)
    showDeleteConfirm.value = false
    deletingId.value = null
  } catch (err) {
    console.error('删除建议失败:', err)
    alert(`删除建议失败: ${err.message || '未知错误'}`)
  }
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 组件挂载时加载数据
onMounted(() => {
  loadSuggestions()
})
</script>

<style scoped>
.manual-suggestions-section {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-top: 1.5rem;
  position: relative;
}

.section-header {
  margin-bottom: 1.25rem;
}

.section-header h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  font-weight: 600;
}

.subtitle {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 2rem 0;
  color: #64748b;
}

/* 建议列表 */
.suggestions-list {
  margin-bottom: 1.5rem;
}

.suggestion-item {
  border-radius: 0.5rem;
  padding: 1rem;
  background: #f8fafc;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: relative;
}

.suggestion-content {
  font-size: 0.95rem;
  color: #334155;
  line-height: 1.5;
  margin-bottom: 0.5rem;
  white-space: pre-line;
}

.suggestion-meta {
  font-size: 0.75rem;
  color: #94a3b8;
}

.delete-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.delete-button:hover {
  background: #fee2e2;
}

/* 添加建议表单 */
.add-suggestion-form {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.add-suggestion-form h4 {
  font-size: 1rem;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.add-suggestion-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  resize: vertical;
  font-family: inherit;
  font-size: 0.95rem;
  margin-bottom: 0.75rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.submit-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover:not(:disabled) {
  background: #2563eb;
}

.submit-button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

/* 删除确认对话框 */
.delete-confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-content h4 {
  font-size: 1.1rem;
  color: #1e293b;
  margin: 0 0 1rem 0;
}

.modal-content p {
  color: #334155;
  margin: 0 0 1.5rem 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.cancel-button {
  background: #e2e8f0;
  color: #334155;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
}

.modal-actions .delete-button {
  position: static;
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.modal-actions .delete-button:hover {
  background: #dc2626;
}
</style> 