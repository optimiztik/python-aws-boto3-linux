#!/usr/bin/python3
import paramiko
import time
import sys
from instance_creation import getRunningInstanceIP,getRunningInstanceID
instance_ips = getRunningInstanceIP()
print("Processing these IPs " + str(instance_ips))
login_id = 'ubuntu'
login_key = paramiko.RSAKey.from_private_key_file('/data/devkeypair.pem')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def install_package():
 try:
   print('Step 1 : Package Installation started')
   commands = ["sudo apt update -y","sudo apt install python3 -y","sudo apt install python3-pip -y", "sudo pip3 install boto3", "sudo pip3 install paramiko", "sudo mkdir /data", "sudo chmod -R 777 /data"]
   for command in commands:
     print("Executing {}".format(command))
     stdin, stdout, stderr = ssh.exec_command(command)
     exit_status = stdout.channel.recv_exit_status()
     if exit_status == 0:
        print("Command executed successfully")
     else:
        print("Command failed to execute")
   print('Package Installation completed')
 except:
     pass

def copy_files():
 try:
     print('Step 2 : File copy started')
     files = ['/data/fssize.py','/data/autoextend.py', '/data/watch_fssize.py']
     for file in files:
         print("copying {}".format(file))
         destination = file
         sftp = ssh.open_sftp()
         sftp.put(file, destination)
         sftp.close()
     print('File copy ended')
     print(stderr.read())
 except:
     pass

def create_cronjobs():
    try:
        print('Step 3 : Create cron jobs')
        commands = ['(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/python3 /data/watch_fssize.py") | crontab -','(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/bin/python3 /data/fssize.py") | crontab -']
        for command in commands:
            print("Executing {}".format(command))
            stdin, stdout, stderr = ssh.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("Command executed successfully")
            else:
                print("Command failed to execute")
        print('Cronjob Entries created')
    except:
        pass


def establish_conn():
 for host in instance_ips:
    print('Connecting to', host)
    ssh.connect(host, username=login_id, pkey=login_key)
    time.sleep(2)
    print('connected')
    time.sleep(2)
    print("---------")
    install_package()
    print("---------")
    copy_files()
    print("---------")
    create_cronjobs()
    print("---------")
    time.sleep(2)

#establish_conn()
