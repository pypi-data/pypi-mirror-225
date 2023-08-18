"""
monitoring_control_3.py
"""

import logging
import re
import traceback

import botocore


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger("Monitoring Logger")


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) LOG_CONF_PATH = os.path.join( BASE_DIR,'..',
# 'logging.conf') LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+ datetime.now().strftime(
# '%Y-%m-%d_%H-%M-%S')+ '.log') logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})


# --- 4 Monitoring ---


class monitoring_control:
    # 4.01 Ensure a log metric filter and alarm exist for unauthorized API calls (Scored)
    def control_4_0_1_ensure_log_metric_filter_unauthorized_api_calls(self, cloudtrails):
        logger.info(
            " ---Inside monitoring_control_4 :: control_4_0_1_ensure_log_metric_filter_unauthorized_api_calls()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.01"
        description = "Ensure a log metric filter and alarm exist for unauthorized API calls"
        scored = True
        failReason = "A log metric filter and alarm does not exist for unauthorized API calls"
        logger.debug(cloudtrails)
        try:
            logger.debug('Check 1')
            for m, n in cloudtrails.items():
                logger.debug('Check 2')
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            logger.debug(o)
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            logger.info(group)
                            client = self.session.client('logs', region_name=m)

                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            logger.debug(filters)
                            logger.debug('Check 3')

                            for p in filters['metricFilters']:
                                # patterns = ["\$\.errorCode\s*=\s*\"?\*UnauthorizedOperation(\"|\)|\s)",
                                #             "\$\.errorCode\s*=\s*\"?AccessDenied\*(\"|\)|\s)"]
                                patterns = '{ ($.errorCode = "*UnauthorizedOperation") || ($.errorCode = "AccessDenied*") || ($.sourceIPAddress!="delivery.logs.amazonaws.com") || ($.eventName!="HeadBucket") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        result = "Compliant"
                                        failReason = ""

                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.02 Ensure a log metric filter and alarm exist for Management Console sign-in without MFA (Scored)
    def control_4_0_2_ensure_log_metric_filter_console_signin_no_mfa(self, cloudtrails):
        logger.info(
            " ---Inside monitoring_control_4 :: control_4_0_2_ensure_log_metric_filter_console_signin_no_mfa()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.02"
        description = "Ensure a log metric filter and alarm exist for Management Console sign-in without MFA"
        scored = True
        failReason = "A log metric filter and alarm does not exist for Management Console sign-in without MFA"
        logger.debug('Check 1 '+ str(cloudtrails))
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        logger.debug('Check 2'+str(o))
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            logger.debug('Check 3' + str(filters))

                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?ConsoleLogin(\"|\)|\s)",
                                #             "\$\.additionalEventData\.MFAUsed\s*\!=\s*\"?Yes"]
                                patterns = '{ ($.eventName = "ConsoleLogin") && ($.additionalEventData.MFAUsed != "Yes") && ($.userIdentity.type = "IAMUser") && ($.responseElements.ConsoleLogin = "Success") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        result = "Compliant"
                                        failReason = ""
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.03 Ensure a log metric filter and alarm exist for usage of "root" account (Scored)
    def control_4_0_3_ensure_log_metric_filter_root_usage(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_0_3_ensure_log_metric_filter_root_usage()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        failReason = ""
        offenders = []
        control = "4.03"
        description = "Ensure a log metric filter and alarm exist for root usage"
        scored = True
        failReason = "A log metric filter and alarm does not exist for root usage"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.userIdentity\.type\s*=\s*\"?Root",
                                #             "\$\.userIdentity\.invokedBy\s*NOT\s*EXISTS",
                                #             "\$\.eventType\s*\!=\s*\"?AwsServiceEvent(\"|\)|\s)"]
                                patterns =  '{ $.userIdentity.type = "Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != "AwsServiceEvent" }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.04 Ensure a log metric filter and alarm exist for IAM policy changes  (Scored)
    def control_4_0_4_ensure_log_metric_iam_policy_change(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_0_4_ensure_log_metric_iam_policy_change()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        ""
        offenders = []
        control = "4.04"
        description = "Ensure a log metric filter and alarm exist for IAM changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for IAM changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?DeleteGroupPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteRolePolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteUserPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutGroupPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutRolePolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutUserPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreatePolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeletePolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreatePolicyVersion(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeletePolicyVersion(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AttachRolePolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DetachRolePolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AttachUserPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DetachUserPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AttachGroupPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DetachGroupPolicy(\"|\)|\s)"]
                                patterns = '{($.eventName="DeleteGroupPolicy")||($.eventName="DeleteRolePolicy")||($.eventName="DeleteUserPolicy")||($.eventName="PutGroupPolicy")||($.eventName="PutRolePolicy")||($.eventName="PutUserPolicy")||($.eventName="CreatePolicy")||($.eventName="DeletePolicy")||($.eventName="CreatePolicyVersion")||($.eventName="DeletePolicyVersion")||($.eventName="AttachRolePolicy")||($.eventName="DetachRolePolicy")||($.eventName="AttachUserPolicy")||($.eventName="DetachUserPolicy")||($.eventName="AttachGroupPolicy")||($.eventName="DetachGroupPolicy")}'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.05 Ensure a log metric filter and alarm exist for CloudTrail configuration changes (Scored)
    def control_4_0_5_ensure_log_metric_cloudtrail_configuration_changes(self, cloudtrails):
        logger.info(
            " ---Inside monitoring_control_4 :: control_4_0_5_ensure_log_metric_cloudtrail_configuration_changes()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.05"
        description = "Ensure a log metric filter and alarm exist for CloudTrail configuration changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for CloudTrail configuration changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?CreateTrail(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?UpdateTrail(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteTrail(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?StartLogging(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?StopLogging(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "CreateTrail") || ($.eventName = "UpdateTrail") || ($.eventName = "DeleteTrail") || ($.eventName = "StartLogging") || ($.eventName = "StopLogging") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.06 Ensure a log metric filter and alarm exist for AWS Management Console authentication failures (Scored)
    def control_4_0_6_ensure_log_metric_console_auth_failures(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_0_6_ensure_log_metric_console_auth_failures()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.06"
        description = "Ensure a log metric filter and alarm exist for console auth failures"
        scored = True
        failReason = "A log metric filter and alarm does not exist for console auth failures"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?ConsoleLogin(\"|\)|\s)",
                                #             "\$\.errorMessage\s*=\s*\"?Failed authentication(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "ConsoleLogin") && ($.errorMessage = "Failed authentication") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.07 Ensure a log metric filter and alarm exist for disabling or scheduled deletion of customer created CMKs (
    # Scored)
    def control_4_0_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk(self, cloudtrails):
        logger.info(
            " ---Inside monitoring_control_4 :: control_4_0_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.07"
        description = "Ensure a log metric filter and alarm exist for disabling or scheduling deletion of KMS CMK"
        scored = True
        failReason = "A log metric filter and alarm does not exist for disabling or scheduling deletion of KMS CMK"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventSource\s*=\s*\"?kms\.amazonaws\.com(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DisableKey(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?ScheduleKeyDeletion(\"|\)|\s)"]
                                patterns = '{($.eventSource = "kms.amazonaws.com") && (($.eventName="DisableKey")||($.eventName="ScheduleKeyDeletion")) }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.08 Ensure a log metric filter and alarm exist for S3 bucket policy changes (Scored)
    def control_4_0_8_ensure_log_metric_s3_bucket_policy_changes(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_0_8_ensure_log_metric_s3_bucket_policy_changes()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.08"
        description = "Ensure a log metric filter and alarm exist for S3 bucket policy changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for S3 bucket policy changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventSource\s*=\s*\"?s3\.amazonaws\.com(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutBucketAcl(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutBucketPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutBucketCors(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutBucketLifecycle(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutBucketReplication(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteBucketPolicy(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteBucketCors(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteBucketLifecycle(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteBucketReplication(\"|\)|\s)"]
                                patterns = '{ ($.eventSource = "s3.amazonaws.com") && (($.eventName = "PutBucketAcl") || ($.eventName = "PutBucketPolicy") || ($.eventName = "PutBucketCors") || ($.eventName = "PutBucketLifecycle") || ($.eventName = "PutBucketReplication") || ($.eventName = "DeleteBucketPolicy") || ($.eventName = "DeleteBucketCors") || ($.eventName = "DeleteBucketLifecycle") || ($.eventName = "DeleteBucketReplication")) }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.09 Ensure a log metric filter and alarm exist for AWS Config configuration changes (Scored)
    def control_4_0_9_ensure_log_metric_config_configuration_changes(self, cloudtrails):
        logger.info(
            " ---Inside monitoring_control_4 :: control_4_0_9_ensure_log_metric_config_configuration_changes()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.09"
        description = "Ensure a log metric filter and alarm exist for for AWS Config configuration changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for for AWS Config configuration changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventSource\s*=\s*\"?config\.amazonaws\.com(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?StopConfigurationRecorder(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteDeliveryChannel(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutDeliveryChannel(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?PutConfigurationRecorder(\"|\)|\s)"]
                                patterns = '{ ($.eventSource = "config.amazonaws.com") && (($.eventName="StopConfigurationRecorder")||($.eventName="DeleteDeliveryChannel")||($.eventName="PutDeliveryChannel")||($.eventName="PutConfigurationRecorder")) }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.1 Ensure a log metric filter and alarm exist for security group changes (Scored)
    def control_4_1_ensure_log_metric_security_group_changes(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_1_ensure_log_metric_security_group_changes()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.1"
        description = "Ensure a log metric filter and alarm exist for security group changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for security group changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?AuthorizeSecurityGroupIngress(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AuthorizeSecurityGroupEgress(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?RevokeSecurityGroupIngress(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?RevokeSecurityGroupEgress(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreateSecurityGroup(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteSecurityGroup(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "AuthorizeSecurityGroupIngress") || ($.eventName = "AuthorizeSecurityGroupEgress") || ($.eventName = "RevokeSecurityGroupIngress") || ($.eventName = "RevokeSecurityGroupEgress") || ($.eventName = "CreateSecurityGroup") || ($.eventName = "DeleteSecurityGroup") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.11 Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL) (Scored)
    def control_4_11_ensure_log_metric_nacl(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_11_ensure_log_metric_nacl()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.11"
        description = "Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL)"
        scored = True
        failReason = "A log metric filter and alarm does not exist for changes to Network Access Control Lists (NACL)"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?CreateNetworkAcl(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreateNetworkAclEntry(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteNetworkAcl(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteNetworkAclEntry(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?ReplaceNetworkAclEntry(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?ReplaceNetworkAclAssociation(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "CreateNetworkAcl") || ($.eventName = "CreateNetworkAclEntry") || ($.eventName = "DeleteNetworkAcl") || ($.eventName = "DeleteNetworkAclEntry") || ($.eventName = "ReplaceNetworkAclEntry") || ($.eventName = "ReplaceNetworkAclAssociation") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.12 Ensure a log metric filter and alarm exist for changes to network gateways (Scored)
    def control_4_12_ensure_log_metric_changes_to_network_gateways(self, cloudtrails):
        logger.info(
            " ---Inside monitoring_control_4 :: control_4_12_ensure_log_metric_changes_to_network_gateways()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        failReason = ""
        offenders = []
        control = "4.12"
        description = "Ensure a log metric filter and alarm exist for changes to network gateways"
        scored = True
        failReason = "A log metric filter and alarm does not exist for changes to network gateways"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?CreateCustomerGateway(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteCustomerGateway(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AttachInternetGateway(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreateInternetGateway(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteInternetGateway(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DetachInternetGateway(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "CreateCustomerGateway") || ($.eventName = "DeleteCustomerGateway") || ($.eventName = "AttachInternetGateway") || ($.eventName = "CreateInternetGateway") || ($.eventName = "DeleteInternetGateway") || ($.eventName = "DetachInternetGateway") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.13 Ensure a log metric filter and alarm exist for route table changes (Scored)
    def control_4_13_ensure_log_metric_changes_to_route_tables(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_13_ensure_log_metric_changes_to_route_tables()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.13"
        description = "Ensure a log metric filter and alarm exist for route table changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for route table changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?CreateRoute(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreateRouteTable(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?ReplaceRoute(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?ReplaceRouteTableAssociation(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteRouteTable(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteRoute(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DisassociateRouteTable(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "CreateRoute") || ($.eventName = "CreateRouteTable") || ($.eventName = "ReplaceRoute") || ($.eventName = "ReplaceRouteTableAssociation") || ($.eventName = "DeleteRouteTable") || ($.eventName = "DeleteRoute") || ($.eventName = "DisassociateRouteTable") }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.14 Ensure a log metric filter and alarm exist for VPC changes (Scored)
    def control_4_14_ensure_log_metric_changes_to_vpc(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_14_ensure_log_metric_changes_to_vpc()--- ")
        self.refresh_session()
        """Summary
    
        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.14"
        description = "Ensure a log metric filter and alarm exist for VPC changes"
        scored = True
        failReason = "A log metric filter and alarm does not exist for VPC changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = ["\$\.eventName\s*=\s*\"?CreateVpc(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteVpc(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?ModifyVpcAttribute(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AcceptVpcPeeringConnection(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?CreateVpcPeeringConnection(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DeleteVpcPeeringConnection(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?RejectVpcPeeringConnection(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?AttachClassicLinkVpc(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DetachClassicLinkVpc(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?DisableVpcClassicLink(\"|\)|\s)",
                                #             "\$\.eventName\s*=\s*\"?EnableVpcClassicLink(\"|\)|\s)"]
                                patterns = '{ ($.eventName = "CreateVpc") || ($.eventName = "DeleteVpc") || ($.eventName = "ModifyVpcAttribute") || ($.eventName = "AcceptVpcPeeringConnection") || ($.eventName = "CreateVpcPeeringConnection") || ($.eventName = "DeleteVpcPeeringConnection") || ($.eventName = "RejectVpcPeeringConnection") || ($.eventName = "AttachClassicLinkVpc") || ($.eventName = "DetachClassicLinkVpc") || ($.eventName = "DisableVpcClassicLink") || ($.eventName = "EnableVpcClassicLink") }'
                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        failReason = ""
                                        result = "Compliant"
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.15 Ensure a log metric filter and alarm exist for Organizations changes (Scored)
    def control_4_15_ensure_log_metric_changes_to_org(self, cloudtrails):
        logger.info(" ---Inside monitoring_control_4 :: control_4_15_ensure_log_metric_changes_to_org()--- ")
        self.refresh_session()
        """Summary

        Returns:
            TYPE: Description
        """
        result = "Not Compliant"
        offenders = []
        control = "4.15"
        description = "Ensure a log metric filter and alarm exist for Organizations  changes"
        scored = True
        failReason = "A log metric filter and alarm does not not exists for organizations changes"
        try:
            for m, n in cloudtrails.items():
                for o in n:
                    try:
                        if o['CloudWatchLogsLogGroupArn']:
                            group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                            client = self.session.client('logs', region_name=m)
                            filters = client.describe_metric_filters(
                                logGroupName=group
                            )
                            for p in filters['metricFilters']:
                                # patterns = [
                                #     "\$\.eventSource\s*=\s*\"?organizations.amazonaws.com(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?AcceptHandshake(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?AttachPolicy(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?CreateAccount(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?CreateOrganizationalUnit(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?CreatePolicy(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?DeclineHandshake(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?DeleteOrganization(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?DeleteOrganizationalUnit(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?DeletePolicy(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?DetachPolicy(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?DisablePolicyType(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?EnablePolicyType(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?InviteAccountToOrganization(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?LeaveOrganization(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?MoveAccount(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?RemoveAccountFromOrganization(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?UpdatePolicy(\"|\)|\s)",
                                #     "\$\.eventName\s*=\s*\"?UpdateOrganizationalUnit(\"|\)|\s)",
                                # ]
                                patterns = '{ ($.eventSource = "organizations.amazonaws.com") && (($.eventName = ' \
                                           '"AcceptHandshake") || ($.eventName = "AttachPolicy") || ($.eventName = ' \
                                           '"CreateAccount") || ($.eventName = "CreateOrganizationalUnit") || (' \
                                           '$.eventName = "CreatePolicy") || ($.eventName = "DeclineHandshake") || (' \
                                           '$.eventName = "DeleteOrganization") || ($.eventName = ' \
                                           '"DeleteOrganizationalUnit") || ($.eventName = "DeletePolicy") || (' \
                                           '$.eventName = "DetachPolicy") || ($.eventName = "DisablePolicyType") || (' \
                                           '$.eventName = "EnablePolicyType") || ($.eventName = ' \
                                           '"InviteAccountToOrganization") || ($.eventName = "LeaveOrganization") || ' \
                                           '($.eventName = "MoveAccount") || ($.eventName = ' \
                                           '"RemoveAccountFromOrganization") || ($.eventName = "UpdatePolicy") || (' \
                                           '$.eventName = "UpdateOrganizationalUnit")) }'

                                if p['filterPattern'] == patterns:
                                    cwclient = self.session.client('cloudwatch', region_name=m)
                                    response = cwclient.describe_alarms_for_metric(
                                        MetricName=p['metricTransformations'][0]['metricName'],
                                        Namespace=p['metricTransformations'][0]['metricNamespace']
                                    )
                                    snsClient = self.session.client('sns', region_name=m)
                                    subscribers = snsClient.list_subscriptions_by_topic(
                                        TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                        #  Pagination not used since only 1 subscriber required
                                    )
                                    if not len(subscribers['Subscriptions']) == 0:
                                        result = "Compliant"
                                        failReason = ""
                                # if self.find_in_string(patterns, str(p['filterPattern'])):
                                #     cwclient = self.session.client('cloudwatch', region_name=m)
                                #     response = cwclient.describe_alarms_for_metric(
                                #         MetricName=p['metricTransformations'][0]['metricName'],
                                #         Namespace=p['metricTransformations'][0]['metricNamespace']
                                #     )
                                #     snsClient = self.session.client('sns', region_name=m)
                                #     subscribers = snsClient.list_subscriptions_by_topic(
                                #         TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                #         #  Pagination not used since only 1 subscriber required
                                #     )
                                #     if not len(subscribers['Subscriptions']) == 0:
                                #         result = "Compliant"
                    except:
                        pass
        except AttributeError as e:
            logger.error(" No details found for CloudTrail!!! ")
        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    # 4.16 Ensure AWS Security Hub is enabled
    def control_4_16_ensure_security_hub_is_enabled(self, regions: list):
        """
        :param self:
        :return:
        """
        logger.info(" ---Inside monitoring_control_4 :: control_4_16_ensure_security_hub_is_enabled()--- ")
        self.refresh_session()

        result = "Compliant"
        failReason = ""
        offenders = []
        control = "4.16"
        description = "Ensure security hub is enabled"
        scored = True

        for region in regions:
            client = self.session.client('securityhub', region_name=region)
            try:
                response = client.describe_hub()
                # Scenario 1: SecurityHub is enabled for an AWS Account
                if response:
                    pass
            except botocore.exceptions.ClientError as error:
                # Scenario 2: SecurityHub is not enabled for an AWS account.
                if error.response['Error']['Code'] == 'InvalidAccessException':
                    result = "Not Compliant"
                    offenders.append(region)
                    failReason = "Security hub is not enable in these regions"

        return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
                'Description': description, 'ControlId': control}

    '''*****************************************************************************'''

    # # 3.15 Ensure appropriate subscribers to each SNS topic (Not Scored)
    # def control_3_15_verify_sns_subscribers(self):
    #     logger.info(" ---Inside monitoring_control_3 :: control_3_15_verify_sns_subscribers()--- ")
    #     """Summary
    #
    #     Returns:
    #         TYPE: Description
    #     """
    #     result = "Manual"
    #     failReason = ""
    #     offenders = []
    #     control = "3.15"
    #     description = "Ensure appropriate subscribers to each SNS topic, please verify manually"
    #     scored = False
    #     failReason = "Control not implemented using API, please verify manually"
    #     return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
    #             'Description': description, 'ControlId': control}
    #
    # # 3.16 Ensure redshift audit logging is enabled
    # def control_3_16_ensure_redshift_audit_logging_enabled(self, regions: list) -> dict:
    #     logger.info(" ---Inside monitoring_control_3 :: control_3_16_ensure_redshift_audit_logging_enabled")
    #
    #     """Summary
    #
    #     Returns:
    #         TYPE: dict
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "3.16"
    #     description = "Ensure audit logging is enabled in all redshift clusters"
    #     scored = True
    #     for n in regions:
    #         clusters = self.list_redshift_clusters(n)
    #         client = self.session.client('redshift', region_name=n)
    #
    #         for cluster in clusters:
    #             response = client.describe_logging_status(
    #                 ClusterIdentifier=cluster
    #             )
    #             if not response['LoggingEnabled']:
    #                 result = "Not Compliant"
    #                 failReason = "Found Redshift cluster with audit logging disabled"
    #                 offenders.append(cluster)
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
    # # 3.17 Ensure ELB access logs are enabled
    # def control_3_17_ensure_elb_access_logs_enabled(self, regions: list) -> dict:
    #     logger.info(" ---Inside monitoring_control_3 :: control_3_17_ensure_elb_access_logging_enabled")
    #
    #     """Summary
    #
    #     Returns:
    #         TYPE: dict
    #     """
    #     result = "Compliant"
    #     failReason = ""
    #     offenders = []
    #     control = "3.17"
    #     description = "Ensure access logging is enabled in all load balancers"
    #     scored = True
    #     for n in regions:
    #         elb_lst = self.list_elb(n)
    #         client = self.session.client('elb', region_name=n)
    #
    #         for elb in elb_lst:
    #             response = client.describe_load_balancer_attributes(
    #                 LoadBalancerName=elb
    #             )
    #             try:
    #                 if not response['LoadBalancerAttributes']['AccessLog']['Enabled']:
    #                     result = "Not Compliant"
    #                     failReason = "Found load balancer with access logging disabled"
    #                     offenders.append(elb)
    #             except KeyError:
    #                 result = "Not Compliant"
    #                 failReason = "Found load balancer with access logging disabled"
    #                 offenders.append(elb)
    #
    #     return {
    #         'Result': result,
    #         'failReason': failReason,
    #         'Offenders': offenders,
    #         'ScoredControl': scored,
    #         'Description': description,
    #         'ControlId': control
    #     }
