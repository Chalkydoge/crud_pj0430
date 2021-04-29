<template>
  <div>
    <el-aside width="200px" style="background-color: rgb(238, 241, 246); min-height: 90vh;">
      <el-menu :default-openeds="['2']">
        <el-menu-item index="1">
          <template slot="title"><i class="el-icon-house"></i><el-link href="/#/" :underline="false">主页</el-link></template>
          </el-menu-item>

          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>功能</template>
            <el-menu-item-group>
              <template slot="title">主要功能</template>
              <el-menu-item index="2-1">
                <el-link href="/#/Search" :underline="false">
                  <i class="el-icon-view"></i>搜索</el-link>
              </el-menu-item>
              <el-menu-item index="2-2">
                <el-link href="/#/Comment/" :underline="false">
                  <i class="el-icon-chat-square"></i>评课</el-link>
              </el-menu-item>
            </el-menu-item-group>
          </el-submenu>

          <el-submenu index="3">
            <template slot="title"><i class="el-icon-user"></i>
              <el-link href="/#/Login" target="_blank">登录</el-link>
            </template>
          <el-menu-item-group>
            <template slot="title">没有账号?</template>
            <el-menu-item index="3-1">
              <el-link href="/#/Register" target="_blank">注册</el-link>
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-menu-item index="4">
          <template slot="title"><i class="el-icon-star-on"></i>
            <el-link href="/#/Admin">管理</el-link>
          </template>
        </el-menu-item>
      </el-menu>
    </el-aside>
  </div>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>
