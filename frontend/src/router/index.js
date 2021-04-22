import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Fuck from '@/components/Fuck'
import Index from '@/components/Index'
import Search from '@/components/Search'
import Register from '@/components/Register'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
import Comment from '@/components/Comment'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index,
      meta: {
        title: '首页'
      }
    },
    {
      path: '/Search',
      name: 'Search',
      component: Search,
      meta: {
        title: '搜索'
      }
    },
    {
      path: '/Fuck',
      name: 'Fuck',
      component: Fuck
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register,
      meta: {
        title: '注册'
      }
    },
    {
      path: '/Login',
      name: 'Login',
      component: Login,
      meta: {
        title: '登录'
      }
    },
    {
      path: '/Logout',
      name: 'Logout',
      component: Logout,
      meta: {
        title: '注销'
      }
    },
    {
      path: '/Comment',
      name: 'Comment',
      component: Comment,
      meta: {
        title: 'qwq 萌萌的评论区~'
      }
    }
  ]
})
