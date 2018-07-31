import os
import psycopg2

#DATABASE_URL = os.environ['DATABASE_URL']

class Database:
    conn = None
    local_members = ['_table_name', '_is_present']

    def __init__(self, table_name, database_url=os.environ['DATABASE_URL']):
        if Database.conn is None:
            Database.conn = psycopg2.connect(database_url, sslmode='require')
        self._table_name = table_name
        self._is_present = True

    @staticmethod
    def __format_db_attributes(ds):
      new_ds = ds.copy()
      for item in Database.local_members:
        try:
          if isinstance(new_ds, dict):
            new_ds.pop(item)
          else:
            new_ds.remove(item)
        except ValueError:
          pass
        except KeyError:
          pass
      return new_ds


    def _insert(self):
        values = list()
        query = None
        dict_ = self.__format_db_attributes(self.__dict__)
        for key, value in dict_.items():
            values.append(value)
        values = str(str(values).rstrip(']')).lstrip( '[' )
        query = "INSERT INTO " + self._table_name + " VALUES (" + values + ");"
        print("Query: " + query)
        res = self.__execute(query, False)
        list1 = (res.split())
        if int(list1.pop()) > 0:
          return True

    def _update(self, value_dict: dict, condition_dict: dict):
      separator = ""
      values = ""
      value_dict = self.__format_db_attributes(value_dict)
      for key, value in value_dict.items():
        values += separator + key + "= '" + value
        separator = "' and"
      conditn = ""
      for key, value in condition_dict.items():
        conditn += key + "= '" + value
      query = "UPDATE " + self._table_name + " SET " + values + "'" + " WHERE " + conditn + "';"
      print("Query: " + query)
      res = self.__execute(query, False)
      list1 = (res.split())
      if int(list1.pop()) > 0:
        return True

    def _delete(self, condition: dict):
        conditn = ""
        for key, value in condition.items():
          conditn += key + "= '" + value
        query = "DELETE FROM " + self._table_name + " WHERE " + conditn + "';"
        print("Query: " + query)
        res = self.__execute(query, False)
        list1 = (res.split())
        if int(list1.pop()) > 0:
          return True

    def _select(self, key_list: list, condition: dict):
      keys = ""
      separator = ""
      key_list = self.__format_db_attributes(key_list)
      for item in key_list:
        keys += separator + item
        separator = ','
      separator = ""
      conditn = ""
      for key, value in condition.items():
        conditn += separator + key + "= '" + value
        separator = "' and"
      query = "SELECT " + keys + " FROM " + self._table_name + " WHERE " + conditn + "';"
      print("Query: " + query)
      values = self.__execute(query, True)
      res = dict(zip(key_list, values))
      return res

    def __execute(self, query, fetch):
        cur = Database.conn.cursor()
        cur.execute(query)
        if fetch is True:
          #data = cur.fetchall()
          data = list(sum(cur.fetchall(), ()))
          Database.conn.commit()
          return data
        else:
          Database.conn.commit()
          return cur.statusmessage
