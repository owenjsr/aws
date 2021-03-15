import boto3
import time
from botocore.exceptions import ClientError
import sys
import os
import time

#version 2 removes the need for the template and launches an instance immediately
#using a resource class

def main():
    print("Running Scenario 3: Exposed Workload recon")
    print("====================================================================")

    #check if any arguments given
    if len(sys.argv) < 3:
        print("Must supply AWS Key and Secret as arguments,,, exiting")
        exit()

    AWS_ACCESS_KEY = sys.argv[1]
    AWS_SECRET_KEY = sys.argv[2]
    #LAUNCH_TEMPLATE_ID = 'AWS-Workshop-WIN2016-Base'
    NUMBER_OF_INSTANCES = 1
    Scan_Count = 250

    exposed_workload_recon(AWS_ACCESS_KEY, AWS_SECRET_KEY,NUMBER_OF_INSTANCES,Scan_Count)

    print ("SCENARIO 03: COMPLETED")
    print("====================================================================")

def exposed_workload_recon(AWS_ACCESS_KEY, AWS_SECRET_KEY,NUMBER_OF_INSTANCES,Scan_Count):
    ec2 = boto3.client('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    #get VPC ID
    try:
        response = ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        print("Recieved VPC ID "+vpc_id)
    except ClientError as e:
        print(e)

    #Create the Needed Security Group
    try:
        response = ec2.create_security_group(GroupName='Allow_3389_Anywhere',
                                             Description='An SG to allow 3389 from anywhere',
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 3389,
                 'ToPort': 3389,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)

    ec2 = boto3.resource('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    #create the windows server
    try:
        instance = ec2.create_instances(
                        ImageId= "ami-08f90fed89a37985d",
                        InstanceType='t2.micro',
                        MaxCount=NUMBER_OF_INSTANCES,
                        MinCount=NUMBER_OF_INSTANCES,
                        SecurityGroups=[
                            'Allow_3389_Anywhere',
                            ],
                        )
        print('Instance created', instance)
    except:
        raise Exception("Couldn't create instance")

    print("Waiting for instance to be up and running")

    for i in instance:
        while i.state['Name'] != 'running':
           print('Instance', i.instance_id,'is', i.state['Name'])
           time.sleep(10)
           i.reload()
        PublicIP = i.public_ip_address
        print("Found Public IP:"+PublicIP)

    print("Starting Attack")

    count = 1
    while (count < Scan_Count):
       print ("*****  PERFORMING SCAN NUMBER: ", count , "of", Scan_Count, end = "\r")
       os.system("nmap -Pn -p 3389 "+PublicIP+" > /dev/null 2>&1 ")
       time.sleep(2)
       count = count + 1

    print ("\rAttack finished")

    try:
        print("Terminating Instance")
        response = i.terminate()
        print(i.instance_id, "terminated")
    except:
        print("There was an error terminating the instance. You may need to terminate it manually")

if __name__ == "__main__":
    main()
