import psycopg2
print("connecting to postgres")



conn = psycopg2.connect(
        host="localhost",
        database="test",
        user="postgres",
        password="1234567890")

print(conn.closed)
sql = """INSERT INTO indskrivning
         VALUES(%s, %s);"""

cur = conn.cursor()
chip = "asd"
battery = 54
cur.execute(sql, ('ad',33))
cur.execute(sql, (chip,battery))
conn.commit()
cur.close()
conn.close()
print(conn.closed)
