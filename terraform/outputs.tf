output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "rds_endpoint" {
  value = module.rds.endpoint
}

output "ecs_cluster_id" {
  value = module.ecs.cluster_id
}
