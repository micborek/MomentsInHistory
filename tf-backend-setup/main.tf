# my-project/backend-setup/main.tf

# Configure the AWS provider
provider "aws" {
  region = var.region # Choose your desired region for the backend resources
}

# 1. S3 Bucket for Terraform State
resource "aws_s3_bucket" "terraform_state_bucket" {
  # IMPORTANT: Bucket names must be globally unique.
  # Choose a unique name, e.g., include your project name and account ID.
  bucket = "${var.resources_prefix}tf-state-bucket"

  tags = {
    Name        = "TerraformStateBucket"
    Environment = "Shared"
    ManagedBy   = "Terraform"
  }
}

# NEW: Use aws_s3_bucket_versioning for managing bucket versioning
resource "aws_s3_bucket_versioning" "terraform_state_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# NEW: Use aws_s3_bucket_server_side_encryption_configuration for default encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_bucket_encryption" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256" # Use AES256 for S3-managed encryption
    }
  }
}

# NEW: Use aws_s3_bucket_public_access_block for managing public access settings
# This resource explicitly blocks all public access to the S3 bucket.
resource "aws_s3_bucket_public_access_block" "terraform_state_bucket_public_access_block" {
  bucket = aws_s3_bucket.terraform_state_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# 2. DynamoDB Table for State Locking
resource "aws_dynamodb_table" "terraform_state_lock" {
  # Name of the DynamoDB table for state locking
  # This name is often referenced in the backend configuration
  name         = "${var.resources_prefix}tf-state-lock" # Replace with a unique name
  billing_mode = "PAY_PER_REQUEST" # Cost-effective for infrequent locking

  # The primary key for the lock table MUST be 'LockID'
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S" # String type
  }

  # Enable server-side encryption for data at rest
  server_side_encryption {
    enabled = true
  }

  tags = {
    Name        = "TerraformStateLockTable"
    Environment = "Shared"
    ManagedBy   = "Terraform"
  }
}

# Output the names and ARNs for easy reference
output "s3_bucket_name" {
  description = "Name of the S3 bucket for Terraform state"
  value       = aws_s3_bucket.terraform_state_bucket.bucket
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table for Terraform state locking"
  value       = aws_dynamodb_table.terraform_state_lock.name
}
