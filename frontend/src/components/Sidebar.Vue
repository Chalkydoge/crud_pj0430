<template>
  <div>
    <el-aside width="200px" style="background-color: rgb(238, 241, 246);min-height: 90vh;">
      <el-menu :default-openeds="[]">
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-message"></i>主页</template>
          <el-menu-item-group>
            <el-menu-item index="1-1">
              <el-link href="/#/Search" :underline="false">搜索</el-link>
            </el-menu-item>
          </el-menu-item-group>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>功能</template>
            <el-menu-item-group>
              <el-menu-item index="2-1">
                <el-link href="/#/Comment/" :underline="false">评课</el-link>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title"><i class="el-icon-setting"></i>
              <el-link href="/#/Login" target="_blank">登录</el-link>
            </template>
          <el-menu-item-group>
            <template slot="title">没有账号?</template>
            <el-menu-item index="3-1">
              <el-link href="/#/Register" target="_blank">注册</el-link>
            </el-menu-item>
          </el-menu-item-group>
          <el-menu-item-group title="登录选项">
            <el-menu-item index="3-2">
              <el-link href="/#/Admin">管理员</el-link></el-menu-item>
            <el-menu-item index="3-3">用户</el-menu-item>
            <el-menu-item index="3-4">注销</el-menu-item>
          </el-menu-item-group>
        </el-submenu>
      </el-menu>
    </el-aside>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>
