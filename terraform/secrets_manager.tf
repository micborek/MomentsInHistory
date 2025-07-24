resource "aws_secretsmanager_secret" "facebook_page_token" {
  name        = "${var.resources_prefix}facebook-page-access-token" # Use an environment suffix
  description = "Meta Graph API Page Access Token for managing Facebook Page"
}

resource "aws_secretsmanager_secret" "facebook_page_id" {
  name        = "${var.resources_prefix}facebook-page-id"
  description = "Facebook Page ID for the managed page"
}