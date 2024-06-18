<template>
    <NavBar />
    <UsersList />
  </template>
  
  <script>
  // @ is an alias to /src
  import NavBar from '@/components/NavBar.vue'
  import UsersList from '@/components/UsersList.vue'

  
  export default {
    name: 'UsersListView',
    components: {
      NavBar, UsersList
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
  