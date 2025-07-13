import mysql.connector


class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self.connector = None
        self.cursor = None

    def __enter__(self,config):
        self.connector = self.connector.connect(**self.config)
        self.cursor = mysql.connector.cursor()
    
    def __exit__(self):
        self.cursor.close()
        self.connector.close()
config = {
    'host' : 'localhost',
    'username' : 'nerdymax@localhost',
    'password': 'Password',
    'database' : 'ALX_prodev'

}
with DatabaseConnection(config) as db:
    db.cursor.execute("SELECT * FROM Users")
    results = db.cursor.fetchall()
    for row in results:
        print (row)



