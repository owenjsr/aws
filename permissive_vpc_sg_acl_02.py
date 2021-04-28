import boto3
from botocore.exceptions import ClientError
import sys
from random import randrange

#check if any arguments given
def main():

    if len(sys.argv) < 3:
        print("Must supply AWS Key and Secret as arguments,,, exiting")
        exit()

    AWS_ACCESS_KEY = sys.argv[1]
    AWS_SECRET_KEY = sys.argv[2]
    AWS_REGION = 'ap-southeast-2'

    print("Running Scenario 2: Permissive VPC SG ACL")
    print("====================================================================")

    premissive_vpc_sg(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_REGION)

    print("Scenario 2: All done")
    print("====================================================================")

def premissive_vpc_sg(AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_REGION):
    #get VPC ID
    try:
        ec2 = boto3.client('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name=AWS_REGION)
        response = ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
        print("Recieved VPC ID "+vpc_id)
    except ClientError as e:
        print(e)

    #create security group
    try:
        response = ec2.create_security_group(GroupName='AWS_Security_Group'+str(randrange(100000)),
                                             Description='An overly permissive SG',
                                             VpcId=vpc_id)
        security_group_id = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 0,
                 'ToPort': 65535,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'udp',
                 'FromPort': 0,
                 'ToPort': 65535,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
        print('Ingress Successfully Set %s' % data)
    except ClientError as e:
        print(e)


if __name__ == "__main__":
    main()
