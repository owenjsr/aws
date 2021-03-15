import csv
import sys
import rogue_workload_01
import permissive_vpc_sg_acl_02
import exposed_workload_recon_03
import data_exfil_04
import ping_bad_gateway_05

if len(sys.argv) < 2:
    print("Must supply the file name with the csv credentials")
    print("Col1: Account Number")
    print("Col2: Access Key")
    print("Col3: Secret Key")
    print("Col4: AWS Bucket Name")
    print("Col5: SWATCH Cloud Domain Name")
    exit()

ACCESS_CODES_FILE =  sys.argv[1]

print("STARTING ATTACKS OF ACCOUNTS")
print("=================================")

with open(ACCESS_CODES_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        AWS_Account_Number = row[0]
        AWS_ACCESS_KEY = row[1]
        AWS_SECRET_KEY = row[2]
        AWS_Bucket_Name = row[3]
        NUMBER_OF_INSTANCES = 2 #Used in attack 01 & 4 (default 2)
        Scan_Count = 250 #Used in Attack03 (default 250)

        print("Attacking Account", AWS_Account_Number)
        print("************************************************************************************************")

        print("AWS_ACCESS_KEY", AWS_ACCESS_KEY)
        print("AWS_SECRET_KEY", AWS_SECRET_KEY)
        print("AWS_Bucket_Name", AWS_Bucket_Name)

        print("Running Scenario 1: launch instances to trigger a watchlist")
        print("====================================================================")

        rogue_workload_01.rogue_workload(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES)

        print ("Scenario 01: All Done")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        print("Running Scenario 2: Permissive VPC SG ACL")
        print("====================================================================")

        permissive_vpc_sg_acl_02.premissive_vpc_sg(AWS_ACCESS_KEY,AWS_SECRET_KEY)

        print("Scenario 2: All done")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        print("Running Scenario 3: Exposed Workload recon")
        print("====================================================================")

        exposed_workload_recon_03.exposed_workload_recon(AWS_ACCESS_KEY, AWS_SECRET_KEY,NUMBER_OF_INSTANCES,Scan_Count)

        print ("SCENARIO 03: COMPLETED")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        print("Running Scenario 4: data exfil via DNS port")
        print("====================================================================")

        data_exfil_04.data_exfil(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES)

        print("Running Scenario 4: Completed")
        print("====================================================================")

        print("Running Scenario 5: generating an instance to ping a bad destination")
        print("====================================================================")

        ping_bad_gateway_05.ping_bad_gw(AWS_ACCESS_KEY, AWS_SECRET_KEY, NUMBER_OF_INSTANCES)

        print("Running Scenario 5: Completed")
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


    print("Processed all lines. Check log for errors.")
