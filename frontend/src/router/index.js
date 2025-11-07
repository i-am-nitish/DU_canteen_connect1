import { createRouter, createWebHistory } from 'vue-router'
import Account from '../views/Account.vue'
import Desktop1 from '@/views/Desktop 1.vue'
import Desktop6 from '../views/Desktop 6.vue'
import Desktop345 from '@/views/Desktop 3,4,5.vue'
import desktop8 from '@/views/Desktop 8.vue'
import desktop9 from '@/views/Desktop 9.vue'
import desktop10 from '@/views/Desktop 10.vue'
import desktop11 from '@/views/Desktop 11.vue'
import Desktop27 from '@/views/Desktop 27.vue'

const routes = [
  { path: '/', redirect: '/desktop1' },
  {path: '/desktop1', component: Desktop1},
  { path: '/desktop6', component: Desktop6 },
  { path: '/login', component: Desktop6 },
  { path: '/account', component: Account },
  { path: '/Desktop345', component: Desktop345},
  { path: '/signup', component: Desktop345},
  { path:'/desktop27', component: Desktop27},
  {path: '/desktop8', component: desktop8},
  {path: '/desktop9', component: desktop9},
  {path: '/desktop10', component: desktop10},
  { path: '/desktop11', component: desktop11}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
