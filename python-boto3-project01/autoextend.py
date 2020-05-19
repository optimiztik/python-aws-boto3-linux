#!/usr/bin/python3
import boto3
import time
from creds import Creds
from botocore.exceptions import ClientError
from instance_creation import getRunningInstanceIP,getRunningInstanceID

creds = Creds("credentials.csv")
print("You are logged in as  :" + " " + creds.username)

REGION = "ap-south-1"
ACCESS_KEY = creds.access_key_id
SECRET_KEY = creds.secret_key
ec2Client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
ec2Resource = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

try:
    instanceId = getRunningInstanceID('SERVER')
    volumeid = []
    for ids in instanceId:
        instance = ec2Resource.Instance(ids)
        for  volume_iterator in instance.volumes.all():
            volumeid = volume_iterator.id
            currvolsize = volume_iterator.size
            print("--- Current volume size : {}".format(currvolsize))
            targetvolsize = currvolsize+1

    def modify_instance_volsize():
        print("--- Instance getting modified ---")
        print("--- Target volume size : {}".format(targetvolsize))
        modifyresponse = ec2Client. modify_volume(
                VolumeId=volumeid,
                Size=targetvolsize)
        time.sleep(3)
        print("volume resize status: " +  modifyresponse['ModificationState'])
except ClientError as e:
    print(e)
#modify_instance_volsize()
