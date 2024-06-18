# Task Management System Frontend Documentation

## Overview

The Task Management System frontend is a Vue.js application designed to interact with the backend API to manage projects, tasks, and users. The application provides a user-friendly interface for managing the various aspects of the system.

## Features

- **Projects View:**
  - Create, retrieve, update, and delete projects.
- **Tasks View:**
  - Add tasks to projects, retrieve all tasks or tasks by project ID, update task details, and delete tasks.
- **Users View:**
  - Register new users, authenticate via login to obtain JWT tokens, refresh tokens, retrieve user information, update user details, and delete users.

## Local Setup

### Prerequisites

- Node.js and npm installed on your local machine.
- Docker installed on your local machine.
- Docker Compose installed.

### Steps

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>/frontend
   ```

2. **Install Dependencies**

   ```bash
   npm install
   ```

3. **Build the Application**

   ```bash
   npm run build
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the `frontend` directory if needed, or configure the environment variables directly in your deployment settings.

5. **Set Up Docker for Local Development**

   - Ensure your Dockerfile in the `frontend` directory is configured to build and serve the application using Nginx.

6. **Run the Frontend with Docker Compose**

   - Use Docker Compose to build and run the frontend service. Ensure the Docker Compose configuration includes both the frontend and backend services.

   ```bash
   docker-compose up --build
   ```

7. **Access the Frontend Application**

   The frontend application will be accessible at `http://localhost:8080`.

## Deployment on AWS ECS

### Prerequisites

- AWS account with necessary permissions.
- AWS CLI configured locally.
- Docker Hub account (or other Docker registry).

### Steps

1. **Containerize the Frontend**

   - Ensure your Dockerfile in the `frontend` directory is correctly set up to build the Vue.js application and serve it using Nginx.

2. **Push Docker Image to Registry**

   - Build and push the Docker image to Docker Hub (or another registry):

     ```bash
     docker build -t <docker-username>/task-management-frontend .
     docker push <docker-username>/task-management-frontend
     ```

3. **Configure ECS Task Definition**

   - Create an ECS task definition that references your Docker image and defines necessary environment variables.

4. **Create ECS Cluster**

   - Create an ECS cluster in your desired AWS region.

5. **Deploy Service on ECS**

   - Create an ECS service using your task definition, configure load balancing if necessary.

6. **Access the Deployed Application**

   - Once deployed, the frontend application will be accessible via the ECS service endpoint.

## Conclusion

The Task Management System frontend provides an intuitive interface for managing projects, tasks, and users. By following these setup instructions, you can deploy and manage the frontend application both locally and on AWS ECS, ensuring scalability and reliability for your application.

