import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """This connects to the DB."""
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="admin",
        port=5432
    )
    return conn


def create_entry(category, title, description):
    """Creates a new entry in the suggestions table."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO suggestions (category, title, description) VALUES (%s, %s, %s)",
        (category, title, description)
    )
    conn.commit()
    cur.close()
    conn.close()

def delete_entry(category, title, description):
    """Deletes entry in the suggestions table."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM suggestions WHERE category = %s AND title = %s AND description = %s",
        (category, title, description)
    )
    conn.commit()
    cur.close()
    conn.close()

def select_random_entry(category):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM suggestions WHERE category=%s ORDER BY RANDOM() LIMIT 1;",
        (category,)
    )
    # get result
    suggestion = cur.fetchone()
    cur.close()
    conn.close()
    return suggestion