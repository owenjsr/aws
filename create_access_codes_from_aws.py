import csv
import sys
import os
import boto3
from botocore.exceptions import ClientError


if len(sys.argv) < 3:
    print("Must supply the input file name with the aws credentials and the outputfile name as credentials")
    exit()

INPUT_FILE =  sys.argv[1]
OUTPUT_FILE =  sys.argv[2]
OUTPUT_LIST = []

print("Starting CSV Creation")
print("=================================")

with open(INPUT_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    x = 0
    for row in csv_reader:
        #y = 0
        x = x + 1
        if row[6] == 'aws-account-id':
            continue
            print("Skipping first row")
        # if x == 3: break   ## Used to process only the first lines
        AWS_Account_Number = row[6]
        print('Account number is', AWS_Account_Number)
        for line in row[10].splitlines():
            #y = y + 1
            input = line.split("=")
            if 'export AWS_ACCESS_KEY_ID' in input:
                AWS_ACCESS_KEY_ID = input[1]
            if 'export AWS_SECRET_ACCESS_KEY' in input:
                AWS_SECRET_ACCESS_KEY = input[1]
            if 'export AWS_SESSION_TOKEN' in input:
                AWS_SESSION_TOKEN = input[1]

        print("ACCESS KEY", AWS_ACCESS_KEY_ID)
        #print("AWS_SECRET_ACCESS_KEY", AWS_SECRET_ACCESS_KEY)
        #print("AWS_SESSION_TOKEN", AWS_SESSION_TOKEN)

        iam = boto3.client('iam', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY, aws_session_token=AWS_SESSION_TOKEN)

        try:
            # Create a user
            print("Creating a user for account ", AWS_Account_Number)
            response = iam.create_user(
                    UserName='aws_provisioning_user',
                    PermissionsBoundary='arn:aws:iam::aws:policy/AdministratorAccess',
                )
        except ClientError as e:
            print(e)

        #Create IAM_USER_NAME
        try:
            # Create an access key
            print("Creating an access key for account", AWS_Account_Number)
            response = iam.create_access_key(
                UserName='aws_provisioning_user'
            )

            #print("Accesskey ID", response['AccessKey']['AccessKeyId'])
            ACCESS_KEY_ID = response['AccessKey']['AccessKeyId']
            #print("Secret Key", response['AccessKey']['SecretAccessKey'])
            ACCESS_SECRET_KEY = response['AccessKey']['SecretAccessKey']
        except ClientError as e:
            print(e)

        OUTPUT_LIST.append([AWS_Account_Number, ACCESS_KEY_ID, ACCESS_SECRET_KEY])


##Write output to files
print("Writing output to File", OUTPUT_FILE)

with open(OUTPUT_FILE, mode='w') as output_file:
    output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in OUTPUT_LIST:
        #print("Writing line,", line)
        output_writer.writerow(line)


print("Processed all lines. Check log for errors. Total of ", x-2)
