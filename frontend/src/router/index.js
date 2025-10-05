import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Account from '../views/Account.vue'
import Signup from '@/views/Signup.vue'
import CreateProfile from '@/views/CreateProfile.vue'
import CanteenPage from '@/views/CanteenPage.vue'
import CanteenDetail from '@/views/CanteenDetail.vue'
import CreateCanteenProfile from '@/views/CreateCanteenProfile.vue'
import Home from '@/views/Home.vue'

const routes = [
  { path: '/', redirect: '/home' },
  {path: '/home', component: Home},
  { path: '/login', component: Login },
  { path: '/account', component: Account },
  { path: '/signup', component: Signup},
  { path:'/signup/profile', component: CreateProfile},
  { path:'/canteenpage', component: CanteenPage},
  { path:'/canteen/:id', component: CanteenDetail, props: true},
  { path: '/signup/canteenprofile', component: CreateCanteenProfile}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
