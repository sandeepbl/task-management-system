resource "aws_ecr_repository" "backend" {
  name = "tms-backend-ecr-repo"
}
resource "aws_ecr_repository" "frontend" {
  name = "tms-frontend-ecr-repo"
}
output "backend_repository_url" {
  value = aws_ecr_repository.backend.repository_url
}
output "frontend_repository_url" {
  value = aws_ecr_repository.frontend.repository_url
}