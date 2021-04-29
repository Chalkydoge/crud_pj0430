<template>
  <div class="Comment">
    <SiteHeader></SiteHeader>
    <div v-if="this.not_login == false">
      <el-container style="border: 1px solid #eee">
        <Sidebar></Sidebar>
        <el-container>
          <el-header>
            <i class="el-icon-chat-line-round"></i>评论区
          </el-header>

          <el-main style="text-align: left">
            <el-row>
              <el-col :span=8>
                <el-input placeholder="找找看! 输入课程序号进行查询~" v-model="searchText" clearable prefix-icon="el-icon-search"></el-input>
              </el-col>
              <el-col :span=2>
                <el-button type="primary" icon="el-icon-search" @click="searchComments();">
                搜索</el-button>
              </el-col>
              <el-col :span=6>
                <el-button type="info" icon="el-icon-edit"
                @click="dialogFormVisible=true">新建</el-button>
                <i class="el-icon-back"></i>
                <span><el-tag>没有找到?来写评论吧</el-tag></span>
              </el-col>
            </el-row>

            <el-row>
              <el-divider></el-divider>
            </el-row>

            <el-table
            :data="comments"
            border
            :default-sort = "{prop: 'p_rate', order: 'descending'}"
            style="width: 80%">
              <el-table-column
                fixed
                prop="p_cid"
                label="课程号"
                width="150">
              </el-table-column>
              <el-table-column
                prop="p_coursename"
                label="课程名称"
                width="200">
              </el-table-column>
              <el-table-column
                prop="p_rate"
                label="评分"
                sortable
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
                  <el-button @click="handleViewClick(scope.row)" type="primary" size="small">查看</el-button>
                  <el-button @click="handleEditClick(scope.row)" type="warning" size="small">编辑</el-button>
                  <el-button @click="handleDeleteClick(scope.row)" type="danger" size="small">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-main>

          <el-footer>
            <el-pagination
            background
            layout="prev, pager, next"
            :total.sync="maxPage"
            :current-page.sync="currentPage"
            @current-change="handleCurrentChange">
            </el-pagination>
          </el-footer>
        </el-container>

      </el-container>
      <!-- Magic Don't touch -->
      <el-dialog title="写评论" :visible.sync="dialogFormVisible">
        <el-form :model="CommentForm">
          <el-form-item label="课程号" :label-width="formLabelWidth">
            <el-input v-model="CommentForm.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="评分" :label-width="formLabelWidth">
            <el-rate v-model="CommentForm.rate" show-text></el-rate>
          </el-form-item>
          <el-form-item label="评论内容" :label-width="formLabelWidth">
            <el-input type="textarea" :rows="2"
            v-model="CommentForm.text" maxlength="200" show-word-limit></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible=false; resetForm();">取 消</el-button>
          <el-button type="primary" @click="addComments();dialogFormVisible=false">确 定</el-button>
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
          <el-form-item label="课程名称" :label-width="formLabelWidth">
            <el-input v-model="CommentDetailForm.coursename" autocomplete="off" :disabled="true"></el-input>
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

      <el-dialog title="修改评论" :visible.sync="editFormVisible">
        <el-form :model="EditCommentForm">
          <el-form-item label="课程号" :label-width="formLabelWidth">
            <el-input v-model="EditCommentForm.name" autocomplete="off" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="评分" :label-width="formLabelWidth">
            <el-rate v-model="EditCommentForm.rate" show-text></el-rate>
          </el-form-item>
          <el-form-item label="评论内容" :label-width="formLabelWidth">
            <el-input type="textarea" :rows="2"
            v-model="EditCommentForm.text" maxlength="200" show-word-limit></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer">
          <el-button @click="editFormVisible=false; resetForm();">取 消</el-button>
          <el-button type="primary" @click="EditedFormSubmit();editFormVisible=false;">修 改</el-button>
        </div>
      </el-dialog>

      <el-drawer title="查到的结果" :visible.sync="drawer" :with-header="true" size="50%">
        <el-table :data="resultForms">
            <el-table-column fixed prop="p_cid" label="课程号" width="150">
            </el-table-column>
            <el-table-column prop="p_rate" label="评分" width="120">
            </el-table-column>
            <el-table-column prop="p_comment" label="评价内容" width="120">
            </el-table-column>
            <el-table-column
              label="操作"
              width="240">
              <template slot-scope="scope">
                <el-button @click="handleViewClick(scope.row)" type="primary" size="small">查看</el-button>
                <el-button @click="handleEditClick(scope.row)" type="warning" size="small">编辑</el-button>
                <el-button @click="handleDeleteClick(scope.row)" type="danger" size="small">删除</el-button>
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
      </el-drawer>

    </div>
    <div v-else>
      <el-page-header @back="goBack" content="404页面">
      </el-page-header>
      <p>Not Logged in! 请登录以查看内容!!</p>
    </div>
  </div>
