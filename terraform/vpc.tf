module "vpc" {
  source = "./modules/vpc"

  aws_region = var.aws_region
}
