terraform {
  backend "s3" {
    bucket = "task-management-system-static-storage"
    key    = "tms-terraform-state/env/terraform.tfstate"
    region = "us-east-2"
  }
}
