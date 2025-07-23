provider "aws" {
  region = var.region
}

# Backend configuration for state storage
# This block tells Terraform where to store its state file
terraform {
  backend "s3" {
    # Replace with the actual name of the S3 bucket created in Step 1
    bucket = "${var.resources_prefix}tf-state-bucket"

    # Key is the path within the S3 bucket for THIS project's state file
    # Use a clear, unique path for each Terraform project/module
    key    = "my-lambda-project/terraform.tfstate" # Example: project-name/path/to/state.tfstate

    # The region where your S3 bucket is located (must match the bucket's region)
    region = var.region

    # Enable encryption for the state file at rest (matches S3 bucket config)
    encrypt = true

    # The name of the DynamoDB table created in Step 1 for state locking
    dynamodb_table = "${var.resources_prefix}tf-state-lock"
  }
}