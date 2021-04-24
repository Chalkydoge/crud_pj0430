<template>
  <div class="hello">
    <Sidebar></Sidebar>
  </div>
</template>

<script>
import Sidebar from '@/components/Sidebar'
export default {
  name: 'HelloWorld',
  components: {Sidebar},
  data () {
    return {
      msg: 'Helloworld'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
