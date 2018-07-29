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
      query = "select kc.column_name from information_schema.table_constraints tc, information_schema.key_column_usage kc where tc.constraint_type = 'UNIQUE'";
      cur = Database.conn.cursor()
      cur.execute(query)
      for key in cur:
        key = str(str(key).rstrip('\',)').lstrip( '(\'' ))
        print(key)
        print(self._value)
        query = "DELETE FROM " + self._table_name + " WHERE " + key + " = '" + self._value + "';"
        print("Query: " + query)
        res = self.__execute(query, False)
        list1 = (res.split())
        if (int(list1.pop()) > 0):
          return True

    def _select(self, key_list: list, condition: dict):
      keys = ""
      separator = ""
      for item in key_list:
        keys += separator + item
        separator = ','
        print(keys)
      separator = ""
      conditn = ""
      for key, value in condition.items():
        conditn += separator + key + "= '" + value
        separator = "' and"
      query = "SELECT " + keys + " FROM " + self._table_name + " WHERE " + conditn + "';"
      print("Query: " + query)
      values = self.__execute(query, True)
      res = dict(zip(key_list, values))
      print("Res: " + str(res))
      return res

    def __execute(self, query, fetch):
        cur = Database.conn.cursor()
        cur.execute(query)
        #print(cur.statusmessage)
        if fetch is True:
          print(cur.fetchall())

          data = cur.fetchall()
          print("========")
          for row in data:
            print(row[0])
          print("========")
          Database.conn.commit()
          return data
        else:
          Database.conn.commit()
          return cur.statusmessage