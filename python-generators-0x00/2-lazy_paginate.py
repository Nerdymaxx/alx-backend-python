import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def paginate_users(page_size, offset):
    """Fetch one page of users from the database at a given offset."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="ALX_prodev"
        )
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(" Error:", err)
        return []

    finally:
        cursor.close()
        conn.close()


def lazy_paginate(page_size):
    """Generator that yields users page by page lazily."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
if __name__ == "__main__":
    for page in lazy_paginate(2):
        for user in page:
            print(f" {user['name']} ({user['email']})")
