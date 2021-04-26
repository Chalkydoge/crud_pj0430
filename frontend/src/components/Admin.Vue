<template>
  <div>
    <SiteHeader></SiteHeader>
    <el-container style="border: 1px solid #eee;">
      <Sidebar></Sidebar>

      <div v-if="this.is_superuser">
        <el-main>
          <el-tabs type="border-card" @tab-click="handleClick">

            <el-tab-pane label="课程信息">
              <el-button type="primary" icon="el-icon-search">新建课程</el-button>
              <el-table :data="course_info">
                <el-table-column prop="c_id" label="课程号" width="140"></el-table-column>
                  <el-table-column prop="c_name" label="课程名称" width="200"></el-table-column>
                  <el-table-column prop="c_teacher_name" label="授课教师" width="140"></el-table-column>
                  <el-table-column prop="c_classroom" label="上课地点" width="140"></el-table-column>
                  <el-table-column prop="c_dept_name" label="开课院系" width="140"></el-table-column>
                  <el-table-column label="操作" width="240">
                    <template slot-scope="scope">
                      <el-button @click="handleCourseViewClick(scope.row)" type="primary" size="small">查看</el-button>
                      <el-button @click="handleCourseEditClick(scope.row)" type="warning" size="small">编辑</el-button>
                      <el-button @click="handleCourseDeleteClick(scope.row)" type="danger" size="small">删除</el-button>
                    </template>
                  </el-table-column>
              </el-table>

              <el-footer>
                <el-pagination
                background
                layout="prev, pager, next"
                :total.sync="maxCoursePage"
                :current-page.sync="currentCoursePage"
                @current-change="handleCurrentCourseChange">
                </el-pagination>
              </el-footer>

            </el-tab-pane>

            <el-tab-pane label="评论信息">
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
                  label="操作"
                  width="240">
                  <template slot-scope="scope">
                    <el-button @click="handleCommentViewClick(scope.row)" type="primary" size="small">查看</el-button>
                    <el-button @click="handleCommentEditClick(scope.row)" type="warning" size="small">编辑</el-button>
                    <el-button @click="handleCommentDeleteClick(scope.row)" type="danger" size="small">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>

              <el-footer>
                <el-pagination
                background
                layout="prev, pager, next"
                :total.sync="maxCommentPage"
                :current-page.sync="currentCommentPage"
                @current-change="handleCurrentCommentChange">
                </el-pagination>
              </el-footer>
            </el-tab-pane>

            <el-tab-pane label="用户管理">
              <el-table :data="user_info">
                <el-table-column prop="username" label="用户名" width="140"></el-table-column>
                <el-table-column prop="password" label="密码" width="650"></el-table-column>

                <el-table-column label="操作" width="320">
                  <template slot-scope="scope">
                    <el-button @click="handleUserBlockClick(scope.row)" type="info" size="small">封禁</el-button>
                    <el-button @click="handleUserViewClick(scope.row)" type="primary" size="small">详细</el-button>
                    <el-button @click="handleUserDeleteClick(scope.row)" type="danger" size="small">删除</el-button>
                    <el-button @click="handleUserUnblockClick(scope.row)" type="info" size="small">解封</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-main>

        <el-dialog title="编辑课程" :visible.sync="EditCourseFormVisible">
          <el-form :model="EditCourseForm">
            <el-form-item label="课程号" :label-width="EditCourseFormLabelWidth">
              <el-input v-model="EditCourseForm.c_id" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="课程名" :label-width="EditCourseFormLabelWidth">
              <el-input v-model="EditCourseForm.c_name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="授课教师" :label-width="EditCourseFormLabelWidth">
              <el-input v-model="EditCourseForm.c_teacher" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="教师院系" :label-width="EditCourseFormLabelWidth">
              <el-input v-model="EditCourseForm.c_tdept" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="上课地点" :label-width="EditCourseFormLabelWidth">
              <el-input v-model="EditCourseForm.c_classroom" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="开课院系" :label-width="EditCourseFormLabelWidth">
              <el-input v-model="EditCourseForm.c_dept" autocomplete="off"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="EditCourseFormVisible=false;">取 消</el-button>
            <el-button type="primary" @click="SubmitEditCourseForm(); EditCourseFormVisible=false">确 定</el-button>
          </div>
        </el-dialog>

        <el-dialog title="评论详情" :visible.sync="CommentDetailFormVisible">
          <el-form :model="CommentDetailForm">
            <el-form-item label="用户" :label-width="formLabelWidth">
              <el-input v-model="CommentDetailForm.user" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="课程号" :label-width="formLabelWidth">
              <el-input v-model="CommentDetailForm.name" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="评分" :label-width="formLabelWidth">
              <el-rate v-model="CommentDetailForm.rate" show-text :disabled="true"></el-rate>
            </el-form-item>
            <el-form-item label="评论内容" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="2"
              v-model="CommentDetailForm.text" :disabled="true"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="CommentDetailFormVisible=false">关闭</el-button>
          </div>
        </el-dialog>

        <el-dialog title="修改评论" :visible.sync="CommentEditFormVisible">
          <el-form :model="CommentEditForm">
            <el-form-item label="课程号" :label-width="formLabelWidth">
              <el-input v-model="CommentEditForm.name" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="评分" :label-width="formLabelWidth">
              <el-rate v-model="CommentEditForm.rate" show-text></el-rate>
            </el-form-item>
            <el-form-item label="评论内容" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="2"
              v-model="CommentEditForm.text"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer">
            <el-button @click="CommentEditFormVisible=false;">取 消</el-button>
            <el-button type="primary" @click="CommentEditFormSubmit();CommentEditFormVisible=false;">修 改</el-button>
          </div>
        </el-dialog>

        <el-dialog title="用户详情" :visible.sync="UserDetailFormVisible">
          <el-form :model="UserDetailForm">
            <el-form-item label="用户" :label-width="formLabelWidth">
              <el-input v-model="UserDetailForm.username" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="密码" :label-width="formLabelWidth">
              <el-input v-model="UserDetailForm.password" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="权限等级" :label-width="formLabelWidth">
              <el-input v-model="UserDetailForm.authority" autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="UserDetailFormVisible=false">关闭</el-button>
          </div>

        </el-dialog>
      </div>

      <div v-else>
        Only Admin can view this site.<br>
        只有管理员可以进入该界面。
      </div>

    </el-container>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar'
