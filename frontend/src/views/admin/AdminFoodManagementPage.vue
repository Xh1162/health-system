<template>
  <div class="food-management-page">
    <h1>食物条目管理</h1>

    <!-- Success Message Display -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <div class="actions">
      <button @click="openCreateModal" class="create-button">创建新食物</button>
    </div>

    <!-- Search and Filter Controls -->
    <div class="controls-container">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="按名称搜索..." 
        class="search-input"
      />
      <select v-model="selectedCategory" class="filter-select">
        <option 
          v-for="cat in categories" 
          :key="cat.value" 
          :value="cat.value"
        >
          {{ cat.text }}
        </option>
      </select>
      <!-- Items per page selector (optional) -->
      <select v-model="itemsPerPage" @change="fetchFoodItems" class="filter-select per-page-select">
        <option value="5">5 / 页</option>
        <option value="10">10 / 页</option>
        <option value="20">20 / 页</option>
        <option value="50">50 / 页</option>
      </select>
      <button 
        @click="clearFiltersAndSearch" 
        class="clear-button"
        v-if="searchTerm || selectedCategory"
      >
        清除
      </button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error && !successMessage" class="error-message">{{ error }}</div>
    <div v-else>
      <table v-if="foodItems.length > 0" class="food-table">
        <thead>
          <tr>
            <!-- Make headers clickable for sorting -->
            <th @click="handleSort('id')" class="sortable-header">
              ID <span class="sort-icon">{{ getSortIcon('id') }}</span>
            </th>
            <th @click="handleSort('name')" class="sortable-header">
              名称 <span class="sort-icon">{{ getSortIcon('name') }}</span>
            </th>
            <th @click="handleSort('category')" class="sortable-header">
              类别 <span class="sort-icon">{{ getSortIcon('category') }}</span>
            </th>
            <th>描述</th> <!-- Assuming description is not sortable -->
            <th>图片URL</th>
            <th @click="handleSort('is_recommended')" class="sortable-header">
              推荐? <span class="sort-icon">{{ getSortIcon('is_recommended') }}</span>
            </th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <!-- Data rows (existing) -->
          <tr v-for="item in foodItems" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.category }}</td>
            <td class="description-cell">{{ item.description || '-' }}</td>
            <td>{{ item.image_url || '-' }}</td>
            <td>{{ item.is_recommended ? '是' : '否' }}</td>
            <td>
              <button @click="editItem(item)" class="edit-button">编辑</button>
              <button @click="deleteItem(item.id)" class="delete-button">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-data">没有找到匹配的食物条目。</p> <!-- Updated no data message -->

      <!-- Pagination Controls -->
      <div v-if="totalPages > 1" class="pagination-controls">
        <button 
          @click="changePage(currentPage - 1)" 
          :disabled="currentPage <= 1"
          class="page-button"
        >
          &laquo; 上一页
        </button>
        <span class="page-info">
          第 {{ currentPage }} 页 / 共 {{ totalPages }} 页 ({{ totalItems }} 条目)
        </span>
        <button 
          @click="changePage(currentPage + 1)" 
          :disabled="currentPage >= totalPages"
          class="page-button"
        >
          下一页 &raquo;
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <h2>{{ isEditing ? '编辑食物条目' : '创建新食物条目' }}</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">名称 <span class="required">*</span></label>
            <input type="text" id="name" v-model="currentItem.name" required />
          </div>
          <div class="form-group">
            <label for="category">类别 <span class="required">*</span></label>
            <select id="category" v-model="currentItem.category" required class="filter-select">
                <option disabled value="">请选择类别</option>
                <option 
                  v-for="cat in categories.filter(c => c.value !== '')" 
                  :key="cat.value" 
                  :value="cat.value"
                >
                  {{ cat.text }}
                </option>
             </select>
            <small>例如: protein, vegetable, staple, fruit, snack</small>
          </div>
          <div class="form-group">
            <label for="description">描述</label>
            <textarea id="description" v-model="currentItem.description"></textarea>
          </div>
          <div class="form-group">
            <label for="image_url">图片URL</label>
            <input type="text" id="image_url" v-model="currentItem.image_url" />
          </div>
           <div class="form-group form-group-checkbox">
            <label for="is_recommended">推荐?</label>
            <input type="checkbox" id="is_recommended" v-model="currentItem.is_recommended" />
          </div>

          <p v-if="modalError" class="error-message modal-error">{{ modalError }}</p>

          <div class="modal-actions">
            <button type="submit" :disabled="modalLoading" class="submit-button">
              {{ modalLoading ? '处理中...' : (isEditing ? '更新' : '创建') }}
            </button>
            <button type="button" @click="closeModal" class="cancel-button">取消</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Use the DeleteConfirmDialog component -->
    <DeleteConfirmDialog 
      :show="showDeleteConfirmDialog" 
      :item-id="itemToDeleteId"
      :item-name="itemToDeleteName"
      @confirm="confirmDeleteItem"
      @cancel="cancelDelete"
    />

  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../../api';
