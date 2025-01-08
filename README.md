# AWS Lambda Function for EBS Snapshot Cleanup

This repository contains a Python Lambda function that identifies and deletes stale EBS snapshots in your AWS account. This helps optimize storage costs by removing unused snapshots.

## Functionality

The script utilizes the boto3 library to interact with the AWS EC2 API.
It retrieves information about all EBS snapshots owned by your account.
It then gathers a list of currently running EC2 instances.
For each snapshot, the script checks the following:

* Age: If the snapshot is older than 60 days.
* Volume Attachment: If the snapshot is attached to a volume.
* Instance State: If the volume is attached to a running instance.

Based on the checks above, the script performs the following actions:

* Deletes snapshots older than 60 days that are not attached to any volume.
* Deletes snapshots older than 60 days that are attached to a volume not currently used by a running instance. (The volume might have been deleted)
* Skips snapshots attached to volumes used by running instances.

## Usage

### Configure AWS Credentials:

1. Create an IAM role with the necessary permissions for the Lambda function to access EC2 resources.
2. Configure the role with your AWS credentials or a secrets manager for secure access.

### Deploy the Lambda Function:

1. Upload the ebs_stale_snapshosts.py script to your preferred deployment platform.
2. Configure the Lambda function to trigger periodically (e.g., daily) or on demand.

## Benefits

* Reduces storage costs by deleting unused EBS snapshots.
* Improves resource management by identifying and cleaning up stale data.

## Contributing

We welcome contributions to improve this script. Please create a pull request with your proposed changes.

## Additional Notes

You can customize the age threshold (currently set to 60 days) to meet your specific retention needs.
