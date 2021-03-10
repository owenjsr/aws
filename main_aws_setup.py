import boto3
import json
import sys
from botocore.exceptions import ClientError


def create_obsrvble_policy(AWS_ACCESS_KEY,AWS_SECRET_KEY,policyname):
    iam = boto3.client('iam', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    obsrvbl_policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "autoscaling:Describe*",
            "cloudtrail:LookupEvents",
            "cloudwatch:Get*",
            "cloudwatch:List*",
            "ec2:Describe*",
            "elasticache:Describe*",
            "elasticache:List*",
            "elasticloadbalancing:Describe*",
            "guardduty:Get*",
            "guardduty:List*",
            "iam:Get*",
            "iam:List*",
            "inspector:*",
            "rds:Describe*",
            "rds:List*",
            "redshift:Describe*",
            "workspaces:Describe*",
            "route53:List*"
          ],
          "Effect": "Allow",
          "Resource": "*"
        },
        {
          "Action": [
            "logs:Describe*",
            "logs:GetLogEvents",
            "logs:FilterLogEvents",
            "logs:PutSubscriptionFilter",
            "logs:DeleteSubscriptionFilter"
          ],
          "Effect": "Allow",
          "Resource": "*"
        },
        {
          "Sid": "CloudCompliance",
          "Action": [
            "access-analyzer:ListAnalyzers",
            "cloudtrail:DescribeTrails",
            "cloudtrail:GetEventSelectors",
            "cloudtrail:GetTrailStatus",
            "cloudtrail:ListTags",
            "cloudwatch:DescribeAlarmsForMetric",
            "config:Get*",
            "config:Describe*",
            "ec2:GetEbsEncryptionByDefault",
            "iam:GenerateCredentialReport",
            "iam:Get*",
            "iam:List*",
            "kms:GetKeyRotationStatus",
            "kms:ListKeys",
            "logs:DescribeMetricFilters",
            "logs:Get*",
            "logs:List*",
            "logs:Lookup*",
            "organizations:ListPolicies",
            "s3:GetAccelerateConfiguration",
            "s3:GetAccessPoint",
            "s3:GetAccessPointPolicy",
            "s3:GetAccessPointPolicyStatus",
            "s3:GetAccountPublicAccessBlock",
            "s3:GetAnalyticsConfiguration",
            "s3:GetBucket*",
            "s3:GetEncryptionConfiguration",
            "s3:GetInventoryConfiguration",
            "s3:GetLifecycleConfiguration",
            "s3:GetMetricsConfiguration",
            "s3:GetObjectAcl",
            "s3:GetObjectVersionAcl",
            "s3:GetReplicationConfiguration",
            "s3:ListAccessPoints",
            "s3:ListAllMyBuckets",
            "securityhub:Get*",
            "sns:ListSubscriptionsByTopic"
          ],
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }

    response = iam.create_policy(
        PolicyName=policyname,
        PolicyDocument=json.dumps(obsrvbl_policy)
    )

    return response

def create_obsrvble_role(AWS_ACCESS_KEY,AWS_SECRET_KEY,rolename,domainname):
    iam = boto3.client('iam', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    AssumedRolePolicyDocument = {"Version": "2012-10-17","Statement": [{"Effect": "Allow","Principal": {"AWS": "arn:aws:iam::757972810156:root"},"Action": "sts:AssumeRole","Condition": {"StringEquals": {"sts:ExternalId": domainname}}}]}

    response = iam.create_role(
        RoleName=rolename,
        AssumeRolePolicyDocument=json.dumps(AssumedRolePolicyDocument),
    )

    return response

def attach_policy_to_role(AWS_ACCESS_KEY,AWS_SECRET_KEY,accountnumber,policyname,policyrole):
    iam = boto3.client('iam', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    response = iam.attach_role_policy(
        RoleName=policyrole,
        PolicyArn='arn:aws:iam::'+accountnumber+':policy/'+policyname
    )

    return response

def create_obsrvble_vpc_policy(AWS_ACCESS_KEY,AWS_SECRET_KEY,policyname,bucketname):
    iam = boto3.client('iam', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    obsrvbl_policy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::"+bucketname
      ]
    },
    {
      "Action": [
        "s3:GetObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::"+bucketname+"/*"
      ]
    }
  ]
}

    response = iam.create_policy(
        PolicyName=policyname,
        PolicyDocument=json.dumps(obsrvbl_policy)
    )

    return response

def create_flow_logs(AWS_ACCESS_KEY,AWS_SECRET_KEY,vpc,bucket):
    ec2 = boto3.client('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    response = ec2.create_flow_logs(
        ResourceIds=[vpc],
            ResourceType='VPC',
            TrafficType='ALL',
            LogDestinationType='s3',
            LogDestination='arn:aws:s3:::'+bucket,
            LogFormat='${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status} ${vpc-id} ${subnet-id} ${instance-id} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr}',
            MaxAggregationInterval=60
    )

    return response

