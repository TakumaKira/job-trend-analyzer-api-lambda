import json
import os
import repository
import transformers


def lambda_handler(event, context):
    try:
        if event.get('path') == '/data':
            allowed_origins = os.environ.get('ALLOWED_FRONTEND_ORIGINS', '').split(',')
            if 'None' in allowed_origins:
                allowed_origins[allowed_origins.index('None')] = None
            origin = None
            if 'headers' in event and 'origin' in event['headers']:
                origin = event['headers']['origin']
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
