import json
from repository import get_results


def lambda_handler(event, context):
    if event.get('path') == '/data':
        return {
            'statusCode': 200,
            'body': json.dumps(get_results())
        }

    return {
        'statusCode': 500,
        'body': json.dumps({'message': 'Internal server error.'})
    }


if __name__ == '__main__':
    lambda_handler({'path': '/data'}, {})
