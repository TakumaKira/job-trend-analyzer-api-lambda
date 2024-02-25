import os
import psycopg2
import aws_secrets_manager_connector


def get_db_secrets():
    if os.getenv('FUNCTION_ENVIRONMENT') == 'aws_lambda':
        secrets = aws_secrets_manager_connector.get_secrets(os.environ['AWS_DB_SECRETS_NAME'], os.environ['AWS_REGION'])
        return {
            'user': secrets['username'],
            'password': secrets['password'],
            'host': os.environ['AWS_RDS_ENDPOINT'],
            'port': secrets['port'],
            'dbname': secrets['dbname']
        }
    return {
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASS'],
        'host': os.environ['DB_HOST'],
        'port': os.environ['DB_PORT'],
        'dbname': os.environ['DB_NAME']
    }

def get_connector():
    secrets = get_db_secrets()
    return psycopg2.connect(f"host={secrets['host']} user={secrets['user']} password={secrets['password']} port={secrets['port']} dbname={secrets['dbname']}")
