import sys
import logging
from typing import List
from time import sleep

import boto3
from botocore.exceptions import ClientError
from experimentvr.ec2.shared import get_test_instance_ids, get_role_from_instance_profile, get_instance_profile_name


def stress_packet_loss(targets: List[str] = None,
					  	test_target_type: str = None,
 					  	tag_key: str = None,
 					  	tag_value: str = None, 
				  		region: str = None,
					  	duration: str = None,
    					interface: str = None,
    					loss: int = None,
    					port_number: int = None,
    					port_type: str = None):
    """
    Runs SSM command StressPacketLoss.yml on all targets with
    specified tag key and value to cause packet loss specified port
    """

    function_name = sys._getframe().f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type=test_target_type,
        										tag_key=tag_key,
        										tag_value=tag_value,
        										instance_ids=targets)

    parameters = {
        "interface": [
            interface,
        ],
        "portNumber": [
            port_number,
        ],
        "portType": [
            port_type,
        ],
        "loss": [
            loss,
        ],
        "duration": [
            duration,
        ],
    }

    logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

    session = boto3.Session()
    ssm = session.client("ssm", region)

    try:
        response = ssm.send_command(InstanceIds=test_instance_ids,
            												CloudWatchOutputConfig={"CloudWatchOutputEnabled": True},
            												DocumentName="StressPacketLoss",
            												Parameters=parameters)
    except ClientError as e:
        logging.error(e)
        raise

    return response


def stress_memory(targets: List[str] = None,
					  	test_target_type: str = None,
 					  	tag_key: str = None,
 					  	tag_value: str = None, 
				  		region: str = None,
					  	duration: str = None,
					  	memory_percentage_per_worker: str = None,
					  	number_of_workers:  str = None
):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'workers': [
			number_of_workers,
		],
		'percent': [
			memory_percentage_per_worker,
		]
  }

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressMemory",
										InstanceIds = test_instance_ids,
										CloudWatchOutputConfig = {
                                			'CloudWatchOutputEnabled': True},
										Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(True)

def stress_cpu(targets: List[str] = None,
					  	test_target_type: str = None,
 					  	tag_key: str = None,
 					  	tag_value: str = None, 
				  		region: str = None,
					  	duration: str = None,
					  	cpu: str = None
):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'cpu': [
			cpu,
		]
  }

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressCPU",
										InstanceIds = test_instance_ids,
										CloudWatchOutputConfig = {
                                			'CloudWatchOutputEnabled': True},
										Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(True)

def stress_network_latency(targets: List[str] = None,
							test_target_type: str ='RANDOM',
							tag_key: str = None, 
 				  			tag_value: str = None, 
				  			region: str = 'us-east-1',
							interface: str = None,
							ports: str = None,
							port_type: str = None,
							delay: str = None,
							duration: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	print(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'ports': [
			ports,
		],
		'portType': [
			port_type,
		],
		'delay': [
			delay,
		],
		'interface': [
			interface,
		],
	}

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressNetworkLatency",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


def stress_io(targets: List[str] = None,
				  	test_target_type: str = None,
 				  	tag_key: str = None, 
 				  	tag_value: str = None, 
				  	region: str = None,
				  	duration: str = None,
				  	iomix: str = None,
				  	percent: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'iomix': [
			iomix,
		],
		'percent' : [
			percent,
		]
  }

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressIO",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


def stress_network_utilization(targets: List[str] = None,
								test_target_type: str = None,
								tag_key: str = None, 
 				  				tag_value: str = None, 
				  			   	region: str = None,
  					   			interface: str =  None,
					   			port_number: str = None,
					   			port_type: str = None,
					   		 	rate: str = None,
					   			duration: str = None): 

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)

	logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'interface': [
			interface,
		],
		'portNumber': [
			port_number,
		],
		'portType': [
			port_type,
		],
		'rate': [
			rate,
		],
		'duration': [
			duration,
		],
  }

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressNetworkUtilization",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


