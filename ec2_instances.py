import boto3
import pytz
import psycopg2
from psycopg2.extras import Json
from datetime import datetime, timezone

class Ec2Instance(object):
    def getInstances(self):
        # Current time and timezone YY/MM/DD
        report_date = datetime.today().strftime('%Y-%m-%d')
        utc_dt = datetime.now(timezone.utc)
        last_update = utc_dt.astimezone()

        # Get Region
        my_session = boto3.session.Session()
        region = my_session.region_name

        account_id = boto3.client('sts').get_caller_identity().get('Account')

        # Fetch EC2 fields
        client = boto3.client('ec2')
        response = client.describe_instances()

        ec2_list = []
        for instances in response['Reservations']:
            for data in instances['Instances']:
                ec2 = {
                    'AwsAccountId':         account_id,
                    'ReportDate':           report_date,
                    'LastUpdate':           last_update,
                    'Region':               region,

                    'InstanceId':           data.get('InstanceId'),
                    'ImageId':              data.get('ImageId'),
                    'Architecture':         data.get('Architecture'),
                    'VirtualizationType':   data.get('VirtualizationType'),
                    'Hypervisor':           data.get('Hypervisor'),
                    'SourceDestinationCheck':   data.get('SourceDestCheck'),
                    'PublicDnsName':        data.get('PublicDnsName'),
                    'InstanceType':         data.get('InstanceType'),
                    'State':                data.get('State'),
                    'StateTransitionReason':    data.get('StateTransitionReason'),
                    'KernelId':             data.get('KernelId'),
                    'ClientToken':          data.get('ClientToken'),
                    'PrivateDnsName':       data.get('PrivateDnsName'),
                    'Monitoring':           data.get('Monitoring'),
                    'AmiLaunchIndex':       data.get('AmiLaunchIndex'),
                    'RootDeviceType':       data.get('RootDeviceType'),
                    'Platform':             data.get('Platform'),
                    'VpcId':                data.get('VpcId'),
                    'SubnetId':             data.get('SubnetId'),
                    'KeyName':              data.get('KeyName'),
                    'PrivateIpAddress':     data.get('PrivateIpAddress'),
                    'PublicIpAddress':      data.get('PublicIpAddress'),
                    'PublicIpAddress2':     data.get('PublicIp'),
                    'Tenancy':              data.get('Tenancy'),
                    'LaunchTime':           data.get('LaunchTime'),
                    'Affinity':             data.get('Affinity'),
                    'AvailabilityZone':     data.get('AvailabilityZone'),
                    'GroupName':            data.get('GroupName'),
                    'SpreadDomain':         data.get('SpreadDomain'),
                    'InstanceLifecycle':    data.get('InstanceLifecycle'),
                    'IamInstanceProfileArn':    data.get('IamInstanceProfile'),
                    'IamInstanceProfileId': data.get('IamInstanceProfile'),
                    'EbsOptimized':         data.get('EbsOptimized'),
                    'HostId':               data.get('HostId')
                }

                ec2_instance_id = data.get('InstanceId'),
                image_id = data.get('ImageId'),
                architecture = data.get('Architecture'),
                virtualization_type = data.get('VirtualizationType'),
                hypervisor = data.get('Hypervisor'),
                source_destination_check = data.get('SourceDestCheck'),
                public_dns_name = data.get('PublicDnsName'),
                instance_type = data.get('InstanceType'),
                state = data.get('State'),
                state_transition_reason = data.get('StateTransitionReason'),
                kernel_id = data.get('KernelId'),
                client_token = data.get('ClientToken'),
                private_dns_name = data.get('PrivateDnsName'),
                monitoring = data.get('Monitoring'),
                ami_launch_index = data.get('AmiLaunchIndex'),
                root_device_type = data.get('RootDeviceType'),
                platform = data.get('Platform'),
                aws_account_id = data.get('OwnerId'),
                vpc_id = data.get('VpcId'),
                subnet_id = data.get('SubnetId'),
                key_name = data.get('KeyName'),
                private_ip_address = data.get('PrivateIpAddress'),
                public_ip_address = data.get('PublicIpAddress'),
                public_ip_address2 = data.get('PublicIp')
                tenancy = data.get('Tenancy'),
                launch_date = data.get('LaunchTime'),
                affinity = data.get('Affinity'),
                availability_zone = data.get('AvailabilityZone'),
                group_name = data.get('GroupName'),
                spread_domain = data.get('SpreadDomain'),
                instance_lifecycle = data.get('InstanceLifecycle'),
                iam_profile_arn = data.get('IamInstanceProfile'),
                iam_profile_id = data.get('IamInstanceProfile'),
                ebs_optimized = data.get('EbsOptimized'),
                host_id = data.get('HostId')


                connection = psycopg2.connect(user="tuckermccoy",
                                  password="password123",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="billing")
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO reserved_instances VALUES (%s, %s, %s,  %s,  %s,  %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (ec2_instance_id, image_id, architecture, virtualization_type, hypervisor, source_destination_check, public_dns_name, instance_type, state, state_transition_reason, kernel_id, client_token, private_dns_name, monitoring, ami_launch_index, root_device_type, platform, aws_account_id, vpc_id, subnet_id, report_date, key_name, private_ip_address, public_ip_address, public_ip_address2, tenancy, last_update, launch_date, affinity, availability_zone, group_name, spread_domain, instance_lifecycle, iam_profile_arn, iam_profile_id, ebs_optimized, host_id, region))
                connection.commit()
                print("Record inserted successfully into table")
            except psycopg2.IntegrityError:
                print(str(reserved_instance_id[0]), "for ", report_date, "exists already!")

        ec2_list.append(ec2)
        print(ec2)

def main():
    x = Ec2Instance()
    x.getInstances()

if __name__ == "__main__":
    main()