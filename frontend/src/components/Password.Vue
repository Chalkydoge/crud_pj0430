<template>
  <div class="PasswordForm">
    <el-container style="height: 700px; border: 1px solid #eee;">
      <el-main>
        <el-tabs v-model="activeName" type="card" @tab-click="handleClick">
          <el-tab-pane label="普通用户" name="first">
            <h1><i class="el-icon-user-solid"></i> Register - 用户注册</h1>
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm"
            label-width="100px" style="width: 500px; margin: 0 auto;">
                <el-form-item label="用户名" prop="user">
                  <el-input type="text" v-model="ruleForm.user" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pass">
                  <el-input type="password" v-model="ruleForm.pass" autocomplete="off" show-password></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                  <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off" show-password></el-input>
                </el-form-item>
                <el-form-item label="验证码">
                  <slide-verify :l="42" :r="10" :w="310" :h="155" slider-text="向右滑动"
                  @success="onSuccess" @fail="onFail" @refresh="onRefresh"></slide-verify>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="submitForm('ruleForm')" icon="el-icon-check">注册</el-button>
                  <el-button @click="resetForm('ruleForm');show_info();" icon="el-icon-close">重置</el-button>
                   <el-link href="/#/Login" type="primary" icon="el-icon-bottom-right" :underline="false">已有账号?快去登录</el-link>
                </el-form-item>
            </el-form>

          </el-tab-pane>
          <el-tab-pane label="管理员" name="second">
            <h1><i class="el-icon-user-solid"></i> Register - 管理员注册</h1>
            <el-form :model="AdminForm" status-icon :rules="AdminRule" ref="AdminForm"
            label-width="100px" style="width: 500px; margin: 0 auto;">
                <el-form-item label="用户名" prop="user">
                  <el-input type="text" v-model="AdminForm.user" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email"
                :rules="[{ required: true, message: '请输入邮箱地址', trigger: 'blur' },
                        { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change']}]">
                  <el-input type="text" v-model="AdminForm.email" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="pass">
                  <el-input type="password" v-model="AdminForm.pass" autocomplete="off" show-password></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                  <el-input type="password" v-model="AdminForm.checkPass" autocomplete="off" show-password></el-input>
                </el-form-item>
                <el-form-item label="验证码">
                  <slide-verify :l="42" :r="10" :w="310" :h="155" slider-text="向右滑动"
                  @success="onSuccess" @fail="onFail" @refresh="onRefresh"></slide-verify>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="submitAdminForm('AdminForm')" icon="el-icon-check">注册</el-button>
                  <el-button @click="resetAdminForm('AdminForm'); show_info();" icon="el-icon-close">重置</el-button>
                </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>

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
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        let pwdRegex = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{8,30}')
        if (!pwdRegex.test(value)) {
          callback(new Error('密码强度太低!必须包含大小写字母,数字!至少8个字符,至多30个字符'))
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass')
          }
          callback()
        }
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    var checkAdmin = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('用户名不能为空'))
      }
      setTimeout(() => {
        callback()
      }, 1000)
    }
    var validateAdminPass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        let pwdRegex = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{8,30}')
        if (!pwdRegex.test(value)) {
          callback(new Error('密码强度太低!必须包含大小写字母,数字!至少8个字符,至多30个字符'))
        } else {
          if (this.AdminForm.checkPass !== '') {
            this.$refs.AdminForm.validateField('checkPass')
          }
          callback()
        }
      }
    }
    var validateAdminPass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.AdminForm.pass) {
        callback(new Error('两次输入密码不一致!'))
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
          { validator: validatePass2, trigger: 'blur' }
        ]
      },
      AdminForm: {
        user: '',
        pass: '',
        email: ''
      },
      AdminRule: {
        user: [
          {validator: checkAdmin, trigger: 'blur'}
        ],
        pass: [
          {validator: validateAdminPass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validateAdminPass2, trigger: 'blur'}
        ]
      },
      activeName: 'first',
      checkCode: false,
      CheckMsg: 'Success'
    }
  },
  methods: {
    onSuccess () {
      this.CheckMsg = '成功'
      this.checkCode = true // 验证码通过
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
    handleClick (tab, event) {

    },
    signup () {
      const that = this
      axios.post('http://localhost:8000/api/users/', {
        username: this.ruleForm.user,
        password: this.ruleForm.pass
      }).then(function (response) {
        that.signupResponse = response.data
        that.$message({
          message: '注册成功!',
          type: 'success'
        })
        that.$router.push({name: 'Login'})
      }).catch(function (error) {
        alert(error.message)
      })
    },
    signupAdmin () {
      const that = this
      axios.post('http://localhost:8000/api/users/', {
        username: this.AdminForm.user,
        password: this.AdminForm.pass,
        is_superuser: true,
        email: this.AdminForm.email
      }).then(function (response) {
        that.signupResponse = response.data
        that.$message({
          message: '注册成功!',
          type: 'success'
        })
        that.$router.push({name: 'Login'})
      }).catch(function (error) {
        alert(error.message)
      })
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid && this.checkCode) {
          this.signup()
        } else {
          this.$notify({
            title: '注册失败',
            message: '请检查您的输入',
            type: 'error'
          })
        }
      })
    },
    submitAdminForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid && this.checkCode) {
          this.signupAdmin()
        } else {
          this.$notify({
            title: '注册失败',
            message: '请检查您的输入',
            type: 'error'
          })
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

</style>
