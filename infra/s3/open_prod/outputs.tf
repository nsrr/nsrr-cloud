output "this_s3_bucket_id" {
  description = "The name of the bucket."
  value       = aws_s3_bucket.log_bucket.id
}

output "this_s3_bucket_arn" {
  description = "The ARN of the bucket. Will be of format arn:aws:s3:::bucketname."
  value       = aws_s3_bucket.log_bucket.arn
}

output "this_s3_bucket_region" {
  description = "The AWS region this bucket resides in."
  value       = aws_s3_bucket.log_bucket.region
}

output "data_bucket_id" {
  description = "The name of the bucket."
  value       = aws_s3_bucket.data_bucket.id
}

output "data_bucket_arn" {
  description = "The ARN of the bucket. Will be of format arn:aws:s3:::bucketname."
  value       = aws_s3_bucket.data_bucket.arn
}

output "data_bucket_region" {
  description = "The AWS region this bucket resides in."
  value       = aws_s3_bucket.data_bucket.region
}