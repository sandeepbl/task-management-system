<template>
    <div class="container" v-if="userAuthenticated">
        <h1>Projects</h1>
        <div v-if="alertBox.visible" :class="alertBox.type" role="alert">
            <strong>{{ alertBox.subject }}</strong> {{ alertBox.message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <button style="float:right" type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#createProject">Create New</button>
        <div class="modal fade" id="createProject" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="createProjectLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="createProjectLabel">Create New Project</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createProject(newProject)">
                        <fieldset>
                            <div class="mb-3 row">
                                <label for="titleInput" class="col-sm-2 col-form-label">Project Title</label>
                                <div class="col-sm-10">
                                    <input required type="text" id="titleInput" class="form-control" placeholder="Project Title" value="" v-model="newProject.title">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label for="descriptionInput" class="col-sm-2 col-form-label">Project Description</label>
                                <div class="col-sm-10">
                                    <textarea rows="6" type="text" id="descriptionInput" class="form-control" placeholder="Project Description" value="" v-model="newProject.description"></textarea>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label for="managerInput" class="col-sm-2 col-form-label">Project Manager</label>
                                <div class="col-sm-10">
                                    <input type="text" id="managerInput" class="form-control" placeholder="Project Manager" value="" v-model="newProject.manager_user_id">
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </fieldset>
                    </form>
                </div>
                </div>
            </div>
        </div>

        <table class="table table-hover table-striped">
        <thead>
        <tr>
            <th scope="col">Title</th>
            <th scope="col">Description</th>
            <th scope="col">Project Manager</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="project in $store.state.projects" :key="project.id">
            <td><router-link :to="'/tasks/'+project.id">{{ project.title }}</router-link></td>
            <td>{{ project.description }}</td>
            <td>{{ project.manager }}</td>
            <td>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#staticBackdrop'+project.id">Edit</button>
                
                <div class="modal fade" :id="'staticBackdrop'+project.id" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="staticBackdropLabel">Modify Project</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="modifyProject(project)">
                                <fieldset>
                                    <div class="mb-3 row">
                                        <label for="titleInput" class="col-sm-2 col-form-label">Project Title</label>
                                        <div class="col-sm-10">
                                            <input required type="text" id="titleInput" class="form-control" placeholder="titleInput" value="{{ project.title }}" v-model="project.title">
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="descriptionInput" class="col-sm-2 col-form-label">Project Description</label>
                                        <div class="col-sm-10">
                                            <textarea rows="6" type="text" id="descriptionInput" class="form-control" placeholder="descriptionInput" value="{{ project.description }}" v-model="project.description"></textarea>
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="managerInput" class="col-sm-2 col-form-label">Project Manager</label>
                                        <div class="col-sm-10">
                                            <input type="text" id="managerInput" class="form-control" placeholder="managerInput" value="{{ project.manager }}" v-model="project.manager">
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </fieldset>
                            </form>
                        </div>
                        </div>
                    </div>
                </div>
                <button type="button" class="btn btn-danger" @click="deleteProject(project)">Delete</button>
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
            newProject:{},
            alertBox: {
                type: '',
                subject: '',
                message: '',
                visible: false
            },
            userAuthenticated: false
        }
    },
    methods: {
        createProject(project) {
            var requestBody = {'title':project.title, 'description': project.description, 'manager_user_id': project.manager_user_id}
            console.log(requestBody)
            axios({method: 'post', url:'/projects/create/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}, data: requestBody}).then(
            (response) => {
                console.log('Project Created. Backend Response: ' + response)

                this.alertBox.visible = true
                this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                this.alertBox.subject = 'Project Created'
                this.alertBox.message = response.data.message
                this.getAllProjects()
                this.$router.push('/projects')
            }
            ).catch(error => {
                console.error("Project Create failed...")
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
                if (error.response.data.error === 'not_registered_user') {
                    console.log('User is not a Registered User. Not Authorized to Create Projects! Please contact the Team.')
                    this.alertBox.visible = true
                    this.alertBox.type = 'alert alert-warning alert-dismissible fade show'
                    this.alertBox.subject = 'User is not a Registered User'
                    this.alertBox.message = 'Not Authorized to Delete Projects! Please contact the Team'
                    this.$router.push('/projects')
                }
                }
            )
        },

        modifyProject(project) {
            var requestBody = {'title':project.title, 'description': project.description, 'manager_user_id': project.manager_user_id}
            axios({method: 'put', url:'/projects/'+project.id+'/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}, data: requestBody}).then(
            (response) => {
                console.log('Project Updated. Backend Response: ' + response.data.message)

                this.alertBox.visible = true
                this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                this.alertBox.subject = 'Project Updated'
                this.alertBox.message = response.data.message
                this.getAllProjects()
                this.$router.push('/projects')
            }
            ).catch(error => {
                console.error("Project Update failed...")
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
                if (error.response.data.error === 'not_manager_user') {

                    console.log('User is not a Manager. Not Authorized to Delete Projects! Please contact the Project Manager.')
                    this.alertBox.visible = true
                    this.alertBox.type = 'alert alert-warning alert-dismissible fade show'
                    this.alertBox.subject = 'User is not a Manager'
                    this.alertBox.message = 'Not Authorized to Delete Projects! Please contact the Project Manager'
                }
            })
            
        },
        deleteProject(project) {
            if (confirm('Are you sure you want to delete the Project: ' + project.title)) {
                axios({method: 'delete', url:'/projects/'+project.id+'/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
                    (response) => {
                        console.log('Project Deleted. Backend Response: '+response.data.message)
                        this.alertBox.visible = true
                        this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                        this.alertBox.subject = 'Project Deleted'
                        this.alertBox.message = response.data.message
                        this.getAllProjects()
                        this.$router.push('/projects')
                    }
                ).catch(error => {
                console.error("Project Delete failed...")
                if (error.response.data.error === 'token_expired') {
                    console.error("token_expired...")
                    axios({method: 'get', url:'/refresh/', headers: { 'Authorization': 'Bearer ' + localStorage.refresh_token}}).then(
                        (response) => {
                            console.log('User access refreshed. Backend Response: ')
                            localStorage.setItem('access_token', response.data.access_token)
                            this.userAuthenticated = true
                        }
                    )
                }
                if (error.response.data.error === 'not_manager_user') {
                    console.log('User is not a Manager. Not Authorized to Delete Projects! Please contact the Project Manager.')
                    this.alertBox.visible = true
                    this.alertBox.type = 'alert alert-warning alert-dismissible fade show'
                    this.alertBox.subject = 'User is not a Manager'
                    this.alertBox.message = 'Not Authorized to Delete Projects! Please contact the Project Manager'
                }
            })

            } else {
                console.log('Delete cancelled...')
            }
        },
        getAllProjects() {
            axios({method: 'get', url:'/projects/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
            (response) => {
                console.log("Receiving Projects")
                this.$store.state.projects = response.data.projects
                this.$store
                this.userAuthenticated = true
            }
            ).catch(error => {
                console.log('failed to get Projects. ' + error)
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
                if (error.response.data.error === 'token_expired') {
                    axios({method: 'get', url:'/refresh/', headers: { 'Authorization': 'Bearer ' + localStorage.refresh_token}}).then(
                        (response) => {
                            console.log('User access refreshed. Backend Response: ')
                            localStorage.setItem('access_token', response.data.access_token)
                            this.userAuthenticated = true
                        }
                    )
                }
                this.userAuthenticated = false
                this.$router.push('/login')
            })

        this.getAllProjects()
        
    }
}

</script>
