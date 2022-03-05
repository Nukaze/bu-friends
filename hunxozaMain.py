import sqlite3
from sqlite3 import Error

class dbController() :
    def create_connection():
        conn = None
        try:
            conn = sqlite3.connect(r"./database/BUFriend.db")
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

if __name__ == '__main__':
    sql = """ CREATE TABLE IF NOT EXISTS projects (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    begin_date text,
                                    end_date text
                                ); """
    conn = dbController.create_connection()
    if conn is not None:
            # create projects table
            dbController.create_table(conn, sql)
    else:
        print("Error! cannot create the database connection.")