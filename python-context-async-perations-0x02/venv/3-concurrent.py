import aiosqlite 
import sqlite3
import asyncio

class Async_query:
    def __init__(self, query, params, db_path):
        self.query = query,
        self.params = None,
        self.db_path = db_path
        self.connect = None
        self.cursor = None
    def __aenter__(self):
        self.connect = aiosqlite.connect(self.db_path)
        self.cursor = self.connect.cursor()
        self.cursor.execute(self.query)
    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()
        self.cursor.close()

        if exc_type:
            print(f"error type {exc_val} occurred")

query = "SELECT * FROM users"
query1 = "SELECT * FROM Users WHERE AGE > 40"
async def async_fetch_users():
   
    db_path = "alx_prodev"
    async with Async_query(query, db_path) as async_query:
        await async_query.connect(db_path)
        return await async_query.execute(query)


db_path = "alx_prodev"    
async def async_fetch_older_users(query1, db_path):
    
    async with Async_query(query1, db_path) as async_query:
        await async_query.connect(db_path)
        return await async_query.execute(query1)
    
async def main():
    db_path = "alx_prodev"
    results = await asyncio.gather(
        async_fetch_users(query, db_path),
        async_fetch_older_users(query1, db_path)
    )
    for i, rows in enumerate(results, 1):
        print(f"\nResults from Query {i}:")
        for row in rows:
            print(row)

asyncio.run(main())



