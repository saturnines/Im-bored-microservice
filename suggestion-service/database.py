import psycopg2

conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="root", port=5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS activity(
id VARCHAR(255))


""")




# Close the Database
conn.commit()
cur.close()
conn.close()
