import csv
import sys
import main_aws_setup
import boto3
import json
from botocore.exceptions import ClientError


if len(sys.argv) < 2:
    print("Must supply the file name with the csv credentials")
    print("Col1: Account Number")
    print("Col2: Access Key")
    print("Col3: Secret Key")
    print("Col4: AWS Bucket Name")
    print("Col5: SWATCH Cloud Domain Name")
    exit()

ACCESS_CODES_FILE =  sys.argv[1]

print("STARTING Cleanup")
print("=================================")

with open(ACCESS_CODES_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        AWS_Account_Number = row[0]
        AWS_ACCESS_KEY = row[1]
        AWS_SECRET_KEY = row[2]
        AWS_Bucket_Name = row[3]
        obsrvbl_domain_name = row[4]
        obsrvbl_role_name = "obsrvbl_role"
        obsrvbl_domain_name = "cisco-aws-apjc-03"
        obsrvbl_vpc_policy_name = 'obsrvble_vpc_policy'
        obsrvbl_policy_name = "obsrvbl_policy"

        print("Cleaning Account", AWS_Account_Number)
        print("==========================================")

        ## Get the VPC name

        try:
            ec2 = boto3.client('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
            response = ec2.describe_vpcs()
            AWS_VPC_Name = response.get('Vpcs', [{}])[0].get('VpcId', '')
            print("Recieved VPC ID "+AWS_VPC_Name)
        except ClientError as e:
            print(e)

        iam = boto3.client('iam', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

        #detach policy
        try:
            print ("Detaching policy")
            response = iam.detach_role_policy(
                RoleName=obsrvbl_role_name,
                PolicyArn='arn:aws:iam::'+AWS_Account_Number+':policy/'+obsrvbl_policy_name
                )
        except ClientError as e:
            print(e)
        else:
            print('policy detach success')

        try:
            print ("Detaching VPC policy")
            response = iam.detach_role_policy(
                RoleName=obsrvbl_role_name,
                PolicyArn='arn:aws:iam::'+AWS_Account_Number+':policy/'+obsrvbl_vpc_policy_name
                )
        except ClientError as e:
            print(e)
        else:
            print('policy detach success')


        try:
            print("Deleting Role")
            response = iam.delete_role(
                RoleName=obsrvbl_role_name
                )
        except ClientError as e:
            print(e)
        else:
            print('delete role success')

        try:
            print("Deleting Policy")
            response = iam.delete_policy(
                PolicyArn='arn:aws:iam::'+AWS_Account_Number+':policy/'+obsrvbl_policy_name
                )
        except ClientError as e:
            print(e)
        else:
            print('delete policy success')

        try:
            print("Deleting VPC Policy")
            response = iam.delete_policy(
                PolicyArn='arn:aws:iam::'+AWS_Account_Number+':policy/'+obsrvbl_vpc_policy_name
                )
        except ClientError as e:
            print(e)
        else:
            print('delete policy success')

        try:
            print("Getting VPC Flow Logs ID")
            response = ec2.describe_flow_logs()
            if 0 in response['FlowLogs']:
                    if 'FlowLogId' in response['FlowLogs'][0]:
                        print('found '+ response['FlowLogs'][0]['FlowLogId'])
                        FlowLogID = response['FlowLogs'][0]['FlowLogId']
                    else:
                        print("Flow log ID not found")
                        FlowLogID='123123123'
            else:
                print("flow log ID not found")
                FlowLogID='123123123'
        except ClientError as e:
            print(e)

        try:
            print("Removing VPC Flow Logs ID ", FlowLogID)
            response = ec2.delete_flow_logs(
                FlowLogIds=[FlowLogID]
                    )
            print('Flow log deleted successfully')
        except ClientError as e:
            print(e)




        print("all done for", AWS_Account_Number)
