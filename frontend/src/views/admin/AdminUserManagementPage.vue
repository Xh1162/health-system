<template>
  <div class="user-management-page">
    <h1>用户管理</h1>
    
    <!-- Top Actions: Create Button -->
    <div class="top-actions">
       <button @click="openCreateModal" class="create-button">创建新用户</button>
    </div>
    
    <!-- Controls: Search, Filters, Clear -->
    <div class="controls-container">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="按用户名或邮箱搜索..." 
        class="search-input"
      />
      <select v-model="selectedRole" class="filter-select">
        <option 
          v-for="opt in roleOptions" 
          :key="opt.value" 
          :value="opt.value"
        >
          {{ opt.text }}
        </option>
      </select>
       <select v-model="selectedStatus" class="filter-select">
        <option 
          v-for="opt in statusOptions" 
          :key="opt.value" 
          :value="opt.value"
        >
          {{ opt.text }}
        </option>
      </select>
      <select v-model="itemsPerPage" class="filter-select per-page-select">
        <option value="10">10 / 页</option>
        <option value="20">20 / 页</option>
        <option value="50">50 / 页</option>
        <option value="100">100 / 页</option>
      </select>
       <button 
        @click="clearFiltersAndSearch" 
        class="clear-button"
        v-if="searchTerm || selectedRole || selectedStatus"
      >
        清除
      </button>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error-message">{{ error }}</div>

    <!-- User Table -->
    <div v-else>
      <table v-if="users.length > 0" class="user-table">
        <thead>
          <tr>
            <th @click="handleSort('id')" class="sortable-header">
              ID <span class="sort-icon">{{ getSortIcon('id') }}</span>
            </th>
            <th @click="handleSort('username')" class="sortable-header">
              用户名 <span class="sort-icon">{{ getSortIcon('username') }}</span>
            </th>
             <th @click="handleSort('email')" class="sortable-header">
              邮箱 <span class="sort-icon">{{ getSortIcon('email') }}</span>
            </th>
             <th @click="handleSort('role')" class="sortable-header">
              角色 <span class="sort-icon">{{ getSortIcon('role') }}</span>
            </th>
             <th @click="handleSort('is_active')" class="sortable-header">
              状态 <span class="sort-icon">{{ getSortIcon('is_active') }}</span>
            </th>
             <th @click="handleSort('created_at')" class="sortable-header">
              注册时间 <span class="sort-icon">{{ getSortIcon('created_at') }}</span>
            </th>
            <th>操作</th> <!-- Actions column -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email || '-' }}</td>
            <td>{{ user.role === 'admin' ? '管理员' : '用户' }}</td>
            <td>
              <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? '激活' : '禁用' }}
              </span>
            </td>
            <td>{{ new Date(user.created_at).toLocaleString() }}</td>
            <td>
              <!-- Add Details Button -->
              <button class="action-button details-button" @click="fetchAndShowUserDetails(user.id)">详情</button>
              <button class="action-button edit-button" @click="openEditModal(user)">编辑</button>
              <button class="action-button delete-button" @click="requestDeleteUser(user)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-data">没有找到匹配的用户。</p>

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

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-content edit-user-modal">
         <h2>编辑用户 (ID: {{ userToEdit?.id }})</h2>
         <p>用户名: <strong>{{ userToEdit?.username }}</strong></p>

         <form @submit.prevent="handleUserUpdate">
           <div class="form-group">
             <label for="edit-role">角色</label>
             <select id="edit-role" v-model="editForm.role" class="filter-select">
               <!-- Filter out the 'All Roles' option -->
               <option 
                 v-for="opt in roleOptions.filter(r => r.value !== '')" 
                 :key="opt.value" 
                 :value="opt.value"
               >
                 {{ opt.text }}
               </option>
             </select>
           </div>

           <div class="form-group">
             <label for="edit-status">账号状态</label>
             <select id="edit-status" v-model="editForm.is_active" class="filter-select">
               <!-- Use true/false as values for boolean binding -->
               <option :value="true">激活</option>
               <option :value="false">禁用</option>
             </select>
           </div>

           <p v-if="editModalError" class="error-message modal-error">{{ editModalError }}</p>

           <div class="modal-actions">
             <button type="submit" :disabled="editModalLoading" class="submit-button">
               {{ editModalLoading ? '保存中...' : '保存更改' }}
             </button>
             <button type="button" @click="closeEditModal" class="cancel-button">取消</button>
           </div>
         </form>
      </div>
    </div>

    <!-- Delete User Confirmation Modal (Using the imported component) -->
    <DeleteConfirmDialog 
      :show="showDeleteConfirmDialog" 
      :item-id="userToDeleteId"
      :item-name="userToDeleteName"
      item-type="用户" 
      @confirm="confirmUserDelete"
      @cancel="cancelDeleteUser"
    />

    <!-- User Details Modal -->
    <div v-if="showDetailsModal" class="modal-overlay" @click.self="closeDetailsModal">
      <div class="modal-content details-modal">
        <h2>用户详情 (ID: {{ userIdForDetails }})</h2>
        
        <!-- Loading and Error States within Modal -->
        <div v-if="detailsLoading" class="loading">加载详细信息中...</div>
        <div v-else-if="detailsError" class="error-message">{{ detailsError }}</div>
        
        <!-- Details Content -->
        <div v-else-if="selectedUserForDetails" class="user-details-content">
          <div class="detail-section">
            <h4>基本信息</h4>
            <p><strong>用户名:</strong> {{ selectedUserForDetails.username }}</p>
            <p><strong>邮箱:</strong> {{ displayProfileData(selectedUserForDetails.email) }}</p>
            <p><strong>电话:</strong> {{ displayProfileData(selectedUserForDetails.phone) }}</p>
            <p><strong>角色:</strong> {{ selectedUserForDetails.role === 'admin' ? '管理员' : '普通用户' }}</p>
            <p><strong>状态:</strong> 
              <span :class="selectedUserForDetails.is_active ? 'status-active' : 'status-inactive'">
                 {{ selectedUserForDetails.is_active ? '激活' : '禁用' }}
              </span>
            </p>
            <p><strong>注册时间:</strong> {{ new Date(selectedUserForDetails.created_at).toLocaleString() }}</p>
            <p><strong>最后更新:</strong> {{ new Date(selectedUserForDetails.updated_at).toLocaleString() }}</p>
          </div>

          <div class="detail-section">
            <h4>个人资料 (Profile)</h4>
            <div v-if="selectedUserForDetails.profile">
              <p><strong>身高:</strong> {{ displayProfileData(selectedUserForDetails.profile.height) }} cm</p>
              <p><strong>体重:</strong> {{ displayProfileData(selectedUserForDetails.profile.weight) }} kg</p>
              <p><strong>出生日期:</strong> {{ displayProfileData(selectedUserForDetails.profile.birth_date) }}</p>
              <p><strong>性别:</strong> {{ displayProfileData(selectedUserForDetails.profile.gender) }}</p>
              <p><strong>目标体重:</strong> {{ displayProfileData(selectedUserForDetails.profile.weight_goal) }} kg</p>
              <p><strong>活动水平:</strong> {{ displayProfileData(selectedUserForDetails.profile.activity_level) }}</p>
            </div>
            <p v-else>该用户尚未填写个人资料。</p>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="modal-actions">
          <button type="button" @click="closeDetailsModal" class="cancel-button">关闭</button>
        </div>
      </div>
    </div>

    <!-- Create User Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeCreateModal">
      <div class="modal-content create-user-modal">
        <h2>创建新用户</h2>
        <form @submit.prevent="handleUserCreate">
          <div class="form-group">
            <label for="create-username">用户名 <span class="required">*</span></label>
            <input id="create-username" type="text" v-model.trim="createForm.username" class="filter-select" required />
          </div>
          <div class="form-group">
            <label for="create-email">邮箱</label>
            <input id="create-email" type="email" v-model.trim="createForm.email" class="filter-select" placeholder="可选" />
          </div>
          <div class="form-group">
            <label for="create-password">密码 <span class="required">*</span></label>
            <input id="create-password" type="password" v-model="createForm.password" class="filter-select" required />
          </div>
          <div class="form-group">
            <label for="create-confirm-password">确认密码 <span class="required">*</span></label>
            <input id="create-confirm-password" type="password" v-model="createForm.confirmPassword" class="filter-select" required />
          </div>
          <div class="form-group">
            <label for="create-role">角色</label>
            <select id="create-role" v-model="createForm.role" class="filter-select">
               <!-- Filter out the 'All Roles' option for creation -->
               <option 
                 v-for="opt in roleOptions.filter(r => r.value !== '')" 
                 :key="opt.value" 
                 :value="opt.value"
               >
                 {{ opt.text }}
               </option>
            </select>
          </div>
          <div class="form-group">
            <label for="create-status">账号状态</label>
            <select id="create-status" v-model="createForm.is_active" class="filter-select">
              <option :value="true">激活</option>
              <option :value="false">禁用</option>
            </select>
          </div>

          <p v-if="createModalError" class="error-message modal-error">{{ createModalError }}</p>

          <div class="modal-actions">
            <button type="submit" :disabled="createModalLoading" class="submit-button">
              {{ createModalLoading ? '创建中...' : '创建用户' }}
            </button>
            <button type="button" @click="closeCreateModal" class="cancel-button">取消</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../../api'; // API client
