import psycopg2

def create_clients_table():
    """Creates a database for authenticating calls to suggestion-service api. """
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="admin", port=5432)
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.clients (
                id SERIAL PRIMARY KEY,
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



if __name__ == "__main__":
    create_clients_table()