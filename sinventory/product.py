import sys
import json
import requests

from sinventory import database

BASE_URL = 'https://gs1datakart.org'
API_ID = 'df4a3e288e73d4e3d6e4a975a0c3212d'
API_KEY = '440f00981a1cc3b1ce6a4c784a4b84ea'

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
    'accept-encoding': 'gzip'
}

class Product(database.Database):
  def __init__(self, barcode=None, use_gs1_api=False):
    super().__init__("product")
    self.gtin = barcode
    self.brand = ''
    self.name = ''
    self.category = ''
    self.measurement = ''
    self.mrp = ''
    self.stock = '0'
    self.alexa_id = 'NOT_IMPLEMENTED'
    #self.last_added = ''
    #self.last_removed = ''

    self._is_present = True

    if self.load() is None:
      self._is_present = False
      if use_gs1_api is True:
        error_msg = None
        try:
          self.__update_gs1_product_details()
        except AttributeError as ex:
          error_msg = str(ex)
        except ValueError as ex:
          error_msg = str(ex)
        except KeyError as ex:
          error_msg = str(ex)
        except IndexError as ex:
          error_msg = str(ex)

        if error_msg is not None:
          print(str(e), file=sys.stderr)
      
  def load(self, data=None):
    """
    Checks if product already present in DB, if present, update the members
    
    Returns:
      True if present, None if does not exist, False for DB errors
    """
    if data is None:
      if self.gtin is None:
        return False
      data = self._select(list(self.__dict__.keys()), {"gtin": self.gtin})

    if data is None or data is False:
      return None
    elif isinstance(data, list):
      data = data[0]

    print(data)

    self.name = data.get('name')
    self.brand = data.get('brand')
    self.category = data.get('category')
    self.measurement = data.get('measurement')
    self.mrp = data.get('mrp')
    self.stock = data.get('stock')
    return True

  def __update_gs1_product_details(self):
    if self.gtin is None:
      return False

    query = 'format=json;'
    query += 'gtin=' + str(self.gtin) + ';'
    query += 'imei=863406032103645;'
    query += 'latitude=22.5685771;'
    query += 'longitude=88.4340235'
    full_path = BASE_URL + '/api/v5/products.q(' + query + ')'
    full_url = full_path + '?apiId=' + API_ID + '&apiKey=' + API_KEY
  
    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
      #print(str(response.content))
      data = json.loads(response.content.decode())
      self.name = data[0].get('name')
      if "not provided" in self.name:
        self.name = ""
      
      self.brand = data[0].get('brand')
      if self.brand == "":
        self.brand = data[0]['company_detail']['contact_info'].get('website')
        if self.brand != "":
          self.brand = self.brand.split('.')[1].capitalize()
      else:
        self.brand = self.brand.capitalize()
        
      if 'weights_and_measures' in data[0]:
        self.measurement = data[0]['weights_and_measures'].get('net_weight') + ' ' +\
          data[0]['weights_and_measures'].get('measurement_unit')
          
      if 'mrp' in data[0]:
        self.mrp = data[0]['mrp'][0].get('mrp')
      
    return True

  @property
  def is_present(self):
    return self._is_present
    
  def get_data(self, is_json=False):
    """
    Returns product information as dict by default. As JSON if 'json' flag is set.
    """
    dict_ = self.__dict__.copy()
    dict_.update({'is_present': self.is_present})
    if is_json is True:
      return json.dumps(dict_)
    return dict_

  def add(self):
    ret = dict()
    if self._insert():
      ret.update({'status': 'OK'})
      ret.update({'name': self.name})
      ret.update({'is_present': self.is_present})
      return json.dumps(ret)
    ret.update({'status': 'FAILURE'})
    ret.update({'is_present': self.is_present})
    ret.update({'error': self._error})
    return json.dumps(ret)

  def remove(self):
    ret = dict()
    if self._delete({"gtin": self.gtin}):
      ret.update({'status': 'OK'})
      ret.update({'name': self.name})
      return json.dumps(ret)
    ret.update({'status': 'FAILURE'})
    ret.update({'error': self._error})
    return json.dumps(ret)

  def update(self, update_dict=None):
    ret = dict()
    if update_dict is None:
      update_dict = self.__dict__
    if self._update(update_dict, {"gtin": self.gtin}):
      ret.update({'status': 'OK'})
      ret.update({'name': self.name})
      ret.update({'is_present': self.is_present})
      return json.dumps(ret)
    ret.update({'status': 'FAILURE'})
    ret.update({'is_present': self.is_present})
    ret.update({'error': self._error})
    return json.dumps(ret)

  def search(self, item):
    column = 'name'
    ret = self._search({column: item})

    if ret is None:
      column = 'category'
      ret = self._search({column: item})

    if ret is None:
      column = 'brand'
      ret = self._search({column: item})

    return ret, column