import useUserStore from '../../stores/userStore'; // User store
import debounce from 'lodash/debounce';
import DeleteConfirmDialog from '../../components/admin/DeleteConfirmDialog.vue';

const users = ref([]);
const loading = ref(false);
const error = ref('');
const successMessage = ref(''); // For potential future success messages
let successTimeout = null;

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// --- State for Pagination, Search, Filter, Sort ---
const currentPage = ref(parseInt(route.query.page) || 1);
const itemsPerPage = ref(parseInt(route.query.per_page) || 10);
const totalItems = ref(0);
const totalPages = ref(1);
const searchTerm = ref(route.query.search || '');
const selectedRole = ref(route.query.role || ''); // '' means all roles
const selectedStatus = ref(route.query.status || ''); // '' means all statuses
const sortBy = ref(route.query.sort_by || 'id'); // Default sort column
const sortOrder = ref(route.query.sort_order || 'asc'); // Default sort order

// Filter options
const roleOptions = ref([
  { value: '', text: '所有角色' },
  { value: 'admin', text: '管理员' },
  { value: 'user', text: '普通用户' },
]);

const statusOptions = ref([
  { value: '', text: '所有状态' },
  { value: 'active', text: '激活' },
  { value: 'inactive', text: '禁用' },
]);

// --- State for Edit User Modal ---
const showEditModal = ref(false);
const userToEdit = ref(null); // Store the whole user object being edited
const editForm = reactive({ // Reactive form data for the modal
  role: '',
  is_active: true
});
const editModalLoading = ref(false);
const editModalError = ref('');