import useUserStore from '../../stores/userStore';
import debounce from 'lodash/debounce';
import DeleteConfirmDialog from '../../components/admin/DeleteConfirmDialog.vue'; // <-- Import the new component

const foodItems = ref([]);
const loading = ref(false);
const error = ref('');
const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// --- State for Pagination, Search, Filter, Sort (Initialize from URL or defaults) ---
const currentPage = ref(parseInt(route.query.page) || 1);
const itemsPerPage = ref(parseInt(route.query.per_page) || 10);
const totalItems = ref(0);
const totalPages = ref(1);
const searchTerm = ref(route.query.search || '');
const selectedCategory = ref(route.query.category || '');
const sortBy = ref(route.query.sort_by || 'name');
const sortOrder = ref(route.query.sort_order || 'asc');

// Categories - Will be fetched from API
const categories = ref([{ value: '', text: '所有类别' }]); // Initialize with 'All' option

// --- Modal State (Existing) ---
const showModal = ref(false);
const isEditing = ref(false);
const currentItem = reactive({
  id: null,
  name: '',
  category: '',
  description: '',
  image_url: '',
  is_recommended: true
});
const modalLoading = ref(false);
const modalError = ref('');
const successMessage = ref(''); // <-- Add ref for success messages
let successTimeout = null; // <-- Timeout ID

// State for Delete Confirmation Dialog
const showDeleteConfirmDialog = ref(false);
const itemToDeleteId = ref(null);
const itemToDeleteName = ref(''); // Store name for display

// Function to show success message and clear it after a delay
const showSuccessMessage = (message) => {
  successMessage.value = message;
  // Clear previous timeout if any
  if (successTimeout) clearTimeout(successTimeout);
  // Set new timeout
  successTimeout = setTimeout(() => {
    successMessage.value = '';
  }, 3000); // Display for 3 seconds
};

// --- Function to update URL query parameters ---
const updateUrlQuery = () => {
  const query = {};
  if (currentPage.value !== 1) query.page = currentPage.value;
  if (itemsPerPage.value !== 10) query.per_page = itemsPerPage.value;
  if (searchTerm.value) query.search = searchTerm.value;
  if (selectedCategory.value) query.category = selectedCategory.value;
  if (sortBy.value !== 'name') query.sort_by = sortBy.value;
  if (sortOrder.value !== 'asc') query.sort_order = sortOrder.value;

  router.push({ query, replace: true }); // Use replace: true to avoid history clutter
};

