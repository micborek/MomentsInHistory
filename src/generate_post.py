import json
import logging
from utils import generate_new_post
from config import (
    PROMPT,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    try:
        logger.debug(f"Received event: {json.dumps(event)}")

        new_post_data = generate_new_post(PROMPT)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Facebook post generated successfully!',
                'post_content': new_post_data
            })
        }

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return {
        'statusCode': 500,
        'body': json.dumps({'error': f'An unexpected error occurred: {str(e)}'})
    }
