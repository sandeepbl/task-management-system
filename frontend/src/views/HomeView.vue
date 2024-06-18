<template>
  <NavBar />
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue';

export default {
  name: 'HomeView',
  components: {
    NavBar, 
  },
  date() {
    return {
      userAuthenticated: false
    }
  },
  mounted() {
    if (localStorage.username) {
      this.userAuthenticated = true
      console.log("User is logged in")
    } else {
      this.$router.push('/login')
    }
  }
}
</script>
