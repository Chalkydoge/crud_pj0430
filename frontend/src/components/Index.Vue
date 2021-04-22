<template>
  <div class="Index">
  <SiteHeader></SiteHeader>
  <el-container style="border: 1px solid #eee">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
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
    </el-aside>

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
        <el-table :data="tableData">
          <el-table-column prop="c_id" label="课程号" width="140">
          </el-table-column>
          <el-table-column prop="c_name" label="课程名称" width="200">
          </el-table-column>
          <el-table-column prop="c_teacher" label="授课教师" width="140">
          </el-table-column>
          <el-table-column prop="c_classroom" label="上课地点" width="140">
          </el-table-column>
          <el-table-column prop="c_dept" label="开课院系" width="140">
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>

  </el-container>
  </div>
</template>

<script>
import {showCourses} from '../api/api.js'
import SiteHeader from '@/components/SiteHeader'

export default {
  components: {SiteHeader},
  data () {
    return {
      tableData: [
        {c_id: 'ph', c_name: 'ph', c_teacher: 'ph', c_classroom: 'ph', c_dept: 'ph'}
      ]
    }
  },
  methods: {
    showC () {
      showCourses().then(response => {
        this.tableData = response.data.results
      })
    }
  },
  created: function () {
    this.showC()
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
