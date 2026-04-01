import { createRouter, createWebHistory } from 'vue-router'

function isSuper () {
  return localStorage.getItem('is_superuser') === '1'
}

function defaultHome () {
  const token = localStorage.getItem('token')
  if (!token) return '/'
  return isSuper() ? '/admin' : '/dashboard'
}

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../views/LandingView.vue'),
    meta: { public: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: { public: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
    meta: { public: true }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('../views/UserDashboardView.vue')
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('../views/AdminDashboardView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isPublic = to.meta && to.meta.public

  if (!token && !isPublic) {
    return next('/login')
  }

  if (token && to.path === '/') {
    return next(defaultHome())
  }

  if (token && (to.path === '/login' || to.path === '/register')) {
    return next(defaultHome())
  }

  if (token && isSuper() && to.path === '/dashboard') {
    return next('/admin')
  }

  if (to.path === '/admin' && localStorage.getItem('is_superuser') !== '1') {
    return next('/dashboard')
  }

  next()
})

export default router
