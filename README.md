
## Local Deployment with Docker Compose

### Prerequisites

- Docker installed on your local machine.
- Docker Compose installed.

### Directory Structure

Ensure your project directory structure looks like this:

```
task-management-system/
├── backend/
│   ├── Dockerfile
│   ├── ...
├── frontend/
│   ├── Dockerfile
│   ├── ...
└── docker-compose.yml
```

### Steps

1. **Navigate to the Project Directory**

   ```bash
   cd task-management-system
   ```

2. **Create a Docker Compose File**

   Ensure you have a `docker-compose.yml` file in the `task-management-system` directory. This file will define the services for the frontend, backend, and any other dependencies.

3. **Build and Start the Containers**

   ```bash
   docker-compose up --build
   ```

4. **Access the Applications**

   - Backend: `http://localhost:5000`
   - Frontend: `http://localhost:8080`

## Local Troubleshooting 

- Run the backend server on a development framework using the below command. This will run the FlaskAPI server locally in debug mode and will print all requests and errors explicitly. Insert print statements to debug a part of the code and make sure this is removed once the debugging is done. 

    ```bash
    flask run --host="0.0.0.0"
    ```
  
- Call the API endpoints either from command line making sure you start with the `/healthcheck/` and then the `/users/login/` endpoint to obtain the `access_token` and `refresh_token` in order to authenticate all calls to JWT protected endpoints.
- 
## Deployment on AWS ECS with Terraform

### Prerequisites

- AWS account with necessary permissions.
- AWS CLI configured locally.
- Terraform installed.

### Steps

1. **Create an S3 Bucket for Terraform State (if needed)**

   ```bash
   aws s3api create-bucket --bucket your-terraform-state-bucket --region your-region
   ```

2. **Initialize Terraform**

   Navigate to your Terraform configuration directory and initialize Terraform.

   ```bash
   terraform init
   ```

3. **Configure AWS RDS for PostgreSQL**

   Set up a PostgreSQL instance on AWS RDS:

   ```bash
   aws rds create-db-instance \
       --db-instance-identifier taskdb \
       --db-instance-class db.t3.micro \
       --engine postgres \
       --master-username admin \
       --master-user-password yourpassword \
       --allocated-storage 20 \
       --vpc-security-group-ids sg-xxxxxx \
       --db-subnet-group-name your-subnet-group
   ```

4. **Create an ECR Repository**

   ```bash
   aws ecr create-repository --repository-name task-management-backend-repo
   aws ecr create-repository --repository-name task-management-frontend-repo
   ```

5. **Push Docker Images to ECR**

   - Authenticate Docker to your ECR registry:

     ```bash
     aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
     ```

   - Build and push the backend image:

     ```bash
     docker build -t task-management-backend ./backend
     docker tag task-management-backend:latest your-account-id.dkr.ecr.your-region.amazonaws.com/task-management-backend-repo:latest
     docker push your-account-id.dkr.ecr.your-region.amazonaws.com/task-management-backend-repo:latest
     ```

   - Build and push the frontend image:

     ```bash
     docker build -t task-management-frontend ./frontend
     docker tag task-management-frontend:latest your-account-id.dkr.ecr.your-region.amazonaws.com/task-management-frontend-repo:latest
     docker push your-account-id.dkr.ecr.your-region.amazonaws.com/task-management-frontend-repo:latest
     ```

6. **Create a VPC and Subnets**

   Use AWS CLI or the AWS Management Console to create a VPC, subnets, and necessary networking components.

7. **Configure Security Groups**

   Set up security groups to allow traffic between ECS containers and the RDS instance.

8. **Create ECS Cluster**

   ```bash
   aws ecs create-cluster --cluster-name task-management-cluster
   ```

9. **Create Task Definitions for Backend and Frontend**

   Define task definitions for both backend and frontend using the ECS console or CLI.

10. **Deploy ECS Services**

    - Create services for both backend and frontend in the ECS cluster using the defined task definitions.

11. **Configure Log Collection to S3**

    Set up CloudWatch Logs and configure log streams to export logs to an S3 bucket.

    ```bash
    aws logs create-log-group --log-group-name /ecs/task-management-backend
    aws logs create-log-group --log-group-name /ecs/task-management-frontend
    ```

    Configure your ECS task definitions to use these log groups and then set up an S3 export task:

    ```bash
    aws logs create-export-task \
        --task-name export-backend-logs \
        --log-group-name /ecs/task-management-backend \
        --from 0 \
        --to $(date +%s)000 \
        --destination your-s3-bucket \
        --destination-prefix backend-logs

    aws logs create-export-task \
        --task-name export-frontend-logs \
        --log-group-name /ecs/task-management-frontend \
        --from 0 \
        --to $(date +%s)000 \
        --destination your-s3-bucket \
        --destination-prefix frontend-logs
    ```

12. **Initialize and Apply Terraform Configuration**

    - Run the following commands to deploy the infrastructure:

      ```bash
      terraform init
      terraform apply
      ```

    - Follow the prompts and confirm the actions to deploy the infrastructure.

13. **Access the Deployed Applications**

    - Once the ECS services are running, you can access the backend and frontend applications via the load balancer DNS names or configured domain names.

## Conclusion

By following these steps, you can deploy the Task Management System frontend and backend locally using Docker Compose and on AWS ECS using Terraform. Ensure to replace placeholders with actual values and adjust configurations based on your specific requirements. This setup ensures a scalable, production-ready deployment of your application.