// --- Fetch Categories from API ---
const fetchCategories = async () => {
  const token = userStore.state.token;
  if (!token) return; // No need to fetch if not logged in

  try {
    const response = await api.get('/admin/food-categories', {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (response && response.success && Array.isArray(response.data)) {
      // Map the fetched category strings to the { value, text } format
      // Keep the 'All' option at the beginning
      const fetchedCategories = response.data.map(cat => ({ value: cat, text: cat }));
      categories.value = [{ value: '', text: '所有类别' }, ...fetchedCategories];
    } else {
      console.error("获取食物类别失败:", response);
      // Keep the default 'All' option on failure
      categories.value = [{ value: '', text: '所有类别' }];
    }
  } catch (error) {
    console.error("获取食物类别 API 错误:", error);
    categories.value = [{ value: '', text: '所有类别' }]; // Keep default on error
  }
};

// --- Get Food Items (Updated) ---
const fetchFoodItems = async () => {
  loading.value = true;
  error.value = '';
  
  // Update URL *before* fetching - ensures URL reflects current state being fetched
  updateUrlQuery(); 

  const token = userStore.state.token;

  if (!token) {
      error.value = '用户未登录或令牌丢失。';
      router.push('/login');
      loading.value = false;
      return;
  }

  // Construct query parameters (state already reflects URL or user action)
  const params = {
    page: currentPage.value,
    per_page: itemsPerPage.value,
    search: searchTerm.value,
    category: selectedCategory.value,
    sort_by: sortBy.value,
    sort_order: sortOrder.value,
  };

  try {
    const response = await api.get('/admin/food-items', { headers: { Authorization: `Bearer ${token}` }, params });

    if (response && response.success && Array.isArray(response.data)) {
      foodItems.value = response.data;
      if (response.pagination) {
        totalItems.value = response.pagination.total_items;
        totalPages.value = response.pagination.total_pages;
        // Don't update currentPage/itemsPerPage from response if it came from URL
        // currentPage.value = response.pagination.current_page; 
        // itemsPerPage.value = response.pagination.per_page;
      } else {
        // Handle case where pagination info might be missing (though unlikely with current backend)
        totalItems.value = response.data.length;
        totalPages.value = 1;
        currentPage.value = 1;
      }
      error.value = '';
    } else {
      console.error("获取食物列表失败，响应数据结构不符合预期:", response);
      error.value = (response && response.message) || '获取食物列表时返回数据格式不正确或操作未成功。';
      // Reset data on failure
      foodItems.value = [];
      totalItems.value = 0;
      totalPages.value = 1;
      currentPage.value = 1;
    }
  } catch (err) {
    console.error("获取食物列表错误:", err);
    // Keep existing error handling
    if (err.response && err.response.status === 401) {
        error.value = '认证失败或令牌过期，请重新登录。';
        router.push('/login');
    } else if (err.response && err.response.data && err.response.data.message) {
         error.value = `获取食物列表失败: ${err.response.data.message}`;
    }
     else {
         error.value = '获取食物列表时发生网络错误或未知错误。';
    }
    // Reset data on error
    foodItems.value = [];
    totalItems.value = 0;
    totalPages.value = 1;
    currentPage.value = 1;
  } finally {
    loading.value = false;
  }
};

// Debounced version - No need to call updateUrlQuery here, watcher does it
const debouncedFetchFoodItems = debounce(() => {
    currentPage.value = 1; // Reset page on search/filter
    fetchFoodItems();
}, 500);

// Watchers - Call fetch directly, which now handles URL update
watch(searchTerm, () => {
  debouncedFetchFoodItems();
});

watch(selectedCategory, () => {
  currentPage.value = 1;
  fetchFoodItems();
});

watch(itemsPerPage, () => {
  currentPage.value = 1;
  fetchFoodItems();
});

// Call fetchFoodItems and fetchCategories on component mount
onMounted(() => {
  fetchFoodItems();
  fetchCategories(); // Fetch categories when component mounts
});

// --- Sorting Logic (Updated) ---
const handleSort = (column) => {
  if (sortBy.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortBy.value = column;
    sortOrder.value = 'asc';
  }
  currentPage.value = 1;
  fetchFoodItems(); // fetchFoodItems will update URL
};

// Helper to get sort indicator class - Using Unicode characters
const getSortIcon = (column) => {
  if (sortBy.value !== column) return '↕'; // Up/Down arrow for non-active columns
  if (sortOrder.value === 'asc') return '▲'; // Up arrow for ascending
  return '▼'; // Down arrow for descending
};

// --- Pagination Logic (Updated) ---
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page;
    fetchFoodItems(); // fetchFoodItems will update URL
  }
};

// --- Clear Filters (Updated) ---
const clearFiltersAndSearch = () => {
  searchTerm.value = '';
  selectedCategory.value = '';
  currentPage.value = 1;
  // Optionally reset sort
  // sortBy.value = 'name';
  // sortOrder.value = 'asc';
  fetchFoodItems(); // fetchFoodItems will update URL
};

// --- Modal Control (Existing) ---
// ... (resetCurrentItem, openCreateModal, openEditModal, closeModal) ...

// --- CRUD Operations (Existing - check refresh logic) ---
// Ensure fetchFoodItems is called after create/update/delete to reflect changes correctly
// considering the current page/filters might change the item's visibility.
// Generally, calling fetchFoodItems() without changing page might be sufficient,
// but deleting the last item on a page requires careful handling (e.g., go to prev page).
// For simplicity, we'll just refresh the current view.

// ... (handleSubmit, editItem, deleteItem - Ensure fetchFoodItems() is called within them) ...

// Add the missing modal control functions here for completeness
const resetCurrentItem = () => {
    currentItem.id = null;
    currentItem.name = '';
    currentItem.category = '';
    currentItem.description = '';
    currentItem.image_url = '';
    currentItem.is_recommended = true;
};

const openCreateModal = () => {
  resetCurrentItem();
  isEditing.value = false;
  modalError.value = '';
  showModal.value = true;
};

