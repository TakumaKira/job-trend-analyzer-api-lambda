import os
import datetime
from unittest.mock import patch, MagicMock
import db.operations as operations
import db
import aws_secrets_manager_connector


class TestDB:
    def test_get_db_secrets_returns_secrets_when_FUNCTION_ENVIRONMENT_is_aws_lambda(self):
        mock_secrets = {'username': 'rds_user_1', 'password': 'rds_password_1', 'port': '1', 'dbname': 'rds_dbname_1'}
        mock_get_secrets = MagicMock(return_value=mock_secrets)
        with patch.object(aws_secrets_manager_connector, 'get_secrets', mock_get_secrets), patch.dict(os.environ, {'FUNCTION_ENVIRONMENT': 'aws_lambda', 'AWS_DB_SECRETS_NAME': 'db/secrets/name', 'AWS_REGION': 'aws_region', 'AWS_RDS_ENDPOINT': 'aws.rds.endpoint'}):
            secrets = db.get_db_secrets()
        expected_secrets = {'user': 'rds_user_1', 'password': 'rds_password_1', 'host': 'aws.rds.endpoint', 'port': '1', 'dbname': 'rds_dbname_1'}
        assert secrets == expected_secrets

    def test_get_db_secrets_returns_secrets_when_FUNCTION_ENVIRONMENT_is_not_aws_lambda(self):
        mock_secrets = {'username': 'rds_user_1', 'password': 'rds_password_1', 'port': '1', 'dbname': 'rds_dbname_1'}
        mock_get_secrets = MagicMock(return_value=mock_secrets)
        with patch.object(aws_secrets_manager_connector, 'get_secrets', mock_get_secrets), patch.dict(os.environ, {'AWS_DB_SECRETS_NAME': 'db/secrets/name', 'AWS_REGION': 'aws_region', 'AWS_RDS_ENDPOINT': 'aws.rds.endpoint', 'DB_USER': 'db_user', 'DB_PASS': 'db_pass', 'DB_HOST': 'db_host', 'DB_PORT': '2', 'DB_NAME': 'db_name'}):
            secrets = db.get_db_secrets()
        expected_secrets = {'user': 'db_user', 'password': 'db_pass', 'host': 'db_host', 'port': '2', 'dbname': 'db_name'}
        assert secrets == expected_secrets

mock_execute = MagicMock()
mock_fetchall = MagicMock()

class MockCursor:
    def execute(self, query):
        mock_execute(query)

    def fetchall(self):
        return mock_fetchall()

mock_cursor = MockCursor()

class MockConn:
  def cursor(self):
    return mock_cursor

class TestOperations:
    def test_get_results(self):
        mock_db_results = [
            (1, 'url_1', 'job_title_1', 'job_location_1', datetime.datetime(2001, 1, 1, 1, 1, 1), 1),
            (2, 'url_2', 'job_title_2', 'job_location_2', datetime.datetime(2002, 2, 2, 2, 2, 2), 2)
        ]
        mock_results = [
            {'id': 1, 'url': 'url_1', 'job_title': 'job_title_1', 'job_location': 'job_location_1', 'scrape_date': '2001-01-01 01:01:01', 'count': 1},
            {'id': 2, 'url': 'url_2', 'job_title': 'job_title_2', 'job_location': 'job_location_2', 'scrape_date': '2002-02-02 02:02:02', 'count': 2}
        ]
        mock_fetchall.return_value = mock_db_results
        mock_conn = MockConn()
        mock_get_connector = MagicMock(return_value=mock_conn)
        with patch.object(db, 'get_connector', mock_get_connector):
            results = operations.get_results()
        assert results == mock_results
