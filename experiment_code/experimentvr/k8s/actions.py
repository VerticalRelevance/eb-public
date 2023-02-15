import sys
import boto3
import logging
from typing import List
from botocore.exceptions import ClientError
from experimentvr.ec2.shared import get_test_instance_ids


def pod_stress_all_network_io(targets: List[str] = None,
                                  test_target_type: str ='RANDOM',
                                  tag_key: str = None, 
                                   tag_value: str = None, 
                                  num_containers_to_target: str = '1',
                                  container_name_pattern: str = None,
                                  region: str = 'us-east-1',
                                  duration: str = '60'):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                 tag_key = tag_key,
                                                 tag_value = tag_value,
                                                 instance_ids = targets)
    print(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
        'duration': [
            duration,
        ],
    }

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = "PodStressAllNetworkIO",
                                    InstanceIds = test_instance_ids,
                                    CloudWatchOutputConfig = {
                                        'CloudWatchOutputEnabled': True},
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as e:
        logging.error(e)
        raise

    return(response)

def pod_stress_memory(targets: List[str] = None,
                          test_target_type: str ='RANDOM',
                           tag_key: str = None,
                           tag_value: str = None, 
                        num_containers_to_target: str = '1',
                        container_name_pattern: str = None,
                          region: str = 'us-east-1',
                          duration: str = '60',
                          memory_percentage_per_worker: str = '80',
                          number_of_workers:  str = '1'):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                 tag_key = tag_key,
                                                 tag_value = tag_value,
                                                 instance_ids = targets)
    logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
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
        response = ssm.send_command(DocumentName = "PodStressMemory",
                                    InstanceIds = test_instance_ids,
                                    CloudWatchOutputConfig = {
                                        'CloudWatchOutputEnabled': True},
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as e:
        logging.error(e)
        raise

    return(True)

def pod_stress_io(targets: List[str] = None,
                          test_target_type: str ='RANDOM',
                           tag_key: str = None, 
                           tag_value: str = None, 
                        num_containers_to_target: str = '1',
                        container_name_pattern: str = None,
                          region: str = 'us-east-1',
                          duration: str = '60',
                          iomix: str = '1',
                          percent: str = '80'):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                 tag_key = tag_key,
                                                 tag_value = tag_value,
                                                 instance_ids = targets)
    logging.info(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
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
        response = ssm.send_command(DocumentName = "PodStressIO",
                                    InstanceIds = test_instance_ids,
                                    CloudWatchOutputConfig = {
                                           'CloudWatchOutputEnabled': True},
                                    Parameters = parameters,
                                       OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as e:
        logging.error(e)
        raise

    return(response)

def pod_stress_network_utilization(targets: List[str] = None,
                                      test_target_type: str ='RANDOM',
                                      tag_key: str = None, 
                                       tag_value: str = None, 
                                    num_containers_to_target: str = '1',
                                    container_name_pattern: str = None,
                                      region: str = 'us-east-1',
                                    duration: str = '60'):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                 tag_key = tag_key,
                                                 tag_value = tag_value,
                                                 instance_ids = targets)
    print(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
        'duration': [
            duration,
        ],
    }

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = "PodStressNetworkUtilization",
                                    InstanceIds = test_instance_ids,
                                    CloudWatchOutputConfig = {
                                        'CloudWatchOutputEnabled': True},
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as e:
        logging.error(e)
        raise

    return(response)


def pod_stress_cpu(targets: List[str] = None,
                          test_target_type: str ='RANDOM',
                           tag_key: str = None, 
                           tag_value: str = None, 
                        num_containers_to_target: str = '1',
                        container_name_pattern: str = None,
                          region: str = 'us-east-1',
                          duration: str = '60',
                          cpu: str = '0'):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                tag_key = tag_key,
                                                tag_value = tag_value)
    print(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
        'duration': [
            duration,
        ],
        'cpu': [
            cpu,
        ],
    }

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = 'PodStressCPU',
                                    InstanceIds = test_instance_ids,
                                       CloudWatchOutputConfig = {'CloudWatchOutputEnabled' : True},
                                       Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as err:
        logging.error(err)
    
    return True

