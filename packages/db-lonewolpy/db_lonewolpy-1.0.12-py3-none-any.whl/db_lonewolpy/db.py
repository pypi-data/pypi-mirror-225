import mysql.connector

class Database:
    connection = None
    cursor = None
    #configuration Parameters
    config = {
        'host':'localhost',
        'user':'root',
        'password':'',
        'database':'',
        'port':'',
    }

    def __init__(self, **kwargs):
        for key in kwargs:
            if key in self.config :
                self.config[key] = kwargs[key]

        if(Database.connection is None):
            Database._create_connection()   

    @staticmethod
    def _create_connection():
        if Database.connection is None:
            try:
                cnx = mysql.connector.connect(user=Database.config['user'], password=Database.config['password'], host=Database.config['host'], database=Database.config['database'])
                Database.connection = cnx
                Database.cursor = cnx.cursor()
                print ("Database connected: ", cnx)
            except mysql.connector.Error as err:
                if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                    return False
                elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                    print ("Database does not exist")
                    return False
                elif err.errno == mysql.connector.errorcode.INTERFACE_ERROR:
                    print("Cursor is closed.")
                else:
                    print(err)
                    return False

        return Database.connection

    @staticmethod
    def query(sql):
        Database._create_connection()
        Database.cursor.execute(sql)
        result = Database.cursor.fetchall()
        return result


    @staticmethod
    def commit():
        Database.connection.commit()

    @staticmethod
    def rollback():
        ''' Rollback changes in case of errors of any kind '''
        Database.connection.rollback()

    @staticmethod
    def close(commit=True):
        if commit:
            Database.connection.commit()
        Database.connection.close()
        Database.connection = None

    @staticmethod
    def execute_query(query, params=None, fetch_one=False):
        Database._create_connection()

        if params is None:
            Database.cursor.execute(query)
        else:
            Database.cursor.execute(query, params)

        if fetch_one:
            result = Database.cursor.fetchone()
        else:
            result = Database.cursor.fetchall()

        return result

    @staticmethod
    def insert(table, data):
        Database._create_connection()
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = Database.cursor
        cursor.execute(query, tuple(data.values()))
        Database.connection.commit()

        primary_key_id = cursor.lastrowid

        return primary_key_id
    
    """
    # Usage

        data_list = [
            {"column1": "value1", "column2": "value2"},
            {"column1": "value3", "column2": "value4"},
            # Add more dictionaries for additional inserts
        ]

        multi_insert("mytable", data_list)
    """
    @staticmethod
    def multi_insert(table, data_list):
        try:
            Database._create_connection()

            if not data_list:
                return

            columns = ', '.join(data_list[0].keys())
            placeholders = ', '.join(['%s'] * len(data_list[0]))

            values = []
            for data in data_list:
                values.append(tuple(data.values()))

            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            Database.cursor.executemany(query, values)
            Database.commit()

            print("Multiple inserts completed successfully.")

        except mysql.connector.Error as err:
            raise err

    """
        # Usage example

            data_list = [
                {"column1": "value1", "column2": "new_value1", "id": 1},
                {"column1": "value2", "column2": "new_value2", "id": 2},
                # ...
            ]

            multi_update("mytable", data_list, "id")
    """
    @staticmethod
    def multi_update(table, data_list, update_column):
        try:
            Database._create_connection()
            # Construct the base SQL UPDATE query
            query = f"UPDATE {table} SET "

            # Create a list to hold the SET clauses for each row
            set_clauses = []

            for column, value in data_list[0].items():
                if column != update_column:
                    set_clauses.append(f"{column} = %s")

            # Combine the SET clauses into the query
            query += ", ".join(set_clauses)

            # Add the WHERE condition for the update_column
            query += f" WHERE {update_column} = %s"

            # Prepare the data for execution
            update_data = []
            for data in data_list:
                update_values = [data[column] for column in data if column != update_column]
                update_values.append(data[update_column])
                update_data.append(update_values)

            print(query)
            # Execute the query multiple times with different data
            Database.cursor.executemany(query, update_data)

            # Commit the changes
            Database.commit()
        except mysql.connector.Error as err:
            raise err

    @staticmethod
    def lastInsertId():
        primary_key_id = Database.cursor.lastrowid
        return primary_key_id

    @staticmethod
    def insert_query(query, params=None):
        Database.execute_query(query, params=params)

    @staticmethod
    def update_query(query, params=None):
        Database.execute_query(query, params=params)

    @staticmethod
    def delete_query(query, params=None):
        Database.execute_query(query, params=params)

class Logger:
    @staticmethod
    def log(message):
        print(message)