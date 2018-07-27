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
  def __init__(self, barcode):
    #super().__init__("product", "postgres://postgres@localhost/wc")
    self.gtin = barcode
    self.company = None
    self.name = None
    self.category = None
    self.measurement = None
    self.mrp = None
    self.is_present = True
    
    if self.__update_product_details() is None:
      self.is_present = False
      self.__update_gs1_product_details()
      
  def __update_product_details(self):
    """
    Checks if product already present in DB, if present, update the members
    
    Returns:
      True if present, None if does not exist, False for DB errors
    """
    return False

  def __update_gs1_product_details(self):
    query = 'format=json;'
    query += 'gtin=' + str(self.gtin) + ';'
    query += 'imei=863406032103645;'
    query += 'latitude=22.5685771;'
    query += 'longitude=88.4340235'
    full_path = BASE_URL + '/api/v5/products.q(' + query + ')'
    full_url = full_path + '?apiId=' + API_ID + '&apiKey=' + API_KEY
  
    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
      data = json.loads(response.content.decode())
      self.name = data.name
      self.company = data.brand
      # need to update rest of the things
      
    return None