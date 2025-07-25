import os
import requests
import logging
import boto3
import io
from config import GRAPH_API_VERSION

logger = logging.getLogger(__name__)
secrets_manager_client = boto3.client('secretsmanager')


def post_to_facebook(generated_post: str, generated_image):
    try:
        page_id = get_secret(os.environ.get('FACEBOOK_PAGE_ID_SECRET_NAME'))
        page_access_token = get_secret(os.environ.get('FACEBOOK_PAGE_TOKEN_SECRET_NAME'))

        post_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/photos"
        payload = {
            'message': generated_post,
            'access_token': page_access_token,
            'published': 'true'
        }
        files = {
            'source': ('image.png', io.BytesIO(generated_image), 'image/png')
        }
        response = requests.post(post_url, data=payload, files=files)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        logger.info(f"Successfully posted to Facebook Page. Post ID: {result.get('id')}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting to Facebook: {e}")
        return None

    except Exception as e:
        logger.error(f'An error occurred while processing: {e}')
        return None


def get_secret(secret_name: str):
    """Retrieves a secret from AWS Secrets Manager."""
    try:
        response = secrets_manager_client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return response['SecretString']
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise
