# my-project/backend-setup/main.tf

# Configure the AWS provider
provider "aws" {
  region = var.region
}

#S3 Bucket for Terraform State
resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "${var.resources_prefix}tf-state-bucket"

  tags = {
    Name        = "TerraformStateBucket"
    Environment = "Shared"
    ManagedBy   = "Terraform"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_bucket_encryption" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256" # Use AES256 for S3-managed encryption
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state_bucket_public_access_block" {
  bucket = aws_s3_bucket.terraform_state_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


# DynamoDB Table for State Locking
resource "aws_dynamodb_table" "terraform_state_lock" {
  name         = "${var.resources_prefix}tf-state-lock"
  billing_mode = "PAY_PER_REQUEST"

  # The primary key for the lock table MUST be 'LockID'
  hash_key = "LockID"

  attribute {
    name = "LockID"
    type = "S" # String type
  }

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
