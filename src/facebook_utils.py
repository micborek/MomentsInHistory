import os
import requests
import logging
import boto3
import io
import json
import time
from config import (
    GRAPH_API_VERSION,
    PUBLISH_WHEN_POSTED,
    IMAGE_FILE_NAME,
    IMAGE_FILE_TYPE
)

logger = logging.getLogger(__name__)
secrets_manager_client = boto3.client('secretsmanager')


def post_to_facebook(generated_post: str, generated_image: bytes) -> bool | None:
    """
    Posts a text message and an image to a Facebook Page.

    This function retrieves Facebook Page ID and Access Token from AWS Secrets Manager,
    constructs a POST request to the Facebook Graph API, and sends the generated
    text and image for publishing.

    Args:
        generated_post (str): The text content of the post to be published on Facebook.
        generated_image (bytes): The image content in bytes to be published along with the post.

    Returns:
        bool | None: True if the post was successful, None otherwise. Returns None
                     in case of network errors, HTTP errors from Facebook API,
                     or any other unexpected exceptions during the process.
    """
    try:
        # get secrets for Facebook API integration
        page_id = get_secret(os.environ.get('FACEBOOK_PAGE_ID_SECRET_NAME'))
        page_access_token = get_secret(os.environ.get('FACEBOOK_PAGE_TOKEN_SECRET_NAME'))

        # construct request for sending the generated photo
        post_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/photos"
        payload = {
            'message': generated_post,
            'access_token': page_access_token,
            'published': PUBLISH_WHEN_POSTED
        }
        files = {
            'source': (IMAGE_FILE_NAME, io.BytesIO(generated_image), IMAGE_FILE_TYPE)
        }

        # send request to API
        response = requests.post(post_url, data=payload, files=files)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()
        uploaded_photo_id = result.get('id')
        if not uploaded_photo_id:
            logger.error(f"Facebook API did not return photo ID after upload: {result}")
            return None

        # add sleep to avoid racing condition
        time.sleep(1)

        # construct request to send a generated post with the photo sent earlier
        feed_post_url = f'https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/feed'
        feed_payload = {
            'message': generated_post,
            'access_token': page_access_token,
            # Attach the photo using its ID.
            'attached_media': json.dumps([{'media_fbid': uploaded_photo_id}])
        }

        response = requests.post(feed_post_url, data=feed_payload)
        response.raise_for_status()
        feed_result = response.json()

        if 'id' in feed_result:
            logger.info(f"Successfully posted! View post at: https://www.facebook.com/{feed_result['id'].replace('_', '/posts/')}")
        else:
            logger.error(f"Error creating feed post: {feed_result}")

        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting to Facebook: {e}")
        return None

    except Exception as e:
        logger.error(f'An error occurred while processing Facebook post: {e}')
        return None


def get_secret(secret_name: str) -> str | None:
    """
    Retrieves a secret string from AWS Secrets Manager.

    This function connects to AWS Secrets Manager using boto3 and fetches
    the secret value associated with the given `secret_name`. It expects
    the secret to be stored as a plain string ('SecretString').

    Args:
        secret_name (str): The name or ARN of the secret to retrieve from AWS Secrets Manager.

    Returns:
        str | None: The secret string if successfully retrieved, otherwise None.
                    Raises an exception if there's an issue with AWS API call
                    (e.g., secret not found, permissions error).
    """
    try:
        response = secrets_manager_client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return response['SecretString']
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise
