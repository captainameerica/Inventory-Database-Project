import sqlite3

def connect_db(db_name="my_database.db"):
    conn = sqlite3.connect(db_name)
    return conn