import db


def get_results():
    conn = db.get_connector()
    cur = conn.cursor()
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
        'id': row[0],
        'url': row[1],
        'job_title': row[2],
        'job_location': row[3],
        'scrape_date': row[4].strftime("%Y-%m-%d %H:%M:%S"),
        'count': row[5]
    } for row in cur.fetchall()]
