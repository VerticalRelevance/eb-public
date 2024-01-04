variable "lambda_relative_path" {
  description = "Used in the Lambda build"
  type        = string
  default     = "/../../Experiment-Broker-Module/experiment_code/"
}

variable "lambda_log_level" {
  description = "Log level for the Lambda Python runtime."
  type        = string
  default     = "ERROR"
}

variable "owner" {
  description = "Name of the team member who owns the resource. Used so multiple lambdas can be deployed"
  type        = string
  default     = "Resiliency_Team"
}

variable "experiment_bucket" {
  description = "Bucket to place the lambda package in"
  type        = string
  default     = "resiliencyvr-package-build-bucket"
}