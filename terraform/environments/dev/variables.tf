variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "project_name" {
  type    = string
  default = "ai-k8s-ops"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "db_name" {
  type    = string
  default = "aik8sops"
}

variable "db_username" {
  type    = string
  default = "aik8sadmin"
}

variable "db_password" {
  type      = string
  sensitive = true
}