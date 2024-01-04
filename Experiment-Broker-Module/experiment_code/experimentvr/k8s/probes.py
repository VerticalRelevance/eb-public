from re import I
import sys
import boto3
import logging
import time
import json
import kubernetes
import inspect
import pytz

from logzero import logger
from kubernetes.client import *
from datetime import datetime, timedelta
from experimentvr.k8s.shared import get_eks_api_client
from experimentvr.ec2.shared import get_test_instance_ids
from botocore.exceptions import ClientError


def assert_pod_healthy(
    cluster_name: str,
    pod_name: str,
    namespace: str,
    region: str = "us-east-1",
) -> bool:
    try:
        function_name = inspect.stack()[0][3]
        logger.info(f"{function_name}(): cluster_name={cluster_name}")
        logger.info(f"{function_name}(): pod_name={pod_name}")
        logger.info(f"{function_name}(): namespace={namespace}")
        logger.info(f"{function_name}(): region={region}")

        logger.debug(f"{function_name}(): Getting eks api cli")
        api_client = get_eks_api_client(cluster_name=cluster_name, region=region)
        logger.debug(
            f"{function_name}(): Creating a CoreV1Api client from the base ApiClient"
        )
        v1: CoreV1Api = CoreV1Api(api_client=api_client)
        time.sleep(5)
        logger.debug(f"{function_name}(): Listing pods in namespace {namespace}")
        pods: V1PodList = v1.list_namespaced_pod(namespace=namespace)

        ready_status_count = 0
        pod: V1Pod
        for pod in pods.items:
            pod_metadata: V1ObjectMeta = pod.metadata
            if pod_name in pod_metadata.name and pod_metadata.namespace == namespace:
                logger.info(pod_metadata.name)
                pod_status: V1PodStatus = pod.status
                container_statuses = pod_status.container_statuses
                if container_statuses is None:
                    logger.info(f"container_statuses for {pod_metadata.name} is None")
                    continue
                else:
                    logger.info(
                        f"Iterating on container_statuses for {pod_metadata.name}"
                    )
                    status: V1ContainerStatus
                    for status in container_statuses:
                        short_status = {
                            "name": status.name,
                            "ready": status.ready,
                            "started": status.started,
                            "image": status.image,
                            "restart_count": status.restart_count,
                        }
                    logger.info(
                        f"container_statuses for {status.name} is: {json.dumps(short_status)}"
                    )
                    status_state: V1ContainerState = status.state
                    if (
                        status.ready == True
                        and status.started == True
                        and status_state.running != None
                    ):
                        ready_status_count += 1
        return ready_status_count > 0
    except Exception as e:
        logger.exception(e)


def pod_healthy(
    region: str = None,
    tag_key=None,
    tag_value=None,
    health_check_port: str = None,
    health_check_path: str = None,
    name_space: str = None,
    cluster_name: str = None,
    output_s3_bucket_name: str = None,
    pod_name_pattern: str = None,
) -> bool:
    function_name = sys._getframe().f_code.co_name

    # The instance on which we run the SSM Document that checks the health of
    # the pod is hardcoded below - it should probably be a Python
    # setup variable or passed in from experiment.
    command_execution_intance = get_test_instance_ids(
        test_target_type="RANDOM", tag_key=tag_key, tag_value=tag_value
    )
    print(function_name, "(): instance_to_send_command= ", command_execution_intance)

    parameters = {
        "podNamePattern": [
            pod_name_pattern,
        ],
        "namespace": [
            name_space,
        ],
        "clustername": [
            cluster_name,
        ],
        "podHealthPort": [
            health_check_port,
        ],
        "podHealthPath": [health_check_path],
    }

    session = boto3.Session()

    print(function_name, "(): About to call ssm")

    print(function_name, "(): Parameters - ", parameters)

    folder_prefix = str(time.time()) + "/"

    ssm = session.client("ssm", region)
    try:
        response = ssm.send_command(
            InstanceIds=command_execution_intance,
            DocumentName="PodHealthCheck",
            Parameters=parameters,
            OutputS3BucketName=output_s3_bucket_name,
            OutputS3KeyPrefix=folder_prefix,
            CloudWatchOutputConfig={"CloudWatchOutputEnabled": True},
        )

    except ClientError as e:
        logging.error(e)
        raise

    time.sleep(10)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(output_s3_bucket_name)

    object_keys = []

    for object in bucket.objects.filter(Prefix=folder_prefix):
        print(function_name, "(): object.key = ", object.key)
        object_key_string = object.key
        pos = object_key_string.find("podHealthCheck")
        object_keys.append(object_key_string)
        if pos != -1:
            contents = (
                object.get()["Body"].read().decode(encoding="utf-8", errors="ignore")
            )
            for pod_status in contents.splitlines():
                print(function_name, "(): pod_status = ", pod_status)
                if pod_status == "UP" or pod_status == "Healthy":
                    pods_healthy = True
                else:
                    print("Raise Activity Failed")
                    pods_healthy = False

    # objects_to_delete = []
    # for object_key in object_keys:
    #     objects_to_delete.append({'Key': object_key})

    # print('objects_to_delete = ', objects_to_delete)

    # s3_client = boto3.client('s3')

    # response = s3_client.delete_objects(Bucket = output_s3_bucket_name,
    #                                     Delete = {'Objects': objects_to_delete})

    return pods_healthy
