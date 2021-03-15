import csv
import sys
import main_aws_setup

if len(sys.argv) < 2:
    print("Must supply the file name with the csv credentials")
    print("Col1: Account Number")
    print("Col2: Access Key")
    print("Col3: Secret Key")
    print("Col4: AWS Bucket Name")
    print("Col5: SWATCH Cloud Domain Name")
    exit()

ACCESS_CODES_FILE =  sys.argv[1]

print("STARTING PROVISIONING OF ACCOUNTS")
print("=================================")


with open(ACCESS_CODES_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        AWS_Account_Number = row[0]
        AWS_ACCESS_KEY = row[1]
        AWS_SECRET_KEY = row[2]
        AWS_Bucket_Name = row[3]
        obsrvbl_domain_name = row[4]

        obsrvbl_policy_name = "obsrvbl_policy"
        obsrvbl_role_name = "obsrvbl_role"
        obsrvbl_vpc_policy_name = 'obsrvble_vpc_policy'
        AWS_REGION = 'ap-southeast-2'

        print("Provisioning Account", AWS_Account_Number)
        print("==========================================")

        print("AWS_ACCESS_KEY", AWS_ACCESS_KEY)
        print("AWS_SECRET_KEY", AWS_SECRET_KEY)
        print("AWS_Bucket_Name", AWS_Bucket_Name)
        print("obsrvbl_domain_name", obsrvbl_domain_name)

        main_aws_setup.initialise_aws_account(AWS_ACCESS_KEY,AWS_SECRET_KEY,AWS_Bucket_Name,obsrvbl_domain_name, AWS_REGION)

        #run an instance with a ping to 8.8.8.8 just to generate some TrafficType

        main_aws_setup.ping_gw(AWS_ACCESS_KEY, AWS_SECRET_KEY, 1, AWS_REGION)


    print("Processed all lines. Check log for errors.")