// --- State for Delete User Confirmation ---
const showDeleteConfirmDialog = ref(false);
const userToDeleteId = ref(null);
const userToDeleteName = ref('');

// --- State for User Details Modal ---
const showDetailsModal = ref(false);
const userIdForDetails = ref(null); // <-- Add ref to store the ID being fetched
const selectedUserForDetails = ref(null); // Stores detailed user data (including profile)
const detailsLoading = ref(false);
const detailsError = ref('');

// --- State for Create User Modal ---
const showCreateModal = ref(false);
const createForm = reactive({ // Reactive form data for the create modal
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'user', // Default to user
  is_active: true // Default to active
});
const createModalLoading = ref(false);
const createModalError = ref('');

// --- Function to update URL query parameters ---
const updateUrlQuery = () => {
  const query = {};
  if (currentPage.value !== 1) query.page = currentPage.value;
  if (itemsPerPage.value !== 10) query.per_page = itemsPerPage.value;
  if (searchTerm.value) query.search = searchTerm.value;
  if (selectedRole.value) query.role = selectedRole.value;
  if (selectedStatus.value) query.status = selectedStatus.value;
  if (sortBy.value !== 'id') query.sort_by = sortBy.value; // Default sort is id
  if (sortOrder.value !== 'asc') query.sort_order = sortOrder.value;

  // Prevent pushing the same query repeatedly if state hasn't changed meaningfully
  if (JSON.stringify(query) !== JSON.stringify(route.query)) {
      router.push({ query, replace: true });
  }
};

// --- Functions for Edit User Modal ---
const openEditModal = (user) => {
  userToEdit.value = user; // Store the user object
  // Initialize form data based on the selected user
  editForm.role = user.role;
  editForm.is_active = user.is_active;
  editModalError.value = ''; // Clear previous errors
  showEditModal.value = true; // Show the modal
};

const closeEditModal = () => {
  showEditModal.value = false;
  userToEdit.value = null; // Clear the user object
};

