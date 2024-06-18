import requests

users_list = [
    {
        "username": "sandeep_bharadwaj",
        "password": "TestPass123",
        "first_name": "Sandeep",
        "last_name": "Bharadwaj",
        "role": "Admin"
    },
    {
        "username": "john_doe",
        "password": "Pass1234",
        "first_name": "John",
        "last_name": "Doe",
        "role": "User"
    },
    {
        "username": "jane_smith",
        "password": "Secure5678",
        "first_name": "Jane",
        "last_name": "Smith",
        "role": "User"
    },
    {
        "username": "alice_jones",
        "password": "Alice@901",
        "first_name": "Alice",
        "last_name": "Jones",
        "role": "Manager"
    },
    {
        "username": "bob_brown",
        "password": "Bob2020",
        "first_name": "Bob",
        "last_name": "Brown",
        "role": "User"
    },
    {
        "username": "charlie_wilson",
        "password": "Char@345",
        "first_name": "Charlie",
        "last_name": "Wilson",
        "role": "User"
    },
    {
        "username": "emily_davis",
        "password": "Emily!789",
        "first_name": "Emily",
        "last_name": "Davis",
        "role": "User"
    },
    {
        "username": "frank_miller",
        "password": "Frank_654",
        "first_name": "Frank",
        "last_name": "Miller",
        "role": "Manager"
    },
    {
        "username": "grace_johnson",
        "password": "Grace2021",
        "first_name": "Grace",
        "last_name": "Johnson",
        "role": "User"
    },
    {
        "username": "henry_taylor",
        "password": "Henry#123",
        "first_name": "Henry",
        "last_name": "Taylor",
        "role": "User"
    },
    {
        "username": "irene_moore",
        "password": "Irene789",
        "first_name": "Irene",
        "last_name": "Moore",
        "role": "Manager"
    },
    {
        "username": "jack_white",
        "password": "Jack@456",
        "first_name": "Jack",
        "last_name": "White",
        "role": "User"
    },
    {
        "username": "karen_hall",
        "password": "Karen789",
        "first_name": "Karen",
        "last_name": "Hall",
        "role": "User"
    },
    {
        "username": "leo_green",
        "password": "Leo@321",
        "first_name": "Leo",
        "last_name": "Green",
        "role": "User"
    },
    {
        "username": "mia_clark",
        "password": "Mia_567",
        "first_name": "Mia",
        "last_name": "Clark",
        "role": "Manager"
    },
    {
        "username": "noah_adams",
        "password": "Noah@890",
        "first_name": "Noah",
        "last_name": "Adams",
        "role": "User"
    },
    {
        "username": "olivia_smith",
        "password": "Olivia#234",
        "first_name": "Olivia",
        "last_name": "Smith",
        "role": "User"
    },
    {
        "username": "paul_lewis",
        "password": "Paul1234",
        "first_name": "Paul",
        "last_name": "Lewis",
        "role": "Manager"
    },
    {
        "username": "quincy_walker",
        "password": "Quincy_567",
        "first_name": "Quincy",
        "last_name": "Walker",
        "role": "User"
    },
    {
        "username": "rachel_king",
        "password": "Rachel#890",
        "first_name": "Rachel",
        "last_name": "King",
        "role": "User"
    },
    {
        "username": "samuel_lee",
        "password": "Sam1234",
        "first_name": "Samuel",
        "last_name": "Lee",
        "role": "User"
    }
]

users_list = []

base_url = 'http://192.168.1.12:5000'
register_user_endpoint = '/users/register/'
for user in users_list:
    print(user['username'], requests.post(f'{base_url}{register_user_endpoint}', json=user))

creds = {
    "username": "sandeep_bharadwaj",
    "password": "TestPass123"
}

projects_list = [
    {
    "title": "Task Management System Backend",
    "description": "Tasks related to the Backend",
    "manager_user_id": 4
    },
    {
    "title": "Task Management System Frontend",
    "description": "Tasks related to the Frontend",
        "manager_user_id": 8
    },
    {
        "title": "Task Management System Deployment",
        "description": "Tasks related to the Deployment",
        "manager_user_id": 11
    }
]

projects_list = []

user_login = requests.post(f"{base_url}/users/login/", json=creds)

access_token = user_login.json()['tokens']['access_token']

headers = {"Authorization": f"Bearer {access_token}"}
create_project_url = '/projects/create/'

for project in projects_list:
    res = requests.post(f'{base_url}{create_project_url}', json=project, headers=headers)
    print(res)
    print(res.json())

tasks_list = [
    {
        "assigned_user_id": 1,
        "description": "Provide fields to register new user",
        "project_id": 2,
        "title": "Make User Registration Page"
    },
    {
        "assigned_user_id": 1,
        "description": "Create Unit Tests for Backend API Endpoints",
        "project_id": 1,
        "title": "Create Unit Tests for Backend"
    },
    {
        "assigned_user_id": 1,
        "description": "Provide UI to Login registered user",
        "project_id": 2,
        "title": "Updated: Make User Login Page"
    },
    {
        "assigned_user_id": 1,
        "description": "Setup the CICD pipline to Deploy the Backend and Frontend",
        "project_id": 2,
        "title": "Setup CICD Pipeline"
    }
]

# tasks_list = []

create_task_url = '/tasks/create/'
for task in tasks_list:
    res = requests.post(f'{base_url}{create_task_url}', json=task, headers=headers)
    print(res)
    print(res.json())