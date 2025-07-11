import mysql.connector
import os
from dotenv import load_dotenv

# Load .env for DB credentials
load_dotenv()

def stream_users_in_batches(batch_size):
    """Yields batches of users from the database."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as err:
        print(" Error:", err)
    finally:
        cursor.close()
        conn.close()

def batch_processing(batch_size):
    """Yields only users over age 25, one batch at a time."""
    for batch in stream_users_in_batches(batch_size):
        # Filter in memory
        over_25 = [user for user in batch if user['age'] > 25]
        yield over_25

if __name__ == "__main__":
    for group in batch_processing(2):
        for user in group:
            print(f" {user['name']} ({user['age']} years old)")
