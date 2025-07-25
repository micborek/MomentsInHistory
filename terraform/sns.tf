resource "aws_sns_topic" "email_notifications_topic" {
  name         = "${var.resources_prefix}notifications"
  display_name = "Email Notification"
  # }
}

resource "aws_sns_topic_subscription" "primary_alert_email" {
  topic_arn = aws_sns_topic.email_notifications_topic.arn
  protocol  = "email"
  endpoint  = var.primary_alert_email_endpoint
}