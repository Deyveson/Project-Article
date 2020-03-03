import os
import sys

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
profile = os.environ['PROFILE']
properties = {}
resources = os.getcwd() + '/app/resources'
sys.path.append(resources)

try:
    app.config.from_object('config_{}'.format(profile))
except FileNotFoundError:
    print('Profile não existe')
    sys.exit(4)

api = Api(app, version='1.0.1', title='Py-Image API', description='Image Controller')
app.wsgi_app = ProxyFix(app.wsgi_app)
ns = api.namespace('image', description='All operations  image')
CORS(app)

from .views import image_view