from unittest.mock import patch, MagicMock
import lambda_function
import repository


class TestLambdaFunction:
    def test_lambda_handler_returns_200_when_pass_is_data(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/data'}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 200
        mock_get_results.assert_called_once()

    def test_lambda_handler_returns_500_when_pass_is_not_data(self):
        mock_get_results = MagicMock(return_value=[])
        event = {'path': '/not-data'}
        context = {}
        with patch.object(repository, 'get_results', mock_get_results):
            result = lambda_function.lambda_handler(event, context)
        assert result['statusCode'] == 500
        mock_get_results.assert_not_called()