const handleUserUpdate = async () => {
  if (!userToEdit.value) return;

  editModalLoading.value = true;
  editModalError.value = '';
  const token = userStore.state.token;
  const userId = userToEdit.value.id;

  // Prepare payload with only the fields being updated
  const payload = {
    role: editForm.role,
    is_active: editForm.is_active
  };

  try {
    const response = await api.put(`/admin/users/${userId}`, payload, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response && response.success) {
      closeEditModal();
      // No need to manually update the table row, fetchUsers refreshes everything
      await fetchUsers(); 
      // TODO: Show success message for update (can reuse existing mechanism)
      showSuccessMessage('用户信息更新成功！'); // Re-enabled success message
    } else {
      editModalError.value = (response && response.message) || '更新用户失败。';
    }
  } catch (err) {
    console.error(`更新用户 ${userId} 错误:`, err);
    if (err.response && err.response.data && err.response.data.message) {
      editModalError.value = `更新失败: ${err.response.data.message}`;
    } else if (err.response && err.response.status === 403) { // Forbidden
      editModalError.value = '更新失败: 权限不足 (例如，试图修改自己的角色/状态)。';
    } else {
      editModalError.value = '更新用户时发生网络错误或未知错误。';
    }
  } finally {
    editModalLoading.value = false;
  }
};

// --- Function to show success message (reuse if needed) ---
const showSuccessMessage = (message) => {
  successMessage.value = message;
  if (successTimeout) clearTimeout(successTimeout);
  successTimeout = setTimeout(() => {
    successMessage.value = '';
  }, 3000);
};

// --- Fetch Users (Main Logic) ---
const fetchUsers = async () => {
  loading.value = true;
  error.value = '';
  
  updateUrlQuery(); // Update URL based on current state

  const token = userStore.state.token;
  if (!token) {
    error.value = '用户未登录或令牌丢失。';
    loading.value = false;
    router.push('/login'); // Redirect to general login
    return;
  }

  // Construct query parameters from state
  const params = {
    page: currentPage.value,
    per_page: itemsPerPage.value,
    search: searchTerm.value,
    role: selectedRole.value,
    status: selectedStatus.value,
    sort_by: sortBy.value,
    sort_order: sortOrder.value,
  };

  try {
    const response = await api.get('/admin/users', {
      headers: { Authorization: `Bearer ${token}` },
      params
    });

    // Revised check: Handle both expected object and potential direct array
    let usersData = null;
    let paginationData = null;
    let success = false;
    let message = null;

    if (response && typeof response === 'object' && response !== null && response.hasOwnProperty('success')) {
        // Case 1: Response is the expected object { success: true, data: [...], ... }
        success = response.success;
        message = response.message; // Capture potential error message from backend
        if (success && Array.isArray(response.data)) {
            usersData = response.data;
            paginationData = response.pagination;
        } else if (!success) {
             console.error("获取用户列表失败 (后端返回 success:false):", response);
        } else {
             console.error("获取用户列表失败 (格式错误，缺少 data 数组):", response);
        }
    } else if (Array.isArray(response)) {
        // Case 2: Response is unexpectedly just the array [...] - Treat as success but log warning
        console.warn("API响应格式非预期，直接收到了用户数组，假设操作成功。");
        usersData = response;
        success = true; // Assume success if we got an array
    } else {
        // Case 3: Unexpected format
         console.error("获取用户列表失败 (API响应格式未知):", response);
    }

    // Process based on extracted data
    if (success && usersData !== null) {
      users.value = usersData;
      if (paginationData) {
        totalItems.value = paginationData.total_items;
        totalPages.value = paginationData.total_pages;
      } else {
        // Fallback if pagination info is missing (e.g., direct array case)
        totalItems.value = usersData.length;
        totalPages.value = 1; 
        currentPage.value = 1; // Reset to page 1 if no pagination info
      }
      error.value = '';
    } else {
      // Use the captured message or a default one
      error.value = message || '获取用户列表时返回数据格式不正确或操作未成功。';
      // Reset data
      users.value = [];
      totalItems.value = 0;
      totalPages.value = 1;
    }

  } catch (err) {
    console.error("获取用户列表错误:", err);
    if (err.response && err.response.status === 401) {
        error.value = '认证失败或令牌过期，请重新登录。';
        router.push('/login');
    } else if (err.response && err.response.data && err.response.data.message) {
         error.value = `获取用户列表失败: ${err.response.data.message}`;
    } else {
         error.value = '获取用户列表时发生网络错误或未知错误。';
    }
    users.value = [];
    totalItems.value = 0;
    totalPages.value = 1;
  } finally {
    loading.value = false;
  }
};

