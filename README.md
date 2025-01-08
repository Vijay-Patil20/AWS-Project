# AWS Lambda Function for EBS Snapshot Cleanup

## Introduction

What are the reasons for companies to migrate from on-premises servers to the Cloud?

* **Maintenance Overhead:** On-premises servers require significant maintenance, including hardware upgrades, software patching, and physical infrastructure upkeep.
* **High Cost:** Maintaining and operating on-premises infrastructure can be very expensive.
* **Not very efficient:** On-premises systems can be less efficient and scalable compared to cloud-based solutions.

**What if a company migrated to the Cloud and these problems still exist? What if the costs aren't being saved either?**

Is it the cloud provider's fault? **No.** It is a **shared responsibility**.

* Cloud providers like AWS, Azure, etc., provide you with numerous services for compute, storage, monitoring, and many more, with the least amount of effort on your end.
* This doesn't mean you can use the resources irresponsibly; it will incur additional charges, and you won't benefit from the migration.
* So, it is a shared responsibility. Use resources responsibly, reap all the benefits.

As a DevOps Engineer, one of your responsibilities is to maintain all the created resources and ensure the deletion of stale resources.

## Problem Explanation

Imagine you created an EC2 instance with an attached root EBS volume to store the data related to your application hosted on that instance. You decided to take a backup of that EBS volume by taking a snapshot, to restore it as a new volume in a different AZ when a disaster strikes. But, you need the snapshots only as long as the application exists. If you decide to shut down your application on the EC2 instance, there will be no need for the snapshot. In that scenario, the snapshots associated with the instance need to be deleted to be financially efficient.

If you just have one or two EC2 instances to manage, this won't be a big deal, and you can easily manage creation and deletion snapshots manually. But, companies usually have a lot of resources and EC2 instances to manage in various AWS regions. So the above task is almost impossible to be done manually. This is when Lambda functions in AWS emerge.

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
