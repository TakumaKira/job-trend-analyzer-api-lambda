from unittest.mock import patch, MagicMock
import repository
import db.operations as operations


class TestRepository:
    def test_get_results(self):
        mock_get_results = MagicMock(return_value=[])
        with patch.object(operations, 'get_results', mock_get_results):
            repository.get_results()
        mock_get_results.assert_called_once()
