import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda function to generate a Facebook post using AWS Bedrock.

    Args:
        event (dict): The event data for the Lambda function.
                      Expected to contain a 'prompt' key with the topic
                      for the Facebook post.
                      Example: {"prompt": "a new product launch for a tech company"}
        context (object): The context object for the Lambda function.

    Returns:
        dict: A dictionary containing the generated Facebook post content
              or an error message.
    """
    logger.info(f"Received event: {json.dumps(event)}")

    # --- AWS Bedrock Configuration ---
    # Bedrock typically uses IAM roles for authentication, not API keys directly in code.
    # Ensure your Lambda function's execution role has permissions to invoke Bedrock models
    # (e.g., 'bedrock:InvokeModel').
    region_name = os.environ.get("AWS_REGION")
    model_id = "amazon.titan-text-express-v1"

    try:
        # Initialize Bedrock Runtime client
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        logger.info(f"Bedrock Runtime client initialized for region: {region_name}")

        # Construct the prompt for the LLM based on Claude's format
        # Claude models typically expect a "Human: ...\n\nAssistant:" format
        llm_prompt = (f"Generate a concise and engaging Facebook post about a random event in history. "
                      f"Make it suitable for a general audience and include relevant emojis or hashtags. Keep it under 200 words.")

        body = json.dumps({
            "inputText": llm_prompt,
            "textGenerationConfig": {
                "temperature": 0.9,
                "topP": 0.9,
                "maxTokenCount": 500,
                "stopSequences": []
            }
        })

        logger.info(f"Invoking Bedrock model '{model_id}' with prompt: {llm_prompt[:100]}...")  # Log truncated prompt
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )
        response_body = json.loads(response.get("body").read())

        print(f"Input token count: {response_body['inputTextTokenCount']}")

        result = response_body['results'][0]
        print(f"Token count: {result['tokenCount']}")
        print(f"Output text: {result['outputText']}")
        print(f"Completion reason: {result['completionReason']}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Facebook post generated successfully!',
                'post_content': result['outputText']
            })
        }


    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'An unexpected error occurred: {str(e)}'})
        }
