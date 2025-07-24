import boto3
import os
import json
import logging
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError
from config import (
    AI_MODEL,
    TEMPERATURE,
    MAX_TOKEN_COUNT,
    STOP_SEQUENCES,
    AI_MODEL_REGION
)

logger = logging.getLogger(__name__)


def generate_new_post(prompt: str) -> Optional[Dict[str, Any]]:
    try:
        # Initialize Bedrock Runtime client
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=AI_MODEL_REGION
        )
        # body structure depends on a used model
        body = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "inferenceConfig": {  # Optional: Customize inference parameters
                "temperature": TEMPERATURE,
                "maxTokens": MAX_TOKEN_COUNT,
                "stopSequences": STOP_SEQUENCES
            }
        })

        logger.info(f"Invoking Bedrock model '{AI_MODEL}' with prompt: {prompt[:80]}...")  # Log truncated prompt
        response = bedrock_runtime.invoke_model(
            modelId=AI_MODEL,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        response_body_str = response.get("body").read().decode('utf-8')
        response_body = json.loads(response_body_str)

        return response_body

    except ClientError as e:
        logger.error(f"Bedrock API error (ClientError): {e.response['Error']['Code']} - {e.response['Error']['Message']}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from Bedrock: {e}")
        return None
    except Exception as e:
        logger.error(f'An error occurred while processing: {e}')
        return None
