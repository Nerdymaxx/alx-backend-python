#!/usr/bin/python3
import mysql.connector

class ExecuteQuery:
    def __init__(self, query ,params,config):
        self.query = query
        self.config = config
        self.params = params
        self.connector = None
        self.cursor = None
    def __enter__(self):
        self.connector = mysql.connector.connect(**self.config)
        self.cursor = self.connector.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb ):
        self.cursor.close()
        self.connector.close()
        if exc_type:
            print(f"error during {exc_val}")
        

config  = {
    'user': 'nerdymax',
    'host': 'localhost',
    'password': 'password',
    'database': 'ALX_prodev'

}
query = "SELECT * FROM users WHERE age > %s"
params = (25,)
with ExecuteQuery(query, params, config) as Execute:
    for row in Execute.fetchall():
        print(row)