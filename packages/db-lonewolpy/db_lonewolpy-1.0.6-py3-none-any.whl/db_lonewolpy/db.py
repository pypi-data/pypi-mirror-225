import mysql.connector
from dotenv import load_dotenv
import os

class Database:
    def __init__(self):
        self.connection = self._create_connection()
        load_dotenv()

    def _create_connection(self):
        MYSQL_HOST = os.getenv("DB_HOST")
        MYSQL_USER = os.getenv("DB_USER")
        MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
        MYSQL_DB = os.getenv("DB_NAME")
        MYSQL_PORT = os.getenv("DB_PORT") if os.getenv("DB_PORT") is None else "3306"

        return mysql.connector.connect(
            host=MYSQL_HOST, port=MYSQL_PORT,
            user=MYSQL_USER, passwd=MYSQL_PASSWORD,
            db=MYSQL_DB,
        )

    def query(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def close(self):
        self.connection.close()

    def execute_query(query, params=None, fetch_one=False):
        connection = mysql.connection
        cursor = connection.cursor()

        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)

        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        cursor.close()

        return result

    def insert(table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        connection = mysql.connection
        cursor = connection.cursor()

        cursor.execute(query, tuple(data.values()))
        connection.commit()

        primary_key_id = cursor.lastrowid

        cursor.close()

        return primary_key_id

    def insert_query(self, query, params=None):
        self.execute_query(query, params=params)

    def update_query(self, query, params=None):
        self.execute_query(query, params=params)

    def delete_query(self, query, params=None):
        self.execute_query(query, params=params)

class Logger:
    def log(self, message):
        print(message)