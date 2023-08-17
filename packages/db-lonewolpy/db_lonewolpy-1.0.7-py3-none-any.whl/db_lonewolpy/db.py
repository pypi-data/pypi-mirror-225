import mysql.connector

class Database:
    def __init__(self, host, port, user, passwd, db):
        self.connection = self._create_connection(host, port, user, passwd, db)

    def _create_connection(self, host, port, user, passwd, db):
        return mysql.connector.connect(host, port, user, passwd, db)

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