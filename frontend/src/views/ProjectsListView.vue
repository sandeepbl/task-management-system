<template>
    <NavBar />
    <ProjectsList />
  </template>
  
  <script>
  // @ is an alias to /src
  import NavBar from '@/components/NavBar.vue'
  import ProjectsList from '@/components/ProjectsList.vue'

  
  export default {
    name: 'ProjectsListView',
    components: {
      NavBar, ProjectsList
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
  