locals {
  lambda_source_path = "${path.module}/../src" # This is correct for your structure
}

resource "null_resource" "install_lambda_dependencies" {
  triggers = {
    dependencies_hash      = filemd5("${local.lambda_source_path}/requirements.txt")
    code_trigger_file_hash = filemd5("${local.lambda_source_path}/generate_post.py")
  }

  provisioner "local-exec" {
    command     = "pip install -r requirements.txt -t ."
    working_dir = local.lambda_source_path
  }
}

# Data source to create a .zip archive of the Lambda function code and its dependencies
data "archive_file" "lambda_zip_package" {
  type        = "zip"
  source_dir  = local.lambda_source_path
  output_path = "${var.resources_prefix}${var.generate_function_name}.zip"

  # Ensure dependencies are installed before archiving
  depends_on = [
    null_resource.install_lambda_dependencies
  ]
}

# AWS Lambda Function Resource
resource "aws_lambda_function" "generate_posts_lambda" {
  function_name = "${var.resources_prefix}${var.generate_function_name}"
  handler       = "generate_post.lambda_handler"
  runtime       = var.runtime
  role          = aws_iam_role.lambda_exec_role.arn
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  # The filename attribute points to the generated zip file
  filename = data.archive_file.lambda_zip_package.output_path
  # source_code_hash ensures Terraform detects changes in the zip file content
  source_code_hash = data.archive_file.lambda_zip_package.output_base64sha256
}