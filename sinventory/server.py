import os
import json
import logging
from flask import *
from flask_ask import Ask, context

from sinventory import profile as dbprofile
from sinventory import product as dbproduct
from sinventory import alexa

API = '/api/v1'
PKG_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, template_folder=PKG_DIR + '/../htdocs')
app.secret_key = 'wanderingcouple1194'
app.config['SESSION_TYPE'] = 'filesystem'
ask = Ask(app, API + '/alexa')

@app.before_first_request
def setup_logging():
  gunicorn_logger = logging.getLogger('gunicorn.error')
  app.logger.handlers = gunicorn_logger.handlers
  app.logger.setLevel(gunicorn_logger.level)

@app.route('/')
def index():
  if 'id' in session:
    data_local = {'8899775544': ('Amul', 'Lassi', '2', '15', '+1')}
    table_data = render_template('table.inc', data=data_local)
    return render_template('template.html', main_data=table_data,
        title="Recent Activity")

  error_no = request.args.get('error', 0)
  login_data = render_template('login.inc', error=int(error_no))
  return render_template('template.html', main_data=login_data)

@app.route('/auth', methods=['POST'])
def auth_redirect():
  pin = request.form['pin']
  resp = authorize(pin)

  if resp.status_code == 200:
    session['id'] = pin
    return redirect(url_for('index'))
  return redirect(url_for('index') + '?error=1')

@app.route('/profile')
def profile():
  profile_data={'name': 'Suku', 'email': 'suku.the.smart@gmail.com',
      'phone': '9804990204'}
  profile_data = render_template('profile.inc',
      data=profile_data, key='1234')
  return render_template('template.html', main_data=profile_data,
      title="User Profile")

@app.route('/logout')
def logout():
  session.pop('id', None)
  return redirect(url_for('index'))

@app.route('/product/<barcode>')
def product(barcode):
  # Fetch product goes here
  product = dbproduct.Product(barcode, use_gs1_api=True)
  product.stock = request.args.get('stock', product.stock)
  product_data = product.get_data()
  product_data = render_template('product.inc',
      barcode=barcode, data=product_data, action='insert')
  if request.args.get('app') is not None:
    return product_data
  else:
    return render_template('template.html', main_data=product_data,
        title="Product Database")

@app.route('/stock/<barcode>')
def stock(barcode):
  stock_data = render_template('stock.inc', barcode=barcode)
  return render_template('template.html', main_data=stock_data,
      title="Product Stock")

# --------------- API ------------------
@app.route(API + '/auth/<pin>', methods=['GET'])
def authorize(pin):
  #user = dbprofile.Profile()
  if True:#user.authorize(pin):
    return Response('{"status": "OK"}')
  else:
    return Response('{"status": "Unauthorized"}', status=401)

@app.route(API + '/product/<action>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def manage_product(action):
  method = request.method
  redirect = False

  product = dbproduct.Product(action)

  if request.method == 'GET':
    product_data = product.get_data(is_json=True)
    return Response(product_data);
  elif request.method == 'POST':
    if action == "insert":
      method = 'PUT'
      redirect = True
    elif action == "update":
      method = 'PATCH'
      redirect = True
    elif action == "delete":
      method = 'DELETE'
      redirect = True
    else:
      return Response('{"status": "Bad Request"}', status=400)

  if method == "PUT":
    product.brand = request.form['company']
    product.name = request.form['name']
    product.category = request.form['category']
    product.measurement = request.form['measurement']
    product.mrp = request.form['mrp']
    product.stock = request.form['stock']
    return Response(product.add())
  elif method == "PATCH":
    return '{"status": "OK"}'
  elif method == "DELETE":
    return Response(product.delete())
  else:
    return Response('{"status": "Internal Server Error"1}', status=500)

@app.route(API + '/stock/<action>', methods=['POST'])
def manage_stock(action):
  try:
    barcode = request.form['barcode']
    quantity = request.form['quantity']
    product = dbproduct.Product(barcode)
    new_stock = 0
  except KeyError:
    return Response('{"status": "Bad Request"}', status=400)
  
  if action == "add":
    new_stock = int(product.stock) + int(quantity)
  elif action == "remove":
    new_stock = int(product.stock) - int(quantity)
    if new_stock < 0:
      new_stock = 0
    
  return Response(product.update({'stock': str(new_stock)}))

# --------------- Alexa ------------------

@ask.launch
def ask_welcome():
  ask_handler = alexa.Alexa(context)
  return ask_handler.welcome()

@ask.intent('FallbackIntent')
def ask_fallback():
  return ask_welcome()

@ask.intent('AccessKey')
def ask_access_key():
  ask_handler = alexa.Alexa(context)
  return ask_handler.access_key() 

@ask.intent('StockQuery')
def ask_stock_query(item):
  ask_handler = alexa.Alexa(context)
  return ask_handler.stock_query(item)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
