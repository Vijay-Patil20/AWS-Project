import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    # Get all EBS snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all active EC2 instance IDs 
    instances_response = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    active_instance_ids = set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    # Iterate through each snapshot and delete if it's older than 60 days AND not attached to a volume or the volume is not attached to a running instance
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')
        start_time = snapshot['StartTime']

        # Calculate the age of the snapshot
        now = datetime.datetime.now(datetime.timezone.utc)
        snapshot_age = now - start_time
        age_in_days = snapshot_age.days

        if age_in_days >= 60:  # Check if the snapshot is older than 60 days
            if not volume_id:
                # Delete the snapshot if it's not attached to any volume
                try:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS snapshot {snapshot_id} (Age: {age_in_days} days) as it was not attached to any volume.")
                except ec2.exceptions.ClientError as e:
                    print(f"Error deleting snapshot {snapshot_id}: {e}")
            else:
                # Check if the volume still exists and is attached to a running instance
                try:
                    volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                    if not volume_response['Volumes'][0]['Attachments']:
                        try:
                            ec2.delete_snapshot(SnapshotId=snapshot_id)
                            print(f"Deleted EBS snapshot {snapshot_id} (Age: {age_in_days} days) as it was taken from a volume not attached to any running instance.")
                        except ec2.exceptions.ClientError as e:
                            print(f"Error deleting snapshot {snapshot_id}: {e}")
                    else:
                        print(f"Snapshot {snapshot_id} (Age: {age_in_days} days) is attached to a volume that is attached to an instance.")
                except ec2.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                        # The volume associated with the snapshot is not found (it might have been deleted)
                        try:
                            ec2.delete_snapshot(SnapshotId=snapshot_id)
                            print(f"Deleted EBS snapshot {snapshot_id} (Age: {age_in_days} days) as its associated volume was not found.")
                        except ec2.exceptions.ClientError as e:
                            print(f"Error deleting snapshot {snapshot_id}: {e}")
                    else:
                      print(f"Error describing volume {volume_id}: {e}")
        else:
            print(f"Snapshot {snapshot_id} is {age_in_days} days old, skipping.")

    return {
        'statusCode': 200,
        'body': 'Snapshot cleanup completed.'
    }