def stress_all_network_io(targets: List[str] = None,
							test_target_type: str = None,
							tag_key: str = None, 
 				  			tag_value: str = None, 
				  			region: str = None,
							duration: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	print(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
	}

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressAllNetworkIO",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


def root_vol_exhaustion(targets: List[str] = None,
							test_target_type: str = None,
							tag_key: str = None, 
 				  			tag_value: str = None, 
				  			region: str = None,
							workers: str = None,
         					filesize: str = None,
              				duration: str = None):
	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	  tag_key = tag_key,
											 	  tag_value = tag_value,
											 	  instance_ids = targets)
	logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'workers': [
			workers,
		],
		'filesize' : [
			filesize,
		]
    }

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "DiskVolumeExhaustion",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


# Modify experiment to call stress_network_latency and remove this function.
def elk_stress_network_latency(targets: List[str] = None,
							  	test_target_type: str ='RANDOM',
							  	tag_key: str = None, 
 				  			  	tag_value: str = None, 
				  			  	region: str = 'us-east-1',
							  	interface: str = None,
							  	ports: str = None,
								port_type: str = None,
							  	delay: str = None,
							  	duration: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	print(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'ports': [
			ports,
		],
		'portType': [
			port_type,
		],
		'delay': [
			delay,
		],
		'interface': [
			interface,
		],
	}

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "StressNetworkLatency",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)


# Modify the experiment to call black_hole_by_port and remove this function.
def black_hole_elk(targets: List[str] = None,
						test_target_type: str ='RANDOM',
						tag_key: str = None, 
 				  		tag_value: str = None, 
				  		region: str = 'us-east-1',
						elk_sports: str = None,
						elk_dports: str = None,
						protocol: str = 'tcp udp',
						duration: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	print(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'protocol':	[
			protocol,
		],
		'elkDports': [
			elk_dports,
		],
		'elkSports': [
			elk_sports,
		],
	}

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "BlackHoleByPort",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True
                                    },
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)



def black_hole_by_port(targets: List[str] = None,
						test_target_type: str ='RANDOM',
						tag_key: str = None, 
 				  		tag_value: str = None, 
				  		region: str = 'us-east-1',
						source_ports: str = '',
						destination_ports: str = '',
						protocol: str = 'tcp udp',
						duration: str = None):

	function_name = sys._getframe(  ).f_code.co_name

	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	tag_key = tag_key,
											 	tag_value = tag_value,
											 	instance_ids = targets)
	print(function_name, "(): test_instance_ids= ", test_instance_ids)

	parameters = {
		'duration': [
			duration,
		],
		'protocol':	[
			protocol,
		],
		'destinationPorts': [
			destination_ports,
		],
		'sourcePorts': [
			source_ports,
		],
	}

	session = boto3.Session()
	ssm = session.client('ssm', region)
	try:
		response = ssm.send_command(DocumentName = "BlackHoleByPort",
									InstanceIds = test_instance_ids,
									CloudWatchOutputConfig = {
                                		'CloudWatchOutputEnabled': True},
									Parameters = parameters)
	except ClientError as e:
		logging.error(e)
		raise

	return(response)

def remove_iam_role(region: str = 'us-east-1',
						name_space: str = None,
						instance_tag_value: str = None,
						profile_tag_value: str = None, 
						sleep_length: int = 10):
	
	command_execution_intance = get_test_instance_ids(test_target_type ='RANDOM',
                                                          tag_key = 'tag:Name',
                                                          tag_value = tag_value)
	

	instance_profile_name = get_instance_profile_name(tagKey = 'tag:Name', tagValue = tag_value)
	role_name = get_role_from_instance_profile(instance_profile_name)

	print(f"IAM policy to remove IAM role from: {instance_profile_name}")
	print(f"IAM role to remove from Instance Profile: {role_name}")
	#print(f"Instance to remove IAM role from: {}")

	session = boto3.Session()
	b3 = session.client('iam', region)

	try:
		response = b3.remove_role_from_instance_profile(InstanceProfileName = instance_profile_name,
														RoleName = role_name)
		sleep(sleep_length)
		resp = b3.add_role_to_instance_profile(InstanceProfileName = instance_profile_name,
											   RoleName = role_name)
	except ClientError as e:
		logging.error(e)
		raise

	return True
  
def terminate_instance(targets: List[str] = None,
							test_target_type: str ='RANDOM',
							tag_key: str = None, 
							tag_value: str = None, 
							region: str = 'us-east-1',
							):
	function_name = sys._getframe(  ).f_code.co_name
	test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
											 	  tag_key = tag_key,
											 	  tag_value = tag_value,
											 	  instance_ids = targets)
	logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)
