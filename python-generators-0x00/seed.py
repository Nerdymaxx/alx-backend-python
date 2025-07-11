#!/usr/bin/python3

from dotenv import load_dotenv
import mysql.connector
import os
import csv
import uuid
load_dotenv()

def connect_db():
    try:
        connect = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")

        )
        print("successfully connected to the database")
        return connect
    except mysql.connector.Error as err:
        print("Connection error:", err)
        return None


def create_database(connect):
    try:
        cursor = connect.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' created or already exists.")
        cursor.execute("USE ALX_prodev")
        print("using ALX_prodev")
    except mysql.connector.Error as err:
        print("failed to create database:", err)
    finally:
        cursor.close()

def create_table(conn):
    try:
        cursor =conn.cursor()
        cursor.execute("""  CREATE TABLE IF NOT EXISTS user_data(
                   user_id CHAR(36) PRIMARY KEY,
                   name VARCHAR(100) NOT NULL,
                   email VARCHAR(100) NOT NULL,
                   age DECIMAL NOT NULL,
                   INDEX(user_id))

""")
        print("table 'user_data' created or already exists.")

    except mysql.connector.Error as err:
        print("failed to create table",err)



    finally:
     cursor.close()

def insert_data(conn, csv_path='user_data.csv'):
    try:
        cursor = conn.cursor()
        with open (csv_path, mode = 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id =str(uuid.uuid4())
                name= row['name']
                email = row['email']
                age = row['age']
                #check if user already exists
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    print(f"⚠️ skipping duplicate: {email}")
                    continue
                cursor.execute(""" INSERT INTO user_data(user_id, name, email, age)
                               VALUES(%s, %s, %s ,%s)""", (user_id, name,email,age))
                print(f"inserted: {name} ({email})")
        conn.commit()
    except Exception as e:
        print("error inserting data:", e)
    finally:
        cursor.close()
def stream_users(conn):
    try:
       cursor = conn.cursor(dictionary=True)
       cursor.execute("SELECT * FROM user_data")
       while True:
           row =cursor.fetchone()
           if row is None:
            break
           yield row
    except mysql.connector.error as err:
     print("failed to connect")

if __name__ == "__main__":
   conn= connect_db()
   if conn:
       create_database(conn)
       create_table(conn)
       insert_data(conn)
       print("\n streaming users from database")
       for user in stream_users(conn):
           print(user)
       conn.close()