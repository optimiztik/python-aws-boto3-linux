#!/usr/bin/python3
import boto3
import time
from creds import Creds
from botocore.exceptions import ClientError

creds = Creds("credentials.csv")
print("Beware You are doing this activity using this account :" + " " + creds.username)

REGION = "ap-south-1"
ACCESS_KEY = creds.access_key_id
SECRET_KEY = creds.secret_key
ec2Client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
ec2Resource = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
#Selected ubuntu AMI Free tier image (intel x86)
image_id = "ami-0b44050b2d893d5f7"
instance_type = "t2.micro"
keypair_name = "devkeypair"
SECURITY_GROUP = "sg-2fdb4e45"
IAM_PROFILE = "admin"
ALLOCATIONID = "eipalloc-03ce504c67b167038"
response = {}

def create_instance():
  global InstanceId
  try:
   response = ec2Resource.create_instances(ImageId=image_id,
                                           InstanceType=instance_type,
                                           KeyName=keypair_name,
                                           SecurityGroupIds=[SECURITY_GROUP],
                                           IamInstanceProfile={'Name': IAM_PROFILE}, MinCount=1, MaxCount=1)
   print("Provisioning instance…")
   # Wait for it to launch before assigning the elastic IP address
   response[0].wait_until_running()

   # Allocate an elastic IP
   eip = ec2Client.allocate_address(Domain='vpc')
   # Associate the elastic IP address with the instance launched above
   ec2Client.associate_address(
    InstanceId=response[0].id,
    AllocationId=eip["AllocationId"])

   print("Your instance is ready...")
   print("Your Instance ID is : " + " " + response[0].id)
   print("Assigned Instance Public IP :" + eip["PublicIp"])
   InstanceId = (str(response[0].id))
   print("Adding Instance name as CLIENT..")
   ec2Client.create_tags(Resources=[InstanceId], Tags=[{'Key': 'Name', 'Value': 'CLIENT'}])
   print("Tag successfully added")
  except ClientError as e:
   print(e)

def getRunningInstanceID(TAGNAME):
 running_instances = ec2Resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
 instance_ids = []
 for instance in running_instances:
    for tag in instance.tags:
        if tag['Value'] == TAGNAME:
           instance_ids.append(instance.id)
 return instance_ids

def getRunningInstanceIP():
    running_instances = ec2Resource.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instance_ips = []
    for instance in running_instances:
        for tag in instance.tags:
            if tag['Value'] == 'CLIENT':
                instance_ips.append(instance.public_ip_address)
    return instance_ips

def terminateInstance():
    instance_ids = getRunningInstanceID('CLIENT')
    response=ec2Client.terminate_instances(InstanceIds=instance_ids)
    print(response['CurrentState'])
