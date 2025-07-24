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
        Resource = "arn:aws:logs:${var.region}:*:*" # Grants access to CloudWatch logs in the specified region
      },
      {
        Action   = ["bedrock:InvokeModel"],
        Effect   = "Allow",
        Resource = "arn:aws:bedrock:${var.ai_model_region}:*:*"
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_attach" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_basic_execution_policy.arn
}

