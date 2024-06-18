<template>
    <div :class="alertLevel" role="alert" v-if="showLoginResponse">
        {{ loginResponse }}
    </div>
    <div class="container" v-if="!userAuthenticated">
        <div class="card">
            <div class="card-header">User Login</div>
            <div class="card-body">
                
                <div class="login" v-if="showLogin">
                    <form @submit.prevent="loginUser">
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" class="form-control" id="username" aria-describedby="emailHelp" v-model="username" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" class="form-control" id="password" v-model="password" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <div class="container" v-else>
        <h3>User Profile</h3>
        <p>User Name: {{ $store.state.currentUser.username }}</p>
        <p>Full Name: {{ $store.state.currentUser.first_name }} {{ $store.state.currentUser.last_name }}</p>
        <p>Role: {{ $store.state.currentUser.role }}</p>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'LoginUser',
    props: {
        msg: String
    },
    data() {
        return {
            userAuthenticated: false,
            username: '',
            password: '',
            errors:[],
            showLogin: true,
            showLoginResponse: false,
            loginResponse: 'Login Response here',
            alertLevel: 'alert alert-primary'
        }
    },
    mounted() {
        axios.headers =  {'Authorization': 'Bearer ' + localStorage.access_token}
        axios.get('/healthcheck/').then(
                (response) => {
                    console.log('Backend: '+response.data.message)
                }
            ).catch(error => {
                console.error("Healthcheck Failed... Backend server not responding.")
            })
        console.log('Checking user access with access token.')
        axios({method: 'get', url:'/access/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
            (response) => {
                console.log('User has access. Backend Response: '+response.data.message)
                this.userAuthenticated = true
            }
            ).catch(error => {
                console.error("User login check failed...")
                this.userAuthenticated = false
            })
    },
    methods: {
        loginUser() {
            
            // Form Validation
            this.errors = []
            if (!this.username) {this.errors.push('Username is empty')}
            if (!this.password) {this.errors.push('Password is empty')}
            console.log(this.errors)

            axios.post('/users/login/', {'username': this.username, 'password': this.password}).then(
                (response) => {
                   
                        this.showLogin = false
                        this.loginResponse = response.data.message
                        this.alertLevel = 'alert alert-success'
                        this.showLoginResponse = true
                        this.userAuthenticated = true
                        localStorage.setItem('access_token', response.data.tokens.access_token)
                        localStorage.setItem('refresh_token', response.data.tokens.refresh_token)
                        localStorage.setItem('first_name', response.data.user.first_name)
                        localStorage.setItem('last_name', response.data.user.last_name)
                        localStorage.setItem('role', response.data.user.role)
                        localStorage.setItem('username', response.data.user.username)
                        this.$store.state.currentUser = {
                            username: response.data.user.username,
                            first_name: response.data.user.first_name,
                            last_name: response.data.user.last_name,
                            role: response.data.user.role
                        }
                }
            ).catch(error => {
                console.log('failed to get login.')
                console.log(error)
                this.loginResponse = error.response.data.error
                this.showLoginResponse = true
                this.alertLevel = 'alert alert-danger'
                console.log("User not logged in")
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                localStorage.removeItem('first_name')
                localStorage.removeItem('last_name')
                localStorage.removeItem('role')
                localStorage.removeItem('username')
                
            })
        }
    }
}
</script>
  
<style>
.login {
    text-align: left;
}

</style>
