import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import Dashboard from '@/views/Dashboard.vue'
import TipPage from '@/views/TipPage.vue'

import { mapGetters } from 'vuex'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      beforeEnter(to, from, next){
        if(!mapGetters('auth', ['isAuthenticated'])){
          next('/')
        } else {
          next()
        }
      }
    },
    {
      path: '/tip/:username',
      name: 'tip',
      props: true,
      component: TipPage
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue')
    }
  ]
})

export default router
