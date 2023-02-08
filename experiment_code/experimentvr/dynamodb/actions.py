import sys
import logging
import boto3
import logging
from typing import List
from botocore.exceptions import ClientError
from typing import List
from experimentvr.ec2.shared import get_test_instance_ids
from experimentvr.network.shared import get_ip_ranges

logging.basicConfig(level=logging.ERROR)

def blackhole_dynamodb(targets: List[str] = None,
					 								 test_target_type: str ='RANDOM',
					 								 tag_key: str = None, 
                     			 tag_value: str = None, 
                     			 region: str = 'us-east-1',
                     			 duration: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
												tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	print(function_name, "(): test_instance_ids= ", test_instance_ids)

	dynamodb_ip_ranges = get_ip_ranges(region = 'us-east-1',
                      					managed_service = 'DYNAMODB')
	
	parameters = {
		'duration': [
			duration,
		],
    'ipAddresses': [
    	dynamodb_ip_ranges,
    ]
	}

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "BlackholeByIPAddress",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
										'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


def main():
    blackhole_dynamodb(tag_key = 'tag:Name',
 				  		tag_value = 'nodes.experimentvr-us-east-1.k8s.local',
						test_target_type ='RANDOM',
						duration = '60')

if __name__ == "__main__":
    main()
