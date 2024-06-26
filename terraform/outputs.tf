output "backend_ecr_repository_url" {
  value = module.ecr.backend_repository_url
}
output "frontend_ecr_repository_url" {
  value = module.ecr.frontend_repository_url
}

output "rds_endpoint" {
  value = module.rds.endpoint
}

output "rds_username" {
  value = module.rds.username
}

output "ecs_cluster_id" {
  value = module.ecs.cluster_id
}

output "ecs_cluster_arn" {
  value = module.ecs.cluster_arn
}

output "ecs_cluster_name" {
  value = module.ecs.cluster_name
}