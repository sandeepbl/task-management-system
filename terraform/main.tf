provider "aws" {
  region = var.aws_region
}

# Include all the other files
module "vpc" {
  source = "./vpc"
}

module "ecr" {
  source = "./ecr"
}

module "ecs" {
  source = "./ecs"
}

module "rds" {
  source = "./rds"
}

module "security_groups" {
  source = "./security_groups"
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
