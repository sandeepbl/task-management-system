module "rds" {
  source = "./modules/rds"

  db_instance_identifier = "taskdb"
  db_username            = var.db_username
  db_password            = var.db_password
  db_subnet_group        = module.vpc.db_subnet_group
  security_group_ids     = [module.security_groups.rds_sg_id]
}
