import boto3
import argparse
import os
from datetime import datetime

# Constants
BUCKET_NAME = 'resume-versioning-bucket'
UPLOAD_DIR = 'resume-uploads'

def upload_resume(file_path):
    s3 = boto3.client('s3')

    if not os.path.exists(file_path):
        print(f"Resume file not found: {file_path}")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    versioned_key = f'{UPLOAD_DIR}/resume-{timestamp}.pdf'

    with open(file_path, 'rb') as file_data:
        s3.upload_fileobj(
            file_data,
            BUCKET_NAME,
            versioned_key,
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        print(f"Uploaded to {BUCKET_NAME}/{versioned_key}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload resume to S3')
    parser.add_argument(
        '--file',
        type=str,
        default='resume/resume.pdf',
        help='Path to the resume file (default: resumes/resume.pdf)'
    )
    args = parser.parse_args()
    upload_resume(args.file)
