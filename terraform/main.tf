provider "aws" {
  region = var.region
}

# Backend configuration for state storage
terraform {
  backend "s3" {
    bucket = "moments-in-history-tf-state-bucket"
    key    = "terraform.tfstate"
    region = var.region
    encrypt = true
    dynamodb_table = "moments-in-history-tf-state-lock"
  }
}