import json
import get_data

def lambda_handler(event, context):
    if event.get('path') == '/data':
        data = get_data.get_data()
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }

    return {
        'statusCode': 500,
        'body': json.dumps({'message': 'Internal server error.'})
    }
