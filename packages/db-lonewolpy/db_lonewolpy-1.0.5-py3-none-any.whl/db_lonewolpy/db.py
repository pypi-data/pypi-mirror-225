import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
class Database:
    def __init__(self):
        self.connection = self._create_connection()

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

class Logger:
    def log(self, message):
        print(message)