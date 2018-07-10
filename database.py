import os
import psycopg2

#DATABASE_URL = os.environ['DATABASE_URL']

class Database:
    conn = None

    def __init__(self, table_name, database_url=os.environ['DATABASE_URL']):
        if Database.conn is None:
            Database.conn = psycopg2.connect(database_url, sslmode='require')
        self._table_name = table_name
    def _insert(self):
        values = list()
        query = None
        dict_ = self.__dict__.copy()
        dict_.pop('_table_name')
        print(dict_)
        for key, value in dict_.items():
            values.append(value)
        values = str(str(values).rstrip(']')).lstrip( '[' )
        query = "INSERT INTO " + self._table_name + " VALUES (" + values + ");"
        print("Query: " + query)
        self.__execute(query)

    def _update(self):
        pass

    def _delete(self):
        for key, value in __dict__.items():
            if key is "alexa_id":
                query = "DELETE FROM " + self._table_name + " WHERE " + key + " = " + value + ");"
        print("Query: " + query)
        self.__execute(query)

    def _select(self):
        for key, value in __dict__.items():
            query = "SELECT " + key + " FROM " + self._table_name + ");"
        print("Query: " + query)
        self.__execute(query)

    def __execute(self, query):
        cur = Database.conn.cursor()
        cur.execute(query)
        Database.conn.commit()