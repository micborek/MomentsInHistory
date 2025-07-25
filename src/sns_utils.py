import boto3
import json
import os
import logging
from typing import Dict, Any
from config import (
    DEFAULT_REGION,
    MESSAGE_SUBJECT
)

logger = logging.getLogger(__name__)

def send_notification(message: str) -> Dict[str, Any]:
    """
    Publishes a message to an AWS SNS (Simple Notification Service) topic.

    Args:
        message (str): The content of the message to be published.

    Returns:
        dict: A dictionary containing the status code and a body with a success
              message and MessageId if successful, or an error message if failed.
              Returns None if the SNS_TOPIC_ARN environment variable is not set.
    """
    try:
        sns_client = boto3.client('sns', region_name=DEFAULT_REGION)
        topic_arn = os.environ.get('SNS_TOPIC_ARN')  # Replace with your topic ARN

        message_subject = MESSAGE_SUBJECT
        message_body = message
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message_body,
            Subject=message_subject
        )
        logger.info(f"SNS message published! Message ID: {response['MessageId']}")

    except Exception as e:
        print(f"Error publishing SNS message: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error publishing SNS message: {str(e)}")
        }
