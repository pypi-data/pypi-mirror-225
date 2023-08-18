import datetime
import logging

import boto3
import pytz
from boto3 import session

from cis_checks_2023_u1.logging_control_3 import logging_control
from cis_checks_2023_u1.monitoring_control_4 import monitoring_control
from cis_checks_2023_u1.networking_control_5 import networking_control
from cis_checks_2023_u1.storage_control_2 import storage_control
from cis_checks_2023_u1.utils import utils
from cis_checks_2023_u1._security_control_5 import *
from cis_checks_2023_u1.iam_control_1 import iam_control

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

__author__ = 'Dheeraj Banodha'
__version__ = '2.1.2'


class aws_client(iam_control, utils, storage_control, logging_control, monitoring_control, networking_control):
    def __init__(self, **kwargs):
        """
        @param str aws_access_key_id: AWS Access Key ID
        @param str aws_secret_access_key: AWS Secret Access Key
        """

        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            if 'iam_role_to_assume' in kwargs.keys():
                self.iam_role_to_assume = kwargs['iam_role_to_assume']
                self.sts_client = boto3.client(
                    'sts',
                    aws_access_key_id=kwargs['aws_access_key_id'],
                    aws_secret_access_key=kwargs['aws_secret_access_key'],
                )
                self.creds = self.sts_client.assume_role(
                    RoleArn=self.iam_role_to_assume,
                    RoleSessionName='RecommenderSession',
                    DurationSeconds=3600
                )
                self.session = session.Session(
                    aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                    aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                    aws_session_token=self.creds['Credentials']['SessionToken']
                )
            else:
                self.session = session.Session(
                    aws_access_key_id=kwargs['aws_access_key_id'],
                    aws_secret_access_key=kwargs['aws_secret_access_key'],
                )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])
        elif 'iam_role_to_assume' in kwargs.keys():
            self.iam_role_to_assume = kwargs['iam_role_to_assume']
            self.sts_client = boto3.client('sts')
            self.creds = self.sts_client.assume_role(
                RoleArn=kwargs['iam_role_to_assume'],
                RoleSessionName='RecommenderSession',
                DurationSeconds=3600
            )
            self.session = session.Session(
                aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                aws_session_token=self.creds['Credentials']['SessionToken']
            )

    # refresh session
    def refresh_session(self):
        try:
            self.sts_client
        except AttributeError:
            logger.info('No need to refresh the session!')
            return
        remaining_duration_seconds = (
                self.creds['Credentials']['Expiration'] - datetime.datetime.now(pytz.utc)).total_seconds()
        if remaining_duration_seconds < 900:
            self.creds = self.sts_client.assume_role(
                RoleArn=self.iam_role_to_assume,
                RoleSessionName='RecommenderSession',
                DurationSeconds=3600
            )
            self.session = session.Session(
                aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                aws_session_token=self.creds['Credentials']['SessionToken']
            )

    # consolidate compliance.py details
    def get_compliance(self) -> list:
        """
        :return list: consolidated list  of compliance.py checks
        """
        logger.info(" ---Inside get_compliance()")

        regions = self.get_regions()
        if type(regions) is dict:
            return [regions]
        CloudTrail = self.get_cloudtrails(regions)
        creds_report = self.get_cred_report()
        password_policy = self.get_account_password_policy()
        s3_buckets = self.list_s3_buckets()
        rds_instances = self.list_rds_instances(regions)

        compliance = [
            # iam_control_1

            self.control_1_01_maintain_contact_details(),
            self.control_1_02_security_contact_information_registered(),
            self.control_1_03_security_questions_registered(),
            self.control_1_04_root_key_exists(creds_report),
            self.control_1_05_root_mfa_enabled(),
            self.control_1_06_root_hardware_mfa_enabled(),
            self.control_1_07_root_use(creds_report),
            self.control_1_08_password_policy_length(password_policy),
            self.control_1_09_password_policy_reuse(password_policy),
            self.control_1_10_mfa_on_password_enabled_iam(creds_report),
            self.control_1_11_no_accesskey_on_initial_setup(creds_report),
            self.control_1_12_unused_credentials(creds_report),
            self.control_1_13_one_active_key(creds_report),
            self.control_1_14_ensure_access_keys_are_rotated_90_days(),
            self.control_1_15_no_policies_on_iam_users(),
            self.control_1_16_no_policies_with_full_administrative_privileges(),
            self.control_1_17_AWS_support_role_created(),
            self.control_1_18_iam_instance_role_for_access_from_instances(),
            self.control_1_19_expired_ssl_tls_certificates_removed(regions),
            self.control_1_2_iam_access_analyzer_enabled(regions),
            self.control_1_21_iam_user_managed_centrally(),

            # storage_control_2

            self.control_2_1_1_s3_default_encryption_at_rest(s3_buckets),
            self.control_2_1_2_s3_deny_http_requests(s3_buckets),
            self.control_2_1_3_s3_mfa_delete_enabled(s3_buckets),
            self.control_2_1_4_ensure_all_data_discovered_classified_secured(),
            self.control_2_1_5_s3_blocks_public_access(s3_buckets),
            self.control_2_2_1_ebs_volumes_encrypted(regions),
            self.control_2_3_1_rds_encryption_enabled(rds_instances),
            self.control_2_3_2_rds_auto_minor_version_upgrade_enabled(rds_instances),
            self.control_2_3_3_rds_publicly_accessible(rds_instances),
            self.control_2_4_1_encryption_enabled_for_efs(),

            # logging control 3
            self.control_3_01_ensure_cloud_trail_all_regions(CloudTrail),
            self.control_3_02_ensure_cloudtrail_validation(CloudTrail),
            self.control_3_03_ensure_cloudtrail_bucket_not_public(CloudTrail),
            self.control_3_04_ensure_cloudtrail_cloudwatch_logs_integration(CloudTrail),
            self.control_3_05_ensure_config_all_regions(regions),
            self.control_3_06_ensure_cloudtrail_bucket_logging(CloudTrail),
            self.control_3_07_ensure_cloudtrail_encryption_kms(CloudTrail),
            self.control_3_08_ensure_kms_cmk_rotation(regions),
            self.control_3_09_ensure_flow_logs_enabled_on_all_vpc(regions),
            self.control_3_1_ensure_logging_enabled_for_s3_write(regions),
            self.control_3_1_1_ensure_logging_enabled_for_s3_read(regions),

            # Monitoring_control_4

            self.control_4_0_1_ensure_log_metric_filter_unauthorized_api_calls(CloudTrail),
            self.control_4_0_2_ensure_log_metric_filter_console_signin_no_mfa(CloudTrail),
            self.control_4_0_3_ensure_log_metric_filter_root_usage(CloudTrail),
            self.control_4_0_4_ensure_log_metric_iam_policy_change(CloudTrail),
            self.control_4_0_5_ensure_log_metric_cloudtrail_configuration_changes(CloudTrail),
            self.control_4_0_6_ensure_log_metric_console_auth_failures(CloudTrail),
            self.control_4_0_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk(CloudTrail),
            self.control_4_0_8_ensure_log_metric_s3_bucket_policy_changes(CloudTrail),
            self.control_4_0_9_ensure_log_metric_config_configuration_changes(CloudTrail),
            self.control_4_1_ensure_log_metric_security_group_changes(CloudTrail),
            self.control_4_11_ensure_log_metric_nacl(CloudTrail),
            self.control_4_12_ensure_log_metric_changes_to_network_gateways(CloudTrail),
            self.control_4_13_ensure_log_metric_changes_to_route_tables(CloudTrail),
            self.control_4_14_ensure_log_metric_changes_to_vpc(CloudTrail),
            self.control_4_15_ensure_log_metric_changes_to_org(CloudTrail),
            self.control_4_16_ensure_security_hub_is_enabled(regions),

            # networking control
            self.control_5_01_no_nacl_allow_ingress(regions),
            self.control_5_02_ensure_admin_ports_open_to_world_over_ipv4(regions),
            self.control_5_03_ensure_ports_open_to_world_over_ipv6(regions),
            self.control_5_04_ensure_default_security_groups_restricts_traffic(regions),
            self.control_5_05_ensure_route_tables_are_least_access(regions)
        ]

        return compliance
