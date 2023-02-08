import logging
from typing import List

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.ERROR)

def install_stress_ng_on_pod(node_key: str, node_values: List[str]):
    """Runs SSM command InstallStressNG.yml on all targets with specified tag key and value """

    session = boto3.Session()
    ssm = session.client('ssm', 'us-east-1')

    try:
        ssm.send_command(Targets=[{'Key': node_key, 'Values': node_values}],
                         DocumentName='InstallStressNG')
    except ClientError as e:
        logging.error(e)
        return False

    return True

