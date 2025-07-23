
# Resume Auto-Updater using S3 + Lambda

This project automates the process of updating your resume on a public S3 URL. When a new resume is uploaded to a specific S3 bucket (e.g., via a GUI or CLI), an AWS Lambda function is triggered to replace the existing file. This ensures your public resume URL always points to the latest version.

## Project Intuition

Manually updating your resume at a public-facing URL can be error-prone and tedious. This project uses AWS S3's event-driven capabilities to:

- Trigger a Lambda function whenever a new resume file is uploaded to a specific bucket/key.
- Automatically update the public resume hosted at a predefined S3 object location.
- Allow CLI and GUI-based uploads to simplify the update process.

Use Case:
> You maintain a public URL (like `https://your-bucket.s3.amazonaws.com/resume.pdf`) that always shows your latest resume.


---

## Prerequisites

- AWS CLI configured with `aws configure`
- IAM user with S3 and Lambda permissions
- Python 3.10+ installed
- An existing S3 bucket (or create one)

---

## Setup Guide

### 1. Create an S3 Bucket (if not already done)

```bash
aws s3 mb s3://your-resume-bucket-name
````

### 2. Upload an Initial Resume (optional)

```bash
aws s3 cp my_resume.pdf s3://your-resume-bucket-name/resume-latest.pdf
```

> This file (`resume-latest.pdf`) will be publicly accessible at:
> `https://<your-bucket>.s3.amazonaws.com/resume-latest.pdf`

---

### 3. Set Up the Lambda Function

#### a. Create a new Lambda function (Python runtime)

* Runtime: Python 3.9 (or compatible with your code)
* Permissions: Add a role with `AmazonS3FullAccess` or scoped permissions to your bucket

#### b. Upload the Lambda code

You can zip and upload manually or use the AWS CLI:

```bash
cd src
zip lambda.zip lambda_function.py
aws lambda update-function-code --function-name resumeUpdaterLambda --zip-file fileb://lambda.zip
```

#### c. Add an S3 Trigger to Lambda

1. Go to the S3 bucket in AWS Console.
2. Choose **Properties > Event notifications**.
3. Create a new event:

   * Event Name: `resume-upload`
   * Event Type: `PUT`
   * Prefix (optional): `uploads/`
   * Suffix: `.pdf`
   * Destination: Your Lambda function

> Alternatively, via CLI (example):

```bash
aws s3api put-bucket-notification-configuration \
    --bucket your-resume-bucket-name \
    --notification-configuration file://s3_event_config.json
```

`s3_event_config.json` example:

```json
{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:REGION:ACCOUNT_ID:function:resumeUpdaterLambda",
      "Events": ["s3:ObjectCreated:Put"],
      "Filter": {
        "Key": {
          "FilterRules": [
            { "Name": "prefix", "Value": "uploads/" },
            { "Name": "suffix", "Value": ".pdf" }
          ]
        }
      }
    }
  ]
}
```

---


## Public Resume URL

Once uploaded and processed by Lambda, your resume will be available at:

```
https://your-resume-bucket-name.s3.amazonaws.com/resume-latest.pdf
```

Make sure this object is public (or served via CloudFront).

---

## Optional Improvements

* Add authentication to the GUI or CLI
* Auto-deploy Lambda via CDK or Terraform
* Monitor with CloudWatch Logs and alerts

---


