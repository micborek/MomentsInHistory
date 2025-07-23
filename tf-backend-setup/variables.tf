variable "resources_prefix" {
  description = "Common prefix for the created resources."
  type        = string
  default     = "moments-in-history-"
}

variable "region" {
  description = "The AWS region to deploy the resources to."
  type        = string
  default     = "us-west-2"
}