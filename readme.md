# AWS File Processing Pipeline Setup

## Steps to Set Up the Pipeline

### 1. Create an S3 Bucket
1. Log in to the AWS Management Console.
2. Go to **S3** and click **Create bucket**.
3. Enter a **Bucket name** (e.g., `csv-upload-bucket`).
4. Select a region (e.g., `ap-south-1`).
5. Leave the default settings or customize as needed.
6. Click **Create bucket**.

### 2. Create a Lambda Function
1. Navigate to **AWS Lambda** and click **Create function**.
2. Choose **Author from scratch**:
   - **Function name**: `csv-file-processor`.
   - **Runtime**: Python 3.x.
3. In the **Permissions** section:
   - Select **Create a new role with basic Lambda permissions**.
4. Click **Create function**.

### 3. Add the Lambda Code
1. In the function’s page, go to the **Code** section.
2. Paste your Python script into the Lambda editor or upload a `.zip` file containing your code.
3. Update the **Handler** to match your file and function name (e.g., `lambda_function.lambda_handler`).
4. Click **Deploy**.

### 4. Set Up an S3 Trigger
1. Go to the **Configuration** tab of your Lambda function and select **Triggers**.
2. Click **Add trigger**:
   - **Trigger configuration**: Select **S3**.
   - **Bucket**: Choose your created bucket.
   - **Event type**: Select **PUT** (for file uploads).
3. Save the trigger.

### 5. Create and Attach an IAM Role for Lambda
1. Go to the **IAM console**.
2. Create a new role:
   - Choose **AWS Service** → **Lambda**.
   - Attach the following policies:
     - `AmazonS3ReadOnlyAccess`.
     - `AmazonDynamoDBFullAccess`.
     - `AmazonSNSFullAccess`.
     - `AWSLambdaBasicExecutionRole`.
3. Save the role and attach it to your Lambda function:
   - In the **Lambda console**, go to **Configuration** → **Permissions**.
   - Click **Edit** and attach the new role.

### 6. Set Up an SNS Topic
1. Go to **Amazon SNS** and click **Create topic**.
2. Choose **Standard**:
   - **Name**: `CSVUploadNotification`.
3. Create the topic.
4. Add a subscription:
   - **Protocol**: Email.
   - **Endpoint**: Enter your email address.
5. Confirm the subscription by clicking the link in the confirmation email.

### 7. Create a DynamoDB Table
1. Go to **DynamoDB** and click **Create table**.
2. Enter the following details:
   - **Table name**: `CSVMetadata`.
   - **Partition key**: `filename` (String).
3. Leave the rest as default and click **Create table**.

### 8. Test the Pipeline
1. Upload a CSV file to the S3 bucket.
2. Check for the following:
   - **Email Notification**: Verify you received an email from SNS.
   - **DynamoDB Table**: Confirm the metadata of the file is added.
   - **CloudWatch Logs**: Review the Lambda logs for any errors.

---

## Debugging Steps via CloudWatch Logs
1. Navigate to **CloudWatch** in the AWS Management Console.
2. Go to **Log groups** and find the log group for your Lambda function (e.g., `/aws/lambda/csv-file-processor`).
3. Click the log group to view **Log streams**.
4. Open the latest log stream to review the execution details.
5. Look for error messages or stack traces to identify issues:
   - **Permission Errors**: Verify the Lambda function’s IAM role has the necessary permissions.
   - **File Access Errors**: Ensure the S3 bucket policy allows Lambda access.
   - **DynamoDB Errors**: Confirm the table name and partition key in the Lambda code match the DynamoDB configuration.

---

## Architecture Diagram

The pipeline consists of the following components:

1. **S3 (CSV files)**: Stores uploaded files and triggers the Lambda function.
2. **Lambda (process files)**:
   - Processes the uploaded CSV file.
   - Extracts metadata and saves it to DynamoDB.
   - Sends an email notification using SNS.
3. **DynamoDB (store metadata)**: Stores metadata extracted from the CSV files.
4. **SNS (email notification)**: Sends notifications about successful CSV uploads.
![Screenshot 2024-12-23 at 2 38 31 PM](https://github.com/user-attachments/assets/e4d1cbc4-30c1-4a9f-b33e-1e155657e564)



