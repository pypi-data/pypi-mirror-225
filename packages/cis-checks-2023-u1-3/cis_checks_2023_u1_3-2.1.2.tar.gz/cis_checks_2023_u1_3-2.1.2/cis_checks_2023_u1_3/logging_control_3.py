"""
logging_control_3.py
"""

from cis_checks_2023_u1_3.utils import *

global logger
logging.basicConfig(level=logging.INFO)


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) LOG_CONF_PATH = os.path.join( BASE_DIR,'..',
# 'logging.conf') LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+ datetime.now().strftime(
# '%Y-%m-%d_%H-%M-%S')+ '.log') logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})


# --- 3 Logging ---


class logging_control:
    # 3.01 Ensure CloudTrail is enabled in all regions (Scored)
    def control_3_01_ensure_cloud_trail_all_regions(self, cloudtrails):
        logger.info(" ---Inside logging_control_3 :: control_3_01_ensure_cloud_trail_all_regions()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            cloudtrails (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        failReason = ""
        offenders = []
        control = "3.01"
        description = "Ensure CloudTrail is enabled in all regions"
        scored = True
        try:
            for m, n in cloudtrails.iteritems():
                for o in n:
                    if o['IsMultiRegionTrail']:
                        client = self.session.client('cloudtrail', region_name=m)
                        response = client.get_trail_status(
                            Name=o['TrailARN']
                        )
                        if response['IsLogging'] is True:
                            result = "Compliant"
                            break
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        if result is False:
            failReason = "No enabled multi region trails found"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.02 Ensure CloudTrail log file validation is enabled (Scored)
    def control_3_02_ensure_cloudtrail_validation(self, cloudtrails):
        logger.info(" ---Inside logging_control_3 :: control_3_02_ensure_cloudtrail_validation()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            cloudtrails (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.02"
        description = "Ensure CloudTrail log file validation is enabled"
        scored = True
        try:
            for m, n in cloudtrails.iteritems():
                for o in n:
                    if o['LogFileValidationEnabled'] is False:
                        result = "Not Compliant"
                        failReason = "CloudTrails without log file validation discovered"
                        offenders.append(str(o['TrailARN']))
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        offenders = set(offenders)
        offenders = list(offenders)
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.03 Ensure the S3 bucket CloudTrail logs to is not publicly accessible (Scored)
    def control_3_03_ensure_cloudtrail_bucket_not_public(self, cloudtrails):
        logger.info(" ---Inside logging_control_3 :: control_3_03_ensure_cloudtrail_bucket_not_public()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            cloudtrails (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.03"
        description = "Ensure the S3 bucket CloudTrail logs to is not publicly accessible"
        scored = True
        try:
            for m, n in cloudtrails.iteritems():
                for o in n:
                    #  We only want to check cases where there is a bucket
                    if "S3BucketName" in str(o):
                        try:
                            response = self.session.client('s3').get_bucket_acl(Bucket=o['S3BucketName'])
                            for p in response['Grants']:
                                # logger.info("Grantee is " + str(p['Grantee']))
                                if re.search(r'(global/AllUsers|global/AuthenticatedUsers)', str(p['Grantee'])):
                                    result = "Not Compliant"
                                    offenders.append(str(o['TrailARN']) + ":PublicBucket")
                                    if "Publically" not in failReason:
                                        failReason = failReason + "Publically accessible CloudTrail bucket discovered."
                        except Exception as e:
                            result = "Not Compliant"
                            if "AccessDenied" in str(e):
                                offenders.append(str(o['TrailARN']) + ":AccessDenied")
                                if "Missing" not in failReason:
                                    failReason = "Missing permissions to verify bucket ACL. " + failReason
                            elif "NoSuchBucket" in str(e):
                                offenders.append(str(o['TrailARN']) + ":NoBucket")
                                if "Trailbucket" not in failReason:
                                    failReason = "Trailbucket doesn't exist. " + failReason
                            else:
                                offenders.append(str(o['TrailARN']) + ":CannotVerify")
                                if "Cannot" not in failReason:
                                    failReason = "Cannot verify bucket ACL. " + failReason
                    else:
                        result = "Not Compliant"
                        offenders.append(str(o['TrailARN']) + "NoS3Logging")
                        failReason = "Cloudtrail not configured to log to S3. " + failReason
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.04 Ensure CloudTrail trails are integrated with CloudWatch Logs (Scored)
    def control_3_04_ensure_cloudtrail_cloudwatch_logs_integration(self, cloudtrails):
        logger.info(" ---Inside logging_control_3 :: control_3_04_ensure_cloudtrail_cloudwatch_logs_integration()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            cloudtrails (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.04"
        description = "Ensure CloudTrail trails are integrated with CloudWatch Logs"
        scored = True
        try:
            for m, n in cloudtrails.iteritems():
                for o in n:
                    try:
                        if "arn:aws:logs" in o['CloudWatchLogsLogGroupArn']:
                            pass
                        else:
                            result = "Not Compliant"
                            failReason = "CloudTrails without CloudWatch Logs discovered"
                            offenders.append(str(o['TrailARN']))
                    except:
                        result = "Not Compliant"
                        failReason = "CloudTrails without CloudWatch Logs discovered"
                        offenders.append(str(o['TrailARN']))
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.05 Ensure AWS Config is enabled in all regions (Scored)
    def control_3_05_ensure_config_all_regions(self, regions):
        logger.info(" ---Inside logging_control_3 :: control_3_05_ensure_config_all_regions()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.05"
        description = "Ensure AWS Config is enabled in all regions"
        scored = True
        globalConfigCapture = False  # Only one region needs to capture global events
        try:
            for n in regions:
                configClient = self.session.client('config', region_name=n)
                response = configClient.describe_configuration_recorder_status()
                # Get recording status
                try:
                    if not response['ConfigurationRecordersStatus'][0]['recording'] is True:
                        result = "Not Compliant"
                        failReason = "Config not enabled in all regions, not capturing all/global events or delivery " \
                                     "channel errors"
                        offenders.append(str(n) + ":NotRecording")
                except:
                    result = "Not Compliant"
                    failReason = "Config not enabled in all regions, not capturing all/global events or delivery " \
                                 "channel errors"
                    offenders.append(str(n) + ":NotRecording")

                # Verify that each region is capturing all events
                response = configClient.describe_configuration_recorders()
                try:
                    if not response['ConfigurationRecorders'][0]['recordingGroup']['allSupported'] is True:
                        result = "Not Compliant"
                        failReason = "Config not enabled in all regions, not capturing all/global events or delivery " \
                                     "channel errors"
                        offenders.append(str(n) + ":NotAllEvents")
                except:
                    pass  # This indicates that Config is disabled in the region and will be captured above.

                # Check if region is capturing global events. Fail is verified later since only one region needs to
                # capture them.
                try:
                    if response['ConfigurationRecorders'][0]['recordingGroup']['includeGlobalResourceTypes'] is True:
                        globalConfigCapture = True
                except:
                    pass

                # Verify the delivery channels
                response = configClient.describe_delivery_channel_status()
                try:
                    if response['DeliveryChannelsStatus'][0]['configHistoryDeliveryInfo']['lastStatus'] != "SUCCESS":
                        result = "Not Compliant"
                        failReason = "Config not enabled in all regions, not capturing all/global events or delivery " \
                                     "channel errors"
                        offenders.append(str(n) + ":S3orSNSDelivery")
                except:
                    pass  # Will be captured by earlier rule
                try:
                    if response['DeliveryChannelsStatus'][0]['configStreamDeliveryInfo']['lastStatus'] != "SUCCESS":
                        result = "Not Compliant"
                        failReason = "Config not enabled in all regions, not capturing all/global events or delivery " \
                                     "channel errors"
                        offenders.append(str(n) + ":SNSDelivery")
                except:
                    pass  # Will be captured by earlier rule
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        # Verify that global events is captured by any region
        if globalConfigCapture is False:
            result = "Not Compliant"
            failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
            offenders.append("Global:NotRecording")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.06 Ensure S3 bucket access logging is enabled on the CloudTrail S3 bucket (Scored)
    def control_3_06_ensure_cloudtrail_bucket_logging(self, cloudtrails):
        logger.info(" ---Inside logging_control_3 :: control_3_06_ensure_cloudtrail_bucket_logging()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            cloudtrails (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.06"
        description = "Ensure S3 bucket access logging is enabled on the CloudTrail S3 bucket"
        scored = True
        try:
            for m, n in cloudtrails.iteritems():
                for o in n:
                    # it is possible to have a cloudtrail configured with a nonexistant bucket
                    try:
                        response = self.session.client('s3').get_bucket_logging(Bucket=o['S3BucketName'])
                    except:
                        result = "Not Compliant"
                        failReason = "Cloudtrail not configured to log to S3. "
                        offenders.append(str(o['TrailARN']))
                    try:
                        if response['LoggingEnabled']:
                            pass
                    except:
                        result = "Not Compliant"
                        failReason = failReason + "CloudTrail S3 bucket without logging discovered"
                        offenders.append("Trail:" + str(o['TrailARN']) + " - S3Bucket:" + str(o['S3BucketName']))
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.07 Ensure CloudTrail logs are encrypted at rest using KMS CMKs (Scored)
    def control_3_07_ensure_cloudtrail_encryption_kms(self, cloudtrails):
        logger.info(" ---Inside logging_control_3 :: control_3_07_ensure_cloudtrail_encryption_kms()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            cloudtrails (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.07"
        description = "Ensure CloudTrail logs are encrypted at rest using KMS CMKs"
        scored = True
        try:
            for m, n in cloudtrails.iteritems():
                for o in n:
                    try:
                        if o['KmsKeyId']:
                            pass
                    except:
                        result = "Not Compliant"
                        failReason = "CloudTrail not using KMS CMK for encryption discovered"
                        offenders.append("Trail:" + str(o['TrailARN']))
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.08 Ensure rotation for customer created CMKs is enabled (Scored)
    def control_3_08_ensure_kms_cmk_rotation(self, regions):
        logger.info(" ---Inside logging_control_3 :: control_3_08_ensure_kms_cmk_rotation()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.08"
        description = "Ensure rotation for customer created CMKs is enabled"
        scored = True
        try:
            for region in regions:
                kms_client = self.session.client('kms', region_name=region)
                paginator = kms_client.get_paginator('list_keys')
                response_iterator = paginator.paginate()
                for page in response_iterator:
                    for n in page['Keys']:
                        try:
                            rotationStatus = kms_client.get_key_rotation_status(KeyId=n['KeyId'])
                            if rotationStatus['KeyRotationEnabled'] is False:
                                keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
                                if "Default master key that protects my" not in str(
                                        keyDescription['KeyMetadata']['Description']):  # Ignore service keys
                                    result = "Not Compliant"
                                    failReason = "KMS CMK rotation not enabled"
                                    offenders.append("Key:" + str(keyDescription['KeyMetadata']['Arn']))
                        except:
                            pass  # Ignore keys without permission, for example ACM key
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.09 Ensure VPC flow logging is enabled in all VPCs (Scored)
    def control_3_09_ensure_flow_logs_enabled_on_all_vpc(self, regions):
        logger.info(" ---Inside networking_control_3 :: control_3_09_ensure_flow_logs_enabled_on_all_vpc()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.09"
        description = "Ensure VPC flow logging is enabled in all VPCs"
        scored = True
        for n in regions:
            client = self.session.client('ec2', region_name=n)
            flowlogs = client.describe_flow_logs(
                #  No paginator support in boto atm.
            )
            activeLogs = []
            for m in flowlogs['FlowLogs']:
                if "vpc-" in str(m['ResourceId']):
                    activeLogs.append(m['ResourceId'])
            vpcs = client.describe_vpcs(
                Filters=[
                    {
                        'Name': 'state',
                        'Values': [
                            'available',
                        ]
                    },
                ]
            )
            for m in vpcs['Vpcs']:
                if not str(m['VpcId']) in str(activeLogs):
                    result = "Not Compliant"
                    failReason = "VPC without active VPC Flow Logs found"
                    offenders.append(str(n) + " : " + str(m['VpcId']))
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

   # 3.1 Ensure that Object-level logging for write events is enabled for S3 bucket

    def control_3_1_ensure_logging_enabled_for_s3_write(self, regions):
        logger.info(" ---Inside networking_control_3 :: control_3_1_ensure_logging_enabled_for_s3_write()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.1"
        description = "Ensure that Object-level logging for write events is enabled for S3 bucket"
        scored = True

        for region in regions:
            try:
                paginator = self.session.client('cloudtrail', region_name=region).get_paginator('list_trails')
                response_iterator = paginator.paginate()
                pagedResult = []
                for page in response_iterator:
                    for n in page['Trails']:
                        pagedResult.append(n)

                for n in pagedResult:
                    event_selectors = self.session.client('cloudtrail', region_name=region).get_event_selectors(
                        TrailName=n['Name']
                    )
                    #print(event_selectors)
                    try:
                        if 'EventSelectors' in event_selectors:
                            for i in event_selectors["EventSelectors"]:

                                if i["DataResources"] == []:
                                    result = 'Not Compliant'
                                    failReason = 'Object-level logging for read/write events is not enabled for S3 bucket'
                                    offenders.append(event_selectors['TrailARN'])
                                else:
                                    continue
                        else:
                            result = 'Not Compliant'
                            failReason = 'Object-level logging for read/write events is not enabled for S3 bucket'
                            offenders.append(event_selectors['TrailARN'])
                    except:
                        KeyError
            except botocore.exceptions.ClientError as error:
                logger.error(f" Exception while listing trails: {error}")
                result = "Not Compliant"
                failReason = "Exception while listing trails "+str(error)
                offenders.append(region)
            except Exception as e:
                logger.error(str(e))
                result = "Not Compliant"
                failReason = "Exception while listing trails " + str(e)
                offenders.append(region)

            
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 3.11 Ensure that Object-level logging for read events is enabled for S3 bucket

    def control_3_1_1_ensure_logging_enabled_for_s3_read(self, regions):
        logger.info(" ---Inside networking_control_3 :: control_3_1_1_ensure_logging_enabled_for_s3_read()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "3.11"
        description = "Ensure that Object-level logging for read events is enabled for S3 bucket"
        scored = True
        for region in regions:

            try:

                paginator = self.session.client('cloudtrail', region_name=region).get_paginator('list_trails')
                response_iterator = paginator.paginate()
                pagedResult = []
                for page in response_iterator:
                    for n in page['Trails']:
                        pagedResult.append(n)

                for n in pagedResult:
                    event_selectors = self.session.client('cloudtrail', region_name=region).get_event_selectors(
                        TrailName=n['Name']
                    )
                    try:

                        if 'EventSelectors' in event_selectors:
                            for i in event_selectors["EventSelectors"]:
                                if i["DataResources"] == []:
                                    result = 'Not Compliant'
                                    failReason = 'Object-level logging for read/write events is not enabled for S3 bucket'
                                    offenders.append(event_selectors['TrailARN'])
                                else:
                                    continue
                        else:
                            result = 'Not Compliant'
                            failReason = 'Object-level logging for read/write events is not enabled for S3 bucket'
                            offenders.append(event_selectors['TrailARN'])
                    except:
                        KeyError
            except botocore.exceptions.ClientError as error:
                logger.error(f" Exception while listing trails: {error}")
                result = "Not Compliant"
                failReason = "Exception while listing trails "+str(error)
                offenders.append(region)

            except Exception as e:
                logger.error(str(e))
                result = "Not Compliant"
                failReason = "Exception while listing trails " + str(e)
                offenders.append(region)
                
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}
