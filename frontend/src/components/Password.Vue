<template>
  <div class="PasswordForm">
    <el-container style="height: 500px; border: 1px solid #eee;">
      <el-main>
        <el-col :span="8" :offset="8" style="min-height: 36px; text-align: center;">
          <h1>Register 注册</h1>
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
          <el-form-item label="年龄" prop="age">
            <el-input v-model.number="ruleForm.age"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')" icon="el-icon-check">注册</el-button>
            <el-button @click="resetForm('ruleForm');show_info();" icon="el-icon-close">重置</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Pwd',
  data () {
    var checkUser = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('用户名不能为空'))
      }
      setTimeout(() => {
        callback()
      }, 1000)
    }
    var checkAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('年龄不能为空'))
      }
      setTimeout(() => {
        if (!Number.isInteger(value)) {
          callback(new Error('请输入数字'))
        } else {
          if (value < 18) {
            callback(new Error('必须满18岁'))
          } else {
            callback()
          }
        }
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
        checkPass: '',
        age: ''
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
        ],
        age: [
          {validator: checkAge, trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    signup () {
      const that = this
      axios.post('http://localhost:8000/api/users/', {
        username: this.ruleForm.user,
        password: this.ruleForm.pass
      }).then(function (response) {
        that.signupResponse = response.data
        alert('注册成功!')
      }).catch(function (error) {
        alert(error.message)
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // do something here!!!
          this.signup()
          // alert('submit')
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

</style>
