<template>
  <div class="PasswordForm">
    <el-row>
      <el-col :span="8" class="grid-content bg-normal">
      </el-col>
      <el-col :span="8" class="grid-content bg-success">
      </el-col>
      <el-col :span="8" class="el-menu-demo">
        <el-menu
          :default-active="activeIndex2"
          mode="horizontal"
          @select="handleSelect"
          background-color="#F2F6FC"
          text-color="#303133"
          active-text-color="#ffd04b">
          <el-submenu index="1">
            <template slot="title">我的工作台</template>
            <el-menu-item index="1-1">选项1</el-menu-item>
            <el-menu-item index="1-2">选项2</el-menu-item>
            <el-menu-item index="1-3">选项3</el-menu-item>
            <el-submenu index="1-4">
              <template slot="title">选项4</template>
              <el-menu-item index="1-4-1">选项1</el-menu-item>
              <el-menu-item index="1-4-2">选项2</el-menu-item>
              <el-menu-item index="1-4-3">选项3</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-menu-item index="2" disabled>消息中心</el-menu-item>
          <el-menu-item index="3"><a href="https://www.ele.me" target="_blank">订单管理</a></el-menu-item>
          <el-menu-item index="4">登录</el-menu-item>
        </el-menu>
      </el-col>
    </el-row>

    <el-container style="height: 500px; border: 1px solid #eee;">
      <el-main>
        <el-col :span="8" :offset="8" style="min-height: 36px; text-align: center;">
          <h1>Login 登录</h1>
        </el-col>
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" style="width: 500px; margin: 0 auto;">
          <el-form-item label="用户名" prop="user">
            <el-input type="text" v-model="ruleForm.user" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass">
            <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')" icon="el-icon-check">登录</el-button>
            <el-button @click="resetForm('ruleForm');show_info();" icon="el-icon-close">取消</el-button>
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
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass')
        }
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请在此输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次密码输入不一致'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        user: '',
        pass: '',
        checkPass: ''
      },
      rules: {
        user: [
          {validator: checkUser, trigger: 'blur'}
        ],
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass2, trigger: 'blur'}
        ]
      },
      activeIndex2: '1',
      activeIndex: '1'
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
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
        //
        that.$router.push({name: 'Index'})
      }).catch(function (error) {
        alert(error.message)
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // do something here!!!
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
        message: '这是一条成功的提示消息',
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
