<template>
    <div class="container" v-if="userAuthenticated">
        <h1>Users</h1>
        <table class="table table-hover table-striped">
        <thead>
        <tr>
            <th scope="col">Username</th>
            <th scope="col">First Name</th>
            <th scope="col">Last Name</th>
            <th scope="col">Role</th>
            <th scope="col">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="user in $store.state.users" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.first_name }}</td>
            <td>{{ user.last_name }}</td>
            <td>{{ user.role }}</td>
            <td>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#staticBackdrop'+user.id">Edit</button>
                
                <div class="modal fade" :id="'staticBackdrop'+user.id" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="staticBackdropLabel">Modify User</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="modifyUser(user)">
                                <fieldset>
                                    <div class="mb-3 row">
                                        <label for="usernameInput" class="col-sm-2 col-form-label">Username</label>
                                        <div class="col-sm-10">
                                            <input required type="text" id="usernameInput" class="form-control" placeholder="Username" value="{{ user.username }}" v-model="user.username">
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="first_nameInput" class="col-sm-2 col-form-label">First Name</label>
                                        <div class="col-sm-10">
                                            <input required type="text" id="first_nameInput" class="form-control" placeholder="First Name" value="{{ user.first_name }}" v-model="user.first_name">
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="last_nameInput" class="col-sm-2 col-form-label">Last Name</label>
                                        <div class="col-sm-10">
                                            <input required type="text" id="last_nameInput" class="form-control" placeholder="Last Name" value="{{ user.last_name }}" v-model="user.last_name">
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="roleInput" class="col-sm-2 col-form-label">Role</label>
                                        <div class="col-sm-10">
                                            <input required type="text" id="rolerInput" class="form-control" placeholder="Role" value="{{ user.role }}" v-model="user.role">
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </fieldset>
                            </form>
                        </div>
                        </div>
                    </div>
                </div>
                <button type="button" class="btn btn-danger" @click="deleteUser(user)">Delete</button>
            </td>
        </tr>
        </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data () {
        return {
            alertBox: {
                type: '',
                subject: '',
                message: '',
                visible: false
            },
            userAuthenticated: false,
            userLoggedIn: true
        }
    },
    methods: {
        modifyUser(user) {
            var requestBody = {'username':user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'role': user.role}
            console.log(requestBody)
            axios({method: 'put', url:'/users/'+user.id+'/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}, data: requestBody}).then(
            (response) => {
                console.log('User Updated. Backend Response: ' + response.data.message)

                this.alertBox.visible = true
                this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                this.alertBox.subject = 'User Updated'
                this.alertBox.message = response.data.message
                this.getAllUsers()
                this.$emit('hide', true)
                this.$('staticBackdrop'+user.id).modal('hide')
                this.$router.push('/users')
            }
            ).catch(error => {
                console.error("User Update failed...")
                console.log(error)
                if (error.response.data.error === 'token_expired') {
                    axios({method: 'get', url:'/refresh/', headers: { 'Authorization': 'Bearer ' + localStorage.refresh_token}}).then(
                        (response) => {
                            console.log('User access refreshed. Backend Response: ')
                            localStorage.setItem('access_token', response.data.access_token)
                            this.userAuthenticated = true
                        }
                    )
                }
            })
            
        },
        deleteUser(user) {
            if (confirm('Are you sure you want to delete the User: ' + user.first_name + ' ' + user.last_name)) {
                axios({method: 'delete', url:'/users/'+user.id+'/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
                    (response) => {
                        console.log('User Deleted. Backend Response: '+response.data.message)
                        this.alertBox.visible = true
                        this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                        this.alertBox.subject = 'User Deleted'
                        this.alertBox.message = response.data.message
                        this.getAllUsers()
                        this.$router.push('/users')
                    }
                ).catch(error => {
                console.error("User Delete failed...")
                if (error.response.data.error === 'token_expired') {
                    axios({method: 'get', url:'/refresh/', headers: { 'Authorization': 'Bearer ' + localStorage.refresh_token}}).then(
                        (response) => {
                            console.log('User access refreshed. Backend Response: ')
                            localStorage.setItem('access_token', response.data.access_token)
                            this.userAuthenticated = true
                        }
                    )
                }
                if (error.response.data.error === 'not_manager_user') {
                    console.log('User is not a Manager. Not Authorized to Delete Users! Please contact the User Manager.')
                    this.alertBox.visible = true
                    this.alertBox.type = 'alert alert-warning alert-dismissible fade show'
                    this.alertBox.subject = 'User is not a Manager'
                    this.alertBox.message = 'Not Authorized to Delete Users! Please contact the User Manager'
                }
            })

            } else {
                console.log('Delete cancelled...')
            }
        },
        getAllUsers() {
            axios({method: 'get', url:'/users/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
            (response) => {
                console.log("Receiving Users")
                this.$store.state.users = response.data.users
                this.userAuthenticated = true
            }
            ).catch(error => {
                console.log('failed to get users. ' + error)
                
            })
        }
    },
    mounted() {

        axios.get('/healthcheck/').then(
                (response) => {
                    console.log('Backend: '+response.data.message)
                }
            ).catch(error => {
                console.error("Healthcheck Failed... Backend server not responding.")
                })
        
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

        this.getAllUsers()
       
        }  
    }
</script>

<style>

</style>