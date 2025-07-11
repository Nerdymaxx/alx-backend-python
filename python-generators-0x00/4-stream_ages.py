import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def stream_user_ages():
    """Generator that yields one user age at a time."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            yield row[0]

    except mysql.connector.Error as err:
        print(" Error:", err)

    finally:
        cursor.close()
        conn.close()


def calculate_average_age():
    """Calculates and prints the average age using the stream_user_ages generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        print(f" Average age of users: {total_age / count:.2f}")
    else:
        print(" No users found.")


if __name__ == "__main__":
    calculate_average_age()
