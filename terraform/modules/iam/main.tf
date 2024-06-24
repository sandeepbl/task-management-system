resource "aws_iam_user" "test_admin" {
  name = "TMSAdmin"
}

resource "aws_iam_user_policy_attachment" "test_admin_attach" {
  user       = aws_iam_user.test_admin.name
  policy_arn = aws_iam_policy.rds_full_access.arn
}
