import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='wamu',
            user='postgres',
            password='1165',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Connection to database was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print({"Error": error})
        time.sleep(2)