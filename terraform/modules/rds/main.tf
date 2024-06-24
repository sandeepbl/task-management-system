resource "aws_db_instance" "main" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "16.2"
  instance_class       = "db.t3.micro"
  username             = "postgres"
  password             = "SuperSecret12345"
  parameter_group_name = "default.postgres16"
  identifier           = "database-tms"
  skip_final_snapshot  = true
  publicly_accessible  = true
}

output "endpoint" {
  value = aws_db_instance.main.endpoint
}

output "username" {
  value = aws_db_instance.main.username
}