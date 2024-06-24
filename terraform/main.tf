provider "aws" {
  region = var.aws_region
}

module "security_groups" {
  source = "./modules/security_groups"

  vpc_id = module.vpc.vpc_id
}

module "ecr" {
  source = "./modules/ecr"
}

module "ecs" {
  source = "./modules/ecs"
}

module "rds" {
  source = "./modules/rds"
}

module "iam" {
  source = "./modules/iam"
}

resource "aws_iam_user" "test_admin" {
  name = "TestAdmin"
}

resource "aws_db_instance" "database-tms" {
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  engine               = "postgres"
  username             = "postgres"
  password             = "SuperSecret12345"
}

resource "aws_s3_bucket" "logs_bucket" {
  bucket = "my-app-logs-bucket"
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs_task_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}
data "aws_caller_identity" "current" {}

resource "aws_iam_policy" "ecs_task_logging_policy" {
  name        = "ecs_task_logging_policy"
  description = "Policy for ECS tasks to write logs to S3 and CloudWatch"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.logs_bucket.bucket}/*",
          "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:flask-app-logs:*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attachment" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_logging_policy.arn
}

output "s3_bucket_name" {
  value = aws_s3_bucket.logs_bucket.bucket
}

output "ecs_task_execution_role_arn" {
  value = aws_iam_role.ecs_task_execution_role.arn
}

module "vpc" {
  source = "./modules/vpc"
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "subnet_ids" {
  value = module.vpc.subnet_ids
}


resource "aws_iam_policy" "ecr_create_repository_policy" {
  name        = "ECRCreateRepositoryPolicy"
  description = "Policy to allow creating ECR repositories"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "ecr:CreateRepository",
          "ecr:DescribeRepositories"
        ],
        Resource = "arn:aws:ecr:us-east-2:730335377087:repository/*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "test_admin_attach" {
  user       = aws_iam_user.test_admin.name
  policy_arn = aws_iam_policy.ecr_create_repository_policy.arn
}
