resource "aws_cloudwatch_event_rule" "weekly_8pm_cest_rule" {
  name                = "weekly-8pm-cest-lambda-trigger"
  description         = "Triggers the Lambda function weekly at 8 PM CEST (18:00 UTC)"
  schedule_expression = "cron(0 18 ? * 2 *)" # Runs every Monday at 18:00 UTC = 8 PM CEST
}

# Define the target for the EventBridge rule (the Lambda function)
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.weekly_8pm_cest_rule
  arn       = aws_lambda_function.generate_posts_lambda.arn
  target_id = "${var.resources_prefix}weekly-lambda-function-target"
}
