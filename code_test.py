import boto3
import pytz
import psycopg2
from psycopg2.extras import Json
from pprint import pprint
from datetime import datetime, timezone

class VPCs(object):
    def getVPC(self):
        # Current time and timezone YY/MM/DD
        report_date = datetime.today().strftime('%Y-%m-%d')
        last_update = datetime.now(tz = pytz.utc)

        # Get Region
        my_session = boto3.session.Session()
        my_region = my_session.region_name

        # Fetch VPC fields
        client = boto3.client('ec2')
        response = client.describe_vpcs()

        vpc_list = []
        for vpcs in response['Vpcs']:
            vpc = {
                'ReportDate':   report_date,
                'LastUpdate':   last_update,
                'Region':   my_region,

                'VpcId':    vpcs.get('VpcId'),
                'InstanceTenancy':  vpcs.get('InstanceTenancy'),
                'IsDefault':    vpcs.get('IsDefault'),
                'State':    vpcs.get('State'),
                'DhcpOptionsId':    vpcs.get('DhcpOptionsId'),
                'OwnerId':  vpcs.get('OwnerId'),
                'CidrBlock':    vpcs.get('CidrBlock')
            }

            vpc_id = vpcs.get('VpcId'),
            instance_tenancy = vpcs.get('InstanceTenancy'),
            is_default = vpcs.get('IsDefault'),
            state = vpcs.get('State'),
            dhcp_options_id = vpcs.get('DhcpOptionsId'),
            aws_account_id = vpcs.get('OwnerId'),
            region = vpcs.get('Region'),
            cidr_block = vpcs.get('CidrBlock')

            connection = psycopg2.connect(user="tuckermccoy",
                                  password="password123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="billing")
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO reserved_instances VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (report_date, vpc_id, instance_tenancy, is_default, state, dhcp_options_id, aws_account_id, region, cidr_block, last_update))
                connection.commit()
                print("Record inserted successfully into table")
            except psycopg2.IntegrityError:
                print(str(vpc_id[0]), "for ", report_date, "exists already!")

            vpc_list.append(vpc)
            pprint(vpc)

        return {'Vpcs': vpc_list}

def main():
    x = VPCs()
    x.getVPC()

if __name__ == "__main__":
    main()