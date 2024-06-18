<template>
    <NavBar />
    <RegisterUser />
  </template>
  
  <script>
  // @ is an alias to /src
  import NavBar from '@/components/NavBar.vue'
  import RegisterUser from '@/components/RegisterUser.vue'

  
  export default {
    name: 'RegisterView',
    components: {
      NavBar, RegisterUser
    },
    date() {
      return {
        userAuthenticated: false
      }
    },
    mounted() {
      if (localStorage.username) {
        this.userAuthenticated = true
      }
    }
  }
  </script>
  