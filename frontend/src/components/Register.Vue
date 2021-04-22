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
      true_god: '42姐',
      message: '登录',
      msg: 'xxx'
    }
  },
  created: {
    showTitle: function () {
      this.SiteHeader.msg = 'xxx'
    }
  }
}
</script>