def delete_pod(region: str = None,
                   tag_key = None,
                   tag_value = None,
                   name_space: str = None,
                   pod_name_pattern: str = None):

    function_name = sys._getframe(  ).f_code.co_name

    # The instance on which we run the SSM Document that deletes the pod
    # is hardcoded below - it should probably be a Python setup variable.
        # Replace Master with new string - sent to this function from experiment
    command_execution_intance = get_test_instance_ids(test_target_type ='RANDOM',
                                                        tag_key = tag_key,
                                                        tag_value = tag_value)
    print(function_name, "(): instance_to_send_command= ", command_execution_intance)


    parameters = {
        'namespace': [
            name_space,
        ],
        'podNamePattern': [
            pod_name_pattern,
        ],
    }

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = 'DeletePod',
                                    InstanceIds = command_execution_intance,
                                    CloudWatchOutputConfig = {
                                        'CloudWatchOutputEnabled': True
                                    },
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')

    except ClientError as e:
        logging.error(e)
        raise

    return True

"""
In next function need to run SSM document on the worker node that is running
the Authlogin Pod.  Not sure how we are going to determine that.  We need to be
on the worker node so that we can run the tc command at the Pod Level using
nsenter.  Should be passing the tag_value to this function from the Experiment.
"""

def pod_high_cpu(region: str = None,
                    namespace: str = None,
                    tag_key: str = None,
                       tag_value: str = None,
                    pod_name_pattern: str = None):
   
    test_instance_ids = get_test_instance_ids(test_target_type ='RANDOM',
                                                            tag_key = tag_key,
                                                            tag_value = tag_value)
    
    parameters = {'namespace': [namespace],
                  'podNamePattern' : [pod_name_pattern]}

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = 'PodHighCPU',
                                    InstanceIds = test_id,
                                    CloudWatchOutputConfig = {'CloudWatchOutputEnabled' : True},
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as err:
        logging.error(err)
    
    return True

"""
Need to find the ID of the Node that has a process named /coredns -conf /etc/coredns/Corefile running.
Cannot map the Pod/Container to the Node ID because Kubectl is not installed on the Worker Nodes.  So,
will run the termination SSM Document on all of the Worker Nodes.  The two Worker Nodes that are not
hosting the Kube DNS Pods will just return an error.
"""

def pod_termination_crash(targets: List[str] = None,
                            test_target_type: str ='RANDOM',
                            tag_key: str = None, 
                               tag_value: str = None, 
                            num_containers_to_target: str = '2',
                            container_name_pattern: str = 'k8s.coredns',
                              region: str = 'us-east-1'):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                 tag_key = tag_key,
                                                 tag_value = tag_value,
                                                 instance_ids = targets)
    print(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
    }

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = "PodTerminationCrash",
                                    InstanceIds = test_instance_ids,
                                    CloudWatchOutputConfig = {
                                        'CloudWatchOutputEnabled': True},
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as e:
        logging.error(e)
        raise

    return(response)


def pod_blackhole_by_port(targets: List[str] = None,
                            test_target_type: str ='ALL',
                            tag_key: str = None, 
                               tag_value: str = None, 
                            num_containers_to_target: str = '2',
                            container_name_pattern: str = 'coredns',
                            protocol: str = 'tcp udp',
                              region: str = 'us-east-1',
                            source_ports: str = '',
                            destination_ports: str = '',
                            duration: str = None):

    function_name = sys._getframe(  ).f_code.co_name

    test_instance_ids = get_test_instance_ids(test_target_type = test_target_type,
                                                 tag_key = tag_key,
                                                 tag_value = tag_value,
                                                 instance_ids = targets)
    print(function_name, "(): test_instance_ids= ", test_instance_ids)

    parameters = {
        'numContainersToTarget': [
            num_containers_to_target,
        ],
        'containerNamePattern': [
            container_name_pattern,
        ],
        'protocol': [
            protocol,
        ],
        'sourcePorts': [
            source_ports,
        ],
        'destinationPorts': [
            destination_ports,
        ],
        'duration': [
            duration,
        ],
    }

    session = boto3.Session()
    ssm = session.client('ssm', region)
    try:
        response = ssm.send_command(DocumentName = "PodBlackholeByPort",
                                    InstanceIds = test_instance_ids,
                                    CloudWatchOutputConfig = {
                                        'CloudWatchOutputEnabled': True},
                                    Parameters = parameters,
                                    OutputS3BucketName = 'resiliency-ssm-command-output')
    except ClientError as e:
        logging.error(e)
        raise

    return(response)


