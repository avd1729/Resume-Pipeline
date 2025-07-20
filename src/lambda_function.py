import boto3
import urllib.parse

s3 = boto3.client('s3')
TARGET_KEY = 'resume.pdf'

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        source_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        try:
            # Copy the uploaded file to 'resume.pdf'
            copy_source = {'Bucket': bucket, 'Key': source_key}
            s3.copy_object(
                CopySource=copy_source,
                Bucket=bucket,
                Key=TARGET_KEY,
                ContentType='application/pdf',
                MetadataDirective='REPLACE'  # Ensures content-type is preserved
            )
            print(f"Copied {source_key} to {TARGET_KEY}")
        except Exception as e:
            print(f"Error copying file: {e}")
            raise e
