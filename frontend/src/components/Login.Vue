<template>
  <div class="PasswordForm">
    <el-page-header @back="goBack" content="登录页面">
    </el-page-header>

    <el-container style="min-height: 90vh; border: 1px solid #eee; ">
      <el-main>
        <el-col :span="8" :offset="8" style="min-height: 36px; text-align: center;">
          <h1><i class="el-icon-s-promotion"></i>Login - 登录</h1>
        </el-col>
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" style="width: 500px; margin: 0 auto;">
          <el-form-item label="用户名" prop="user">
            <el-input type="text" v-model="ruleForm.user" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off" show-password></el-input>
          </el-form-item>
          <el-form-item label="验证码" prop="checkCode">
            <slide-verify :l="42" :r="10" :w="310" :h="155" slider-text="向右滑动"
            @success="onSuccess" @fail="onFail" @refresh="onRefresh"></slide-verify>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')" icon="el-icon-check">登录</el-button>
            <el-button @click="resetForm('ruleForm');show_info();" icon="el-icon-close">取消</el-button>
            <el-link href="/#/Register" type="primary" icon="el-icon-question" :underline="false">没有账号?快去注册</el-link>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data () {
    var checkUser = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('用户名不能为空'))
      }
      setTimeout(() => {
        callback()
      }, 1000)
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        callback()
      }
    }
    var validateCode = (rule, value, callback) => {
      if (value !== true) {
        callback(new Error('验证失败'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        user: '',
        pass: '',
        checkCode: false
      },
      rules: {
        user: [
          {validator: checkUser, trigger: 'blur'}
        ],
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkCode: [
          {validator: validateCode, trigger: 'blur'}
        ]
      },
      CheckMsg: ''
    }
  },
  methods: {
    goBack () {
      this.$router.push({name: 'Index'})
    },
    decodeError (msg) {
      let pat = /[0-9]{3}/
      let code = pat.exec(msg)[0]
      let res = ''
      switch (code) {
        case '401':
          res = '注意, 您还未认证! 请留意登陆情况或是输入密码/账号是否有误!'
          break
        case '403':
          res = '抱歉, 您没有权限操作!'
          break
        case '404':
          res = '抱歉, 找不到资源!'
          break
        case '500':
          res = '服务器发生错误!'
          break
        default:
          res = '未知错误'
      }
      return res
    },
    onSuccess () {
      this.CheckMsg = '成功'
      this.ruleForm.checkCode = true // 验证码通过
      this.$message({
        message: this.CheckMsg,
        type: 'success'
      })
    },
    onFail () {
      this.CheckMsg = '失败'
      this.$message({
        message: this.CheckMsg,
        type: 'error'
      })
    },
    onRefresh () {
      this.CheckMsg = '刷新中'
      this.$message({
        message: this.CheckMsg,
        type: 'info'
      })
    },
    signIn () {
      const that = this
      axios.post('http://localhost:8000/api/token/', {
        username: this.ruleForm.user,
        password: this.ruleForm.pass
      }).then(function (response) {
        const storage = localStorage
        console.log(response)
        // Date(...).getTime() 返回1970.01.01以来的毫秒数
        const expiredTime = (new Date()).getTime() + 300000
        console.log(expiredTime)
        // set the localStorage
        storage.setItem('access.mysite', response.data.access)
        storage.setItem('refresh.mysite', response.data.refresh)
        storage.setItem('expiredTime.mysite', expiredTime)
        storage.setItem('username.mysite', that.ruleForm.user)
        // notify message
        that.$notify({
          title: '登录成功',
          message: '欢迎' + that.ruleForm.user,
          type: 'success'
        })
        that.$router.push({name: 'Index'})
      }).catch(function (error) {
        that.$notify({
          title: '登陆失败',
          message: that.decodeError(error.message),
          type: 'error'
        })
        that.resetForm('ruleForm')
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.signIn()
        } else {
          console.log('Error submit!!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    show_info () {
      this.$notify({
        title: '成功重置',
        message: '',
        type: 'success'
      })
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