</template>

<script>
import SiteHeader from '@/components/SiteHeader'
import axios from 'axios'
import Sidebar from '@/components/Sidebar'

export default {
  name: 'Comment',
  components: {SiteHeader, Sidebar},
  inject: ['reload'],
  data () {
    return {
      count: 0,
      comments: [], // 页面上评论区内部显示的评论数组,
      not_login: false,
      searchText: '',
      baseSearchUrl: '',
      currentPage: 0, // 当前的页码
      maxPage: 10000000, // 最大能够翻到的页码
      userEdit: '',
      userDelete: '',
      CommentForm: { // 新建评论的数据表格
        name: '',
        rate: 0,
        text: ''
      },
      EditCommentForm: { // 编辑评论的数据表格
        p_id: 0,
        name: '',
        rate: 0,
        text: ''
      },
      // 评论详情展示表
      CommentDetailForm: {
        user: '',
        name: '',
        coursename: '',
        rate: 0,
        text: ''
      },
      dialogFormVisible: false,
      editFormVisible: false,
      CommentDetailFormVisible: false,
      formLabelWidth: '120px',
      drawer: false,
      resultForms: [], // 查询到的评论表格数据
      currentCommentPage: 0, // 查询结果的当前页码
      maxCommentPage: 100 // 默认最大值
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
    handleCurrentChange () {
      this.showComments()
    },
    handleCurrentCommentChange () {
      const that = this
      const page = that.currentCommentPage
      let url = that.baseSearchUrl
      if (page !== 1 && page !== 0) {
        url = url + '&page=' + page
      }
      console.log(url)
      axios.get(url).then(function (response) {
        that.resultForms = response.data.results
      }).catch(function (error) {
        that.$notify({
          title: '出现错误',
          message: that.decodeError(error.message),
          type: 'error'
        })
      })
    },
    // 显示课评 完成
    showComments () {
      // TODO fetch data from backend
      const that = this
      const page = that.currentPage
      let url = 'http://localhost:8000/api/comments'
      if (page !== 1 && page !== 0) {
        url = url + '/?page=' + page
      } else {
        url = url + '/'
      }
      axios.get(url).then(function (response) {
        that.comments = response.data.results
        that.maxPage = (Math.ceil(response.data.count / 10)) * 10
      }).catch(function (error) {
        that.$notify({
          title: '出现错误',
          message: that.decodeError(error.message),
          type: 'error'
        })
      })
    },
    // 新建课评 完成
    addComments () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.post('http://localhost:8000/api/comments/', {
        p_cid: that.CommentForm.name,
        p_rate: that.CommentForm.rate * 20,
        p_comment: that.CommentForm.text,
        p_owner: localStorage.getItem('username.mysite')
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then(function (response) {
        // 成功发布, 则弹出通知
        that.$notify({
          title: '发表成功',
          message: '您已成功发布评论,快去看看吧~',
          type: 'success'
        })
      }).catch(function (error) {
        that.$notify({
          title: '出现错误',
          message: that.decodeError(error.message),
          type: 'warning'
        })
      })
    },
    // OK
    searchComments () {
      let ans = this.getSearchCount()
      const that = this
      that.drawer = true
      ans.then(() => {
        // console.log(that.baseSearchUrl) // 可能存在的下一个数据页面url
        // console.log(that.maxCommentPage) // 最大评论区页码数
        if (that.baseSearchUrl) {
          that.baseSearchUrl = that.baseSearchUrl.slice(0, -7)
        }
        // Fetch the first page
        axios.get('http://localhost:8000/api/comments/', {
          params: {
            p_cid: that.searchText
          }
        }).then(function (response) {
          that.resultForms = response.data.results
          that.$notify({
            title: '搜索信息',
            message: that.searchText,
            type: 'success'
          })
        }).catch(function (error) {
          console.log(error)
          that.$notify({
            title: '出现错误',
            message: that.decodeError(error.message),
            type: 'danger'
          })
        })
      })
    },
    getUserInfo () {
      const that = this
      const storage = localStorage
      that.not_login = (storage.getItem('username.mysite') === null)
    },
    // OK
    handleViewClick (row) {
      const that = this
      that.getCommentUser(row.p_id).then((response) => {
        if (!response.data.count) {
          that.CommentDetailForm.user = 'Unknown'
        } else {
          that.CommentDetailForm.user = response.data.results[0].m_username
        }
        that.CommentDetailForm.name = row.p_cid
        that.CommentDetailForm.rate = row.p_rate / 20
        that.CommentDetailForm.text = row.p_comment
        that.CommentDetailForm.coursename = row.p_coursename
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: that.decodeError(error.message),
          type: 'error'
        })
      })
      that.CommentDetailFormVisible = true
    },
    // OK
    handleEditClick (row) {
      const curUser = localStorage.getItem('username.mysite')
      const that = this
      that.getCommentUser(row.p_id).then((response) => {
        if (!response.data.count) {
          that.userEdit = 'Unknown'
        } else {
          that.userEdit = response.data.results[0].m_username
        }

        if (curUser !== that.userEdit) {
          that.$notify({
            title: '错误',
            message: '不能修改别人的评论哦',
            type: 'error'
          })
        } else {
          that.EditCommentForm.p_id = row.p_id
          that.EditCommentForm.name = row.p_cid
          that.editFormVisible = true
        }
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: that.decodeError(error.message),
          type: 'error'
        })
      })
    },
    // OK
    handleDeleteClick (row) {
      const curUser = localStorage.getItem('username.mysite')
      const that = this
      const token = localStorage.getItem('access.mysite')
      that.getCommentUser(row.p_id).then((response) => {
        if (!response.data.count) {
          that.userDelete = 'Unknown'
        } else {
          that.userDelete = response.data.results[0].m_username
        }
        if (curUser !== that.userDelete) {
          this.$notify({
            title: '错误',
            message: '不能删除别人的评论!',
            type: 'error'
          })
        } else {
          that.$confirm('此操作将永久删除该课程评论的信息,是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            axios.delete('http://localhost:8000/api/comments/' +
            row.p_id + '/', {
              params: {
                p_cid: row.p_cid,
                p_rate: row.p_rate,
                p_owner: row.p_owner
              },
              headers: {Authorization: 'Bearer ' + token}
            }).then((result) => {
              that.$notify({
                title: '完成删除!',
                message: '请刷新界面',
                type: 'success'
              })
            }).catch((error) => {
              that.$notify({
                title: '出现错误',
                message: that.decodeError(error.message),
                type: 'warning'
              })
            })
          })
        }
      })
    },
    // OK
    EditedFormSubmit () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.put('http://localhost:8000/api/comments/' +
        that.EditCommentForm.p_id + '/', {
        p_cid: that.EditCommentForm.name,
        p_rate: that.EditCommentForm.rate * 20,
        p_comment: that.EditCommentForm.text
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
          message: that.decodeError(error.message),
          type: 'error'
        })
      })
    },
    // OK
    resetForm () {
      this.$notify({
        title: '撤销成功',
        message: '还没想好怎么写嘛wow 没事~',
        type: 'success'
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
    },
    async getSearchCount () {
      const that = this
      try {
        let response = await axios.get('http://localhost:8000/api/comments/', {
          params: {
            p_cid: that.searchText
          }
        })
        that.maxCommentPage = (Math.ceil(response.data.count / 10)) * 10
        that.baseSearchUrl = response.data.next
      } catch (error) {
        console.log(error.message)
      }
    }
  },
  created: function () {
    this.getUserInfo()
    setTimeout(this.showComments(), 1000)
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
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 1.7;
  font-size: 25px;
  text-align: left;
}

</style>