const openEditModal = (item) => {
  isEditing.value = true;
  modalError.value = '';
  // Assign values carefully to avoid reactivity issues if needed
  currentItem.id = item.id;
  currentItem.name = item.name;
  currentItem.category = item.category;
  currentItem.description = item.description || '';
  currentItem.image_url = item.image_url || '';
  currentItem.is_recommended = item.is_recommended;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const handleSubmit = async () => {
  modalError.value = ''; 
  modalLoading.value = true;
  const token = userStore.state.token;
  if (!token) {
      modalError.value = '认证令牌丢失，请重新登录。';
      modalLoading.value = false;
      return;
  }
  if (!currentItem.name || !currentItem.category) {
      modalError.value = '名称和类别是必填项。';
      modalLoading.value = false;
      return;
  }
  const payload = {
      name: currentItem.name,
      category: currentItem.category,
      description: currentItem.description,
      image_url: currentItem.image_url,
      is_recommended: currentItem.is_recommended
  };
  try {
      let response;
      if (isEditing.value) {
          response = await api.put(`/admin/food-items/${currentItem.id}`, payload, {
              headers: { Authorization: `Bearer ${token}` }
          });
      } else {
          response = await api.post('/admin/food-items', payload, {
              headers: { Authorization: `Bearer ${token}` }
          });
      }
      if (response && response.success) {
          closeModal();
          await fetchFoodItems(); // Refresh the list - important!
          // Show success message
          showSuccessMessage(isEditing.value ? '食物条目更新成功！' : '食物条目创建成功！');
      } else {
          modalError.value = (response && response.message) || (isEditing.value ? '更新失败' : '创建失败');
      }
  } catch (err) {
      console.error("提交食物条目错误:", err);
      if (err.response && err.response.status === 401) {
          modalError.value = '认证失败或令牌过期。';
          router.push('/login');
      } else if (err.response && err.response.data && err.response.data.message) {
          modalError.value = `操作失败: ${err.response.data.message}`;
      } else {
          modalError.value = '发生网络错误或未知错误。';
      }
  } finally {
      modalLoading.value = false;
  }
};

const editItem = (item) => {
    openEditModal(item);
};

// Modified deleteItem trigger - just sets state
const deleteItem = (id) => {
    const item = foodItems.value.find(i => i.id === id);
    if (item) {
        itemToDeleteId.value = id;
        itemToDeleteName.value = item.name;
        showDeleteConfirmDialog.value = true;
    } else {
        console.error(`Item with id ${id} not found for deletion.`);
    }
};

// confirmDeleteItem function - handles the actual deletion after confirmation
// This function is now triggered by the child component's 'confirm' event
const confirmDeleteItem = async () => {
  if (!itemToDeleteId.value) return;

    const id = itemToDeleteId.value;
    showDeleteConfirmDialog.value = false; // Close the dialog

    const token = userStore.state.token;
    if (!token) {
        error.value = '认证令牌丢失，请重新登录。';
        return;
    }
    loading.value = true; 
    error.value = '';
    try {
        const response = await api.delete(`/admin/food-items/${id}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        if (response && response.success) {
            if (foodItems.value.length === 1 && currentPage.value > 1) {
                currentPage.value--;
            }
            await fetchFoodItems(); 
            showSuccessMessage('食物条目删除成功！');
        } else {
            error.value = (response && response.message) || '删除失败。';
        }
    } catch (err) {
        console.error("删除食物条目错误:", err);
        if (err.response && err.response.status === 401) {
            error.value = '认证失败或令牌过期，请重新登录。';
            router.push('/login');
        } else if (err.response && err.response.data && err.response.data.message) {
            error.value = `删除失败: ${err.response.data.message}`;
        } else if (err.response) {
             error.value = `删除失败: 服务器返回状态 ${err.response.status}`;
        } else {
            error.value = '删除时发生网络错误或未知错误。';
        }
    } finally {
        loading.value = false;
        itemToDeleteId.value = null; // Reset id
        itemToDeleteName.value = ''; // Reset name
    }
};

// Function to handle cancellation from the dialog
const cancelDelete = () => {
  showDeleteConfirmDialog.value = false;
  itemToDeleteId.value = null;
  itemToDeleteName.value = '';
};

</script>

<style scoped>
.food-management-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
}

h1 {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 30px;
  font-size: 28px;
}

.actions {
  margin-bottom: 20px;
  display: flex;
  justify-content: flex-end;
}

.create-button {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #27ae60;
}

.create-button::before {
  content: "+";
  margin-right: 8px;
  font-size: 16px;
  font-weight: bold;
}

.loading {
  text-align: center;
  padding: 30px;
  color: #7f8c8d;
  font-size: 18px;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-left: 4px solid #f5222d;
}

.food-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.food-table th {
  background-color: #3498db;
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
}

.food-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
}

.food-table tr:last-child td {
  border-bottom: none;
}

.food-table tr:hover {
  background-color: #f8f9fa;
}

.description-cell {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.edit-button, .delete-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  margin-right: 5px;
  transition: background-color 0.3s;
}

.edit-button {
  background-color: #3498db;
  color: white;
}

.edit-button:hover {
  background-color: #2980b9;
}

.delete-button {
  background-color: #e74c3c;
  color: white;
}

.delete-button:hover {
  background-color: #c0392b;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-size: 16px;
  border: 1px dashed #ccc;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-content h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
}

.form-group small {
  color: #7f8c8d;
  display: block;
  margin-top: 5px;
  font-size: 12px;
}

.form-group input[type="text"], 
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-group input[type="text"]:focus,
.form-group textarea:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-group textarea {
  min-height: 80px;
  resize: vertical;
}

.form-group-checkbox {
  display: flex;
  align-items: center;
}

.form-group-checkbox label {
  margin-right: 10px;
  margin-bottom: 0;
}

.form-group-checkbox input[type="checkbox"] {
  transform: scale(1.2);
}

.required {
  color: #e74c3c;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
  gap: 10px;
}

.submit-button, .cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.submit-button {
  background-color: #3498db;
  color: white;
}

.submit-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.submit-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.cancel-button {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

.cancel-button:hover {
  background-color: #dfe6e9;
}

.modal-error {
  margin-top: 15px;
  margin-bottom: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .food-table {
    display: block;
    overflow-x: auto;
  }
  
  .modal-content {
    width: 95%;
    padding: 15px;
  }
  
  .description-cell {
    max-width: 150px;
  }
}

.form-group .input-with-hint {
  position: relative;
}

.form-group .hint {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
  font-size: 12px;
}

/* Controls Container */
.controls-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  flex-grow: 1; /* Allow search input to take available space */
  min-width: 200px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.search-input:focus {
  border-color: #3498db;
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
  cursor: pointer;
}

.per-page-select {
  min-width: 80px;
}

/* Table Header Sorting */
.sortable-header {
  cursor: pointer;
  position: relative;
  padding-right: 20px; /* Space for sort icon */
  user-select: none;
}

.sortable-header:hover {
  background-color: #2980b9; /* Slightly darker blue on hover */
}

/* Style for new sort icon span */
.sort-icon {
  display: inline-block;
  margin-left: 5px;
  width: 1em; /* Ensure space is allocated */
  text-align: center;
  color: rgba(255, 255, 255, 0.7); /* Slightly transparent white */
}

.sortable-header:hover .sort-icon {
  color: white; /* Opaque on hover */
}

/* Pagination Controls */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.page-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
  margin: 0 10px;
}

.page-button:hover:not(:disabled) {
  background-color: #2980b9;
}

.page-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
  opacity: 0.7;
}

.page-info {
  color: #34495e;
  font-weight: 500;
  font-size: 14px;
}

/* Adjust modal category select */
.modal-content .filter-select {
   width: 100%;
   padding: 10px; /* Match other inputs */
}

/* Adjust modal small text positioning */
.modal-content .form-group small {
   margin-top: 8px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  /* ... existing responsive styles ... */
  .controls-container {
    flex-direction: column; /* Stack controls vertically */
    align-items: stretch; /* Make controls take full width */
  }
  
  .search-input,
  .filter-select {
    width: 100%; /* Full width on small screens */
  }

  .pagination-controls {
    flex-direction: column;
    gap: 10px;
  }
}

/* Success Message Style */
.success-message {
  background-color: #d4edda; /* Light green */
  color: #155724; /* Dark green */
  padding: 12px 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  border-left: 4px solid #28a745; /* Green border */
  animation: fadeIn 0.5s ease-out;
}

/* Add fadeIn animation */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Remove styles specific to the old inline delete confirmation dialog */
/*
.delete-confirm-modal p { ... }
.item-to-delete-info { ... }
.item-to-delete-info strong { ... }
.delete-confirm-button { ... }
.delete-confirm-button:hover { ... }
*/

/* Keep general modal styles if they were used by the old dialog and are still needed */
.modal-overlay { /* Might be needed by create/edit modal */
  /* ... */
}
.modal-content { /* Might be needed by create/edit modal */
  /* ... */
}
.modal-actions { /* Might be needed by create/edit modal */
  /* ... */
}
.cancel-button { /* Might be needed by create/edit modal */
 /* ... */
}

</style>