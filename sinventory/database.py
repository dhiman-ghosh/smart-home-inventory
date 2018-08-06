"""
  Contains base class for core level database manipulation functions
"""

import os
import sys
import psycopg2

class Database:
    conn = None
    local_members = ['_table_name', '_is_present', '_error']

    def __init__(self, table_name, database_url=os.environ['DATABASE_URL']):
        if Database.conn is None:
            Database.conn = psycopg2.connect(database_url, sslmode='require')
        self._table_name = table_name
        self._is_present = True
        self._error = None

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

    def _setup(self):
      query = "CREATE TABLE IF NOT EXISTS profile (alexa_id VARCHAR(256) NOT NULL UNIQUE, pin INT NOT NULL UNIQUE, name VARCHAR(50), email VARCHAR(355), mobile BIGINT, PRIMARY KEY(alexa_id));"
      res = self.__execute(query, False)
      query = "CREATE TABLE IF NOT EXISTS product (gtin VARCHAR(32) NOT NULL UNIQUE, brand VARCHAR(64) NOT NULL, name VARCHAR(64)  NOT NULL, category VARCHAR(50), measurement VARCHAR(10), \
          mrp INT, stock INT, last_added date, last_removed date,  alexa_id VARCHAR(256) REFERENCES profile(alexa_id), PRIMARY KEY(gtin));"
      res = self.__execute(query, False)
      return True

    def _insert(self):
      values = list()
      keys = ""
      query = None
      dict_ = self.__format_db_attributes(self.__dict__)
      for key, value in dict_.items():
          keys = keys + key + ","
          values.append(value)
      keys = keys.rstrip(',')
      values = str(str(values).rstrip(']')).lstrip( '[' )
      query = "INSERT INTO " + self._table_name + " (" + keys + ") VALUES (" + values + ");"
      print("Query: " + query)

      try:
        res = self.__execute(query, False)
        list1 = (res.split())
        if int(list1.pop()) > 0:
          return True
      except psycopg2.IntegrityError as err:
        # (gtin, alexa_id) pair already exists
        self._error = str(err)
        print(err, file=sys.stderr)
        return None
      except psycopg2.DatabaseError as err:
        # Other DB Errors
        self._error = str(err)
        print(err, file=sys.stderr)
        return False

      print("Unknown error occurred in _insert", file=sys.stderr)
      return False

    def _update(self, value_dict: dict, condition_dict: dict):
      separator = ""
      values = ""
      value_dict = self.__format_db_attributes(value_dict)
      for key, value in value_dict.items():
        values += separator + key + "='" + str(value)
        separator = "',"
      conditn = ""
      for key, value in condition_dict.items():
        conditn += key + "='" + value
      query = "UPDATE " + self._table_name + " SET " + values + "'" + " WHERE " + conditn + "';"
      print("Query: " + query)

      try:
        res = self.__execute(query, False)
        result_list = (res.split())
        if int(result_list.pop()) > 0:
          return True
      except psycopg2.IntegrityError as err:
        # (gtin, alexa_id) pair already exists
        self._error = str(err)
        print(err, file=sys.stderr)
        return None
      except psycopg2.DatabaseError as err:
        # Other DB Errors
        self._error = str(err)
        print(err, file=sys.stderr)
        return False

      print("Unknown error occurred in _insert", file=sys.stderr)
      return False

    def _delete(self, condition: dict):
      conditn = ""
      for key, value in condition.items():
        conditn += key + "='" + value
      query = "DELETE FROM " + self._table_name + " WHERE " + conditn + "';"
      print("Query: " + query)

      try:
        res = self.__execute(query, False)
        list1 = (res.split())
        if int(list1.pop()) > 0:
          return True
      except psycopg2.DatabaseError as err:
        # DB Errors
        self._error = str(err)
        print(err, file=sys.stderr)
      return False

    def _select(self, key_list: list, condition: dict):
      keys = ""
      separator = ""
      conditn = ""
      key_list = self.__format_db_attributes(key_list)

      for item in key_list:
        keys += separator + item
        separator = ','
      separator = ""

      for key, value in condition.items():
        conditn += separator + key + "='" + value
        separator = "' and"

      query = "SELECT " + keys + " FROM " + self._table_name + " WHERE " + conditn + "';"
      print("Query: " + query)

      try:
        res = self.__execute(query, True)
        if res:
          return res
        return None
      except psycopg2.DatabaseError as err:
        # DB Errors
        self._error = str(err)
        print(err, file=sys.stderr)
        return False

    def _search(self, query: dict):
      keys = ""
      dict_ = self.__format_db_attributes(self.__dict__)
      for key, value in dict_.items():
        keys = keys + key + ","
      keys = keys.rstrip(',')
      separator = ""
      conditn = ""
      for key, value in query.items():
        conditn += separator + "LOWER(" + key + ") LIKE LOWER('%" + value
        separator = "%') and"
      query = "SELECT " + keys + " FROM " + self._table_name + " WHERE " + conditn +  "%');"
      print("Query: " + query)
      
      try:
        res = self.__execute(query, True)
        if res:
          return res
        return None
      except psycopg2.DatabaseError as err:
        # DB Errors
        self._error = str(err)
        print(err, file=sys.stderr)
        return False


    def __execute(self, query, fetch):
      try:
        cur = Database.conn.cursor()
        cur.execute(query)
        if fetch is True:
          ncols = len(cur.description)
          colnames = [cur.description[i][0] for i in range(ncols)]
          data = []
          for row in cur.fetchall():
            res = {}
            for i in range(ncols):
              res[colnames[i]] = row[i]
            data.append(res)
            #print(data)

          Database.conn.commit()
          return data

        Database.conn.commit()
        return cur.statusmessage
      
      except psycopg2.DatabaseError:
        Database.conn.rollback()
        raise

