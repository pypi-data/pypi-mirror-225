import mysql.connector

class Database:
    connection = None
    def __init__(self, host, port, user, passwd, db):
        if(Database.connection is None):
            Database.connection = self._create_connection(host, port, user, passwd, db)

    def _create_connection(self, host, port, user, passwd, db):
        return mysql.connector.connect(host=host, port=port, user=user, passwd=passwd, db=db)

    @staticmethod
    def query(sql):
        cursor = Database.connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def close():
        Database.connection.close()

    @staticmethod
    def execute_query(query, params=None, fetch_one=False):
        cursor = Database.connection.cursor()

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

    @staticmethod
    def insert(table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = Database.connection.cursor()

        cursor.execute(query, tuple(data.values()))
        Database.connection.commit()

        primary_key_id = cursor.lastrowid

        cursor.close()

        return primary_key_id

    @staticmethod
    def insert_query(self, query, params=None):
        self.execute_query(query, params=params)

    @staticmethod
    def update_query(self, query, params=None):
        self.execute_query(query, params=params)

    @staticmethod
    def delete_query(self, query, params=None):
        self.execute_query(query, params=params)

class Logger:
    @staticmethod
    def log(message):
        print(message)