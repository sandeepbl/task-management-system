<template>
  <div class="container-fluid">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container">
      <a class="navbar-brand" href="/">TMS</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a class="nav-link" href="/tasks">Tasks</a>
          <a class="nav-link" href="/projects">Projects</a>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <span v-if="$store.state.currentUser.username">{{ $store.state.currentUser.username }}</span>
              <span v-else>Users</span>
            </a>
            <ul class="dropdown-menu">
              <li><a class="dropdown-item" href="/users">Manage Users</a></li>
              <li><a class="dropdown-item" href="/register">Register New User</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="/login">{{ userLoginText }}</a></li>
              <li><a class="dropdown-item" href="#" @click="logoutUser">Logout</a></li>
            </ul>
          </li>
        </div>
      </div>
    </div>
  </nav>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data () {
    return {
      userLoginText: "Login User",
    }
  },
  methods: {
    logoutUser() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('first_name')
      localStorage.removeItem('last_name')
      localStorage.removeItem('role')
      localStorage.removeItem('username')
      this.$router.push('/login')
      this.$store.state.currentUser.username = null
    }
  },
  mounted() {
    if (localStorage.username) {
      this.$store.state.currentUser.firstName = localStorage.first_name
      this.$store.state.currentUser.lastName = localStorage.last_name
      this.$store.state.currentUser.username = localStorage.username
      this.$store.state.currentUser.role = localStorage.role
      this.userLoginText = 'User Profile: ' +  localStorage.first_name + ' ' + localStorage.last_name + ' (' + localStorage.role + ') '
    }
  }
}
</script>



