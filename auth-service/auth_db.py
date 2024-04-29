import psycopg2

def create_db():
    """Creates a database for authenticating calls to suggestion-service api. """
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="admin", port=5432)
    cur = conn.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.clients (
                "Id" SERIAL PRIMARY KEY,
                "ClientId" VARCHAR(128) NOT NULL,
                "ClientSecret" BYTEA NOT NULL,
                "IsAdmin" BOOLEAN NOT NULL DEFAULT FALSE,
                CONSTRAINT "ClientId_unique" UNIQUE ("ClientId")
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.blacklist (
                "token" VARCHAR(256) NOT NULL
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
    create_db()