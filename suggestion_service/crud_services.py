import psycopg2


#Logging imports
import sys
sys.path.append(r"C:\Users\Kevin\Desktop\bored_microservice")  # Change this for AWS.
from logging_service import logger_sender
logger = logger_sender.configure_logging('crud_services',fluentd_host='fluentd', fluentd_port=24224)


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
    logger.info('Created Entry In the DB!')
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
    logger.info('Deleted Entry In the DB!')
    conn.commit()
    cur.close()
    conn.close()

def random_entry():
    """get random entry"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT category, title, description FROM suggestions ORDER BY RANDOM() LIMIT 1"
    )
    logger.info('Got random entry In the DB!')
    entry = cur.fetchone()
    cur.close()
    conn.close()
    return entry