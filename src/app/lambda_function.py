import json
import os
import repository
import transformers


def lambda_handler(event, context):
    try:
        if event.get('path') == '/data':
            if 'headers' in event and 'Origin' in event['headers']:
                origin = event['headers']['Origin']
                allowed_origins = [os.environ['FRONTEND_ORIGIN_PROD'], os.environ['FRONTEND_ORIGIN_DEV']]
                if origin not in allowed_origins:
                    response = {
                        "statusCode": 400,
                        "headers": {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Origin": "*",  # Allow requests from any origin for error responses
                        },
                        "body": json.dumps({"error": "Invalid request origin"})
                    }
                    return response
                allowed_origin = origin
            else:
                allowed_origin = os.environ['FRONTEND_ORIGIN_PROD']
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': allowed_origin,
                    },
                    'body': json.dumps(transformers.bundle(repository.get_results(), 'url', ['job_title', 'job_location', 'scrape_date', 'count']))
                }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Not found.'})
            }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error.'})
        }


if __name__ == '__main__':
    lambda_handler({'path': '/data'}, {})
