<template>
    <NavBar />
    <LoginUser />
  </template>
  
  <script>
  // @ is an alias to /src
import LoginUser from '@/components/LoginUser.vue';
import NavBar from '@/components/NavBar.vue'

  
  export default {
    name: 'LoginView',
    components: {
      NavBar, LoginUser
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
  