import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASSWORD = os.getenv("DB_PASSWORD")
MYSQL_DB = os.getenv("DB_NAME")
MYSQL_PORT = os.getenv("DB_PORT") if os.getenv("DB_PORT") is None else "3306"

mydb = mysql.connector.connect(
    host=MYSQL_HOST, port=MYSQL_PORT,
    user=MYSQL_USER, passwd=MYSQL_PASSWORD,
    db=MYSQL_DB,
)

print(mydb)