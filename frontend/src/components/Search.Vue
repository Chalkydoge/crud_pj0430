<template>
  <div class="Search">
  <SiteHeader></SiteHeader>
  <el-container style="height: 150%; border: 1px solid #eee;">
    <Sidebar></Sidebar>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <el-dropdown>
          <i class="el-icon-setting" style="margin-top: 10px; margin-right: 20px; font-size:28px;"></i>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>
              <el-button type="text" @click="dialogVisible = true;">新增</el-button>
            </el-dropdown-item>
            <el-dropdown-item>删除</el-dropdown-item>
          </el-dropdown-menu>
          <span>工具选项</span>
        </el-dropdown>
      </el-header>
      <el-main>
        <el-form ref="form" :model="form" label-width="80px" style="text-align: left;">
          <el-row>
            <el-col :span="8">
              <el-form-item label="课程号" prop="c_id">
                <el-input v-model="form.c_id"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="8">
              <el-form-item label="课程名" prop="c_name">
                <el-input v-model="form.c_name"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-form-item label="上课地点" prop="c_classroom">
              <el-col :span="4">
                <el-select v-model="form.c_classroom" placeholder="请选择上课地点" >
                <el-option label="二教" value="H2"></el-option>
                <el-option label="三教" value="H3"></el-option>
                <el-option label="四教" value="H4"></el-option>
                <el-option label="五教" value="H5"></el-option>
                <el-option label="六教" value="H6"></el-option>
                <el-option label="江湾1号楼" value="JA1"></el-option>
                <el-option label="江湾2号楼" value="JB1"></el-option>
                <el-option label="光华西" value="HGX"></el-option>
                <el-option label="光华东" value="HGD"></el-option>
                <el-option label="枫林" value="F"></el-option>
                </el-select>
              </el-col>
              <el-col :span="4">
                <el-input v-model="form.c_room_no" placeholder="请输入教室号"></el-input>
              </el-col>
            </el-form-item>
          </el-row>

          <el-row>
            <el-col :span="8">
              <el-form-item label="授课教师" prop="c_teacher">
                <el-input v-model="form.c_teacher_name"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="8">
              <el-form-item label="开课院系" prop="c_dept">
                <el-input v-model="form.c_dept_name"></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item>
            <el-button type="primary" @click="onSubmit(); drawer = true;" icon="el-icon-search">搜索</el-button>
            <el-button @click="resetForm('form')" icon="el-icon-delete">重置</el-button>
          </el-form-item>
        </el-form>
      </el-main>

      <el-drawer
        title="搜索结果✔"
        :visible.sync="drawer"
        :direction="direction"
        :before-close="handleClose"
        size="40%">
        <el-table :data="info">
          <el-table-column prop="c_id" label="课程号" width="140"></el-table-column>
            <el-table-column prop="c_name" label="课程名称" width="200"></el-table-column>
            <el-table-column prop="c_teacher_name" label="授课教师" width="140"></el-table-column>
            <el-table-column prop="c_classroom" label="上课地点" width="140"></el-table-column>
            <el-table-column prop="c_dept_name" label="开课院系" width="140"></el-table-column>
        </el-table>
      </el-drawer>
    </el-container>

  </el-container>

  <el-dialog
    title="新建课程信息"
    :visible.sync="dialogVisible"
    width=30%
    :before-close="createHandleClose">
    <el-form :model="submitForm">
      <el-form-item label="课程号" :label-width="submitFormLabelWidth">
        <el-input v-model="submitForm.c_id" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="课程名称" :label-width="submitFormLabelWidth">
        <el-input v-model="submitForm.c_name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="授课教师" :label-width="submitFormLabelWidth">
        <el-input v-model="submitForm.c_teacher_name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="教师院系" :label-width="submitFormLabelWidth">
        <el-input v-model="submitForm.c_tdept_name" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="上课地点" :label-width="submitFormLabelWidth">
        <el-input v-model="submitForm.c_classroom" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="开课院系" :label-width="submitFormLabelWidth">
        <el-input v-model="submitForm.c_dept_name" autocomplete="off"></el-input>
      </el-form-item>
    </el-form>

    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible=false">取 消</el-button>
      <el-button type="primary" @click="dialogVisible = false; createCourses();">提 交</el-button>
    </span>
  </el-dialog>

  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar'
import SiteHeader from '@/components/SiteHeader'
import axios from 'axios'

export default {
  components: {SiteHeader, Sidebar},
  data () {
    return {
      form: {
        c_id: '',
        c_name: '',
        c_classroom: '',
        c_room_no: '',
        c_teacher_name: '',
        c_dept_name: ''
      },
      submitForm: {
        c_id: '',
        c_name: '',
        c_classroom: '',
        c_teacher_name: '',
        c_tdept_name: '',
        c_dept_name: ''
      },
      info: [],
      dialogVisible: false,
      drawer: false,
      direction: 'rtl',
      submitFormLabelWidth: '120px'
    }
  },
  methods: {
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.$notify({
        title: '成功重置',
        message: '完成!',
        type: 'success'
      })
    },
    searchCourses () {
      const that = this
      const classroom = that.form.c_classroom + that.form.c_room_no
      axios.get('http://localhost:8000/api/courses/', {
        params: {
          c_id: that.form.c_id,
          c_name: that.form.c_name,
          c_teacher_name: that.form.c_teacher_name,
          c_classroom: classroom,
          c_dept_name: that.form.c_dept_name
        }
      }).then(function (response) {
        that.info = response.data.results
        console.log(response)
        that.$notify({
          title: '成功√',
          message: '找到了很多信息',
          type: 'success'
        })
      }).catch(function (error) {
        alert(error.message)
      })
    },
    // TODO createCourses
    createCourses () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.post('http://localhost:8000/api/courses/', {
        c_id: that.submitForm.c_id,
        c_name: that.submitForm.c_name,
        c_teacher_name: that.submitForm.c_teacher_name,
        c_tdept_name: that.submitForm.c_tdept_name,
        c_classroom: that.submitForm.c_classroom,
        c_dept_name: that.submitForm.c_dept_name
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then(function (response) {
        // TODO get the response data
        that.$notify({
          title: '完成创建!',
          message: '🆗',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出错了!',
          message: error.message,
          type: 'error'
        })
      })
    },
    onSubmit () {
      console.log('submit!')
      const that = this
      that.searchCourses()
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    createHandleClose (done) {
      this.$confirm('确认提交?').then(_ => {
        done()
      }).catch(_ => {})
    }
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
    margin-bottom: 5px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 1.7;
    font-size: 30px;
    text-align: left;
  }
</style>
