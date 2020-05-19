#!/usr/bin/python3
# !/usr/bin/msfconsole
import os
import time
from pick import pick
import instance_creation as create
import initial_setup as postinstall
import create_attach_volume as addstorage
from instance_creation import terminateInstance
title = 'Please choose your action: '
options = ['Create-new-instance', 'PostInstall-deployed-instance','Create-attach-ebs-volumes','Run-all(1.Deploy, 2.PostInstall)','Terminate-Instances']
option, index = pick(options, title)

def main():
    if index == 0:
        print('-------------')
        print("You have selected to perform : ", (option))
        x = int(input("How many instance you want to provision : "))
        for i in range(x):
            print("Deploying instance", i)
            create.create_instance()
        print('-------------')
    if index == 1:
        print('-------------')
        print("You have selected to perform : ", (option))
        print("Lets start pushing setup to new instance....")
        time.sleep(3)
        postinstall.establish_conn()
        print('-------------')
    if index == 2:
        print('-------------')
        print("You have selected to perform : ", (option))
        print("If you wish to create & attaching volume - makesure your instance is in Zone : ap-south-1a")
        print("Lets start creating volume and attach it to instances....")
        time.sleep(3)
        addstorage.create_volume()
        print('-------------')

    if index == 3:
        print('-------------')
        print("You have selected to perform : ", (option))
        print("Step 1 : Creating new instance")
        x = int(input("How many instance you want to provision : "))
        for i in range(x):
            print("Deploying instance", i)
            create.create_instance()
            time.sleep(40)
            print('-------------')
            print("Step 2 : Pushing Initial setup to newly deployed machine")
            postinstall.establish_conn()
            print('-------------')
    if index == 4:
        print('------------')
        print("You have selected to perform : ", (option))
        print("Termination of CLIENT instances begins... ")
        terminateInstance()
        print('-------------')

main()
