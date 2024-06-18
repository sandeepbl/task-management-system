
# Task Management System Backend Documentation

## Overview

The Task Management System backend is a Flask API application designed to manage projects, tasks, and users through a RESTful interface. It utilizes PostgreSQL for data storage and authentication via JWT (JSON Web Tokens).

## Features

- **Projects Management:**
  - Create, retrieve, update, and delete projects.
- **Tasks Management:**
  - Add tasks to projects, retrieve all tasks or tasks by project ID, update task details, and delete tasks.
- **User Management:**
  - Register new users, authenticate via login to obtain JWT tokens, refresh tokens, retrieve user information, update user details, and delete users.
- **Authorization:**
  - JWT tokens provide access and admin authorization checks.
- **Health Check and Access Validation:**
  - Endpoint to check API server status and validate JWT token access.


## Database Setup

### RDS with PostgresSQL running on AWS

- Using the AWS Management console, spinup a database with the PostgresSQL engine.
- Note the credentials as they will be used in the .env or as environment variables in all our local and cloud deployments

### Database Schema

- The schema for the tables of Users, Tasks and Projects and maintained in the `models.py` file of the Python Flask application.
- The tables are defined in classes with the `init` and other builtin methods to get and set information from the data tables.

### Database Migration

Flask-Migrate is a plugin to Flask API that provides database migration methods to create migration scripts , updgrade and rollback or downgrade the changes needed to be made on the data tables. This plugin is installed by running the following command.

```bash
pip install Flask-Migrate
```

Once the required changes are made to the database tables, run the `db init` command to initialize the migration. This prepares the folder structure where the migration scripts are stored.

```bash
flask db init
```
Now you are ready to generate the migration scripts with the `db migrate` command. The generated scripts are stored in the above created **migrations** folder.

```bash
flask db migrate -m "migration commit message"
```
Now you are ready to perform the database migration with the `upgrade` command.
```bash
flask db upgrade
```
If the desired outcome is not achieved, Flask-Migrate give the option of `downgrade` to rollback the changes with this command.
```bash
flask db downgrade
```
The migration scripts are version controlled by the library and can be checked in to the source controlled repository.  


## Swagger UI 

Swagger UI is Open API tool that can be used to visualize, test and interact with the API for understand and debugging our API application when setup right. This library is installed from the `pip` repository using this command.
```bash
pip install flask-swagger-ui
```
Use the Swagger Editor also provided by the Open API community to quickly build the UI. The config file can be downloaded in the `json` or `yaml` formats can be used to include the tool as a part of the application and source controlled as code. Once fully setup the UI is available at the http://localhost:5000/swagger endpoint.

## Local Setup

### Prerequisites

- Docker installed on your local machine.
- Docker Compose installed.

### Steps

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Configure Environment Variables**

   Create a `.env` file in the `backend` directory and define the following variables:

   ```plaintext
   FLASK_ENV=development
   DATABASE_URL=postgresql://postgres:password@localhost:5432/taskdb
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

   Replace `password` with your PostgreSQL password.

3. **Build and Run the Backend**

   ```bash
   docker-compose up --build
   ```

4. **Access the API**

   The backend API is accessible at `http://localhost:5000`.

## Deployment on AWS ECS

### Prerequisites

- AWS account with necessary permissions.
- AWS CLI configured locally.
- Docker Hub account (or other Docker registry).

### Steps

1. **Containerize the Backend**

   - Ensure the `Dockerfile` in the `backend` directory is configured to use Gunicorn and expose port `5000`.

2. **Push Docker Image to Registry**

   - Build and push the Docker image to Docker Hub (or another registry):

     ```bash
     docker build -t <docker-username>/task-management-backend .
     docker push <docker-username>/task-management-backend
     ```

3. **Configure ECS Task Definition**

   - Create an ECS task definition that references your Docker image and defines environment variables.

4. **Create ECS Cluster**

   - Create an ECS cluster in your desired AWS region.

5. **Deploy Service on ECS**

   - Create an ECS service using your task definition, configure load balancing if necessary.

6. **Access the Deployed API**

   - Once deployed, the backend API will be accessible via the ECS service endpoint.

## Conclusion

The Task Management System backend provides a robust API for managing projects, tasks, and users securely. By following these setup instructions, you can deploy and manage the backend both locally and on AWS ECS, ensuring scalability and reliability for your application.

