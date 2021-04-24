<template>
  <div>
    <SiteHeader></SiteHeader>
    <el-container style="border: 1px solid #eee;">
      <Sidebar></Sidebar>
    </el-container>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar'
import SiteHeader from '@/components/SiteHeader'

export default {
  name: 'Admin',
  components: {Sidebar, SiteHeader}
}
</script>
