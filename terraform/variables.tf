variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-2"
}

variable "db_username" {
  description = "The username for the RDS instance"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "The password for the RDS instance"
  type        = string
  sensitive   = true
  default     = "SuperSecret12345"
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr_blocks" {
  description = "List of CIDR blocks for subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-2a", "us-east-2b"]
}
