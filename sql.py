import psycopg2
import os


DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
conn = psycopg2.connect("dbname=ride-my-way user=postgres password=baraka")
#with sqlite3.connect("sample.db") as connection:
c = conn.cursor()
#c.execute(" DROP TABLE posts")
c.execute("CREATE TABLE posts(title TEXT, description TEXT )")
c.execute('INSERT INTO posts VALUES("GOOD", "I\'m GOOD")')
c.execute('INSERT INTO posts VALUES("WELL", "I\'m WELL")') 
c.execute('INSERT INTO posts VALUES("Saturday", "Went for Burrial at Jimmy")') 