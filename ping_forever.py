import csv
import sys
import main_aws_setup
import boto3
import time

def ping_gw(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES, AWS_REGION):

    ec2 = boto3.resource('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name=AWS_REGION)

    print("Creating the instance to ping 8.8.8.8")
    try:
        instance = ec2.create_instances(
                        ImageId='ami-0b72132eb3104947d',
                        InstanceType='t2.micro',
                        MaxCount=NUMBER_OF_INSTANCES,
                        MinCount=NUMBER_OF_INSTANCES,
                        UserData='IyEvYmluL2Jhc2gKcGluZyA4LjguOC44',
                        )
        print(instance)
    except:
        raise Exception("Couldn't create instance")

    print("Instance created, will wait until it runs")

    for i in instance:
        while i.state['Name'] != 'running':
           print('Instance is %s' % i.state['Name'])
           time.sleep(10)
           i.reload()


if len(sys.argv) < 2:
    print("Must supply the file name with the csv credentials")
    print("Col1: Account Number")
    print("Col2: Access Key")
    print("Col3: Secret Key")
    print("Col4: AWS Bucket Name")
    print("Col5: SWATCH Cloud Domain Name")
    exit()

ACCESS_CODES_FILE =  sys.argv[1]

print("STARTING PING OF ACCOUNTS")
print("=================================")

with open(ACCESS_CODES_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        AWS_Account_Number = row[0]
        AWS_ACCESS_KEY = row[1]
        AWS_SECRET_KEY = row[2]
        AWS_Bucket_Name = row[3]
        obsrvbl_domain_name = row[4]

        #obsrvbl_policy_name = "obsrvbl_policy"
        #obsrvbl_role_name = "obsrvbl_role"
        #obsrvbl_vpc_policy_name = 'obsrvble_vpc_policy'
        AWS_REGION = 'ap-southeast-2'

        print("Ping for account:", AWS_Account_Number)
        print("SCA Account", obsrvbl_domain_name)
        print("**** role path:")
        print("arn:aws:iam::"+AWS_Account_Number+":role/obsrvbl_role")
        print(AWS_Bucket_Name)
        print("==========================================")

        #run an instance with a ping to 8.8.8.8 just to generate some TrafficType

        ping_gw(AWS_ACCESS_KEY, AWS_SECRET_KEY, 1, AWS_REGION)
