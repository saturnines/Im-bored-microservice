import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="admin", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS suggestions (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    title VARCHAR(255),
    desc VARCHAR(255)
)"""
)



# Finish db add stuff

# Close the Database
conn.commit()
cur.close()
conn.close()
