terraform {
  required_version = ">= 0.13.1"

  required_providers {
    aws    = ">= 3.60"
  }
 backend "s3" {
    bucket = "nsrr-cloud-tf-backend"
    key    = "prod/iam/password-policy"
    region = "us-east-1"
  }
}

provider "aws" {
  profile = "tf-service-account-strides"
  region = "us-east-1"
}

resource "aws_iam_account_alias" "alias" {
  account_alias = "strides-nsrr-prod"
}

resource "aws_iam_account_password_policy" "strict" {
  max_password_age               = 90
  minimum_password_length        = 8
  allow_users_to_change_password = true
  hard_expiry                    = false
  password_reuse_prevention      = 3
  require_lowercase_characters   = true
  require_uppercase_characters   = true
  require_numbers                = true
  require_symbols                = true
}
