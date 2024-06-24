resource "aws_iam_policy" "rds_full_access" {
  name        = "RDSFullAccess"
  description = "Provides full access to RDS resources"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "rds:CreateDBInstance",
          "rds:DeleteDBInstance",
          "rds:DescribeDBInstances",
          "rds:ModifyDBInstance",
          "rds:StopDBInstance",
          "rds:StartDBInstance",
          "rds:RebootDBInstance",
          "rds:ListTagsForResource",
          "rds:AddTagsToResource",
          "rds:RemoveTagsFromResource"
        ],
        Resource = "*"
      }
    ]
  })
}
