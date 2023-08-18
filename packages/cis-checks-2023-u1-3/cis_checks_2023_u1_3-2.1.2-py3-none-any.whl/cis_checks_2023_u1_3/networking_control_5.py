"""
networking_control_5
"""
import logging.config

from cis_checks_2023_u1_3.utils import *

global logger
logging.basicConfig(level=logging.INFO)


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join(BASE_DIR, '..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs',
#                              'cis_automation_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})


# --- 5 Networking ---


class networking_control:
    # 5.01 Ensure no Network ACLs allow ingress from 0.0.0.0/0 to remote server administration ports
    def control_5_01_no_nacl_allow_ingress(self, regions):
        """
        :param self:
        :param regions:
        :return:
        """
        logger.info(" ---Inside Networking_control :: control_5_01_no_nacl_allow_ingress()--- ")
        self.refresh_session()

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.01"
        description = "Ensure no NACL allow ingress from 0.0.0.0/0 to Admin Ports (22, 3389)"
        scored = True

        for region in regions:
            client = self.session.client('ec2', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response = client.describe_network_acls()
                else:
                    response = client.describe_network_acls(
                        NextToken=marker
                    )

                for acl in response['NetworkAcls']:
                    for rule in acl['Entries']:
                        if not rule['Egress'] and rule['RuleAction'] == 'allow':
                            logger.debug(rule)
                            try:
                                if rule['PortRange']['From'] <= 22 <= rule['PortRange']['To']:
                                    if rule['CidrBlock'] == '0.0.0.0/0':
                                        result = "Not Compliant"
                                        failReason = "Found Network ACL (NACL) which allows unrestricted traffic on " \
                                                     "TCP port 22 and/or 3389"
                            except KeyError:
                                continue
                            try:
                                if rule['PortRange']['From'] <= 3389 <= rule['PortRange']['To']:
                                    if rule['CidrBlock'] == '0.0.0.0/0':
                                        result = "Not Compliant"
                                        failReason = "Found Network ACL (NACL) which allows unrestricted traffic on " \
                                                     "TCP port 22 and/or 3389"
                            except KeyError:
                                continue

                try:
                    marker = response['NextToken']
                    if marker is None or marker == '':
                        break
                except KeyError:
                    break

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 5.02 Ensure no security groups allow ingress from 0.0.0.0/0 to admin ports (Scored)
    def control_5_02_ensure_admin_ports_open_to_world_over_ipv4(self, regions):
        logger.info(" ---Inside networking_control_5 :: control_5_02_ensure_admin_ports_open_to_world_over_ipv4()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.02"
        description = "Ensure no security groups allow ingress from 0.0.0.0/0 to Admin Ports (22, 3389)"
        scored = True
        for n in regions:
            client = self.session.client('ec2', region_name=n)
            response = client.describe_security_groups()
            for m in response['SecurityGroups']:
                if "0.0.0.0/0" in str(m['IpPermissions']):
                    for o in m['IpPermissions']:
                        try:
                            if int(o['FromPort']) <= 22 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (0.0.0.0/0)"
                                offenders.append(str(m['GroupId']))
                        except:
                            if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (0.0.0.0/0)"
                                offenders.append(str(n) + " : " + str(m['GroupId']))

                        try:
                            if int(o['FromPort']) <= 3389 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (0.0.0.0/0)"
                                offenders.append(str(m['GroupId']))
                        except:
                            if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (0.0.0.0/0)"
                                offenders.append(str(n) + " : " + str(m['GroupId']))

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 5.03 Ensure no security groups allow ingress from ::/0 to admin ports (Scored)
    def control_5_03_ensure_ports_open_to_world_over_ipv6(self, regions):
        logger.info(" ---Inside networking_control_5 :: control_5_03_ensure_ports_open_to_world_over_ipv6()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.03"
        description = "Ensure no security groups allow ingress from ::/0 to Admin Ports (22, 3389)"
        scored = True
        for n in regions:
            client = self.session.client('ec2', region_name=n)
            response = client.describe_security_groups()
            for m in response['SecurityGroups']:
                if "::/0" in str(m['IpPermissions']):
                    for o in m['IpPermissions']:
                        try:
                            if int(o['FromPort']) <= 22 <= int(o['ToPort']) and '::/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (::/0)"
                                offenders.append(str(m['GroupId']))
                        except:
                            if str(o['IpProtocol']) == "-1" and '::/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (::/0)"
                                offenders.append(str(n) + " : " + str(m['GroupId']))

                        try:
                            if int(o['FromPort']) <= 3389 <= int(o['ToPort']) and '::/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (::/0)"
                                offenders.append(str(m['GroupId']))
                        except:
                            if str(o['IpProtocol']) == "-1" and '::/0' in str(o['IpRanges']):
                                result = "Not Compliant"
                                failReason = "Found Security Group with port 22 or 3389 open to the world (::/0)"
                                offenders.append(str(n) + " : " + str(m['GroupId']))

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 5.04 Ensure the default security group of every VPC restricts all traffic (Scored)
    def control_5_04_ensure_default_security_groups_restricts_traffic(self, regions):
        logger.info(
            " ---Inside networking_control_5 :: control_5_04_ensure_default_security_groups_restricts_traffic()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.04"
        description = "Ensure the default security group of every VPC restricts all traffic"
        scored = True
        for n in regions:
            client = self.session.client('ec2', region_name=n)
            response = client.describe_security_groups(
                Filters=[
                    {
                        'Name': 'group-name',
                        'Values': [
                            'default',
                        ]
                    },
                ]
            )
            for m in response['SecurityGroups']:
                if not (len(m['IpPermissions']) + len(m['IpPermissionsEgress'])) == 0:
                    result = "Not Compliant"
                    failReason = "Default security groups with ingress or egress rules discovered"
                    offenders.append(str(n) + " : " + str(m['GroupId']))
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 5.05 Ensure routing tables for VPC peering are "least access" (Not Scored)
    def control_5_05_ensure_route_tables_are_least_access(self, regions):
        logger.info(" ---Inside networking_control_5 :: control_5_05_ensure_route_tables_are_least_access()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Compliant"
        failReason = ""
        offenders = []
        control = "5.05"
        description = "Ensure routing tables for VPC peering are least access"
        scored = False
        for n in regions:
            client = self.session.client('ec2', region_name=n)
            response = client.describe_route_tables()
            for m in response['RouteTables']:
                for o in m['Routes']:
                    try:
                        if o['VpcPeeringConnectionId']:
                            if int(str(o['DestinationCidrBlock']).split("/", 1)[1]) < 24:
                                result = "Not Compliant"
                                failReason = "Large CIDR block routed to peer discovered, please investigate"
                                offenders.append(str(n) + " : " + str(m['RouteTableId']))
                    except:
                        pass
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    '''****************************************************************************'''

    # 4.2 Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389 (Scored)
    # def control_4_2_ensure_rdp_not_open_to_world(self, regions):
    #     logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_rdp_not_open_to_world()--- ")
    #     self.refresh_session()
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "4.2"
    #     description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389"
    #     scored = True
    #     for n in regions:
    #         client = self.session.client('ec2', region_name=n)
    #         response = client.describe_security_groups()
    #         for m in response['SecurityGroups']:
    #             if "0.0.0.0/0" in str(m['IpPermissions']):
    #                 for o in m['IpPermissions']:
    #                     try:
    #                         if int(o['FromPort']) <= 3389 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 3389 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(m['GroupId']))
    #                     except:
    #                         if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 3389 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(n) + " : " + str(m['GroupId']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # def control_4_2_ensure_20_not_open_to_world(self, regions):
    #     logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_20_not_open_to_world()--- ")
    #     self.refresh_session()
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "4.2"
    #     description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 20"
    #     scored = True
    #     for n in regions:
    #         client = self.session.client('ec2', region_name=n)
    #         response = client.describe_security_groups()
    #         for m in response['SecurityGroups']:
    #             if "0.0.0.0/0" in str(m['IpPermissions']):
    #                 for o in m['IpPermissions']:
    #                     try:
    #                         if int(o['FromPort']) <= 20 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 20 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(m['GroupId']))
    #                     except:
    #                         if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 20 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(n) + " : " + str(m['GroupId']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # def control_4_2_ensure_21_not_open_to_world(self, regions):
    #     logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_21_not_open_to_world()--- ")
    #     self.refresh_session()
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "4.2"
    #     description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 21"
    #     scored = True
    #     for n in regions:
    #         client = self.session.client('ec2', region_name=n)
    #         response = client.describe_security_groups()
    #         for m in response['SecurityGroups']:
    #             if "0.0.0.0/0" in str(m['IpPermissions']):
    #                 for o in m['IpPermissions']:
    #                     try:
    #                         if int(o['FromPort']) <= 21 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 21 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(m['GroupId']))
    #                     except:
    #                         if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 21 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(n) + " : " + str(m['GroupId']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # def control_4_2_ensure_3306_not_open_to_world(self, regions):
    #     logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_3306_not_open_to_world()--- ")
    #     self.refresh_session()
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "4.2"
    #     description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 3306"
    #     scored = True
    #     for n in regions:
    #         client = self.session.client('ec2', region_name=n)
    #         response = client.describe_security_groups()
    #         for m in response['SecurityGroups']:
    #             if "0.0.0.0/0" in str(m['IpPermissions']):
    #                 for o in m['IpPermissions']:
    #                     try:
    #                         if int(o['FromPort']) <= 3306 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 3306 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(m['GroupId']))
    #                     except:
    #                         if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 3306 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(n) + " : " + str(m['GroupId']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # def control_4_2_ensure_4333_not_open_to_world(self, regions):
    #     logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_4333_not_open_to_world()--- ")
    #     self.refresh_session()
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "4.2"
    #     description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 4333"
    #     scored = True
    #     for n in regions:
    #         client = self.session.client('ec2', region_name=n)
    #         response = client.describe_security_groups()
    #         for m in response['SecurityGroups']:
    #             if "0.0.0.0/0" in str(m['IpPermissions']):
    #                 for o in m['IpPermissions']:
    #                     try:
    #                         if int(o['FromPort']) <= 4333 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 4333 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(m['GroupId']))
    #                     except:
    #                         if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
    #                             result = "Not Compliant"
    #                             failReason = "Found Security Group with port 4333 open to the world (0.0.0.0/0)"
    #                             offenders.append(str(n) + " : " + str(m['GroupId']))
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 4.6 ensure security group dont have large range of ports open
    # def control_4_6_ensure_sg_dont_have_large_range_of_ports_open(self, regions: list) -> dict:
    #     logger.info(" ---Inside networking_control_4 :: control_4_6_ensure_sg_dont_have_large_range_of_ports_open")
    #     self.refresh_session()
    #
    #     """Summary
    #
    #     Returns:
    #         TYPE: dict
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "4.6"
    #     description = "Ensure security groups don't have large range of ports open"
    #     scored = True
    #
    #     for region in regions:
    #         client = self.session.client('ec2', region_name=region)
    #         marker = ''
    #         while True:
    #             if marker == '' or marker is None:
    #                 response = client.describe_security_groups()
    #             else:
    #                 response = client.describe_security_groups(
    #                     NextToken=marker
    #                 )
    #             for sg in response['SecurityGroups']:
    #                 for port_range in sg['IpPermissions']:
    #                     try:
    #                         count = port_range['ToPort'] - port_range['FromPort']
    #                         if count > 1:
    #                             result = "Not Compliant"
    #                             failReason = "Found Security group with range of port open"
    #                             offenders.append(sg['GroupName'])
    #                             continue
    #                     except KeyError:
    #                         continue
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
    #
    # # 4.7 Ensure use of https for cloudfront distributions
    # def control_4_7_use_https_for_cloudfront_distribution(self) -> dict:
    #     logger.info(" ---Inside networking_control_4 :: control_4_7_use_https_for_cloudfront_distribution")
    #     self.refresh_session()
    #
    #     """Summary
    #
    #     Returns:
    #         TYPE: dict
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = '4.7'
    #     description = "Use https for cloudfront distributions"
    #     scored = True
    #
    #     client = self.session.client('cloudfront')
    #     marker = ''
    #     while True:
    #         if marker == '' or marker == None:
    #             response = client.list_distributions()
    #         else:
    #             response = client.list_distributions(
    #                 Marker=marker
    #             )
    #         try:
    #             for item in response['DistributionList']['Items']:
    #                 protocol_policy = item['DefaultCacheBehavior']['ViewerProtocolPolicy']
    #                 if protocol_policy == 'allow-all':
    #                     result = "Not Compliant"
    #                     failReason = "Found cloudfront distribution which accepts http also"
    #                     offenders.append(item['Id'])
    #                     continue
    #
    #                 try:
    #                     for cache_behaviour in item['CacheBehaviors']['Items']:
    #                         protocol_policy = cache_behaviour['ViewerProtocolPolicy']
    #                         if protocol_policy == 'allow-all':
    #                             result = "Not Compliant"
    #                             failReason = "Found cloudfront distribution which accepts http also"
    #                             offenders.append(item['Id'])
    #                             continue
    #
    #                 except KeyError:
    #                     pass
    #         except KeyError:
    #             break
    #         try:
    #             marker = response['NextMarker']
    #             if marker == '':
    #                 break
    #         except KeyError:
    #             break
    #
    #     return {
    #         'Result': result,
    #         'failReason': failReason,
    #         'Offenders': offenders,
    #         'ScoredControl': scored,
    #         'Description': description,
    #         'ControlId': control
    #     }
