resource "aws_ecr_repository" "flask_api_repo" {
  name = "task-management-backend-repo"
}

resource "aws_ecr_repository" "frontend_repo" {
  name = "task-management-frontend-repo"
}
