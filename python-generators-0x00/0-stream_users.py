import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
def stream_users():
    """generator function that streams data from the database"""
    try:
        conn=mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database= "ALX_prodev"
        )
        cursor = conn.cursor(dictionary= True)
        user_data =cursor.execute("SELECT * FROM user_data")
        print(user_data)

        for row in cursor:
            yield row
        return row
    except mysql.connector.Error as err:
      print("unable to connect to the database")
    finally:
        cursor.close()
        conn.close()
if __name__ == "__main__":
    for user in stream_users():
        print(user)
stream_users()