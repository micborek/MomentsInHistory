import json
import logging
from ai_utils import (
    generate_new_post,
    extract_generated_data
)
from config import (
    PROMPT,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        raw_generated_data = generate_new_post(PROMPT)
        clean_data = extract_generated_data(raw_generated_data)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Facebook post generated successfully!',
                'post_content': clean_data
            })
        }

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'An unexpected error occurred: {str(e)}'})
        }
