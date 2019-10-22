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

# # MONGODB
# myclient = pymongo.MongoClient(properties['mongoAddr'])
# mybd = myclient["bd_img"]
# mycol = mybd["Imagens"]

@app.route("/test", methods=['GET', 'POST'])
def hello():
    # dado = {"_id": 1, "name": "test", "base64": "asdasdasdsadasd"}
    # x = mycol.insert(dado)
    return "Sucess"