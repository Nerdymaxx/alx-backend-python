import sqlite3
import functools
import datetime
#### decorator to lof SQL queries


def log_queries(func):
   @functools.wraps
   async def wrapper(*args, **kwargs):
      query= kwargs.get("query") or (args[1] if len(args) > 1 else None)
      params =kwargs.get("params") or (args[2] if len(args) > 2 else None)
       

      if query:
         now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         log_phrase = f"[{now}] Executing {query} | params {params} \n"
         with open("query.log", 'a') as f:
            f.write(log_phrase)
         return await func(*args, **kwargs)
      return wrapper
           
       
      
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
