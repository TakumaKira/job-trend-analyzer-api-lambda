import os
from unittest.mock import patch, MagicMock
import lambda_function
import repository


class TestLambdaFunction:
    def test_lambda_handler_returns_200_when_path_is_data(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/data', 'headers': {'origin': 'https://my-website.com'}}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results), patch.dict(os.environ, {'ALLOWED_FRONTEND_ORIGINS': 'https://my-website.com,http://localhost.com,None'}):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 200
        mock_get_results.assert_called_once()

    def test_lambda_handler_returns_404_when_path_is_not_data(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/not-data', 'headers': {'origin': 'https://my-website.com'}}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results), patch.dict(os.environ, {'ALLOWED_FRONTEND_ORIGINS': 'https://my-website.com,http://localhost.com,None'}):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 404
        mock_get_results.assert_not_called()

    def test_lambda_handler_returns_400_when_request_does_not_have_allowed_origin(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/data', 'headers': {'origin': 'https://not-my-website.com'}}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results), patch.dict(os.environ, {'ALLOWED_FRONTEND_ORIGINS': 'https://my-website.com,http://localhost.com,None'}):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 400
        mock_get_results.assert_not_called()

    def test_lambda_handler_returns_200_when_request_does_not_have_origin_in_headers_and_no_origin_is_allowed(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/data', 'headers': {}}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results), patch.dict(os.environ, {'ALLOWED_FRONTEND_ORIGINS': 'https://my-website.com,http://localhost.com,None'}):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 200
        mock_get_results.assert_called_once()

    def test_lambda_handler_returns_200_when_request_does_not_have_headers_and_no_origin_is_allowed(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/data'}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results), patch.dict(os.environ, {'ALLOWED_FRONTEND_ORIGINS': 'https://my-website.com,http://localhost.com,None'}):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 200
        mock_get_results.assert_called_once()
