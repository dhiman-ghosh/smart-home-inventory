from flask_ask import statement

from sinventory import product as dbproduct
from sinventory import profile as dbprofile

class Alexa:
  def __init__(self, context):
    self.id = context.System.user.userId.split('.')[3]

  def welcome(self):
    msg = """Welcome to Smart Home Invenntory.
          You can ask for any stock of any product
          or get a suggestion for shopping."""
    return statement(msg)

  def access_key(self):
    profile = dbprofile.Profile()
    key = profile.get_access_key(self.id)
    return statement('Your Smart Home Inventory Access Key is ' + str(key))

  def stock_query(self, item):
    product = dbproduct.Product()
    res, col = product.search(item)
    if res is None:
      return statement('Sorry, ' + item + ' not found in stock')
    else:
      product.load(res[0])
      return statement(item + ' has ' + str(product.stock) + ' quantities in stock')

