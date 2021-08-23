import boto3
import time
from botocore.exceptions import ClientError
import sys

#version 2: removed the need for the template by launcing instance with a
#resource instead of a client

def rogue_workload(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES, AWS_REGION):


    ec2 = boto3.resource('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY, region_name=AWS_REGION)

    try:
        instance = ec2.create_instances(
                        ImageId='ami-0b3d7a5ecc2daba4c',
                        InstanceType='t2.micro',
                        MaxCount=NUMBER_OF_INSTANCES,
                        MinCount=NUMBER_OF_INSTANCES,
                        UserData='IyEvYmluL2Jhc2gKcGluZyAtYyAxMCA5Mi42My4xOTcuNDgKc2h1dGRvd24gLWggbm93Cg==',
                        )
        print("Instances created")
        print(instance)
    except:
        raise Exception("Instances creation failed")


    print("waiting for instances to run, will then terminate them")

    for i in instance:
        print('Waiting for instance',i.instance_id,'to run')
        while i.state['Name'] != 'running':
           print('Instance', i.instance_id,'is', i.state['Name'])
           time.sleep(10)
           i.reload()
        try:
            print("Terminating Instance", i.instance_id)
            response = i.terminate()
            print("Instance Terminated")
        except:
            print("There was an error terminating the instance. You may need to terminate it manually")



def main():

    print("Running Scenario 1: launch instances to trigger a watchlist")
    print("====================================================================")


    #check if any arguments given
    if len(sys.argv) < 3:
        print("Must supply AWS Key and Secret as arguments,,, exiting")
        exit()

    AWS_ACCESS_KEY = sys.argv[1]
    AWS_SECRET_KEY = sys.argv[2]
    #LAUNCH_TEMPLATE_ID = 'AWS_Workshop_Template'
    NUMBER_OF_INSTANCES = 2
    AWS_REGION = 'ap-southeast-2'

    rogue_workload(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES, AWS_REGION)

    print ("Scenario 01: All Done")
    print("====================================================================")


if __name__ == "__main__":
    main()
