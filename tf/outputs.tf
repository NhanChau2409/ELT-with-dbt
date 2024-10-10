output "bucket_url" {
  description = "The url S3 bucket"
  value       = "s3//:${aws_s3_bucket.flight_data.id}"
}

output "snowflake_key_id" {
  value = aws_iam_access_key.snowflake.id
}

output "snowflake_secret" {
  value = aws_iam_access_key.snowflake.secret
  sensitive = true
}