// Debounced fetch for search input
const debouncedFetchUsers = debounce(() => {
    currentPage.value = 1; // Reset page on search
    fetchUsers();
}, 500);

// --- Watchers for state changes ---
watch(searchTerm, () => {
  debouncedFetchUsers();
});

watch([selectedRole, selectedStatus, itemsPerPage], () => {
  currentPage.value = 1; // Reset page on filter/perPage change
  fetchUsers();
});

// --- Sorting Logic ---
const handleSort = (column) => {
  if (sortBy.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortBy.value = column;
    sortOrder.value = 'asc';
  }
  currentPage.value = 1;
  fetchUsers();
};

const getSortIcon = (column) => {
  if (sortBy.value !== column) return '↕'; 
  if (sortOrder.value === 'asc') return '▲';
  return '▼';
};

// --- Pagination Logic ---
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== currentPage.value) {
    currentPage.value = page;
    fetchUsers();
  }
};

// --- Clear Filters Logic ---
const clearFiltersAndSearch = () => {
  searchTerm.value = '';
  selectedRole.value = '';
  selectedStatus.value = '';
  currentPage.value = 1;
  // Optionally reset sort
  // sortBy.value = 'id';
  // sortOrder.value = 'asc';
  fetchUsers(); 
};

// --- Functions for Delete User Confirmation ---
const requestDeleteUser = (user) => {
  if (user) {
    userToDeleteId.value = user.id;
    userToDeleteName.value = user.username; // Use username for confirmation display
    showDeleteConfirmDialog.value = true;
  } else {
    console.error('User object is missing for delete request.');
  }
};

const cancelDeleteUser = () => {
  showDeleteConfirmDialog.value = false;
  userToDeleteId.value = null;
  userToDeleteName.value = '';
};

