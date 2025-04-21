import useUserStore from '../stores/userStore'

export default function adminGuard(to, from, next) {
  const userStore = useUserStore()
  
  if (!userStore || !userStore.state) {
    console.warn('userStore未正确初始化，跳过管理员权限检查')
    next('/login?redirect=' + to.path)
    return
  }
  
  // 检查是否已登录且是管理员
  const isAdmin = userStore.state.isAuthenticated && 
                 userStore.state.userData?.role === 'admin'
  
  console.log('管理员路由守卫 - 目标路由:', to.path)
  console.log('管理员路由守卫 - 是否管理员:', isAdmin)
  
  if (isAdmin) {
    next()
  } else {
    console.log('需要管理员权限，重定向到登录页')
    next('/login?redirect=' + to.path + '&message=需要管理员权限')
  }
} 