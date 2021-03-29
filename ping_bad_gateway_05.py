import boto3
import time
from botocore.exceptions import ClientError
import sys

def main():
#check if any arguments given
    if len(sys.argv) < 3:
        print("Must supply AWS Key and Secret as arguments,,, exiting")
        exit()

    AWS_ACCESS_KEY = sys.argv[1]
    AWS_SECRET_KEY = sys.argv[2]
    NUMBER_OF_INSTANCES = 1
    AWS_REGION = 'ap-southeast-2'

    print("Running Scenario 5: generating an instance to ping a bad destination")
    print("====================================================================")

    ping_bad_gw(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES)

    print("Running Scenario 5: Completed")
    print("====================================================================")

def ping_bad_gw(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES, AWS_REGION):

    ec2 = boto3.resource('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name=AWS_REGION)

    print("Creating the instance to ping the bad resource")
    try:
        instance = ec2.create_instances(
                        ImageId='ami-0b3d7a5ecc2daba4c',
                        InstanceType='t2.micro',
                        MaxCount=NUMBER_OF_INSTANCES,
                        MinCount=NUMBER_OF_INSTANCES,
                        UserData='IyEvYmluL2Jhc2gKcGluZyAtYyAxMCA5Mi42My4xOTcuNDgKc2h1dGRvd24gLWggbm93Cg==',
                        )
        print(instance)
    except:
        raise Exception("Couldn't create instance")

    print("Instance created, will wait until it runs then stops")

    for i in instance:
        while i.state['Name'] != 'stopped':
           print('Instance is %s' % i.state['Name'])
           time.sleep(10)
           i.reload()
        try:
            print("Terminating Instance")
            response = i.terminate()
            print("Instance Terminated")
        except:
            print("There was an error terminating the instance. You may need to terminate it manually")

if __name__ == "__main__":
    main()
