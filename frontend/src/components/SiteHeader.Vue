<template>
  <div class="demo-header">
  <el-row>
    <el-col :span="4" class="grid-content bg-normal">
      <div v-if="hasLogin">
        Welcome, {{username}}
      </div>
      <div v-else>
        RMA70-12!!!
      </div>
    </el-col>
    <el-col :span="12" class="grid-content bg-success">
    </el-col>
    <el-col :span="8" class="el-menu-demo">
      <el-menu
        mode="horizontal"
        background-color="#F2F6FC"
        text-color="#303133"
        active-text-color="#67C23A">

        <el-submenu index="1">
          <template slot="title">我的工作台</template>
          <el-menu-item index="1-1">新增</el-menu-item>

          <el-submenu index="1-2">
            <template slot="title">修改</template>
            <el-menu-item index="1-2-1">修改信息</el-menu-item>
            <el-menu-item index="1-2-1">删除信息</el-menu-item>
          </el-submenu>
        </el-submenu>

        <el-submenu index="2">
            <template slot="title">评价</template>
            <el-menu-item index="2-1">写评论</el-menu-item>
            <el-menu-item index="2-2">进入讨论区</el-menu-item>
        </el-submenu>

        <el-submenu index="3">
          <template slot="title">消息中心</template>
          <el-menu-item index="3-1">消息</el-menu-item>
          <el-menu-item index="3-2">评论</el-menu-item>
        </el-submenu>

        <el-submenu index="4">
          <template slot="title">登陆选项</template>
            <el-menu-item index="4-1">
              <div v-if="hasLogin">
                <el-button type="text" @click="logOut" style="margin: 0 auto;">注销</el-button>
              </div>
              <div v-else>
                <el-button type="text" @click="logIn" style="margin: 0 auto;">登录</el-button>
              </div>
            </el-menu-item>
        </el-submenu>

      </el-menu>
    </el-col>
  </el-row>

  </div>
</template>

<script>
// import axios from 'axios'
import authorization from '@/api/authorization'
export default {
  name: 'SiteHeader',
  data () {
    return {
      hasLogin: false,
      username: ''
    }
  },
  mounted () {
    authorization().then((data) => {
      [this.hasLogin, this.username] = data
    })
  },
  methods: {
    logOut () {
      const that = this
      that.hasLogin = false
      const storage = localStorage
      storage.clear()
      that.$router.push({name: 'Index'})
    },
    logIn () {
      const that = this
      that.$router.push({name: 'Login'})
    }
  }
}
</script>

<style scoped>
  .el-col {
    border-radius: 4px;
  }
  .bg-normal {
    background: #F2F6FC;
  }
  .bg-success {
    background: #F2F6FC;
  }
  .grid-content {
    border-radius: 0px;
    min-height: 60px;
    text-align: left;
    font-weight: bold;
    font-size: 18px;
  }
  .el-row {
    margin-bottom: 0px;
    &:last-child {
      margin-bottom: 0;
    }
  }
</style>
