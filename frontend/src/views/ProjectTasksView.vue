<template>
    <NavBar />
    <ProjectTasksList />
  </template>
  
  <script>
  // @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import ProjectTasksList from '@/components/ProjectTasksList.vue';

  
  export default {
    name: 'ProjectTasksList',
    components: {
      NavBar, ProjectTasksList
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