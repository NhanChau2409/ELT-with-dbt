# Flight Data Collection and Storage Project

This project automates the collection of flight data from an API and stores it in an AWS S3 bucket. It uses Terraform for infrastructure provisioning and a Python Lambda function for data fetching and processing.

## Project Structure

- `tf/`: Terraform configuration files
- `api_call/`: Python code for the Lambda function
- `.gitignore`: Git ignore file

## Prerequisites

- AWS account
- Terraform installed (version >= 1.0.0)
- Python 3.10
- API key for the flight data API

## Setup

1.  Clone this repository.

    a. Set up your AWS credentials:

    - Create an AWS IAM user with appropriate permissions.
    - Configure your AWS CLI or set the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.

    b. Create a `terraform.tfvars` file in the `tf/` directory with the following content:

         ```
         api_key = "your_api_key_here"
         access_key = "your_aws_access_key"
         secret_key = "your_aws_secret_key"
         ```

    c. Modify the `tf/locals.tf` file to set your desired airport ICAO code and date range.

    d. Package the Lambda function:

         ```
         cd api_call
         pip install -r requirements.txt -t package/
         zip -r ../lambda_function.zip main.py package/
         cd ..
         ```
2. Set up dbt Cloud
3. Set up Snowflake
4. Authenicate Snowflake with dbt
## Deployment

1. Initialize Terraform:

   ```
   cd tf
   terraform init
   ```

2. Review the Terraform plan:

   ```
   terraform plan -var-file=terraform.tfvars
   ```

3. Apply the Terraform configuration:
   ```
   terraform apply -var-file=terraform.tfvars
   ```

## Usage

The Lambda function will automatically fetch flight data for the specified airport and date range, and store it in the S3 bucket. The data is stored in CSV format with the following structure:

- airport_icao
- timestamp
- fromdate
- todate
- response_code
- response (JSON)

## Cleanup

To remove all created resources:

```
terraform destroy
```
