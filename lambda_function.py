import boto3
import csv
from datetime import datetime

# Initialize AWS service
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

# Configuration
DYNAMODB_TABLE = "CSVMetadata"

SNS_TOPIC_ARN = "arn:aws:sns:ap-south-1:<<acc no(removed for privacy)>>:CSVUploadNotification"


def lambda_handler(event, context):
    # Extract bucket and object information from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Download the CSV file from S3
    csv_file = f'/tmp/{object_key}'
    s3_client.download_file(bucket_name, object_key, csv_file)

    # Extract metadata from the CSV
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        column_names = next(csv_reader)
        row_count = sum(1 for row in csv_reader)

    # Prepare metadata
    metadata = {
        'filename': object_key,
        'upload_timestamp': datetime.now().isoformat(),
        'file_size_bytes': event['Records'][0]['s3']['object']['size'],
        'row_count': row_count,
        'column_count': len(column_names),
        'column_names': column_names
    }

    # Store metadata in DynamoDB
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.put_item(Item=metadata)

    # Notify via SNS
    notify_sns(metadata)

    return {"statusCode": 200, "body": "Processing completed successfully"}

def notify_sns(metadata):
    # Construct the notification message
    subject = "CSV File Uploaded Successfully"
    message = f"""
    A CSV file has been uploaded to the S3 bucket.

    File Name: {metadata['filename']}
    Upload Time: {metadata['upload_timestamp']}
    File Size: {metadata['file_size_bytes']} bytes
    Row Count: {metadata['row_count']}
    Column Count: {metadata['column_count']}
    Column Names: {', '.join(metadata['column_names'])}
    """

    # Publish the message to the SNS topic
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
