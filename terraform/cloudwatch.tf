resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.resources_prefix}${var.generate_function_name}"
}