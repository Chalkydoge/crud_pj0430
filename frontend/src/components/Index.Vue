<template>
  <div class="Index">
  <SiteHeader></SiteHeader>
  <el-container style="border: 1px solid #eee;">
    <Sidebar></Sidebar>
    <el-container>
      <el-header style="text-align: right; font-size: 12px;">
      </el-header>

      <el-main>
        <el-image :src="src">
          <div slot="placeholder" class="image-slot">
            加载中<span class="dot">...</span>
          </div>
        </el-image>
      </el-main>
    </el-container>
  </el-container>
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
      tableData: [
        {c_id: 'ph', c_name: 'ph', c_teacher: 'ph', c_classroom: 'ph', c_dept: 'ph'}
      ],
      user_id: 0,
      src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg'
    }
  },
  methods: {
    async demo () {
      const that = this
      // const token = localStorage.getItem('access.mysite')
      axios.get('http://localhost:8000/api/users/', {
        params: {
          username: localStorage.getItem('username.mysite')
        }
      }).then((response) => {
        that.user_id = response.data.results[0].id
        console.log(that.user_id)
      }).catch((error) => {
        console.log(error.message)
      })
    },
    block () {
      const that = this
      const token = localStorage.getItem('access.mysite')
      axios.patch('http://localhost:8000/api/users/' + '11' + '/', {
        username: 'Fuck',
        in_blacklist: true
      }, {
        headers: {Authorization: 'Bearer ' + token}
      }).then((response) => {
        that.$notify({
          title: '作死按钮',
          message: '哈哈哈 成功封号',
          type: 'success'
        })
      }).catch((error) => {
        that.$notify({
          title: '出现错误',
          message: error.message,
          type: 'danger'
        })
      })
    },
    wrap () {
      setTimeout(this.block(), 2000) // async handling info
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
    margin-bottom: 0px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 5px;
  }
</style>
