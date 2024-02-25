import db


def get_results():
    conn = db.get_connector()
    cur = conn.cursor()
    cur.execute("SELECT id, url, job_title, job_location, scrape_date, count FROM results")
    return [{
        'id': row[0],
        'url': row[1],
        'job_title': row[2],
        'job_location': row[3],
        'scrape_date': row[4].strftime("%Y-%m-%d %H:%M:%S"),
        'count': row[5]
    } for row in cur.fetchall()]
