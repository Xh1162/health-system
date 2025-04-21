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

// 创建userStore实例
const userStore = useUserStore()

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
  // 管理员路由
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    beforeEnter: adminGuard,
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('../views/admin/Dashboard.vue')
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('../views/admin/UserManagement.vue')
      },
      {
        path: 'announcements',
        name: 'AnnouncementManagement',
        component: () => import('../views/admin/Dashboard.vue') // 暂时使用仪表盘作为占位符
      },
      {
        path: 'logs',
        name: 'SystemLogs',
        component: () => import('../views/admin/Dashboard.vue') // 暂时使用仪表盘作为占位符
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // 检查userStore是否正确初始化
  if (!userStore || !userStore.state) {
    console.warn('userStore未正确初始化，跳过认证检查')
    next()
    return
  }
  
  const isAuthenticated = userStore.state.isAuthenticated
  
  // 添加调试信息
  console.log('路由守卫 - 目标路由:', to.path)
  console.log('路由守卫 - 认证状态:', isAuthenticated)
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要认证但未登录，重定向到登录页
    console.log('需要认证但未登录，重定向到登录页')
    next({ name: 'Login', query: { redirect: to.fullPath }})
  } else if (to.name === 'Login' && isAuthenticated) {
    // 已登录用户访问登录页，重定向到首页
    console.log('已登录用户访问登录页，重定向到首页')
    next({ name: 'Dashboard' })
  } else {
    console.log('正常导航到:', to.path)
    next()
  }
})

export default router 