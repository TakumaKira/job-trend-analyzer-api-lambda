import json
import repository


def lambda_handler(event, context):
    if event.get('path') == '/data':
        return {
            'statusCode': 200,
            'headers': {
                # TODO: Control properly
                'Access-Control-Allow-Origin': 'http://localhost:3000',
            },
            'body': json.dumps(repository.get_results())
        }

    return {
        'statusCode': 500,
        'body': json.dumps({'message': 'Internal server error.'})
    }


if __name__ == '__main__':
    lambda_handler({'path': '/data'}, {})
