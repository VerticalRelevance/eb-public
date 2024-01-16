import io
import logging
import sys
import json
import boto3

from datetime import datetime

from experimentvr.s3.shared import get_object, create_presigned_url
from chaoslib.experiment import run_experiment
from chaoslib.loader import load_experiment
from chaostoolkit.logging import configure_logger
from logzero import logger


configure_logger()


# name the package: resiliency (chaostoolkit-resiliency)


def handler(event, context):
    """Runs an experiment by `experiment_source`.

    Provide the following event data to invoke the function:

    {
      "experiment_source": "authorizations/tc001.yml",
      "bucket_name": "chaos-testing-bucket",
      ...(additional values for running experiment: AZ, Region, Environment, etc.)
    }
    """
    log_capture, report_capture = __capture_experiment_logs()

    experiment_source = event.get("experiment_source")
    experiment_state = event.get("state")
    if experiment_source:
        logger.info("ChaosToolkit attempting to load experiment: %s", experiment_source)

    try:
        get_object(
            event.get("bucket_name"), experiment_source, event.get("configuration", {})
        )
    except Exception as e:
        logger.exception("Unable to retrieve experiment %s: %s", experiment_source, e)

    experiment = load_experiment(
        create_presigned_url(event.get("bucket_name"), experiment_source)
    )

    resp = run_experiment(experiment)

    print("resp: " + str(resp))
    if resp.get("status") == "success" or resp.get("status") == "completed":
        event.update({"state": "done"})
    else:
        event.update({"state": "failed"})

    event.update({"response": json.dumps(resp)})
    event.update({"report_capture": str(report_capture.getvalue())})

    session = boto3.Session()
    dynamodb = session.resource("dynamodb")

    response = dynamodb.Table("experiment_pipeline_alpha_reporting").put_item(
        Item={"ISO8601": datetime.now().isoformat(), "event": event}
    )

    return event


def __capture_experiment_logs():
    """Captures logs for ChaosToolkit experiments"""
    log_capture_string = io.StringIO()
    error_handler = logging.StreamHandler(log_capture_string)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(error_handler)

    report_capture_string = io.StringIO()
    info_handler = logging.StreamHandler(report_capture_string)
    info_handler.setLevel(logging.INFO)
    logger.addHandler(info_handler)

    return log_capture_string, report_capture_string
