import transformers


class TestTransformers:
    def test_bundle(self):
        records = [
            {'url': 'example.com', 'job_title': 'Software Engineer', 'job_location': 'New York', 'scrape_date': '2024-03-15', 'count': 1},
            {'url': 'example.com', 'job_title': 'Data Scientist', 'job_location': 'San Francisco', 'scrape_date': '2024-03-16', 'count': 2},
            {'url': 'anotherexample.com', 'job_title': 'Product Manager', 'job_location': 'Seattle', 'scrape_date': '2024-03-14', 'count': 3}
        ]
        bundled_records = transformers.bundle(records, 'url', ['job_title', 'job_location', 'scrape_date', 'count'])
        expected_result = {
            'example.com': [
                {'job_title': 'Software Engineer', 'job_location': 'New York', 'scrape_date': '2024-03-15', 'count': 1},
                {'job_title': 'Data Scientist', 'job_location': 'San Francisco', 'scrape_date': '2024-03-16', 'count': 2}
            ],
            'anotherexample.com': [
                {'job_title': 'Product Manager', 'job_location': 'Seattle', 'scrape_date': '2024-03-14', 'count': 3}
            ]
        }
        assert bundled_records == expected_result
