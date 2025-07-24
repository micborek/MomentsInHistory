import json
import logging
from config import (
    PROMPT,
    GENERATED_POST,
    IMAGE_GENERATION_PROMPT
)
from ai_utils import (
    generate_new_post,
    extract_generated_data
)
from facebook_utils import post_to_facebook

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        # generate and extract AI generated data
        raw_generated_data = generate_new_post(PROMPT)
        clean_data = extract_generated_data(raw_generated_data)
        # generate an image here to be passed to fb post

        # a comment
        post_to_facebook(clean_data[GENERATED_POST])

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
