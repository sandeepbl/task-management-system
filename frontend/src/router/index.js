import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import TasksListView from '../views/TasksListView.vue'
import ProjectsListView from '../views/ProjectsListView.vue'
import UsersListView from '../views/UsersListView.vue'
import ProjectTasksList from '@/components/ProjectTasksList.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: TasksListView
  },
  {
    path: '/projects',
    name: 'projects',
    component: ProjectsListView
  },
  {
    path: '/users',
    name: 'users',
    component: UsersListView
  },
  {
    path: '/tasks/:pid',
    name: 'projecttasks',
    component: ProjectTasksList
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
