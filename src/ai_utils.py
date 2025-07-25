import boto3
import json
import logging
import base64
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError
from config import (
    AI_MODEL,
    TEMPERATURE,
    MAX_TOKEN_COUNT,
    STOP_SEQUENCES,
    AI_MODEL_REGION,
    IMAGE_GENERATION_PROMPT,
    GENERATED_POST,
    PROMPT_ROLE,
    PROMPT_CONTEXT,
    PROMPT_PERIOD_INSTRUCTION,
    PROMPT_INSTRUCTIONS,
    PROMPT_OUTPUT_FORMAT,
    DEFAULT_REGION
)

logger = logging.getLogger(__name__)


def generate_new_post(prompt: str) -> Optional[Dict[str, Any]]:
    """
    Invokes an AWS Bedrock AI model to generate a new post based on a given prompt.

    This function initializes a Bedrock Runtime client and sends a structured
    request to the configured AI model with the user's prompt and
    inference parameters (temperature, max tokens, stop sequences).
    It logs the invocation process and handles potential API errors,
    JSON decoding issues, or other exceptions.

    Args:
        prompt (str): The text prompt to send to the AI model for content generation.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the raw response body
        from the Bedrock model if the invocation is successful, otherwise None.
        The structure of the returned dictionary depends on the specific
        AI model used.
    """
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

        logger.info(f"Invoking Bedrock model '{AI_MODEL}' with prompt: {prompt}")
        response = bedrock_runtime.invoke_model(
            modelId=AI_MODEL,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        response_body_str = response.get("body").read().decode('utf-8')
        response_body = json.loads(response_body_str)

        logger.info('Bedrock model invoked successfully.')

        return response_body

    except ClientError as e:
        logger.error(
            f"Bedrock API error (ClientError): {e.response['Error']['Code']} - {e.response['Error']['Message']}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from Bedrock: {e}")
        return None
    except Exception as e:
        logger.error(f'An error occurred while processing: {e}')
        return None


def extract_generated_data(data: dict) -> Optional[Dict[str, str]]:
    """
    Extracts structured data (generated post, tags, image generation prompt)
    from the raw response dictionary received from the Bedrock AI model.

    This function expects the 'text' content within the Bedrock response
    to be a JSON string wrapped in Markdown code blocks (e.g., ```json\n...\n```).
    It parses this inner JSON and extracts specific fields defined by
    `GENERATED_POST`, `TAGS`, and `IMAGE_GENERATION_PROMPT` from the config.

    Args:
        data (dict): The raw response dictionary obtained from the
                     `generate_new_post` function's successful invocation.
                     Expected to contain nested keys like
                     `data['output']['message']['content'][0]['text']`.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the extracted
        'generated_post', 'tags', and 'image_generation_prompt' as strings,
        if successful. Returns None if any error occurs during parsing
        or data extraction (e.g., malformed JSON, missing keys).
    """
    try:
        text_content = data['output']['message']['content'][0]['text']

        # Remove the wrapping ```json\n and trailing ```
        json_str = text_content.strip('```json\n').rstrip('```')

        # Parse the inner JSON string
        inner_json = json.loads(json_str)

        #  Extract the fields
        generated_post = inner_json[GENERATED_POST]
        image_generation_prompt = inner_json[IMAGE_GENERATION_PROMPT]

        logger.info(f"Generated Post: {generated_post}")
        logger.info(f"Generated Image Prompt: {image_generation_prompt}")

        return {GENERATED_POST: generated_post, IMAGE_GENERATION_PROMPT: image_generation_prompt}
    except Exception as e:
        logger.error(f'An error occurred while extracting generated data: {e}')
        return None


def prepare_prompt(historical_period):
    logger.info(f"Preparing prompt for: {historical_period}")
    return PROMPT_ROLE + PROMPT_CONTEXT + PROMPT_PERIOD_INSTRUCTION + historical_period + PROMPT_INSTRUCTIONS + PROMPT_OUTPUT_FORMAT

def generate_image(image_prompt:str):
    # Initialize Bedrock Runtime client
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=DEFAULT_REGION
    )

    body = json.dumps({
        'prompt': image_prompt,
        'aspect_ratio': "16:9",
        'mode': "text-to-image",
        'output_format': "PNG"

    })

    model_id = 'stability.sd3-5-large-v1:0'
    logger.info(f"Invoking Bedrock model {model_id} with prompt: {image_prompt}")
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
    )

    output_body = json.loads(response["body"].read().decode("utf-8"))
    base64_output_image = output_body["images"][0]
    image_data = base64.b64decode(base64_output_image)


    logger.info(f"Successfully generated image with {model_id}")

    return image_data
