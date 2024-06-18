variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "db_username" {
  description = "The username for the RDS instance"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "The password for the RDS instance"
  type        = string
  sensitive   = true
}
