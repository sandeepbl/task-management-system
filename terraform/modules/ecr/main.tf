resource "aws_ecr_repository" "main" {
  name = "tms-ecr-repo"
}
output "repository_url" {
  value = aws_ecr_repository.main.repository_url
}