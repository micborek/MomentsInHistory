# IAM Role for the Lambda function
resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.resources_prefix}lambda-exec-role"

  # Defines the trust policy that allows Lambda to assume this role
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

# IAM Policy for basic Lambda execution and CloudWatch logging
resource "aws_iam_policy" "lambda_basic_execution_policy" {
  name = "${var.resources_prefix}lambda-execution-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect   = "Allow",
        Resource = aws_cloudwatch_log_group.lambda_log_group.arn
      },
      {
        Action   = ["bedrock:InvokeModel"],
        Effect   = "Allow",
        Resource = "arn:aws:bedrock:*:*:*"
      },
      {
        Effect   = "Allow",
        Action   = ["secretsmanager:GetSecretValue"],
        Resource = [
          aws_secretsmanager_secret.facebook_page_token.arn,
          aws_secretsmanager_secret.facebook_page_id.arn
        ]
      },
      {
        Effect = "Allow",
        Action = ["sns:Publish"],
        Resource = [aws_sns_topic.email_notifications_topic.arn]
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_basic_execution_policy.arn
}

