import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import OnboardingPage from '../views/OnboardingPage.vue'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import ActivityLevelPage from '../views/ActivityLevelPage.vue'
import UserInfoPage from '../views/UserInfoPage.vue'
import AuthPage from '../views/AuthPage.vue'
import DashboardPage from '../views/DashboardPage.vue'
import RecordsPage from '../views/RecordsPage.vue'
import ReportsPage from '../views/ReportsPage.vue'
import ProfilePage from '../views/ProfilePage.vue'
import HomePage from '../views/HomePage.vue'
import AvatarTest from '../components/AvatarTest.vue'
import useUserStore from '../stores/userStore'
import adminGuard from './adminGuard'

// 导入管理员页面组件
import AdminLoginPage from '../views/admin/AdminLoginPage.vue'
import AdminDashboardPage from '../views/admin/AdminDashboardPage.vue'
import AdminFoodManagementPage from '../views/admin/AdminFoodManagementPage.vue'
import AdminLayout from '../views/admin/AdminLayout.vue'

// 创建userStore实例
const userStore = useUserStore()

// --- 管理员导航守卫 ---
const requireAdminAuth = (to, from, next) => {
  // 从 userStore 获取认证状态和用户角色
  const isAuthenticated = userStore.state.isAuthenticated;
  const userRole = userStore.state.userData?.role; 

  console.log('Admin Guard - isAuthenticated:', isAuthenticated, 'Role:', userRole); // 添加日志

  if (isAuthenticated && userRole === 'admin') {
    // 已登录且是管理员
    console.log('Admin Guard - Access granted.');
    next(); // 允许访问
  } else {
    // 未登录或不是管理员，重定向到普通登录页（或首页）
    console.log('Admin Guard - Access denied. Redirecting to Login.');
    // 重定向到普通登录页，因为不再需要单独的管理员登录
    // 如果已经登录但不是管理员，也可以考虑重定向到用户仪表盘或首页
    next({ name: 'Login', query: { redirect: to.fullPath } }); 
  }
};

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/onboarding',
    name: 'Onboarding',
    component: OnboardingPage
  },
  {
    path: '/activity-level',
    name: 'ActivityLevel',
    component: ActivityLevelPage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage
  },
  {
    path: '/user-info',
    name: 'UserInfo',
    component: UserInfoPage
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthPage
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/records',
    name: 'Records',
    component: RecordsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: ReportsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/recommendations',
    redirect: '/reports',
    meta: { requiresAuth: true }
  },
  {
    path: '/avatar-test',
    name: 'AvatarTest',
    component: AvatarTest,
    meta: { requiresAuth: true }
  },

  // --- 管理员登录路由 (保持独立) ---  // 注释掉或移除，因为不再需要单独登录
  /*
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLoginPage,
    beforeEnter: (to, from, next) => {
      // 检查 userStore 而不是 admin_token
      if (userStore.state.isAuthenticated && userStore.state.userData?.role === 'admin') {
        next({ name: 'AdminDashboard' }); // Redirect to dashboard if already logged in as admin
      } else {
        next(); // Allow access to login page otherwise
      }
    }
  },
  */

  // --- 管理员主路由 (使用 AdminLayout) ---
  {
    path: '/admin', // Parent route for admin section
    component: AdminLayout, // Use the new layout
    redirect: '/admin/dashboard', // Redirect /admin to /admin/dashboard
    meta: { requiresAdmin: true }, // <-- ADD metadata to identify admin routes
    children: [
      {
        path: 'dashboard', // Becomes /admin/dashboard
        name: 'AdminDashboard',
        component: AdminDashboardPage
      },
      {
        path: 'food-items', // Becomes /admin/food-items
        name: 'AdminFoodManagement',
        component: AdminFoodManagementPage
      },
      {
        path: 'users', // Becomes /admin/users
        name: 'AdminUserManagement',
        // Use lazy loading for potentially large pages
        component: () => import('../views/admin/AdminUserManagementPage.vue')
      },
      {
        path: 'user-reports', // Becomes /admin/user-reports
        name: 'AdminUserReports',
        component: () => import('../views/admin/UserReportsPage.vue') // Use lazy loading
      },
      {
        path: 'user-report/:userId', // 动态路由，匹配用户ID
        name: 'UserReport', // 与 UserReportsPage.vue 中使用的名称匹配
        component: () => import('../views/admin/UserReportDetailPage.vue'), // 指向新的详情页组件
        props: true // 允许将路由参数作为 props 传递给组件
      },
      {
        path: 'advice', // 路径变为 /admin/advice
        name: 'AdminAdviceManagement',
        component: () => import('../views/admin/AdviceManagementPage.vue') // 指向新的管理页面组件
      }
      // --- 未来可以添加更多子路由 ---
      // {
      //   path: 'users',
      //   name: 'AdminUserManagement',
      //   component: () => import('../views/admin/AdminUserManagementPage.vue')
      // },
      // {
      //   path: 'suggestions',
      //   name: 'AdminSuggestionManagement',
      //   component: () => import('../views/admin/AdminSuggestionManagementPage.vue')
      // }
    ]
  }
  // --- 移除或注释掉旧的/冲突的 /admin 路由配置 ---
  /*
   {
     path: '/admin/dashboard',
     name: 'AdminDashboard_Old', // Renamed to avoid conflict during refactor
     component: AdminDashboardPage,
     beforeEnter: requireAdminAuth
   },
   {
     path: '/admin/food-items',
     name: 'AdminFoodManagement_Old', // Renamed to avoid conflict
     component: AdminFoodManagementPage,
     beforeEnter: requireAdminAuth
   },
   */
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- 全局前置守卫 (处理所有认证) ---
router.beforeEach((to, from, next) => {
  const isAuthenticated = userStore.state.isAuthenticated;
  const userRole = userStore.state.userData?.role;
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin); // Check for admin meta

  console.log('Global Guard - Path:', to.path, 'RequiresAuth:', requiresAuth, 'RequiresAdmin:', requiresAdmin, 'IsAuth:', isAuthenticated, 'Role:', userRole);

  if (requiresAdmin) {
    // --- Admin Route Check ---
    if (isAuthenticated && userRole === 'admin') {
      console.log('Global Guard - Admin access granted.');
      next(); // Allow access
    } else {
      console.log('Global Guard - Admin access denied. Redirecting to Login.');
      // Redirect non-admins or unauthenticated users trying to access admin pages
      next({ name: 'Login', query: { redirect: to.fullPath } });
    }
  } else if (requiresAuth) {
    // --- Regular Authenticated Route Check ---
    if (isAuthenticated) {
      console.log('Global Guard - Regular authenticated access granted.');
      next(); // Allow access
    } else {
      console.log('Global Guard - Regular requires auth but not authenticated. Redirecting to Login.');
      next({ name: 'Login', query: { redirect: to.fullPath } });
    }
  } else if (to.name === 'Login' && isAuthenticated) {
      // --- Prevent logged-in users from accessing Login page ---
      // Redirect based on role
      if (userRole === 'admin') {
          console.log('Global Guard - Admin already logged in, redirecting to Admin Dashboard.');
          next({ name: 'AdminDashboard' });
      } else {
          console.log('Global Guard - User already logged in, redirecting to User Dashboard.');
          next({ name: 'Dashboard' });
      }
  } else {
    // --- Public Route or other cases ---
    console.log('Global Guard - Public route or unhandled case.');
    next(); // Allow access to public routes
  }
})

export default router 