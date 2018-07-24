from sinventory import database

base_url = 'https://gs1datakart.org'
path = '/api/v5/products.q(format=json;gtin=8901207019234;imei=863406032103645;latitude=22.5685771;longitude=88.4340235)'
api_id = 'df4a3e288e73d4e3d6e4a975a0c3212d'
api_key = '440f00981a1cc3b1ce6a4c784a4b84ea'
full_url = base_url + path + '?apiId=' + api_id + '&apiKey=' + api_key

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
    'accept-encoding': 'gzip'
}

class Product(database.Database):
  def __init__(self):
    super().__init__("product", "postgres://postgres@localhost/wc")
    self.gtin = None
    self.company = None
    self.name = None
    self.category = None
    self.measurement = None
    self.mrp = None

  def add(self):
    self._insert()

  def delete(self, val):
    self._delete(val)

  def select(self):
    self._select()

  def get_product_info(self):
    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
      return response.content.decode()
    return None
