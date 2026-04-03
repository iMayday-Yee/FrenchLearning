import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('@/views/Home.vue') },
  { path: '/register', component: () => import('@/views/Register.vue') },
  { path: '/bindwechat', component: () => import('@/views/BindWeChat.vue') },
  { path: '/agreement', component: () => import('@/views/Agreement.vue') },
  { path: '/register-done', component: () => import('@/views/RegisterDone.vue') },
  { path: '/login', component: () => import('@/views/Login.vue') },
  { path: '/chat', component: () => import('@/views/Chat.vue'), meta: { auth: true } },
  { path: '/assessment', component: () => import('@/views/Assessment.vue'), meta: { auth: true } },
  { path: '/result', component: () => import('@/views/Result.vue'), meta: { auth: true } },
  { path: '/waiting', component: () => import('@/views/Waiting.vue'), meta: { auth: true } },
  { path: '/completed', component: () => import('@/views/Completed.vue'), meta: { auth: true } },
  { path: '/ended', component: () => import('@/views/Ended.vue') },
  { path: '/admin', component: () => import('@/views/admin/AdminLogin.vue') },
  { path: '/admin/dashboard', component: () => import('@/views/admin/Dashboard.vue'), meta: { admin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from) => {
  const userStore = await import('@/stores/user')
  const store = userStore.useUserStore()

  if (to.meta.auth && !store.token) {
    return '/login'
  }

  if (to.meta.admin && !localStorage.getItem('admin_token')) {
    return '/admin'
  }

  // 注册页面检查：如果是第11天起，不允许注册
  if (to.path === '/register') {
    try {
      const res = await fetch('/api/study/can_register')
      const data = await res.json()
      if (!data.can_register) {
        return '/ended'
      }
    } catch (e) {
      // ignore, allow registration attempt
    }
  }

  if (to.path === '/chat') {
    const studyStore = (await import('@/stores/study')).useStudyStore()
    await studyStore.fetchStatus()
    if (studyStore.phase === 'not_started') return '/waiting'
    if (studyStore.phase === 'completed') return '/ended'
  }
})

export default router
