terraform {
  backend "s3" {
    bucket         = "ai-k8s-ops-terraform-state-eric"
    key            = "dev/terraform.tfstate"
    region         = "eu-west-2"
    encrypt        = true
    dynamodb_table = "ai-k8s-ops-terraform-locks"
  }
}
