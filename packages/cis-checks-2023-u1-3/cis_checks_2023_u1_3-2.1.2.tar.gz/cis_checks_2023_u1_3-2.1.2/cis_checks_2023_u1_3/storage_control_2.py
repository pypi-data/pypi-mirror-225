"""storage_control_2.py"""
from botocore.exceptions import ClientError

from cis_checks_2023_u1_3.utils import *

global logger
logging.basicConfig(level=logging.INFO)


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join( BASE_DIR,'..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+
# datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})


# --- Control Parameters ---


# --- Global ---
# def __init__(self):
#     IAM_CLIENT = self.session.client('iam')
#     S3_CLIENT = self.session.client('iam')

# --- 2 Storage ---

# --- 2.1 Simple Storage Service (S3) ---


class storage_control:
    # 2.1.1 Ensure all S3 buckets employ encryption-at-rest
    def control_2_1_1_s3_default_encryption_at_rest(self, buckets):
        logger.info(" ---Inside storage_control_2 :: control_2_1_1_s3_default_encryption_at_rest()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.1.1"
        description = "Ensure all S3 buckets employ encryption-at-rest"
        scored = True
        client = self.session.client('s3')
        for bucket in buckets:
            bucket_name = bucket['Name']

            try:
                resp = client.get_bucket_encryption(
                    Bucket=bucket_name
                )
                rules = resp['ServerSideEncryptionConfiguration']['Rules']
                # print(rules)
                for i in rules:
                    if i['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms' or 'AES256':
                        continue

            except botocore.exceptions.ClientError:
                result = "Not Compliant"
                failReason = "Default server side encryption is not enabled for S3 Bucket"
                offenders.append(bucket_name)
                continue

            # except KeyError:
            #     result = False
            #     failReason = "The S3 buckets are not encrypted with AWS Key Management Service(AWS KMS)"
            #     offenders.append(bucket_name)
            #     continue
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.1.2 Ensure S3 Bucket Policy is set to deny HTTP requests
    def control_2_1_2_s3_deny_http_requests(self, buckets):
        logger.info(" ---Inside storage_control_2 :: control_2_1_2_s3_deny_http_requests()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.1.2"
        description = "Ensure S3 Bucket Policy is set to deny HTTP requests"
        scored = True
        client = self.session.client('s3')
        for bucket in buckets:
            bucket_name = bucket['Name']

            try:
                resp = client.get_bucket_policy(
                    Bucket=bucket_name
                )
                ssl_requests_only = ""
                # print(resp)
                policy = json.loads(resp["Policy"])
                for i in policy["Statement"]:
                    if i["Effect"] == "Deny" and i["Condition"] == {'Bool': {'aws:SecureTransport': 'false'}}:
                        ssl_requests_only = "True"
                        break
                    elif i["Effect"] == "Allow" and i["Condition"] == {'Bool': {'aws:SecureTransport': 'true'}}:
                        ssl_requests_only = "True"
                        break
                if ssl_requests_only != "True":
                    raise KeyError
            except botocore.exceptions.ClientError:
                result = "Not Compliant"
                failReason = "An error occurred (NoSuchBucketPolicy) when calling the GetBucketPolicy operation: The " \
                             "bucket policy does not exist"
                offenders.append(bucket_name)
                continue
            except KeyError:
                result = "Not Compliant"
                failReason = "The S3 buckets doesn't have policies that require requests to use Secure Socket Layer (" \
                             "SSL)"
                offenders.append(bucket_name)
                continue

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.1.3 Ensure MFA Delete is enabled on S3 buckets
    def control_2_1_3_s3_mfa_delete_enabled(self, buckets):
        logger.info(" ---Inside storage_control_2 :: control_2_1_3_s3_mfa_delete_enabled()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.1.3"
        description = "Ensure MFA Delete is enabled on S3 buckets"
        scored = True
        client = self.session.client('s3')
        for bucket in buckets:
            bucket_name = bucket['Name']

            try:
                resp = client.get_bucket_versioning(
                    Bucket=bucket_name,
                )
                mfa_delete = resp['MFADelete']
            except KeyError:
                result = "Not Compliant"
                failReason = "Either bucket versioning is not enabled or configuration not found"
                offenders.append(bucket_name)
                continue
            except ClientError as e:
                result = "Not Compliant"
                failReason = e.response['Error']['Code']
                offenders.append(bucket_name)
                continue

            if not mfa_delete == 'Enabled':
                result = "Not Compliant"
                failReason = "MFA Delete is not enabled on S3 buckets"
                offenders.append(bucket_name)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.1.4 Ensure all data in Amazon S3 has been discovered, classified and secured when required
    def control_2_1_4_ensure_all_data_discovered_classified_secured(self):
        logger.info(" ---Inside storage_control_2 :: control_2_1_4_ensure_all_data_discovered_classified_secured()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        offenders = []
        control = "2.1.4"
        description = "Ensure all data in Amazon S3 has been discovered, classified and secured when required, " \
                      "please verify manually"
        scored = True
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 2.1.5 Ensure that S3 Buckets are configured with 'Block public access (bucket settings)'
    def control_2_1_5_s3_blocks_public_access(self, buckets):
        logger.info(" ---Inside storage_control_2 :: control_2_1_5_s3_blocks_public_access()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        offenders = []
        control = "2.1.5"
        description = "Ensure that S3 Buckets are configured with 'Block public access (bucket settings)"
        scored = True
        failReason = ""
        client = self.session.client('s3')
        for bucket in buckets:
            bucket_name = bucket['Name']

            try:
                resp = client.get_public_access_block(
                    Bucket=bucket_name
                )

                public_access_block = resp['PublicAccessBlockConfiguration']
                if public_access_block['BlockPublicAcls'] == 'False':
                    raise KeyError
                if public_access_block['IgnorePublicAcls'] == 'False':
                    raise KeyError
                if public_access_block['BlockPublicPolicy'] == 'False':
                    raise KeyError
                if public_access_block['RestrictPublicBuckets'] == 'False':
                    raise KeyError

            except botocore.exceptions.ClientError:
                result = "Not Compliant"
                failReason = "The Block Public Access setting does not restrict public bucket ACLs or the public " \
                             "policies"
                offenders.append(bucket_name)
                continue
            except KeyError:
                result = "Not Compliant"
                failReason = "The Block Public Access setting does not restrict public bucket ACLs or the public " \
                             "policies"
                offenders.append(bucket_name)
                continue

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # --- 2.2 Elastic Compute Cloud (EC2) ---
    # 2.2.1 Ensure that all your Amazon Elastic Block Store (EBS) volumes are encrypted
    def control_2_2_1_ebs_volumes_encrypted(self, regions: list) -> dict:
        logger.info(" ---Inside storage_control_2 :: control_2_2_1_ebs_volumes_encrypted()---")
        self.refresh_session()

        """Summary
        
        Args:
            regions TYPE: list
    
        Returns:
            TYPE: dict
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.2.1"
        description = "Ensure that all your Amazon Elastic Block Store (EBS) volumes are encrypted"
        scored = True

        for region in regions:
            client = self.session.client('ec2', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response = client.describe_volumes()
                else:
                    response = client.describe_volumes(
                        NextToken=marker
                    )
                for volume in response['Volumes']:
                    encrypted = volume['Encrypted']
                    if not encrypted:
                        result = "Not Compliant"
                        offenders.append(volume['VolumeId'])
                        failReason = "Volume is not encrypted"

                try:
                    marker = response['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

    # --- 2.3 Relational Database Service (RDS) ---
    # 2.3.1 Ensure that encryption is enabled for RDS Instances

    def control_2_3_1_rds_encryption_enabled(self, rds_instances: dict) -> dict:
        logger.info(" ---Inside storage_control_2 :: control_2_3_1_rds_encryption_enabled()---")
        self.refresh_session()

        """Summary
        
        Args:
            regions TYPE: list
    
        Returns:
            TYPE: dict
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.3.1"
        description = "Ensure that encryption is enabled for RDS Instances"
        scored = True

        for region, instances in rds_instances.items():
            for instance in instances:
                encrypted = instance['StorageEncrypted']
                if not encrypted:
                    result = "Not Compliant"
                    offenders.append(instance['DBInstanceIdentifier'])
                    failReason = 'DB instance is not encrypted'

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

    # 2.3.2 Ensure Auto Minor Version Upgrade feature is Enabled for RDS Instances

    def control_2_3_2_rds_auto_minor_version_upgrade_enabled(self, rds_instances: dict) -> dict:
        logger.info(" ---Inside storage_control_2 :: control_2_3_2_rds_auto_minor_version_upgrade_enabled()---")
        self.refresh_session()

        """Summary
        
        Args:
            regions TYPE: list
    
        Returns:
            TYPE: dict
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.3.2"
        description = "Ensure Auto Minor Version Upgrade feature is Enabled for RDS Instances"
        scored = True

        for region, instances in rds_instances.items():
                for instance in instances:
                    version_upgrade = instance['AutoMinorVersionUpgrade']
                    if not version_upgrade:
                        result = "Not Compliant"
                        offenders.append(instance['DBInstanceIdentifier'])
                        failReason = 'Auto Minor Version Upgrade feature is not Enabled for RDS Instances'

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

    # 2.3.3 Ensure that public access is not given to RDS Instance
    def control_2_3_3_rds_publicly_accessible(self, rds_instances: dict) -> dict:
        logger.info(" ---Inside storage_control_2 :: control_2_3_3_rds_publicly_accessible()")
        self.refresh_session()

        """Summary
        
        Args:
            regions TYPE: list
    
        Returns:
            TYPE: dict
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "2.3.3"
        description = "Ensure that public access is not given to RDS Instance"
        scored = True

        for region, instances in rds_instances.items():
            for instance in instances:
                public = instance['PubliclyAccessible']
                if public:
                    result = "Not Compliant"
                    offenders.append(instance['DBInstanceIdentifier'])
                    failReason = 'DB Instance is publicly accessible'

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

    # 2.4.1 Ensure that encryption is enabled for EFS file systems
    def control_2_4_1_encryption_enabled_for_efs(self):
        logger.info(" ---Inside storage_control_2 :: control_2_4_1_encryption_enabled_for_efs()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        offenders = []
        control = "2.4.1"
        description = "Ensure that encryption is enabled for EFS file systems, please verify manually"
        scored = True
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}
