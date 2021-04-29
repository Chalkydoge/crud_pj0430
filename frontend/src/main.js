// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import axios from 'axios'
import SlideVerify from 'vue-monoplasty-slide-verify'

Vue.config.productionTip = false

Vue.use(ElementUI)

Vue.use(SlideVerify)

Vue.prototype.$axios = axios

axios.defaults.headers.post['Content-Type'] = 'application/json'

/* eslint-disable no-new */
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
