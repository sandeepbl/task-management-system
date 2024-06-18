<template>
  <div class="container">
    <h2>Register New User</h2>
    <div class="registerationForm">
    <form @submit.prevent="registerUser">
        <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input required type="text" class="form-control" id="username" aria-describedby="usernameHelp" v-model="username">
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input required type="password" class="form-control" id="password" v-model="password">
        </div>
        <div class="mb-3">
            <label for="first_name" class="form-label">First Name</label>
            <input required type="text" class="form-control" id="first_name" aria-describedby="first_nameHelp" v-model="first_name">
        </div>
        <div class="mb-3">
            <label for="last_name" class="form-label">Last Name</label>
            <input required type="text" class="form-control" id="last_name" aria-describedby="last_nameeHelp" v-model="last_name">
        </div>
        <div class="mb-3">
            <label for="role" class="form-label">User Role</label>
            <input type="text" class="form-control" id="role" aria-describedby="roleHelp" v-model="role" disabled readonly>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    </div>
    <div v-if="alert.visibility">{{ alert.registrationMessage}}</div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
    data () {
        return {
            username: '',
            password: '',
            first_name: '',
            last_name: '',
            role: 'User',
            alert: {
                visibility: false,
                registrationMessage: '',
                alertLevel: 'alert alert-warning alert-dismissible fade show'
            }
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
                this.$router.push('/login')
            })
    },
    methods: {
        registerUser() {
            const authHeader = { headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}
            var registerationData = {'username': this.username, 
                                    'password': this.password, 
                                    'first_name': this.first_name, 
                                    'last_name': this.last_name, 
                                    'role': this.role}

            axios.post('/users/register/', registerationData, authHeader).then(
                (response) => {
                    this.alert.registrationMessage = 'Registration was successful! User: ' + this.first_name + ' ' + this.last_name
                    this.alert.visibility = true
                }
            ).catch(error => {                
                this.alert.registrationMessage = registrationMessage = 'Registration was Failed! User: ' + error.response.data.error
                this.alert.visibility = true
                console.log(error.response.data.error)
            })
        }
    }
}
</script>

<style scoped>
.container {
    border: 20px;
}
.registerationForm {
    margin: auto;
    width: 800px;
    border: 2px solid lightgray;
    padding: 10px;
    border-radius: 10px;
    text-align: left;
    text-indent: 10px;
}
.registerationFormButton {
    width: fit-content;
}
</style>