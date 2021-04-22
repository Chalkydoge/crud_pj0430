<template>
  <div>

  </div>
</template>

<script>
export default {
  name: 'Logout',
  methods: {
  },
  created: {
    logOut () {
      const that = this
      that.hasLogin = false
      const storage = localStorage
      storage.clear()
      this.$router.push({name: 'Index'})
    }
  }
}
</script>