const confirmUserDelete = async () => {
  if (!userToDeleteId.value) return;

  const id = userToDeleteId.value;
  const currentUsername = userToDeleteName.value; // Keep username for success message
  cancelDeleteUser(); // Close dialog and clear state immediately
  loading.value = true; // Show loading indicator for the page
  error.value = '';

  const token = userStore.state.token;
  if (!token) {
      error.value = '认证令牌丢失，请重新登录。';
      loading.value = false;
      return;
  }

  try {
    const response = await api.delete(`/admin/users/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    if (response && response.success) {
        // Handle pagination if the deleted user was the last on the page
        if (users.value.length === 1 && currentPage.value > 1) {
            currentPage.value--; // Go to previous page before fetching
        }
        await fetchUsers(); // Refresh the list
        showSuccessMessage(`用户 "${currentUsername}" (ID: ${id}) 已成功删除！`);
    } else {
        error.value = (response && response.message) || '删除用户失败。';
    }
  } catch (err) {
      console.error(`删除用户 ${id} 错误:`, err);
      if (err.response && err.response.data && err.response.data.message) {
          error.value = `删除失败: ${err.response.data.message}`;
      } else if (err.response && err.response.status === 403) { // Forbidden
           error.value = '删除失败: 权限不足 (例如，试图删除自己)。';
      } else {
          error.value = '删除用户时发生网络错误或未知错误。';
      }
  } finally {
      loading.value = false;
  }
};

// --- Functions for User Details Modal ---
const fetchAndShowUserDetails = async (userId) => {
  userIdForDetails.value = userId; // <-- Store the ID when opening
  detailsLoading.value = true;
  detailsError.value = '';
  selectedUserForDetails.value = null; 
  showDetailsModal.value = true; 

  const token = userStore.state.token;
  if (!token) {
      detailsError.value = '认证令牌丢失，请重新登录。';
      detailsLoading.value = false;
      // Don't close modal here, let user see the error
      return;
  }

  try {
    const response = await api.get(`/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    // Revised check for details response
    if (response && typeof response === 'object' && response !== null && response.hasOwnProperty('success')) {
      // Case 1: Expected object { success: true, data: {...} }
      if (response.success && response.data) {
          selectedUserForDetails.value = response.data;
      } else {
          detailsError.value = (response && response.message) || '无法加载用户详情 (后端返回错误)。';
          console.error("获取用户详情失败 (后端返回 success:false 或缺少 data):", response);
      }
    } else {
        // Case 2: Unexpected format - Log error
        detailsError.value = '无法加载用户详情 (API 响应格式非预期)。';
        console.error("获取用户详情失败 (API 响应格式非预期):", response);
    }

  } catch (err) {
    console.error(`获取用户 ${userId} 详情错误:`, err);
     if (err.response && err.response.status === 404) {
         detailsError.value = '未找到该用户。';
     } else {
        detailsError.value = '加载用户详情时出错。';
     }
  } finally {
    detailsLoading.value = false;
  }
};

const closeDetailsModal = () => {
  showDetailsModal.value = false;
  userIdForDetails.value = null; // <-- Clear the ID when closing
};

// --- Utility function for displaying profile data safely ---
const displayProfileData = (data) => {
    return data !== null && data !== undefined ? data : '未提供';
};

// --- Functions for Create User Modal ---
const openCreateModal = () => {
  // Reset form fields
  createForm.username = '';
  createForm.email = '';
  createForm.password = '';
  createForm.confirmPassword = '';
  createForm.role = 'user';
  createForm.is_active = true;
  createModalError.value = ''; // Clear previous errors
  showCreateModal.value = true; // Show the modal
};

const closeCreateModal = () => {
  showCreateModal.value = false;
};

const handleUserCreate = async () => {
  createModalLoading.value = true;
  createModalError.value = '';

  // Frontend Validation
  if (!createForm.username || !createForm.password || !createForm.confirmPassword) {
      createModalError.value = '用户名、密码和确认密码是必填项。';
      createModalLoading.value = false;
      return;
  }
  if (createForm.password !== createForm.confirmPassword) {
      createModalError.value = '密码和确认密码不匹配。';
      createModalLoading.value = false;
      return;
  }
  // Basic email format check (can be more robust)
  if (createForm.email && !/.+@.+\..+/.test(createForm.email)) {
       createModalError.value = '请输入有效的邮箱格式。';
       createModalLoading.value = false;
       return;
  }

  const token = userStore.state.token;
  if (!token) {
    createModalError.value = '认证令牌丢失，请重新登录。';
    createModalLoading.value = false;
    return;
  }

  // Prepare payload
  const payload = {
    username: createForm.username,
    email: createForm.email || null, // Send null if empty
    password: createForm.password,
    role: createForm.role,
    is_active: createForm.is_active
  };

  try {
    const response = await api.post('/admin/users', payload, {
        headers: { Authorization: `Bearer ${token}` }
    });

    if (response && response.success) {
        closeCreateModal();
        await fetchUsers(); // Refresh the user list
        showSuccessMessage(`用户 "${payload.username}" 创建成功！`);
    } else {
        createModalError.value = (response && response.message) || '创建用户失败。';
    }
  } catch (err) {
    console.error('创建用户错误:', err);
    if (err.response && err.response.data && err.response.data.message) {
        createModalError.value = `创建失败: ${err.response.data.message}`;
    } else if (err.response && err.response.status === 409) { // Conflict
        createModalError.value = '创建失败: 用户名或邮箱已存在。';
    } else {
        createModalError.value = '创建用户时发生网络错误或未知错误。';
    }
  } finally {
    createModalLoading.value = false;
  }
};

// --- Call fetchUsers on Mount ---
onMounted(() => {
  console.log('Admin User Management Page Mounted. Fetching initial data...');
  fetchUsers(); // Fetch initial data based on URL/defaults
});

</script>

<style scoped>
/* Base Page Styles */
.user-management-page {
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

/* Top Actions */
.top-actions {
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
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #27ae60;
}

/* Controls Container */
.controls-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  flex-grow: 1;
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

.clear-button {
  padding: 8px 15px;
  border: 1px solid #bdc3c7;
  background-color: #ecf0f1;
  color: #7f8c8d;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s, color 0.3s;
}

.clear-button:hover {
  background-color: #dfe6e9;
  color: #34495e;
}

/* Loading and Error */
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

/* User Table */
.user-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
}

.user-table th {
  background-color: #3498db;
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
  white-space: nowrap;
}

.user-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  color: #333;
  font-size: 14px;
}

.user-table tr:last-child td {
  border-bottom: none;
}

.user-table tr:hover {
  background-color: #f8f9fa;
}

/* Sortable Headers */
.sortable-header {
  cursor: pointer;
  position: relative;
  padding-right: 20px; 
  user-select: none;
}