def get_vpc_id(AWS_ACCESS_KEY,AWS_SECRET_KEY):
    try:
        ec2 = boto3.client('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
        response = ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        print("Recieved VPC ID "+vpc_id)
        return vpc_id
    except ClientError as e:
        print(e)

def create_s3_bucket(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Bucket_Name):
    REGION = "ap-southeast-2"
    s3_client = boto3.client('s3', region_name=REGION, aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
    location = {'LocationConstraint': REGION}
    s3_client.create_bucket(Bucket=AWS_Bucket_Name, CreateBucketConfiguration=location)

def main():

    if len(sys.argv) < 4:
        print("Must supply the following arguments")
        print("1- AWS Account Key")
        print("2- AWS Secret Key")
        print("3- AWS Bucket Name to be created")
        exit()



    AWS_ACCESS_KEY = sys.argv[1]
    AWS_SECRET_KEY = sys.argv[2]
    AWS_Bucket_Name = sys.argv[3]
    obsrvbl_policy_name = "obsrvbl_policy"
    obsrvbl_role_name = "obsrvbl_role"
    obsrvbl_domain_name = "cisco-aws-apjc-03"
    obsrvbl_vpc_policy_name = 'obsrvble_vpc_policy'

    print("Starting to initalise AWS Account")
    print("=================================")


    initialise_aws_account(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Bucket_Name)

    print("AWS Account Done. Check for errors if any")
    print("=================================")

def initialise_aws_account(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Bucket_Name,obsrvbl_domain_name):

    obsrvbl_policy_name = "obsrvbl_policy"
    obsrvbl_role_name = "obsrvbl_role"
    #obsrvbl_domain_name = "cisco-aws-apjc-03"
    obsrvbl_vpc_policy_name = 'obsrvble_vpc_policy'

    #try to get the account NUMBER
    try:
        sts = boto3.client("sts", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        AWS_Account_Number = sts.get_caller_identity()["Account"]
        print("Got account number",AWS_Account_Number)
    except ClientError as e:
        raise Exception(e)

    ### Try to create obsrvble policy, continue if failed
    try:
        print("Creating Policy "+obsrvbl_policy_name)
        policy_creation_response = create_obsrvble_policy(AWS_ACCESS_KEY,AWS_SECRET_KEY,obsrvbl_policy_name)
    except ClientError as e:
        print(e)
        print("Carrying on...")

    else:
        print("Policy Creation Success")

    ### Try to create obsrvble Role, continue if failed
    try:
        print("Creating Role "+obsrvbl_role_name)
        role_creation_response = create_obsrvble_role(AWS_ACCESS_KEY,AWS_SECRET_KEY,obsrvbl_role_name,obsrvbl_domain_name)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("Role Creation Success")


    ##Attach obsrvbl_policy to role
    try:
        print("Attaching Role "+obsrvbl_role_name)
        role_attach_response = attach_policy_to_role(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Account_Number,obsrvbl_policy_name,obsrvbl_role_name)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("Role Attach Success")

    ### Try to create obsrvble vpc policy, exit if failed
    try:
        print("Creating VPC Policy "+obsrvbl_vpc_policy_name)
        policy_creation_response = create_obsrvble_vpc_policy(AWS_ACCESS_KEY,AWS_SECRET_KEY,obsrvbl_vpc_policy_name,AWS_Bucket_Name)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("Policy Creation Success")

    ##Attach obsrvbl_vpc_policy to role
    try:
        print("Attaching to VPC Role "+obsrvbl_role_name)
        role_attach_response = attach_policy_to_role(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Account_Number,obsrvbl_vpc_policy_name,obsrvbl_role_name)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("VPC Role Attach Success")

    ##Create S3 Bucket
    try:
        print("Creating S3 Bucket",AWS_Bucket_Name)
        response = create_s3_bucket(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Bucket_Name)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("S3 Bucket Creation Success")

    ##Getting the VPC Name
    try:
        print("Getting the VPC Name")
        AWS_VPC_Name = get_vpc_id(AWS_ACCESS_KEY,AWS_SECRET_KEY)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("Got VPC Name", AWS_VPC_Name)

    ##Create Flow logs
    try:
        print("Creating VPC Logs on "+AWS_VPC_Name)
        vpc_flow_creation = create_flow_logs(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_VPC_Name,AWS_Bucket_Name)
    except ClientError as e:
        print(e)
        print("Carrying on...")
    else:
        print("VPC Flow Creation Success")

if __name__ == '__main__':
    main()
