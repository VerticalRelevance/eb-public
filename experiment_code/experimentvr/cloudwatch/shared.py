import sys
import boto3
import logging

logging.basicConfig(level=logging.ERROR)

def get_cloudwatch_metric_alarm_status(cloudwatchAlarmName):
    """Returns a str of instance IAM profile instances 'name' from a given tagname"""

    function_name = sys._getframe(  ).f_code.co_name
    
    session = boto3.Session()
    cloudwatch = session.client('cloudwatch', 'us-east-1')

    cloudwatch_alarm_status = cloudwatch.describe_alarms(
        AlarmNames=[cloudwatchAlarmName]
    )
    return_value = cloudwatch_alarm_status['MetricAlarms'][0]['StateValue']

    return return_value