import SiteHeader from '@/components/SiteHeader'
import axios from 'axios'

export default {
  name: 'Admin',
  components: {Sidebar, SiteHeader},
  inject: ['reload'],
  data () {
    return {
      formLabelWidth: '120px',
      is_superuser: false,
      course_info: [],
      comments: [],
      user_info: [],
      EditCourseForm: {
        c_id: '',
        c_name: '',
        c_teacher: '',
        c_classroom: '',
        c_dept: '',
        c_tdept: ''
      },
      CommentDetailForm: {
        user: '',
        name: '',
        rate: 0,
        text: ''
      },
      CommentEditForm: {
        p_id: 0,
        user: '',
        name: '',
        text: '',
        rate: 0
      },
      UserDetailForm: {
        username: '',
        password: '',
        authority: false
      },
      CommentDetailFormVisible: false,
      CommentEditFormVisible: false,
      UserDetailFormVisible: false,
      EditCourseFormLabelWidth: '120px',
      EditCourseFormVisible: false,
      currentCommentPage: 0, // 当前评论对应的页码
      maxCommentPage: 10000000,
      currentCoursePage: 0, // 当前课程信息对应页码
      maxCoursePage: 100
    }
  },
  methods: {
    getUserLevel () {
      const that = this
      const username = localStorage.getItem('username.mysite')
      if (username) {
        axios.get('http://localhost:8000/api/users/', {
          params: {
            username: localStorage.getItem('username.mysite')
          }
        }).then((response) => {
          that.is_superuser = response.data.results[0].is_superuser
          console.log(that.is_superuser)
        }).catch((error) => {
          that.$notify({
            title: '出现错误',
            message: error.message,
            type: 'error'
          })
        })
      }
    },
    // 主界面panel的控制函数
    handleClick (tab, event) {
      const type = tab.label
      const that = this
      if (type === '课程信息') {
        axios
          .get('http://localhost:8000/api/courses/')
          .then((response) => {
            if (!response.data.count) {
              that.maxCoursePage = 10
            } else {
              that.maxCoursePage = (Math.ceil(response.data.count / 10)) * 10
            }
          }).catch((error) => {
            that.$notify({
              title: 'Error',
              message: error.message,
              type: 'error'
            })
          })
      } else if (type === '评论信息') {
        axios.get('http://localhost:8000/api/comments/').then((response) => {
          that.comments = response.data.results
          that.maxCommentPage = (Math.ceil(response.data.count / 10)) * 10
          console.log(response.data.count)
        }).catch((error) => {
          that.$notify({
            title: 'Error',
            message: error.message,
            type: 'error'
          })
        })
      } else if (type === '用户管理') {
        axios.get('http://localhost:8000/api/users/').then((response) => {
          that.user_info = response.data.results
          console.log(that.user_info[0].username)
        }).catch((error) => {
          that.$notify({
            title: 'Error',
            message: error.message,
            type: 'error'
          })
        })
      } else {
        alert('error')
      }
    },
    // 用户权限操作的控制函数
    handleUserBlockClick (row) {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.put('http://localhost:8000/api/users/' + row.id + '/', {
        id: row.id,
        username: row.username,
        password: row.password,
        perm: 'blocked'
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((response) => {
        that.$notify({
          title: '成功',
          message: '已封禁该用户',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
    },
    // 解封
    handleUserUnblockClick (row) {
      const that = this
      console.log(row.id)
      const token = localStorage.getItem('access.mysite')
      axios.put('http://localhost:8000/api/users/' + row.id + '/', {
        id: row.id,
        username: row.username,
        password: row.password,
        perm: 'unblocked'
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((response) => {
        that.$notify({
          title: '成功',
          message: '已解封该用户',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
    },
    // 用户详情页
    handleUserViewClick (row) {
      this.UserDetailForm.username = row.username
      this.UserDetailForm.password = row.password
      if (row.is_superuser) {
        this.UserDetailForm.authority = '管理员'
      } else {
        this.UserDetailForm.authority = '普通用户'
      }
      this.UserDetailFormVisible = true
    },
    // 删除用户
    handleUserDeleteClick (row) {
      const that = this
      console.log(row.id)
      const token = localStorage.getItem('access.mysite')
      axios.delete('http://localhost:8000/api/users/' + row.id + '/', {
        id: row.id,
        username: row.username,
        password: row.password,
        is_superuser: row.is_superuser
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((response) => {
        that.$notify({
          title: '成功',
          message: '已注销该用户',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
    },

    // 评论分页
    handleCurrentCommentChange () {
      const that = this
      const page = that.currentCommentPage
      let url = 'http://localhost:8000/api/comments'
      if (page !== 1 && page !== 0) {
        url = url + '/?page=' + page
      } else {
        url = url + '/'
      }
      axios.get(url).then(function (response) {
        that.comments = response.data.results
      }).catch(function (error) {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
    },
    // 课程分页
    handleCurrentCourseChange () {
      const that = this
      const page = that.currentCoursePage
      let url = 'http://localhost:8000/api/courses'
      if (page !== 1 && page !== 0) {
        url = url + '/?page=' + page
      } else {
        url = url + '/'
      }
      axios.get(url).then(function (response) {
        that.comments = response.data.results
      }).catch(function (error) {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
    },
    // 课程信息修改 OK
    handleCourseEditClick (row) {
      this.EditCourseForm.c_id = row.c_id
      this.EditCourseForm.c_name = row.c_name
      this.EditCourseForm.c_teacher = row.c_teacher_name
      this.EditCourseForm.c_classroom = row.c_classroom
      this.EditCourseForm.c_dept = row.c_dept_name
      this.EditCourseForm.c_tdept = ''
      this.EditCourseFormVisible = true
    },
    // 提交课程信息修改表
    SubmitEditCourseForm () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.put('http://localhost:8000/api/courses/' + that.EditCourseForm.c_id + '/', {
        c_id: that.EditCourseForm.c_id,
        c_name: that.EditCourseForm.c_name,
        c_teacher_name: that.EditCourseForm.c_teacher,
        c_classroom: that.EditCourseForm.c_classroom,
        c_dept_name: that.EditCourseForm.c_dept,
        c_tdept_name: that.EditCourseForm.c_tdept
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((response) => {
        console.log(1)
      }).catch((error) => {
        console.log(error.message)
      })
    },
    // 课程删除 OK
    handleCourseDeleteClick (row) {
      const that = this
      const token = localStorage.getItem('access.mysite')
      that.$confirm('此操作将永久删除该课程的信息,是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete('http://localhost:8000/api/courses/' + row.c_id + '/', {
          params: {
            c_id: row.c_id,
            c_name: row.c_name,
            c_teacher_name: row.c_teacher,
            c_classroom: row.c_classroom,
            c_dept_name: row.c_dept
          },
          headers: {Authorization: 'Bearer ' + token}
        }).then((response) => {
          that.reload()
          that.$message({
            type: 'success',
            message: '删除成功'
          })
        })
      }).catch((error) => {
        if (error.message) {
          that.$message({
            type: 'error',
            message: error.message
          })
        } else {
          that.$message({
            type: 'info',
            message: '删除取消'
          })
        }
      })
    },
    // 评论详情 OK
    handleCommentViewClick (row) {
      const that = this
      that.getCommentUser(row.p_id).then((response) => {
        console.log(response.data)
        if (!response.data.count) {
          that.CommentDetailForm.user = 'Unknown'
        } else {
          that.CommentDetailForm.user = response.data.results[0].m_username
        }
        that.CommentDetailForm.name = row.p_cid
        that.CommentDetailForm.rate = row.p_rate / 20
        that.CommentDetailForm.text = row.p_comment
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
      that.CommentDetailFormVisible = true
    },
    // 编辑评论 OK
    handleCommentEditClick (row) {
      const that = this
      that.getCommentUser(row.p_id).then((response) => {
        if (!response.data.count) {
          that.CommentEditForm.user = 'Unknown'
        } else {
          that.CommentEditForm.user = response.data.results[0].m_username
        }
        that.CommentEditForm.p_id = row.p_id
        that.CommentEditForm.name = row.p_cid
        that.CommentEditForm.rate = row.p_rate / 20
        that.CommentEditForm.text = row.p_comment
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
      that.CommentEditFormVisible = true
    },
    CommentEditFormSubmit () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.put('http://localhost:8000/api/comments/' +
        that.CommentEditForm.p_id + '/', {
        p_cid: that.CommentEditForm.name,
        p_rate: that.CommentEditForm.rate * 20,
        p_comment: that.CommentEditForm.text
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((result) => {
        that.$notify({
          title: '可以',
          message: '完成修改！',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'error'
        })
      })
    },
    // 删除评论 OK
    handleCommentDeleteClick (row) {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.delete('http://localhost:8000/api/comments/' + row.p_id + '/', {
        params: {
          p_cid: row.p_cid,
          p_rate: row.p_rate,
          p_owner: row.p_owner
        },
        headers: {Authorization: 'Bearer ' + token}
      }).then((result) => {
        that.reload()
        that.$notify({
          title: '完成删除!',
          message: '请刷新界面',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'warning'
        })
      })
    },

    // OK
    async getCommentUser (commentId) {
      let ans
      try {
        let response = await axios.get('http://localhost:8000/api/make_comment/', {
          params: {
            m_commentid: commentId
          }
        })
        ans = response
      } catch (error) {
        console.log(error.message)
      }
      return ans
    }
  },
  created: function () {
    const that = this
    that.getUserLevel()
  },
  mounted () {
    const that = this
    axios.get('http://localhost:8000/api/courses/').then((response) => {
      that.course_info = response.data
      that.maxCoursePage = (Math.ceil(response.data.count / 10)) * 10
    }).catch((error) => {
      that.$notify({
        title: 'Error',
        message: error.message,
        type: 'error'
      })
    })
  }
}
</script>
