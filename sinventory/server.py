import os
import json
import logging
from flask import *

API = '/api/v1'
PKG_DIR = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, template_folder=PKG_DIR + '/../htdocs')
app.secret_key = 'wanderingcouple1194'
app.config['SESSION_TYPE'] = 'filesystem'

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

@app.route('/logout')
def logout():
  session.pop('id', None)
  return redirect(url_for('index'))

@app.route('/product/<barcode>')
def product(barcode):
  # Fetch product goes here
  product_data={'name': 'Lassi', 'company': 'Amul',
      'category': 'food', 'price': '15', 'measurement': '100 ml'}
  product_data = render_template('product.inc',
      barcode=barcode, data=product_data, action='insert')
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
  if pin == '123456':
    return Response("{'status': 'OK'}")
  else:
    return Response("{'status': 'Unauthorized'}", status=401)

@app.route(API + '/product/<action>', methods=['POST', 'PUT', 'PATCH', 'DELETE'])
def manage_product(action):
  method = request.method
  if request.method == 'POST':
    if action == "insert":
      method = 'PUT'
    elif action == "update":
      method = 'PATCH'
    elif action == "delete":
      method = 'DELETE'
    else:
      return Response("{'status': 'Bad Request'}", status=400)

  if method == "PUT":
    return "{'status': 'OK'}"
  elif method == "PATCH":
    return "{'status': 'OK'}"
  elif method == "DELETE":
    return "{'status': 'OK'}"
  else:
    return Response("{'status': 'Internal Server Error'}", status=500)

@app.route(API + '/stock/<barcode>')
def update_stock(barcode):
  return {'status': 'OK'}
