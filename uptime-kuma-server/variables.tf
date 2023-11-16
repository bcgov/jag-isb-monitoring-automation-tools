variable "region" {
  description = "The region where environment is going to be deployed"
  type        = string
  default     = "ca-central-1"
}

variable "aws_access_key" {
  type      = string
  sensitive = true
}

variable "aws_secret_key" {
  type      = string
  sensitive = true
}

variable "aws_token" {
  type      = string
  sensitive = true
}

# VPC variables

variable "vpc_cidr" {
  description = "CIDR range for VPC"
  type        = string
  default     = ""
}

variable "vpc_id" {}

variable "subnet_id" {}