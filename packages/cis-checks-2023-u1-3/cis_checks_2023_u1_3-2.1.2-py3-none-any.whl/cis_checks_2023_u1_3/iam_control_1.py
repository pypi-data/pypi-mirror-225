"""iam_control_1.py"""
import sys

import pytz
from botocore.exceptions import ClientError
from dateutil.relativedelta import relativedelta

from cis_checks_2023_u1_3.utils import *

global logger
logging.basicConfig(level=logging.INFO)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join( BASE_DIR,'..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+
# datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})

# --- Control Parameters ---

# Control 1.18 - IAM manager and master role names <Not implemented yet, under review>
IAM_MASTER = "iam_master"
IAM_MANAGER = "iam_manager"
IAM_MASTER_POLICY = "iam_master_policy"
IAM_MANAGER_POLICY = "iam_manager_policy"

# Control 1.1 - Days allowed since use of root account.
CONTROL_1_1_DAYS = 0


# --- Global ---
# def __init__(self):
#     IAM_CLIENT = self.session.client('iam')
#     S3_CLIENT = self.session.client('iam')

# --- 1 Identity and Access Management ---

class iam_control:
    # 1.01 Maintain current contact details
    def control_1_01_maintain_contact_details(self):
        logger.info(" ---Inside iam_control_1 :: control_1_01_maintain_contact_details()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        offenders = []
        control = "1.01"
        description = "Ensure Current contact details is maintained, please verify manually"
        scored = True
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.02 Ensure security contact information is registered
    def control_1_02_security_contact_information_registered(self):
        logger.info(" ---Inside iam_control_1 :: control_1_02_security_contact_information_registered()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        offenders = []
        control = "1.02"
        description = "Ensure security contact details is registered, please verify manually"
        scored = True
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.03 Ensure security questions are registered in the AWS account (Not Scored/Manual)
    def control_1_03_security_questions_registered(self):
        logger.info(" ---Inside iam_control_1 :: control_1_03_security_questions_registered()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        offenders = []
        control = "1.03"
        description = "Ensure security questions are registered in the AWS account, please verify manually"
        scored = False
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.04 Ensure no root account access key exists (Scored)
    def control_1_04_root_key_exists(self, credreport):
        logger.info(" ---Inside iam_control_1 :: control_1_04_root_key_exists()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            credreport (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.04"
        description = "Ensure no root account access key exists"
        scored = True

        if type(credreport) == str:
            result = "Not Compliant"
            failReason = credreport
            offenders.append(credreport) 

        elif type(credreport) == list:
            if len(credreport) >= 1:
                try:
                    if (credreport[0]['access_key_1_active'] == "true") or (credreport[0]['access_key_2_active'] == "true"):
                        result = "Not Compliant"
                        failReason = "Root Account have active access keys"
                        offenders.append('root')
                except:
                    result = "Not Compliant"
                    failReason = "Credentials report is not generated properly"
                    offenders.append("Credentials report is not generated properly")

            else:
                result = "Not Compliant"
                failReason = "Credentials report is not generated properly"
                offenders.append("Credentials report is not generated properly")
                           
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.05 Ensure MFA is enabled for the "root" account (Scored)
    def control_1_05_root_mfa_enabled(self):
        logger.info(" ---Inside iam_control_1 :: control_1_05_root_mfa_enabled()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.05"
        description = "Ensure MFA is enabled for the root account"
        scored = True
        # global IAM_CLIENT
        response = self.session.client('iam').get_account_summary()
        if response['SummaryMap']['AccountMFAEnabled'] != 1:
            result = "Not Compliant"
            failReason = "Root account not using MFA"
            offenders.append('root')
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.06 Ensure hardware MFA is enabled for the "root" account (Scored)
    def control_1_06_root_hardware_mfa_enabled(self):
        logger.info(" ---Inside iam_control_1 :: control_1_06_root_hardware_mfa_enabled()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.06"
        description = "Ensure hardware MFA is enabled for the root account"
        scored = True
        # global IAM_CLIENT
        # First verify that root is using MFA (avoiding false positive)
        response = self.session.client('iam').get_account_summary()
        if response['SummaryMap']['AccountMFAEnabled'] == 1:
            paginator = self.session.client('iam').get_paginator('list_virtual_mfa_devices')
            response_iterator = paginator.paginate(
                AssignmentStatus='Any',
            )
            pagedResult = []
            for page in response_iterator:
                for n in page['VirtualMFADevices']:
                    pagedResult.append(n)
            if "mfa/root-account-mfa-device" in str(pagedResult):
                failReason = "Root account not using hardware MFA"
                result = "Not Compliant"
                offenders.append('root')
        else:
            result = "Not Compliant"
            failReason = "Root account not using Hardware MFA"
            offenders.append('root')
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.07 Avoid the use of the "root" account (Scored)
    def control_1_07_root_use(self, credreport):
        logger.info(" ---Inside iam_control_1 :: control_1_07_root_use()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            credreport (TYPE): Description
    
        Returns:
            TYPE: Description
        """

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.07"
        description = "Avoid the use of the root account"
        scored = True
        # if "Fail" in credreport:  # Report failure in control
        #     sys.exit(credreport)
        # Check if root is used in the last 24h
        now = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(time.time()))
        frm = "%Y-%m-%dT%H:%M:%S+00:00"

        if type(credreport) == str:
            result = "Not Compliant"
            failReason = credreport
            offenders.append(credreport) 

        elif type(credreport) == list:

            if len(credreport) >= 1:

                try:
                    # logger.info(credreport[0])
                    pwdDelta = (datetime.strptime(now, frm) - datetime.strptime(credreport[0]['password_last_used'], frm))
                    if (pwdDelta.days == CONTROL_1_1_DAYS) & (pwdDelta.seconds > 0):  # Used within last 24h
                        failReason = "Used within 24h"
                        result = "Not Compliant"
                        offenders.append('root')
                except:
                    if credreport[0]['password_last_used'] == "N/A" or "no_information":
                        pass
                    else:
                        logger.error(" Something went wrong")

                try:
                    key1Delta = (datetime.strptime(now, frm) - datetime.strptime(credreport[0]['access_key_1_last_used_date'],
                                                                                frm))
                    if (key1Delta.days == CONTROL_1_1_DAYS) & (key1Delta.seconds > 0):  # Used within last 24h
                        failReason = "Used within 24h"
                        result = "Not Compliant"
                        offenders.append('root')
                except:
                    if credreport[0]['access_key_1_last_used_date'] == "N/A" or "no_information":
                        pass
                    else:
                        logger.error("Something went wrong")
                try:
                    key2Delta = datetime.strptime(now, frm) - datetime.strptime(credreport[0]['access_key_2_last_used_date'],
                                                                                frm)
                    if (key2Delta.days == CONTROL_1_1_DAYS) & (key2Delta.seconds > 0):  # Used within last 24h
                        failReason = "Used within 24h"
                        result = "Not Compliant"
                        offenders.append('root')
                except:
                    if credreport[0]['access_key_2_last_used_date'] == "N/A" or "no_information":
                        pass
                    else:
                        logger.error("Something went wrong")
            else:
                result = "Not Compliant"
                failReason = "Credentials report is not generated properly"
                offenders.append("Credentials report is not generated properly") 

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.08 Ensure IAM password policy requires minimum length of 14 or greater (Scored)
    def control_1_08_password_policy_length(self, passwordpolicy):
        logger.info(" ---Inside iam_control_1 :: control_1_08_password_policy_length()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            passwordpolicy (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.08"
        description = "Ensure IAM password policy requires minimum length of 14 or greater"
        scored = True
        if passwordpolicy is False:
            result = "Not Compliant"
            failReason = "Account does not have a IAM password policy."
        else:
            if passwordpolicy['MinimumPasswordLength'] < 14:
                result = "Not Compliant"
                failReason = "Password policy does not require at least 14 characters"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.09 Ensure IAM password policy prevents password reuse (Scored)
    def control_1_09_password_policy_reuse(self, passwordpolicy):
        logger.info(" ---Inside iam_control_1 :: control_1_09_password_policy_reuse()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            passwordpolicy (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.09"
        description = "Ensure IAM password policy prevents password reuse"
        scored = True
        if passwordpolicy is False:
            result = "Not Compliant"
            failReason = "Account does not have a IAM password policy."
        else:
            try:
                if passwordpolicy['PasswordReusePrevention'] == 24:
                    pass
                else:
                    result = "Not Compliant"
                    failReason = "Password policy does not prevent reusing last 24 passwords"
            except:
                result = "Not Compliant"
                failReason = "Password policy does not prevent reusing last 24 passwords"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.10 Ensure multifactor authentication (MFA) is enabled for all IAM users that have a console password (Scored)
    def control_1_10_mfa_on_password_enabled_iam(self, credreport):
        logger.info(" ---Inside iam_control_1 :: control_1_10_mfa_on_password_enabled_iam()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            credreport (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.10"
        description = "Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console " \
                      "password"
        scored = True

        if type(credreport) == str:
            result = "Not Compliant"
            failReason = credreport
            offenders.append(credreport)

        elif type(credreport) == list:
            if len(credreport) >= 1:
                for i in range(len(credreport)):
                    # Verify if the user have a password configured
                    if credreport[i]['password_enabled'] == "true":
                        # Verify if password users have MFA assigned
                        if credreport[i]['mfa_active'] == "false":
                            result = "Not Compliant"
                            failReason = "No MFA on users with password. "
                            offenders.append(str(credreport[i]['arn']))
            else:
                result = "Not Compliant"
                failReason = "Credentials report is not generated properly"
                offenders.append("Credentials report is not generated properly")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.11 Do not set up access keys during initial user setup for all IAM users that have a console password
    def control_1_11_no_accesskey_on_initial_setup(self, credreport):
        logger.info(" ---Inside iam_control_1 :: control_1_11_no_accesskey_on_initial_setup()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            credreport (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.11"
        description = "Ensure no access keys have been created during initial user setup for all IAM users that have " \
                      "a console password"
        scored = True
        if type(credreport) == str:
            result = "Not Compliant"
            failReason = credreport
            offenders.append(credreport)

        elif type(credreport) == list:
            if len(credreport) >= 1:
                for i in range(len(credreport)):
                    if credreport[i]['user_creation_time'] == credreport[i]['access_key_1_last_rotated']:
                        result = "Not Compliant"
                        failReason = "Access keys have been created during initial user setup for IAM users that have a " \
                                     "console password"
                        offenders.append(str(credreport[i]['arn']))
            else:
                result = "Not Compliant"
                failReason = "Credentials report is not generated properly"
                offenders.append("Credentials report is not generated properly")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.12 Ensure credentials unused for 90 days or greater are disabled (Scored)
    def control_1_12_unused_credentials(self, credreport):
        logger.info(" ---Inside iam_control_1 :: control_1_12_unused_credentials()--- ")
        self.refresh_session()
        """Summary
    
        Args:
            credreport (TYPE): Description
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.12"
        description = "Ensure credentials unused for 45 days or greater are disabled"
        scored = True
        # Get current time
        now = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(time.time()))
        frm = "%Y-%m-%dT%H:%M:%S+00:00"
        if type(credreport) == str:
            result = "Not Compliant"
            failReason = credreport
            offenders.append(credreport)

        elif type(credreport) == list:
            if len(credreport) >= 1:
                # Look for unused credentails
                for i in range(len(credreport)):
                    if credreport[i]['password_enabled'] == "true":
                        try:
                            delta = datetime.strptime(now, frm) - datetime.strptime(credreport[i]['password_last_used'], frm)
                            # Verify password have been used in the last 90 days
                            if delta.days > 45:
                                result = "Not Compliant"
                                failReason = "Credentials unused > 45 days detected. "
                                offenders.append(str(credreport[i]['arn']) + ":password")
                        except:
                            pass  # Never used
                    if credreport[i]['access_key_1_active'] == "true":
                        try:
                            delta = datetime.strptime(now, frm) - datetime.strptime(
                                credreport[i]['access_key_1_last_used_date'],
                                frm)
                            # Verify password have been used in the last 90 days
                            if delta.days > 45:
                                result = "Not Compliant"
                                failReason = "Credentials unused > 45 days detected. "
                                offenders.append(str(credreport[i]['arn']) + ":key1")
                        except:
                            pass
                    if credreport[i]['access_key_2_active'] == "true":
                        try:
                            delta = datetime.strptime(now, frm) - datetime.strptime(
                                credreport[i]['access_key_2_last_used_date'],
                                frm)
                            # Verify password have been used in the last 90 days
                            if delta.days > 45:
                                result = "Not Compliant"
                                failReason = "Credentials unused > 45 days detected. "
                                offenders.append(str(credreport[i]['arn']) + ":key2")
                        except:
                            # Never used
                            pass
            else:
                result = "Not Compliant"
                failReason = "Credentials report is not generated properly"
                offenders.append("Credentials report is not generated properly")

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.13 Ensure there is only one active access key available for any single IAM user
    def control_1_13_one_active_key(self, credsreport):
        """
        :param self:
        :param credsreport:
        :return:
        """
        logger.info(" ---Inside iam_control_1 :: control_1_13_one_active_key()--- ")
        self.refresh_session()

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.13"
        description = "Ensure there is only one active access key for single IAM user"
        scored = True

        if type(credsreport) == str:
            result = "Not Compliant"
            failReason = credsreport
            offenders.append(credsreport)

        elif type(credsreport) == list:
            if len(credsreport) >= 1:
                for user in credsreport:
                    k1 = True if user['access_key_1_active'] == 'true' else False
                    k2 = True if user['access_key_2_active'] == 'true' else False
                    r = not (k1 and k2)

                    if not r:
                        result = 'Not Compliant'
                        failReason = "found more that 1 active access key"
                        offenders.append(user['user'])
            else:
                result = "Not Compliant"
                failReason = "Credentials report is not generated properly"
                offenders.append("Credentials report is not generated properly")

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

    # 1.14 Ensure access keys are rotated every 90 days or less

    def control_1_14_ensure_access_keys_are_rotated_90_days(self):
        logger.info(" ---Inside iam_control_1 :: control_1_14_ensure_access_keys_are_rotated_90_days()---")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.14"
        description = "Ensure that all your IAM user access keys are rotated every 90 days or less"
        scored = True

        datetime_90_days_ago = datetime.now() - relativedelta(months=3)
        timezone = pytz.timezone("UTC")
        datetime_90_days_ago = timezone.localize(datetime_90_days_ago)

        client = self.session.client('iam')
        marker = ''
        while True:
            if marker == '':
                response = client.list_users()
            else:
                response = client.list_users(
                    Marker=marker
                )
            for user in response['Users']:
                access_keys = client.list_access_keys(
                    UserName=user['UserName']
                )
                for key in access_keys['AccessKeyMetadata']:
                    if key['CreateDate'] < datetime_90_days_ago:
                        result = "Not Compliant"
                        offenders.append(key['UserName'])
                        failReason = 'IAM access Keys are not rotated since 3 month or more'

            try:
                marker = response['Marker']
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

    # 1.15 Ensure IAM policies are attached only to groups or roles (Scored)
    def control_1_15_no_policies_on_iam_users(self):
        logger.info(" ---Inside iam_control_1 :: control_1_15_no_policies_on_iam_users()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.15"
        description = "Ensure IAM policies are attached only to groups or roles"
        scored = True
        # global IAM_CLIENT
        paginator = self.session.client('iam').get_paginator('list_users')
        response_iterator = paginator.paginate()
        pagedResult = []
        for page in response_iterator:
            for n in page['Users']:
                pagedResult.append(n)
        offenders = []
        for n in pagedResult:
            policies = self.session.client('iam').list_user_policies(
                UserName=n['UserName'],
                MaxItems=1
            )
            if policies['PolicyNames']:
                result = "Not Compliant"
                failReason = "IAM user have inline policy attached"
                offenders.append(str(n['Arn']))
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.16 Ensure IAM policies that allow full "*:*" administrative privileges are not attached (Scored)
    def control_1_16_no_policies_with_full_administrative_privileges(self):
        logger.info(
            " ---Inside iam_control_1 :: control_1_16_no_policies_with_full_administrative_privileges()--- ")
        self.refresh_session()
        """Summary

        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.16"
        description = "Ensure IAM policies that allow full *:* administrative privileges are not attached"
        scored = True
        # global IAM_CLIENT

        try:
            paginator = self.session.client('iam').get_paginator('list_policies')
            response_iterator = paginator.paginate(OnlyAttached=True)
            pagedResult = []
            for page in response_iterator:
                for n in page['Policies']:
                    pagedResult.append(n)
            offenders = []
            for n in pagedResult:
                policy = self.session.client('iam').get_policy_version(
                    PolicyArn=n["Arn"],
                    VersionId=n["DefaultVersionId"]
                )

                statements = policy['PolicyVersion']['Document']['Statement']
                try:

                    if type(statements) == list:
                        for statement in statements:
                            if type(statement) == dict:
                                if statement["Effect"] == "Allow":
                                    if statement["Action"] == "*" and (
                                            statement["Resource"] == "*" or statement["Resource"] == ["*"]):
                                        result = "Not Compliant"
                                        failReason = "IAM policies that allow full *:* administrative privileges are attached"
                                        offenders.append(n["Arn"])
                                else:
                                    continue
                            else:
                                raise KeyError

                    elif type(statements) == dict:
                        if statements["Effect"] == "Allow":
                            if statements["Action"] == "*" and (
                                    statements["Resource"] == "*" or statements["Resource"] == ["*"]):
                                result = "Not Compliant"
                                failReason = "IAM policies that allow full *:* administrative privileges are attached"
                                offenders.append(n["Arn"])
                        else:
                            continue
                    else:
                        raise KeyError

                except KeyError:
                    pass

        except botocore.exceptions.ClientError as error:
            logger.error(f" Exception while listing policies: {error}")
            result = "Not Compliant"
            failReason = "Client Error while listing policies " + str(error)

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.17 Ensure a support role has been created to manage incidents with AWS Support (Scored)
    def control_1_17_AWS_support_role_created(self):
        logger.info(" ---Inside iam_control_1 :: control_1_17_AWS_support_role_created()--- ")
        self.refresh_session()
        """Summary
    
        Args:
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.17"
        description = "Ensure a support role has been created to manage incidents with AWS Support"
        scored = True

        paginator = self.session.client('iam').get_paginator('list_policies')
        response_iterator = paginator.paginate()
        offenders = []
        for page in response_iterator:
            for n in page['Policies']:
                if n['PolicyName'] == 'AWSSupportAccess':
                    role = self.session.client('iam').list_entities_for_policy(
                        PolicyArn=n["Arn"],
                        EntityFilter='Role')
                    if not role['PolicyRoles']:
                        offenders.append(n["Arn"])
                        result = "Not Compliant"
                        failReason = "No support role has been created to manage incidents with AWS Support"

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.18 Ensure IAM instance roles are used for AWS resource access from instances
    def control_1_18_iam_instance_role_for_access_from_instances(self):
        logger.info(" ---Inside iam_control_1 :: control_1_18_iam_instance_role_for_access_from_instances()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        failReason = ""
        offenders = []
        control = "1.18"
        description = "Ensure IAM instance roles are used for AWS resource access from instances, please verify " \
                      "manually"
        scored = True
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 1.19 Ensure that all the expired SSL/TLS certificates stored in AWS IAM are removed
    def control_1_19_expired_ssl_tls_certificates_removed(self, regions: list) -> dict:
        logger.info(" ---Inside iam_control_1 :: control_1_19_expired_ssl_tls_certificates_removed")
        self.refresh_session()

        """Summary
        
        Returns:
            TYPE: dict
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.19"
        description = "Ensure that all the expired SSL/TLS certificates stored in AWS IAM are removed"
        scored = True

        for region in regions:
            client = self.session.client('acm', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response = client.list_certificates(
                        CertificateStatuses=['EXPIRED']
                    )
                else:
                    response = client.list_certificates(
                        CertificateStatuses=['EXPIRED'],
                        NextToken=marker
                    )

                for certificate in response['CertificateSummaryList']:
                    try:
                        if certificate['InUse']:
                            result = "Not Compliant"
                            failReason = "Found expired SSL/TLS certificates in use"
                            offenders.append(certificate['CertificateArn'])
                    except KeyError:
                        pass

                try:
                    marker = response['NextToken']
                    if marker == '':
                        break
                except:
                    break

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

    # 1.2 Ensure that IAM Access analyzer is enabled for all regions
    def control_1_2_iam_access_analyzer_enabled(self, regions: list) -> dict:
        logger.info(" ---Inside iam_control_1 :: control_1_2_iam_access_analyzer_enabled")
        self.refresh_session()

        """Summary
        
        Returns:
            TYPE: dict
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "1.2"
        description = "Ensure that IAM Access analyzer is enabled for all regions"
        scored = True

        for region in regions:
            client = self.session.client('accessanalyzer', region_name=region)
            try:

                response = client.list_analyzers()
                # print(response)
                try:
                    if response['analyzers'] == []:
                        result = "Not Compliant"
                        failReason = "IAM Access analyzer is not enabled for all regions"
                        offenders.append(region)
                    else:
                        continue
                except KeyError:
                    pass
            except botocore.exceptions.ClientError as error:
                logger.error(f" Exception while listing analyzers: {error}")
                result = "Not Compliant"
                failReason = "Exception while listing analyzers " + str(error)
                offenders.append(region)

        return {
            'Result': result,
            'failReason': failReason,
            'Offenders': offenders,
            'ScoredControl': scored,
            'Description': description,
            'ControlId': control
        }

        # 1.21 Ensure IAM users are managed centrally via identity federation or AWS Organizations for multi-account

    # environments
    def control_1_21_iam_user_managed_centrally(self):
        logger.info(" ---Inside iam_control_1 :: control_1_21_iam_user_managed_centrally()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Manual"
        offenders = []
        control = "1.21"
        description = "Ensure IAM users are managed centrally via identity federation or AWS Organizations for " \
                      "multi-account environments, please verify manually"
        scored = True
        failReason = "Control not implemented using API, please verify manually"
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    '''****************************************************************************'''

    # # 1.5 Ensure IAM password policy requires at least one uppercase letter (Scored)
    # def control_1_5_password_policy_uppercase(self, passwordpolicy):
    #     logger.info(" ---Inside iam_control_1 :: control_1_5_password_policy_uppercase()--- ")
    #     """Summary
    #
    #     Args:
    #         passwordpolicy (TYPE): Description
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.5"
    #     description = "Ensure IAM password policy requires at least one uppercase letter"
    #     scored = True
    #     if passwordpolicy is False:
    #         result = "Not Compliant"
    #         failReason = "Account does not have a IAM password policy."
    #     else:
    #         if passwordpolicy['RequireUppercaseCharacters'] is False:
    #             result = "Not Compliant"
    #             failReason = "Password policy does not require at least one uppercase letter"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.6 Ensure IAM password policy requires at least one lowercase letter (Scored)
    # def control_1_6_password_policy_lowercase(self, passwordpolicy):
    #     logger.info(" ---Inside iam_control_1 :: control_1_6_password_policy_lowercase()--- ")
    #     """Summary
    #
    #     Args:
    #         passwordpolicy (TYPE): Description
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.6"
    #     description = "Ensure IAM password policy requires at least one lowercase letter"
    #     scored = True
    #     if passwordpolicy is False:
    #         result = "Not Compliant"
    #         failReason = "Account does not have a IAM password policy."
    #     else:
    #         if passwordpolicy['RequireLowercaseCharacters'] is False:
    #             result = "Not Compliant"
    #             failReason = "Password policy does not require at least one uppercase letter"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.7 Ensure IAM password policy requires at least one symbol (Scored)
    # def control_1_7_password_policy_symbol(self, passwordpolicy):
    #     logger.info(" ---Inside iam_control_1 :: control_1_7_password_policy_symbol()--- ")
    #     """Summary
    #
    #     Args:
    #         passwordpolicy (TYPE): Description
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.7"
    #     description = "Ensure IAM password policy requires at least one symbol"
    #     scored = True
    #     if passwordpolicy is False:
    #         result = "Not Compliant"
    #         failReason = "Account does not have a IAM password policy."
    #     else:
    #         if passwordpolicy['RequireSymbols'] is False:
    #             result = "Not Compliant"
    #             failReason = "Password policy does not require at least one symbol"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.8 Ensure IAM password policy requires at least one number (Scored)
    # def control_1_8_password_policy_number(self, passwordpolicy):
    #     logger.info(" ---Inside iam_control_1 :: control_1_8_password_policy_number()--- ")
    #     """Summary
    #
    #     Args:
    #         passwordpolicy (TYPE): Description
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.8"
    #     description = "Ensure IAM password policy requires at least one number"
    #     scored = True
    #     if passwordpolicy is False:
    #         result = "Not Compliant"
    #         failReason = "Account does not have a IAM password policy."
    #     else:
    #         if passwordpolicy['RequireNumbers'] is False:
    #             result = "Not Compliant"
    #             failReason = "Password policy does not require at least one number"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.11 Ensure IAM password policy expires passwords within 90 days or less (Scored)
    # def control_1_11_password_policy_expire(self, passwordpolicy):
    #     logger.info(" ---Inside iam_control_1 :: control_1_11_password_policy_expire()--- ")
    #     """Summary
    #
    #     Args:
    #         passwordpolicy (TYPE): Description
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.11"
    #     description = "Ensure IAM password policy expires passwords within 90 days or less"
    #     scored = True
    #     if passwordpolicy is False:
    #         result = "Not Compliant"
    #         failReason = "Account does not have a IAM password policy."
    #     else:
    #         if passwordpolicy['ExpirePasswords'] is True:
    #             if 0 < passwordpolicy['MaxPasswordAge'] > 90:
    #                 result = "Not Compliant"
    #                 failReason = "Password policy does not expire passwords after 90 days or less"
    #         else:
    #             result = "Not Compliant"
    #             failReason = "Password policy does not expire passwords after 90 days or less"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.16 Ensure IAM policies are attached only to groups or roles (Scored)
    # def control_1_16_no_policies_on_iam_users(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_16_no_policies_on_iam_users()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.16"
    #     description = "Ensure IAM policies are attached only to groups or roles"
    #     scored = True
    #     # global IAM_CLIENT
    #     paginator = self.session.client('iam').get_paginator('list_users')
    #     response_iterator = paginator.paginate()
    #     pagedResult = []
    #     for page in response_iterator:
    #         for n in page['Users']:
    #             pagedResult.append(n)
    #     for n in pagedResult:
    #         policies = self.session.client('iam').list_user_policies(
    #             UserName=n['UserName'],
    #             MaxItems=1
    #         )
    #         if policies['PolicyNames']:
    #             result = "Not Compliant"
    #             failReason = "IAM user have inline policy attached"
    #             offenders.append(str(n['Arn']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.17 Enable detailed billing (Scored)
    # def control_1_17_detailed_billing_enabled(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_17_detailed_billing_enabled()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Manual"
    #     offenders = []
    #     control = "1.17"
    #     description = "Enable detailed billing, please verify manually"
    #     scored = True
    #     failReason = "Control not implemented using API, please verify manually"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.18 Ensure IAM Master and IAM Manager roles are active (Scored)
    # def control_1_18_ensure_iam_master_and_manager_roles(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_18_ensure_iam_master_and_manager_roles()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = "No IAM Master or IAM Manager role created"
    #     offenders = []
    #     control = "1.18"
    #     description = "Ensure IAM Master and IAM Manager roles are active. Control under review/investigation"
    #     scored = True
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.19 Maintain current contact details (Scored)
    # def control_1_19_maintain_current_contact_details(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_19_maintain_current_contact_details()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Manual"
    #     offenders = []
    #     control = "1.19"
    #     description = "Maintain current contact details, please verify manually"
    #     scored = True
    #     failReason = "Control not implemented using API, please verify manually"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.21 Ensure IAM instance roles are used for AWS resource access from instances (Scored)
    # def control_1_21_ensure_iam_instance_roles_used(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_21_ensure_iam_instance_roles_used()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #
    #     control = "1.21"
    #     description = "Ensure IAM instance roles are used for AWS resource access from instances, " \
    #                   "application code is not audited"
    #     scored = True
    #     failReason = "Instance not assigned IAM role for EC2"
    #     client = self.session.client('ec2', region_name='us-east-1')
    #     response = client.describe_instances()
    #     offenders = []
    #     for n, _ in enumerate(response['Reservations']):
    #         try:
    #             if response['Reservations'][n]['Instances'][0]['IamInstanceProfile']:
    #                 pass
    #         except:
    #             result = "Not Compliant"
    #             offenders.append(str(response['Reservations'][n]['Instances'][0]['InstanceId']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.22 Ensure a support role has been created to manage incidents with AWS Support (Scored)
    # def control_1_22_ensure_incident_management_roles(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_22_ensure_incident_management_roles()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     control = "1.22"
    #     description = "Ensure a support role has been created to manage incidents with AWS Support"
    #     scored = True
    #     offenders = []
    #     # global IAM_CLIENT
    #     try:
    #         response = self.session.client('iam').list_entities_for_policy(
    #             PolicyArn='arn:aws:iam::aws:policy/AWSSupportAccess'
    #         )
    #         if (len(response['PolicyGroups']) + len(response['PolicyUsers']) + len(response['PolicyRoles'])) == 0:
    #             result = "Not Compliant"
    #             failReason = "No user, group or role assigned AWSSupportAccess"
    #     except:
    #         result = "Not Compliant"
    #         failReason = "AWSSupportAccess policy not created"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.23 Do not set up access keys during initial user setup for all IAM users that have a console password (Not
    # # Scored)
    # def control_1_23_no_active_initial_access_keys_with_iam_user(self, credreport):
    #     logger.info(" ---Inside iam_control_1 :: control_1_23_no_active_initial_access_keys_with_iam_user()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     control = "1.23"
    #     description = "Do not setup access keys during initial user setup for all IAM users that have a console " \
    #                   "password"
    #     scored = False
    #     offenders = []
    #     # global IAM_CLIENT
    #     for n, _ in enumerate(credreport):
    #         if (credreport[n]['access_key_1_active'] or credreport[n]['access_key_2_active'] == 'true') and n > 0:
    #             try:
    #                 response = self.session.client('iam').list_access_keys(UserName=str(credreport[n]['user']))
    #                 for m in response['AccessKeyMetadata']:
    #                     if re.sub(r"\s", "T", str(m['CreateDate'])) == credreport[n]['user_creation_time']:
    #                         result = "Not Compliant"
    #                         failReason = "Users with keys created at user creation time found"
    #                         offenders.append(str(credreport[n]['arn']) + ":" + str(m['AccessKeyId']))
    #             except botocore.exceptions.ClientError as error:
    #                 if error.response['Error']['Code'] == 'NoSuchEntityException':
    #                     logger.error(f" AccessKey credentails not found for user: {str(credreport[n]['user'])}")
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.24  Ensure IAM policies that allow full "*:*" administrative privileges are not created (Scored)
    # def control_1_24_no_overly_permissive_policies(self):
    #     logger.info(" ---Inside iam_control_1 :: control_1_24_no_overly_permissive_policies()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.24"
    #     description = "Ensure IAM policies that allow full administrative privileges are not created"
    #     scored = True
    #     offenders = []
    #     # global IAM_CLIENT
    #     paginator = self.session.client('iam').get_paginator('list_policies')
    #     response_iterator = paginator.paginate(
    #         Scope='Local',
    #         OnlyAttached=False,
    #     )
    #     pagedResult = []
    #     for page in response_iterator:
    #         for n in page['Policies']:
    #             pagedResult.append(n)
    #     for m in pagedResult:
    #         policy = self.session.client('iam').get_policy_version(
    #             PolicyArn=m['Arn'],
    #             VersionId=m['DefaultVersionId']
    #         )
    #
    #         statements = []
    #         # a policy may contain a single statement, a single statement in an array, or multiple statements in an
    #         # array
    #         if isinstance(policy['PolicyVersion']['Document']['Statement'], list):
    #             for statement in policy['PolicyVersion']['Document']['Statement']:
    #                 statements.append(statement)
    #         else:
    #             statements.append(policy['PolicyVersion']['Document']['Statement'])
    #
    #         for n in statements:
    #             # a policy statement has to contain either an Action or a NotAction
    #             if 'Action' in n.keys() and n['Effect'] == 'Allow':
    #                 if ("'*'" in str(n['Action']) or str(n['Action']) == "*") and (
    #                         "'*'" in str(n['Resource']) or str(n['Resource']) == "*"):
    #                     result = "Not Compliant"
    #                     failReason = "Found full administrative policy"
    #                     offenders.append(str(m['Arn']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 1.25 Ensure MFA is enable to delete cloudtrail buckets
    # def control_1_25_require_mfa_to_delete_cloudtrail_buckets(self, regions: list) -> dict:
    #     # returns the list trails
    #     def list_trails(region) -> dict:
    #         # trails_lst = []
    #         trails_lst_with_bucket = {}
    #         client = self.session.client('cloudtrail', region_name=region)
    #
    #         response = client.describe_trails(
    #             trailNameList=[],
    #             includeShadowTrails=False
    #         )
    #         for trail in response['trailList']:
    #             trails_lst_with_bucket[trail['Name']] = trail['S3BucketName']
    #
    #         return trails_lst_with_bucket
    #
    #     logger.info(" ---Inside iam_control_1 :: control_1_25_require_mfa_to_delete_cloudtrail_buckets")
    #
    #     """Summary
    #
    #     Returns:
    #         TYPE: dict
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.25"
    #     description = "Require MFA to delete cloudtrail buckets"
    #     scored = True
    #     for n in regions:
    #         trails = list_trails(n)
    #         client = self.session.client('s3')
    #         for trail, bucket in trails.items():
    #             try:
    #                 response = client.get_bucket_versioning(
    #                     Bucket=bucket
    #                 )
    #                 try:
    #                     if response['MFADelete'] == 'Disabled':
    #                         result = "Not Compliant"
    #                         failReason = "Found cloudtrail s3 bucket with MFA delete disabled"
    #                         offenders.append(trail)
    #                 except KeyError:
    #                     result = "Not Compliant"
    #                     failReason = "Found cloudtrail s3 bucket with MFA delete disabled"
    #                     offenders.append(trail)
    #             except botocore.exceptions.ClientError as e:
    #                 if e.response['Error']['Code'] == 'AccessDenied':
    #                     result = "Not Compliant"
    #                     failReason = "S3 access denied"
    #                     offenders.append(trail)
    #                 elif e.response['Error']['Code'] == 'NoSuchBucket':
    #                     result = "Not Compliant"
    #                     failReason = "Cloudtrail bucket {} not found".format(bucket)
    #                     offenders.append(trail)
    #
    #     return {
    #         'Result': result,
    #         'failReason': failReason,
    #         'Offenders': offenders,
    #         'ScoredControl': scored,
    #         'Description': description,
    #         'ControlId': control
    #     }
    #
    # # 1.26 Ensure expired ssl and tls certificate are not in use
    # def control_1_26_dont_use_expired_ssl_tls_certificate(self, regions: list) -> dict:
    #     logger.info(" ---Inside iam_control_1 :: control_1_26_dont_use_expired_ssl_tls_certificate")
    #
    #     """Summary
    #
    #     Returns:
    #         TYPE: dict
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "1.26"
    #     description = "Don't use expired ssl/tls certificate"
    #     scored = True
    #
    #     for region in regions:
    #         client = self.session.client('acm', region_name=region)
    #         marker = ''
    #         while True:
    #             if marker == '' or marker is None:
    #                 response = client.list_certificates(
    #                     CertificateStatuses=['EXPIRED']
    #                 )
    #             else:
    #                 response = client.list_certificates(
    #                     CertificateStatuses=['EXPIRED'],
    #                     NextToken=marker
    #                 )
    #
    #             for certificate in response['CertificateSummaryList']:
    #                 try:
    #                     if certificate['InUse']:
    #                         result = "Not Compliant"
    #                         failReason = "Found expired SSL/TLS certificate which is in use"
    #                         offenders.append(certificate['CertificateArn'])
    #                 except KeyError:
    #                     pass
    #
    #             try:
    #                 marker = response['NextToken']
    #                 if marker == '':
    #                     break
    #             except:
    #                 break
    #
    #     return {
    #         'Result': result,
    #         'failReason': failReason,
    #         'Offenders': offenders,
    #         'ScoredControl': scored,
    #         'Description': description,
    #         'ControlId': control
    #     }
