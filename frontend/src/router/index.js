import { createRouter, createWebHistory } from 'vue-router'
import shop from '../views/ShopView.vue'
import profile from '../views/ProfileView.vue'
import auth from '../views/CommonForm.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: shop
    },
    {
      path: '/shop',
      name: 'shop',
      component: shop
    },
    {
      path: '/profile',
      name: 'profile',
      component: profile
    },
    {
      path: '/auth',
      name: 'auth',
      component: auth
    },
  ]
})

export default router
