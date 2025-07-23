import json

def lambda_handler(event, context):
    response_body = {
        "message": f"Greeting from your Terraform-deployed Lambda!",
        "event": event
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_body)
    }
