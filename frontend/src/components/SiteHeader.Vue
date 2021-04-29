<template>
  <div class="demo-header">
  <el-row>
    <el-col :span="4" class="grid-content bg-normal">
      <div v-if="hasLogin">
        Welcome, {{username}}
      </div>
      <div v-else>
        <i class="el-icon-message"></i>TinyXK 简易课评系统
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
            <template slot="title">评价</template>
            <el-menu-item index="1-1">
              <el-link type="text" href="/#/Comment">
              写评论</el-link></el-menu-item>
            <el-menu-item index="1-2">
              <el-link type="text" href="/#/Comment">
              进入讨论区</el-link></el-menu-item>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title">消息中心</template>
            <el-menu-item index="2-1">
              <div v-if="messageCount > 0">
                <el-badge :value="messageCount">
                  <el-popover
                    placement="top-start"
                    title="消息"
                    width="200"
                    trigger="hover">
                    <div v-if="isAdmin">
                      <div v-for="item in badComment" :key="item.username">
                        {{ '用户' + item.b_username + '存在违禁行为!'}}
                      </div>
                    </div>
                    <div v-else>
                      <p>{{ msg }}</p>
                    </div>
                    <el-button slot="reference" type="text">消息</el-button>
                  </el-popover>
                </el-badge>
              </div>
              <div v-else>
                <el-button type="text">消息</el-button>
              </div>
            </el-menu-item>
        </el-submenu>

        <el-submenu index="3">
          <template slot="title">登录选项</template>
            <el-menu-item index="3-1">
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
import axios from 'axios'
import authorization from '@/api/authorization'

export default {
  name: 'SiteHeader',
  inject: ['reload'],
  data () {
    return {
      formLabelWidth: '120px',
      hasLogin: false,
      username: '',
      userid: 0,
      messageCount: 0,
      badComment: [],
      msg: '暂时没有消息哦',
      isAdmin: false
    }
  },
  mounted () {
    const that = this
    authorization().then((data) => {
      [that.hasLogin, that.username] = data
    }).then(() => {
      console.log(that.username)
      if (that.username) {
        axios.get('http://localhost:8000/api/users/', {
          params: {
            username: that.username
          }
        }).then((response) => {
          let curUser = response.data.results[0] // only one assumed
          that.userid = curUser.id
          if (curUser.is_superuser) {
            // 是管理员
            const token = localStorage.getItem('access.mysite')
            axios.get('http://localhost:8000/api/bad_comment/', {
              params: {
                b_username: that.username,
                option: 'check'
              },
              headers: {Authorization: 'Bearer ' + token}
            }).then((response) => {
              that.badComment = response.data.results
              that.isAdmin = true
              that.messageCount = that.badComment.length
            })
          } else {
            // 普通用户
            const token = localStorage.getItem('access.mysite')
            axios.get('http://localhost:8000/api/bad_comment/', {
              params: {
                b_username: that.username
              },
              headers: {Authorization: 'Bearer ' + token}
            }).then((response) => {
              that.badComment = response.data.results
              that.isAdmin = false
              if (that.badComment.length > 0 &&
                that.badComment[0].b_count >= 5) {
                that.messageCount = 1
                that.msg = '请注意发表的言论信息🔥'
              }
            })
          }
        })
      }
    })
  },
  methods: {
    func () {
      this.MessageFormVisible = true
      this.messageCount += 1
    },
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
  .item {
    margin-top: 10px;
    margin-right: 40px;
  }
</style>
