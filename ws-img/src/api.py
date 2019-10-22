from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import pymongo
import requests
import os
import json
import sys
from PIL import Image

app = Flask(__name__)
CORS(app)

profile = os.environ['PROFILE']
properties = {}

try:
    with open('./resources/profile-{}.properties'.format(profile)) as json_file:
        properties = json.load(json_file)
except FileNotFoundError:
    print('Profile não existe')
    sys.exit(4)

# MONGODB
mg_client = pymongo.MongoClient(properties['mongoAddr'])
pdt_db = mg_client["baseImages"]
pdt_col = pdt_db["produtos"]


@app.route("/")
def hello():
    return "Hello World!"