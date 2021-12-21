terraform {
  required_version = ">= 0.13.1"

  required_providers {
    aws    = ">= 3.60"
  }

  backend "s3" {
    bucket = "nsrr-cloud-tf-backend"
    key    = "prod/s3/all-open"
    region = "us-east-1"
  }

}

provider "aws" {
  profile = "tf-service-account-strides"
  region = "us-east-1"
}

locals {
  bucket_name = "nsrr-dataset-all-open"
}

resource "aws_s3_bucket" "log_bucket"{
  bucket                         = "log-${local.bucket_name}"
  acl                            = "log-delivery-write"
  force_destroy                  = true
  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "log_block_public_access" {
  bucket                  = aws_s3_bucket.log_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "data_bucket" {
  bucket  = local.bucket_name
  acl     = "private"
  force_destroy = true
  versioning {
    enabled = true
  }
  logging {
    target_bucket = aws_s3_bucket.log_bucket.id
    target_prefix = "log/"
  } 
  tags = {
    Owner = "nsrr"
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "AES256"
      }
    }
  }

  object_lock_configuration {
    object_lock_enabled = "Enabled"
    rule {
      default_retention {
        mode  = "GOVERNANCE"
        years = 5
      }
    }
  }

  cors_rule {
    allowed_headers = ["Authorization", "Content-Range", "Accept", "Content-Type", "Origin", "Range"]
    expose_headers  = ["Content-Range","Content-Length","ETag"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}


resource "aws_s3_bucket_policy" "readpolicy" {
  bucket = aws_s3_bucket.data_bucket.id
  policy = <<EOF
{
  "Id": "READPOLICY",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicList",
      "Action": "s3:ListBucket",
      "Effect": "Allow",
      "Resource": "${aws_s3_bucket.data_bucket.arn}",
      "Principal": "*"
    }, 
    {
      "Sid": "AllowPublicGet",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion"
      ],
      "Effect": "Allow",
      "Resource": "${aws_s3_bucket.data_bucket.arn}/*",
      "Principal": "*"
    }
  ]
}
EOF
}
