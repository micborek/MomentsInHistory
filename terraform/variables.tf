variable "resources_prefix" {
  description = "Common prefix for the created resources."
  type        = string
  default     = "moments-in-history-"
}

variable "generate_function_name" {
  description = "Name for lambda generating posts"
  type        = string
  default     = "generate-post"
}

# us-west-2 allows image generation in AWS Bedrock
variable "region" {
  description = "The AWS region to deploy the resources to."
  type        = string
  default     = "us-west-2"
}

# us-west-2 did not reply successfully for on-demand requests for nova lite
variable "ai_model_region" {
  description = "Region for the model generating posts"
  type        = string
  default     = "us-east-1"
}

variable "runtime" {
  description = "The runtime for the Lambda functions."
  type        = string
  default     = "python3.13" #
}

variable "lambda_timeout" {
  description = "The maximum execution time for the Lambda functions in seconds."
  type        = number
  default     = 30
}

variable "lambda_memory_size" {
  description = "The amount of memory allocated to the Lambda functions in MB."
  type        = number
  default     = 128
}