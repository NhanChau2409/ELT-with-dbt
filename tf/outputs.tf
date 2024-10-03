output "bucket_name" {
  description = "The name of the created S3 bucket"
  value       = aws_s3_bucket.flight_data.id
}

output "airbyte_access_key" {
    value = aws_iam_access_key.airbyte.id
}

output "airbyte_secret_key" {
    value = aws_iam_access_key.airbyte.secret
    sensitive = true
}   