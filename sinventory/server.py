import os
from flask import Flask, render_template

pkg_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, template_folder=pkg_dir + '/../htdocs')

@app.route('/')
def index():
  login_data = render_template('login.inc')
  return render_template('template.html', main_data=login_data)

