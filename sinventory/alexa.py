import inflect
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
    eng = inflect.engine()
    profile = dbprofile.Profile()
    key = eng.number_to_words(int(profile.get_access_key(self.id)), group=1)
    return statement('Your Smart Home Inventory Access Key is, ' + key + '. I repeat, ' + key)

  def stock_query(self, item):
    product = dbproduct.Product()
    res, col = product.search(item)
    if res is None:
      return statement('Sorry, ' + item + ' not found in stock')

    #found_numbers = len(res)
    product.load(res[0])
    
    if product.stock == '0':
      msg = product.brand + ' ' + product.name + ' is running out of stock'
    elif product.stock == '1':
      msg = product.brand + ' ' + product.name + ' has only one quantity left in stock'
    else:
      msg = product.brand + ' ' + product.name + ' has ' + str(product.stock) + ' quantities in stock'
    
    return statement(msg)
