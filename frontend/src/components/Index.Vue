<template>
  <div class="Index">
  <SiteHeader></SiteHeader>
  <el-container style="border: 1px solid #eee;">
<!--     <el-aside width="200px" style="background-color: rgb(238, 241, 246); min-height: 90vh;">
      <el-menu :default-openeds="[]">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>主页</template>
          <el-menu-item-group>
            <el-menu-item index="1-1">
              <el-link href="http://localhost:8080/#/Search" target="_blank">搜索</el-link>
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title"><i class="el-icon-menu"></i>功能</template>
          <el-menu-item-group>
            <el-menu-item index="2-1">
              <el-link href="http://localhost:8080/#/Comment" :underline="false">评课</el-link>
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title"><i class="el-icon-setting"></i>
            <el-link href="http://localhost:8080/#/Login" target="_blank">登录</el-link>
          </template>
          <el-menu-item-group>
            <template slot="title">没有账号?</template>
            <el-menu-item index="3-1"><el-link href="http://localhost:8080/#/Register" target="_blank">注册</el-link></el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="登录选项">
            <el-menu-item index="3-2">管理员</el-menu-item>
            <el-menu-item index="3-3">用户</el-menu-item>
            <el-menu-item index="3-4">注销</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
      </el-menu>
    </el-aside> -->
    <Sidebar></Sidebar>
    <el-container>
      <el-header style="text-align: right; font-size: 12px;">
        <el-dropdown>
          <i class="el-icon-setting" style="margin-right: 15px; margin-top:20px;"></i>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>查看</el-dropdown-item>
            <el-dropdown-item>新增</el-dropdown-item>
            <el-dropdown-item>删除</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-header>

      <el-main>
        <el-button type="primary" @click="wrap();">神奇按钮</el-button>
      </el-main>
    </el-container>

  </el-container>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar'
import SiteHeader from '@/components/SiteHeader'
import axios from 'axios'

export default {
  components: {SiteHeader, Sidebar},
  data () {
    return {
      tableData: [
        {c_id: 'ph', c_name: 'ph', c_teacher: 'ph', c_classroom: 'ph', c_dept: 'ph'}
      ],
      user_id: 0
    }
  },
  methods: {
    async demo () {
      const that = this
      // const token = localStorage.getItem('access.mysite')
      axios.get('http://localhost:8000/api/users/', {
        params: {
          username: localStorage.getItem('username.mysite')
        }
      }).then((response) => {
        that.user_id = response.data.results[0].id
        console.log(that.user_id)
      }).catch((error) => {
        console.log(error.message)
      })
    },
    block () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.patch('http://localhost:8000/api/users/' + '11' + '/', {
        username: 'Fuck',
        in_blacklist: true
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((response) => {
        that.$notify({
          title: '作死按钮',
          message: '哈哈哈 成功封号',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'danger'
        })
      })
    },
    wrap () {
      setTimeout(this.block(), 2000) // async handling info
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 5px;
  }
</style>
