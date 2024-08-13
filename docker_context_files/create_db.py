import psycopg2

def create_db():
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="admin", port=5432)

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS suggestions (
        id SERIAL PRIMARY KEY,
        category VARCHAR(255),
        title VARCHAR(255),
        description VARCHAR(255)
    )"""
                )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    create_db()