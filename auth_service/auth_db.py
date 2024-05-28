import psycopg2

import sys
sys.path.append(r"C:\Users\Kevin\Desktop\bored_microservice")  # Change this for AWS.
from logging_service import logger_sender
logger = logger_sender.configure_logging('auth_service',fluentd_host='fluentd', fluentd_port=24224)



def table_connection():
    """This connects to the DB."""
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="admin",
        port=5432
    )
    return conn



def create_clients_table():
    """Creates a database for authenticating calls to suggestion-service api. """
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="admin", port=5432)
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.clients (
                username  VARCHAR(128) NOT NULL,
                password BYTEA NOT NULL,
                rank INT NOT NULL DEFAULT 0,
                CONSTRAINT username_unique UNIQUE (username)
            );
        """)
        logger.info('Created Entry In the auth DB!')
        conn.commit()
    except psycopg2.DatabaseError as e:
        logger.error('Database Error when creating client table')
        print("Database error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_user_cred(username, hashed_password, rank=1):
    conn = table_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO public.clients (username, password, rank) VALUES (%s, %s, %s)
        """, (username, hashed_password, rank))
        logger.info('Inserted Entry In the Auth DB!')
        conn.commit()
    except Exception as e:
        logger.error(f'Database error when trying to insert {e} !')
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def delete_user_cred(username):
    conn = table_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM public.clients WHERE username = %s
        """, (username,))
        logger.info(f'Inserted {username} In the Auth DB!')
        conn.commit()
    except Exception as e:
        logger.error(f"Error in deleting {e} from the db.")
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def get_user_info(username):
    conn = table_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, password, rank FROM public.clients WHERE username = %s", (username,))
        user_info = cur.fetchone()
        logger.info(f"Got {username} from the Auth DB!")
        return user_info
    except Exception as e:
        logger.error(f"Error in fetching {e} from the db.")
        print(f"Error fetching user info: {e}")
        conn.rollback()
        return None # Not found
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_clients_table()

