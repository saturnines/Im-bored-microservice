import psycopg2

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
        conn.commit()
    except psycopg2.DatabaseError as e:
        print("Database error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_user_cred(username, hashed_password):
    conn = table_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO public.clients (username, password) VALUES (%s, %s)
        """, (username, hashed_password))
        conn.commit()
    except Exception as e:
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
        conn.commit()
    except Exception as e:
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
        return user_info
    except Exception as e:
        print(f"Error fetching user info: {e}")
        conn.rollback()
        return None # Not found
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    create_clients_table()

