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
    DEFAULT_REGION,
    IMAGE_ASPECT_RATIO,
    IMAGE_GENERATION_MODE,
    IMAGE_OUTPUT_FORMAT,
    IMAGE_GENERATION_MODEL
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
        # The 'body' structure depends on the specific AI model being used
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
            "inferenceConfig": {
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
        # ClientError specifically captures issues related to AWS service calls (e.g., invalid parameters, permissions)
        logger.error(
            f"Bedrock API error (ClientError): {e.response.get('Error', {}).get('Code')} - {e.response.get('Error', {}).get('Message')}",
            exc_info=True  # Log traceback for detailed debugging
        )
        return None
    except json.JSONDecodeError as e:
        # Catches errors if the response body from Bedrock is not valid JSON
        logger.error(f"Failed to parse JSON response from Bedrock: {e}", exc_info=True)
        return None
    except Exception as e:
        # Generic catch-all for any other unforeseen errors
        logger.error(f'An unexpected error occurred in generate_new_post: {e}', exc_info=True)
        return None


def extract_generated_data(data: dict) -> Optional[Dict[str, str]]:
    """
    Extracts structured data (generated post and image generation prompt)
    from the raw response dictionary received from the Bedrock AI model.

    This function expects the 'text' content within the Bedrock response
    to be a JSON string wrapped in Markdown code blocks (e.g., ```json\\n...\\n```).
    It parses this inner JSON and extracts specific fields defined by
    `GENERATED_POST` and `IMAGE_GENERATION_PROMPT` from the config.

    Args:
        data (dict): The raw response dictionary obtained from the
                     `generate_new_post` function's successful invocation.
                     Expected to contain nested keys like
                     `data['content'][0]['text']` if using the Bedrock Messages API.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the extracted
        'generated_post' and 'image_generation_prompt' as strings,
        if successful. Returns None if any error occurs during parsing
        or data extraction (e.g., malformed JSON, missing keys, unexpected structure).
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
    except (TypeError, IndexError) as e:
        logger.error(f"Unexpected data structure from Bedrock response during extraction: {e}", exc_info=True)
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse inner JSON from AI response text: {e}", exc_info=True)
        return None
    except Exception as e:
        # Catch any other unforeseen errors during extraction
        logger.error(f'An unexpected error occurred while extracting generated data: {e}', exc_info=True)
        return None


def prepare_prompt(historical_period: str) -> str:
    """
    Constructs a detailed prompt for the AI model based on a selected historical period
    and predefined instructions.

    This function concatenates several predefined prompt components (role, context,
    period-specific instructions, general instructions, and output format) with
    the dynamically provided historical period to form a complete instruction
    for the AI model.

    Args:
        historical_period (str): The specific historical period to incorporate
                                 into the AI prompt, guiding the content generation.

    Returns:
        str: The complete, formatted prompt string ready to be sent to the AI model.
    """
    logger.info(f"Preparing AI prompt for historical period: '{historical_period}'")
    # Concatenate prompt components defined in config.
    # The order and content of these constants are crucial for AI's response format.
    prompt_str = (
            PROMPT_ROLE +
            PROMPT_CONTEXT +
            PROMPT_PERIOD_INSTRUCTION + historical_period +
            PROMPT_INSTRUCTIONS +
            PROMPT_OUTPUT_FORMAT
    )

    return prompt_str


def generate_image(image_prompt: str) -> Optional[bytes]:
    """
    Generates an image using an AWS Bedrock text-to-image model based on a given prompt.

    This function initializes a Bedrock Runtime client, constructs a request
    for a specified image generation model (e.g., Stability Diffusion),
    and sends the image prompt along with desired aspect ratio and output format.
    It decodes the base64-encoded image from the response.

    Args:
        image_prompt (str): The text description or prompt used to guide the
                            image generation AI model.

    Returns:
        Optional[bytes]: The generated image content as bytes if successful,
                         otherwise None if an error occurs during invocation,
                         response parsing, or decoding.
    """
    try:
        # Initialize Bedrock Runtime client for image generation
        # Using DEFAULT_REGION as configured for image models if different from AI_MODEL_REGION
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=DEFAULT_REGION
        )

        # Body structure for Stability AI models via Bedrock
        body = json.dumps({
            'prompt': image_prompt,
            'aspect_ratio': IMAGE_ASPECT_RATIO,  # Configurable aspect ratio
            'mode': IMAGE_GENERATION_MODE,  # Specifying text-to-image mode
            'output_format': IMAGE_OUTPUT_FORMAT  # Desired output image format
        })

        model_id = 'stability.sd3-5-large-v1:0'
        logger.info(f"Invoking Bedrock model {model_id} with prompt: {image_prompt}")
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
        )

        output_body = json.loads(response["body"].read().decode("utf-8"))
        base64_output_image = output_body["images"][0]  # Stability Diffusion returns a list of images
        image_data = base64.b64decode(base64_output_image)

        logger.info(f"Successfully generated image using model '{model_id}'.")

        return image_data

    except ClientError as e:
        logger.error(
            f"Bedrock image generation API error (ClientError): {e.response.get('Error', {}).get('Code')} - {e.response.get('Error', {}).get('Message')}",
            exc_info=True
        )
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from Bedrock image generation: {e}", exc_info=True)
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Unexpected response structure from Bedrock image generation model: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f'An unexpected error occurred in generate_image: {e}', exc_info=True)
        return None
