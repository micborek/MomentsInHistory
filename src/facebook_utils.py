import os
import requests
import logging
from config import GRAPH_API_VERSION

logger = logging.getLogger(__name__)

def post_to_facebook(generated_post: str):
    try:
        page_id = os.environ.get('FACEBOOK_PAGE_ID')
        page_access_token = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')

        post_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{page_id}/feed"
        payload = {
            'message': generated_post,
            'access_token': page_access_token
        }

        response = requests.post(post_url, data=payload)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()

        logger.info(f"Successfully posted to Facebook Page. Post ID: {result.get('id')}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting to Facebook: {e}")
        return None

    except Exception as e:
        logger.error(f'An error occurred while processing: {e}')
        return None
