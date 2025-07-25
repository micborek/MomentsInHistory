import json
import logging
import random
from config import (
    GENERATED_POST,
    IMAGE_GENERATION_PROMPT,
    HISTORICAL_PERIODS,
    SUCCESS_MESSAGE,
    ERROR_MESSAGE
)
from ai_utils import (
    generate_new_post,
    extract_generated_data,
    prepare_prompt,
    generate_image
)
from sns_utils import send_notification
from facebook_utils import post_to_facebook

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        logger.debug(f"Received context: {context}")

        # prepare prompt about random historical period
        prepared_prompt = prepare_prompt(random.choice(HISTORICAL_PERIODS))

        # generate and extract AI generated data
        raw_generated_data = generate_new_post(prepared_prompt)
        clean_data = extract_generated_data(raw_generated_data)

        # generate an image here to be passed to fb post
        image_bytes = generate_image(clean_data.get(IMAGE_GENERATION_PROMPT))

        # post generated post and image to facebook
        post_to_facebook(clean_data.get(GENERATED_POST), image_bytes)

        # send notification to SNS
        send_notification(SUCCESS_MESSAGE)

        logger.info(f"Lambda finished successfully.")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Facebook post generated successfully!',
                'post_content': clean_data
            })
        }

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        send_notification(ERROR_MESSAGE+str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'An unexpected error occurred: {str(e)}'})
        }
