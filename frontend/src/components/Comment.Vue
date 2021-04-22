<template>
  <div class="Comment">
    <SiteHeader></SiteHeader>
    <div v-if="this.not_login == false">
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
                <el-menu-item index="2-1">评课</el-menu-item>
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
          <el-header style="text-align: left; font-size: 25px;">
            查看课评
            <br>
            想要写评论? <el-button type="info" icon="el-icon-edit" @click="addComments()">新建</el-button>
          </el-header>

          <el-main style="text-align: left">
            <el-row>
              <el-col :span=2>
                没有找到评论?
              </el-col>
              <el-col :span=8>
                <el-input placeholder="找找看!" v-model="searchText" clearable prefix-icon="el-icon-search"></el-input>
              </el-col>
              <el-col :span=2>
                <el-button type="primary" icon="el-icon-search" :loading="true">搜索</el-button>
              </el-col>
            </el-row>

            <el-row>
              borderline
            </el-row>

            <el-row>
              评论区
            </el-row>

            <el-table
            :data="comments"
            border
            style="width: 100%">
              <el-table-column
                fixed
                prop="p_cid"
                label="课程号"
                width="150">
              </el-table-column>
              <el-table-column
                prop="p_rate"
                label="评分"
                width="120">
              </el-table-column>
              <el-table-column
                prop="p_comment"
                label="评价内容"
                width="120">
              </el-table-column>
              <el-table-column
                prop="p_owner"
                label="用户"
                width="120">
              </el-table-column>
              <el-table-column
                label="操作"
                width="240">
                <template slot-scope="scope">
                  <el-button @click="handleClick(scope.row)" type="primary" size="small">查看</el-button>
                  <el-button @click="handleClick(scope.row)" type="warning" size="small">编辑</el-button>
                  <el-button @click="handleClick(scope.row)" type="danger" size="small">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-main>
        </el-container>
      </el-container>

      <el-dialog title="写评论" :visible.sync="dialogFormVisible">
        <el-form :model="CommentForm">
          <el-form-item label="课程号" :label-width="formLabelWidth">
            <el-input v-model="CommentForm.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="评分" :label-width="formLabelWidth">
            <el-select v-model="CommentForm.rate" placeholder="请选择活动区域">
              <el-option label="区域一" value="shanghai"></el-option>
              <el-option label="区域二" value="beijing"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="评论内容" :label-width="formLabelWidth">
            <el-input type="textarea" :rows="2"
            v-model="CommentForm.text"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible=false; resetForm();">取 消</el-button>
          <el-button type="primary" @click="addComments();dialogFormVisible=false">确 定</el-button>
        </div>
      </el-dialog>

    </div>
    <div v-else>
      <p>Not Logged in! 请登录以查看内容!!</p>
    </div>
  </div>
</template>

<script>
import SiteHeader from '@/components/SiteHeader'
import axios from 'axios'

export default {
  name: 'Comment',
  components: {SiteHeader},
  data () {
    return {
      count: 0,
      comments: [], // storing comments,
      not_login: false,
      searchText: '',
      CommentForm: {
        name: '',
        rate: '',
        text: ''
      },
      dialogFormVisible: false,
      formLabelWidth: '120px'
    }
  },
  methods: {
    showComments () {
      // TODO fetch data from backend
      const that = this
      axios.get('http://localhost:8000/api/comments/').then(function (response) {
        that.comments = response.data.results
      }).catch(function (error) {
        alert(error.message)
      })
    },
    addComments () {
      const that = this
      axios.post('/api/comments/', {
        p_cid: that.CommentForm.name,
        p_rate: that.CommentForm.rate,
        p_owner: localStorage.getItem('username.mysite')
      }).then(function (response) {
        // handling responses from backend
        console.log(response)
        // 成功发布, 则弹出通知
        that.$notify({
          title: '发表成功',
          message: '您已成功发布评论,快去看看吧~',
          type: 'success'
        })

      }).catch(error) {
        // alert(error.message)
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'warning'
        })
      }
    },
    getUserInfo () {
      const that = this
      const storage = localStorage
      that.not_login = (storage.getItem('username.mysite') === null)
      console.log(that.not_login)
    },
    handleClick (row) {
      console.log(row)
    },
    resetForm () {
      this.$notify({
        title: '撤销成功',
        message: '还没想好怎么写嘛wow 没事~',
        type: 'success'
      })
    }
  },
  created: function () {
    this.getUserInfo()
    this.showComments()
  }
}
</script>

<style type="text/css">
.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 480px;
}

</style>
