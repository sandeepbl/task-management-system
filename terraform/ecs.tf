module "ecs" {
  source = "./modules/ecs"

  cluster_name     = "task-management-cluster"
  backend_repo_url = module.ecr.flask_api_repo.repository_url
  frontend_repo_url = module.ecr.frontend_repo.repository_url
}
