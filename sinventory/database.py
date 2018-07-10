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
        for key, value in dict_.items():
            values.append(value)
        values = str(str(values).rstrip(']')).lstrip( '[' )
        query = "INSERT INTO " + self._table_name + " VALUES (" + values + ");"
        print("Query: " + query)
        self.__execute(query, False)

    def _update(self):
        pass

    def _delete(self, value):
      self._value = value;
      query = "select kc.column_name from information_schema.table_constraints tc, information_schema.key_column_usage kc where tc.constraint_type = 'PRIMARY KEY'";
      cur = Database.conn.cursor()
      cur.execute(query)
      primary_key = cur.fetchone()
      key = str(str(primary_key).rstrip('\',)').lstrip( '(\'' ))
      query = "DELETE FROM " + self._table_name + " WHERE " + key + " = '" + self._value + "';"
      print("Query: " + query)
      self.__execute(query, False)

    def _select(self):
        for key, value in self.__dict__.items():
          if key is "alexa_id":
            query = "SELECT " + key + " FROM " + self._table_name + ";"
        print("Query: " + query)
        self.__execute(query, True)

    def __execute(self, query, fetch):
        cur = Database.conn.cursor()
        cur.execute(query)
        #print(cur.statusmessage)
        if fetch is True:
          print(cur.fetchall())
        Database.conn.commit()