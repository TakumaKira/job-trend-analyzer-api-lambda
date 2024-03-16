import json
import repository
import transformers


def lambda_handler(event, context):
    if event.get('path') == '/data':
        return {
            'statusCode': 200,
            'headers': {
                # TODO: Control properly
                'Access-Control-Allow-Origin': 'http://localhost:3000',
            },
            'body': json.dumps(transformers.bundle(repository.get_results(), 'url', ['job_title', 'job_location', 'scrape_date', 'count']))
        }

    return {
        'statusCode': 500,
        'body': json.dumps({'message': 'Internal server error.'})
    }


if __name__ == '__main__':
    lambda_handler({'path': '/data'}, {})
