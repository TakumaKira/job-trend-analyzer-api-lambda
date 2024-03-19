import db


def get_results():
    conn = db.get_connector()
    cur = conn.cursor()
    # When updating the query, make sure to update `mock_db_results` in tests/test_db.py accordingly
    query = """
        SELECT
            url,
            job_title,
            job_location,
            scrape_date,
            count
        FROM
            (
                SELECT
                    url,
                    job_title,
                    job_location,
                    scrape_date,
                    count,
                    ROW_NUMBER() OVER (PARTITION BY url ORDER BY scrape_date) AS row_num
                FROM
                    results
            ) AS ranked_results
        ORDER BY
            url,
            row_num;
    """
    cur.execute(query)
    return [{
        'url': row[0],
        'job_title': row[1],
        'job_location': row[2],
        'scrape_date': row[3].strftime("%Y-%m-%d %H:%M:%S"),
        'count': row[4]
    } for row in cur.fetchall()]
