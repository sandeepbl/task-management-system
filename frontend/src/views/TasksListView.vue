<template>
    <NavBar />
    <TasksList />
  </template>
  
  <script>
  // @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import TasksList from '@/components/TasksList.vue';

  
  export default {
    name: 'TasksListView',
    components: {
      NavBar, TasksList
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
  