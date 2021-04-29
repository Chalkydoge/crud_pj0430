<template>
  <div>
    <SiteHeader></SiteHeader>
    <Pwd></Pwd>
  </div>
</template>

<script>
import SiteHeader from '@/components/SiteHeader'
import Pwd from '@/components/PassWord'

export default {
  name: 'Register',
  components: {SiteHeader, Pwd},
  data: function () {
    return {
      message: '登录',
      msg: 'xxx'
    }
  }
}
</script>
