<template>
  <div class="Fuck">
  <el-container style="height: 100%; border: 1px solid #eee">
    <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
      <el-menu :default-openeds="['2']">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>主页</template>
          <el-menu-item-group>
            <template slot="title">选课信息</template>
            <el-menu-item index="1-1"></el-menu-item>
            <el-menu-item index="1-2">狂暴蹲饼组长</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title"><i class="el-icon-menu"></i>功能</template>
          <el-menu-item-group>
            <el-submenu index="2-1">
              <template slot="title">添加信息</template>
              <el-menu-item index="2-1-1">???</el-menu-item>
              <el-menu-item index="2-1-2">xxx</el-menu-item>
            </el-submenu>
          </el-menu-item-group>
          <el-menu-item-group>
            <el-submenu index="2-2">
              <template slot="title"></template>
              <el-menu-item index="2-2-1">修改干员</el-menu-item>
              <el-menu-item index="2-2-2">修改组织</el-menu-item>
            </el-submenu>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title"><i class="el-icon-setting"></i>登录</template>
          <el-menu-item-group>
            <template slot="title">没有账号?</template>
            <el-menu-item index="3-1">注册</el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="登录选项">
            <el-menu-item index="3-2">管理员登录</el-menu-item>
            <el-menu-item index="3-3">用户登录</el-menu-item>
          </el-menu-item-group>
          <el-submenu index="注销账号">
            <template slot="title">注销选项</template>
            <el-menu-item index="3-4">注销</el-menu-item>
          </el-submenu>
        </el-submenu>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-dropdown>
          <i class="el-icon-setting" style="margin-right: 15px"></i>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>查看</el-dropdown-item>
            <el-dropdown-item>新增</el-dropdown-item>
            <el-dropdown-item>删除</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <span>Admin</span>
      </el-header>

      <el-main>
        <el-table :data="orgs">
          <el-table-column prop="org_id" label="ID" width="140">
          </el-table-column>
          <el-table-column prop="org_name" label="组织名" width="120">
          </el-table-column>
          <el-table-column prop="org_desc" label="介绍">
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
  </div>
</template>

<script>
export default {
  data () {
    const item = {
      date: '2016-05-02',
      name: '王小虎',
      address: '上海市普陀区金沙江路 1518 弄'
    }
    return {
      tableData: Array(15).fill(item)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }

  .el-aside {
    color: #333;
  }
</style>