.sortable-header:hover {
  background-color: #2980b9;
}

.sort-icon {
  display: inline-block;
  margin-left: 5px;
  width: 1em; 
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}

.sortable-header:hover .sort-icon {
  color: white;
}

/* Status Indicator */
.status-active,
.status-inactive {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  display: inline-block;
  white-space: nowrap;
}

.status-active {
  background-color: #d4edda;
  color: #155724;
}

.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
}

/* Action Buttons */
.action-button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  margin-right: 5px;
  transition: background-color 0.3s;
  font-size: 13px;
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

/* No Data Message */
.no-data {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-size: 16px;
  border: 1px dashed #ccc;
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

/* Responsive adjustments */
@media (max-width: 992px) {
  .user-table {
    display: block;
    overflow-x: auto;
  }
}

@media (max-width: 768px) {
  .controls-container {
    flex-direction: column; 
    align-items: stretch; 
  }
  
  .search-input,
  .filter-select {
    width: 100%; 
  }

  .pagination-controls {
    flex-direction: column;
    gap: 10px;
  }
}

/* Edit User Modal */
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
  z-index: 1000; /* Ensure modals are on top */
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease-out; /* Reusing animation */
}

.edit-user-modal h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
  font-size: 20px;
}

.edit-user-modal p {
  margin-bottom: 15px;
  color: #34495e;
}

.edit-user-modal .form-group {
  margin-bottom: 20px;
}

.edit-user-modal .form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
}

.edit-user-modal .filter-select { /* Reuse filter select style */
  width: 100%;
  padding: 10px;
}

.edit-user-modal .modal-actions {
  margin-top: 25px;
}

.edit-user-modal .modal-error {
  margin-top: 15px;
  margin-bottom: 0;
}

.submit-button {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #2980b9;
}

.submit-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
  opacity: 0.7;
}

.cancel-button {
  background-color: #e74c3c;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #c0392b;
}

/* Delete User Confirmation Modal */
.delete-user-modal {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease-out; /* Reusing animation */
}

.delete-user-modal h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
  font-size: 20px;
}

.delete-user-modal p {
  margin-bottom: 15px;
  color: #34495e;
}

.delete-user-modal .modal-actions {
  margin-top: 25px;
}

.confirm-button {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.confirm-button:hover {
  background-color: #2980b9;
}

/* User Details Modal */
.details-modal {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease-out; /* Reusing animation */
}

.details-modal h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
  font-size: 22px;
}

.details-modal p {
  margin-bottom: 15px;
  color: #34495e;
}

.details-modal .modal-actions {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.close-button {
  background-color: #e74c3c;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.close-button:hover {
  background-color: #c0392b;
}

/* Details Button Style */
.details-button {
  background-color: #17a2b8; /* Teal color */
  color: white;
}

.details-button:hover {
  background-color: #138496;
}

/* User Details Modal Specific Styles */
.user-details-content {
  max-height: 60vh; /* Limit height and make scrollable */
  overflow-y: auto;
  padding-right: 10px; /* Space for scrollbar */
}

.detail-section {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.detail-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.detail-section h4 {
  color: #3498db;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
}

.detail-section p {
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}

.detail-section p strong {
  display: inline-block;
  width: 80px; /* Align keys */
  color: #555;
}

.details-modal .loading,
.details-modal .error-message {
  margin-top: 20px;
  margin-bottom: 20px;
}

/* Create User Modal */
.create-user-modal {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease-out; /* Reusing animation */
}

.create-user-modal h2 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
  font-size: 20px;
}

.create-user-modal .form-group {
  margin-bottom: 20px;
}

.create-user-modal .form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #34495e;
}

.create-user-modal .filter-select,
.create-user-modal input[type="text"],
.create-user-modal input[type="email"],
.create-user-modal input[type="password"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.create-user-modal .filter-select:focus,
.create-user-modal input:focus {
   border-color: #3498db;
   outline: none;
   box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.create-user-modal .required {
  color: #e74c3c;
  margin-left: 4px;
}

.create-user-modal .modal-actions {
  margin-top: 25px;
}

.create-user-modal .modal-error {
  margin-top: 15px;
  margin-bottom: 0;
}

.submit-button {
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #2980b9;
}

.submit-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
  opacity: 0.7;
}

.cancel-button {
  background-color: #e74c3c;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #c0392b;
}

</style> 