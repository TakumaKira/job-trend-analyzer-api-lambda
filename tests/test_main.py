from main import lambda_handler


class TestMain:
    def test_lambda_handler_returns_200_when_pass_is_data(self):
        event = {'path': '/data'}
        context = {}
        result = lambda_handler(event, context)
        assert result['statusCode'] == 200

    def test_lambda_handler_returns_500_when_pass_is_not_data(self):
        event = {'path': '/not-data'}
        context = {}
        result = lambda_handler(event, context)
        assert result['statusCode'] == 500
