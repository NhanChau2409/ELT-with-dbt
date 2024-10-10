# S3 bucket for flight data
resource "aws_s3_bucket" "flight_data" {
  bucket = "project-flight-data-bucket"
}

resource "aws_s3_bucket_ownership_controls" "flight_data_ownership" {
  bucket = aws_s3_bucket.flight_data.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "flight_data_acl" {
  bucket = aws_s3_bucket.flight_data.id
  acl    = "private"
  depends_on = [aws_s3_bucket_ownership_controls.flight_data_ownership]
}

resource "aws_s3_bucket_versioning" "flight_data_versioning" {
  bucket = aws_s3_bucket.flight_data.id
  versioning_configuration {
    status = "Disabled"
  }
}

# Policy for full access user to the flight data S3 bucket
data "aws_iam_policy_document" "s3_flight_data_full_access" {
  statement {
    effect = "Allow"
    actions = [
      "s3:*",
    ]
    resources = [
      aws_s3_bucket.flight_data.arn,
      "${aws_s3_bucket.flight_data.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "s3_flight_data_full_access" {
  name   = "s3-flight-data-full-access"
  policy = data.aws_iam_policy_document.s3_flight_data_full_access.json
}

# Lambda
resource "aws_iam_role" "lambda" {
  name = "lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_s3_full_access" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.s3_flight_data_full_access.arn 
}

resource "aws_lambda_function" "s3_flight_data_lambda" {
  function_name = "s3-flight-data-lambda"
  role          = aws_iam_role.lambda.arn
  runtime       = "python3.10"      
  filename      = "lambda_function.zip"  
  handler       = "main.fetch_and_write_flight_data"
  timeout       = 3 * 60

  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      API_KEY = var.api_key
      BUCKET_NAME = aws_s3_bucket.flight_data.id
      START_DATE = local.start_date
      END_DATE = local.end_date
      AIRPORT_ICAO = local.airport_icao
    }
  }
}

# Snowflake
resource "aws_iam_user" "snowflake" {
  name = "snowflake"
  force_destroy = true
}

resource "aws_iam_user_policy_attachment" "snowflake_s3_full_access" {
  user       = aws_iam_user.snowflake.name
  policy_arn = aws_iam_policy.s3_flight_data_full_access.arn 
}

resource "aws_iam_access_key" "snowflake" {
  user = aws_iam_user.snowflake.name
  status = "Active"
}