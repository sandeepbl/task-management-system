<template>
    <div class="container" v-if="userAuthenticated">
        <h1>Tasks</h1>
        <div v-if="alertBox.visible" :class="alertBox.type" role="alert">
            <strong>{{ alertBox.subject }}</strong> {{ alertBox.message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <button style="float:right" type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#createTask">Create New</button>
        <div class="modal fade" id="createTask" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="createTaskLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="createTaskLabel">Create New Task</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createTask(newTask)">
                        <fieldset>
                            <div class="mb-3 row">
                                <label for="titleInput" class="col-sm-2 col-form-label">Task Title</label>
                                <div class="col-sm-10">
                                    <input required type="text" id="titleInput" class="form-control" placeholder="Task Title" value="" v-model="newTask.title">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label for="descriptionInput" class="col-sm-2 col-form-label">Task Description</label>
                                <div class="col-sm-10">
                                    <textarea rows="6" type="text" id="descriptionInput" class="form-control" placeholder="Task Description" value="" v-model="newTask.description"></textarea>
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label for="managerInput" class="col-sm-2 col-form-label">Project ID</label>
                                <div class="col-sm-10">
                                    <input type="text" id="managerInput" class="form-control" placeholder="Project ID" value="" v-model="newTask.project_id">
                                </div>
                            </div>
                            <div class="mb-3 row">
                                <label for="managerInput" class="col-sm-2 col-form-label">Assigned User ID</label>
                                <div class="col-sm-10">
                                    <input type="text" id="managerInput" class="form-control" placeholder="Assigned User ID" value="" v-model="newTask.assigned_user_id">
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
            <th scope="col">Project Name</th>
            <th scope="col">Assignee</th>
            <th scope="col" v-if="$store.state.currentUser.role == 'Admin'">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="task in $store.state.tasks" :key="task.id">
            <td>{{ task.title }}</td>
            <td>{{ task.description }}</td>
            <td>{{ task.project_title }}</td>
            <td>{{ task.assigned_user }}</td>
            <td  v-if="$store.state.currentUser.role == 'Admin'">
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#staticBackdrop'+task.id">Edit</button>
                
                <div class="modal fade" :id="'staticBackdrop'+task.id" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="staticBackdropLabel">Modify Task</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="modifyTask(task)">
                                <fieldset>
                                    <div class="mb-3 row">
                                        <label for="titleInput" class="col-sm-2 col-form-label">Task Title</label>
                                        <div class="col-sm-10">
                                            <input required type="text" id="titleInput" class="form-control" placeholder="Task Title" value="{{ task.title }}" v-model="task.title">
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="descriptionInput" class="col-sm-2 col-form-label">Task Description</label>
                                        <div class="col-sm-10">
                                            <textarea rows="6" type="text" id="descriptionInput" class="form-control" placeholder="Task Description" value="{{ task.description }}" v-model="task.description"></textarea>
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="managerInput" class="col-sm-2 col-form-label">Project ID</label>
                                        <div class="col-sm-10">
                                            <input type="text" id="managerInput" class="form-control" placeholder="Project ID" value="{{ task.project_id }}" v-model="task.project_id">
                                        </div>
                                    </div>
                                    <div class="mb-3 row">
                                        <label for="managerInput" class="col-sm-2 col-form-label">Assigned User ID</label>
                                        <div class="col-sm-10">
                                            <input type="text" id="managerInput" class="form-control" placeholder="Assigned User ID" value="{{ task.assigned_user_id }}" v-model="task.assigned_user_id">
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Submit</button>
                                </fieldset>
                            </form>
                        </div>
                        </div>
                    </div>
                </div>
                <button type="button" class="btn btn-danger" @click="deleteTask(task)">Delete</button>
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
            newTask:{},
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
        createTask(task) {
            console.log(task)
            var requestBody = {'title':task.title, 'description': task.description, 'project_id': task.project_id, 'assigned_user_id': task.assigned_user_id}
            console.log(requestBody)
            axios({method: 'post', url:'/tasks/create/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}, data: requestBody}).then(
            (response) => {
                console.log('Task Created. Backend Response: ' + response)

                this.alertBox.visible = true
                this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                this.alertBox.subject = 'Task Created'
                this.alertBox.message = response.data.message
                this.getAllTasks()
                this.$router.push('/tasks')
                }
                ).catch(error => {
                    console.error("Task Create failed...")
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
                    console.log('User is not a Registered User. Not Authorized to Create Tasks! Please contact the Team.')
                    this.alertBox.visible = true
                    this.alertBox.type = 'alert alert-warning alert-dismissible fade show'
                    this.alertBox.subject = 'User is not a Registered User'
                    this.alertBox.message = 'Not Authorized to Delete Tasks! Please contact the Team'
                }
                }
            )
        },

        modifyTask(task) {
            var requestBody = {'title':task.title, 'description': task.description, 'project_id': task.project_id, 'assigned_user_id': task.assigned_user_id}
            axios({method: 'put', url:'/tasks/'+task.id+'/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}, data: requestBody}).then(
            (response) => {
                console.log('Task Updated. Backend Response: ' + response.data.message)

                this.alertBox.visible = true
                this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                this.alertBox.subject = 'Task Updated'
                this.alertBox.message = response.data.message
                this.getAllTasks()
                this.$router.push('/tasks')
            }
            ).catch(error => {
                console.error("Task Update failed...")
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
        deleteTask(task) {
            if (confirm('Are you sure you want to delete the Task: ' + task.title)) {
                axios({method: 'delete', url:'/tasks/'+task.id+'/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
                    (response) => {
                        console.log('Task Deleted. Backend Response: '+response.data.message)
                        this.alertBox.visible = true
                        this.alertBox.type = 'alert alert-success alert-dismissible fade show'
                        this.alertBox.subject = 'Task Deleted'
                        this.alertBox.message = response.data.message
                        this.getAllTasks()
                        this.$router.push('/tasks')
                    }
                ).catch(error => {
                console.error("Task Delete failed...")
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
                    console.log('User is not a Manager. Not Authorized to Delete Tasks! Please contact the Task Manager.')
                    this.alertBox.visible = true
                    this.alertBox.type = 'alert alert-warning alert-dismissible fade show'
                    this.alertBox.subject = 'User is not a Manager'
                    this.alertBox.message = 'Not Authorized to Delete Tasks! Please contact the Task Manager'
                }
            })

            } else {
                console.log('Delete cancelled...')
            }
        },
        getAllTasks() {
            axios({method: 'get', url:'/tasks/', headers: { 'Authorization': 'Bearer ' + localStorage.access_token}}).then(
            (response) => {
                console.log("Receiving Tasks")
                // console.log(response.data.task_list)

                this.$store.state.tasks = response.data.task_list
                this.userAuthenticated = true
            }
            ).catch(error => {
                console.log('failed to get tasks. ' + error)
                
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
                console.log(response.data.access_token)
                localStorage.setItem('access_token', response.data.access_token)
                this.userAuthenticated = true
                
            }
            )
                }
                this.userAuthenticated = false
                this.$router.push('/login')
            })

        this.getAllTasks()
        
    }
}

</script>
