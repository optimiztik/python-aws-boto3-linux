#!/usr/bin/python3
import boto3
import sys
from creds import Creds

creds = Creds("credentials.csv")
#print("Beware You are doing this activity using this account :" + " " + creds.username)

REGION = "ap-south-1"
ACCESS_KEY = creds.access_key_id
SECRET_KEY = creds.secret_key
ec2 = boto3.resource('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)

instance_ids = ec2.instances.all()
for id in instance_ids:
 print(id.terminate())

