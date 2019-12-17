from flask import Flask, jsonify, request, send_file
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

# CONNECT MONGODB
myclient = pymongo.MongoClient(properties['mongoAddr'])
mybd = myclient["bd_img"]
mycol = mybd["Imagens"]

@app.route('/get_image')
def get_image():
    if request.args.get('type') == '1':
       filename = 'ok.jpg'
    else:
       filename = 'error.gif'
    return send_file(filename, mimetype='image/jpg')

@app.route("/findImage", methods=['GET', 'POST'])
def searchImage():

    data = []

    for req in request.json:
        print(req)
        data.append(buscaImg(req['Codigo'], req['Name']))

    if len(data) > 0:
        
        return jsonify(data)

    elif len(data) == 0: 

        data = mycol.find({})
        response = []
        
        for value in data:
            response.append(value)
       
        # response = compactTransformImg(codigo, name);
        # jsonify(response)

    # else:
    #     response["menssage"] = "Imagem não existe no servidor"
   
    return jsonify(response)
   

def buscaImg(codigo, name):

    query1 = {"_id": codigo, "name": name}

    response = mycol.find_one(query1)

    return response


def compactTransformImg(codigo: int, name: str):

    arquivo = properties['diretorio'] + name + "/" + codigo + ".JPG"
    basewidth = 400
    img = Image.open(arquivo)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    new_img.save(properties['diretorio'] + name + "/newImg" + codigo + ".JPG", optimize=True)

    new_arquivo = properties['diretorio'] + name + "/newImg" + codigo + ".JPG"

    f = open(new_arquivo, 'rb')
    imgCompact = f.read()
    f.close()

    encodedImg = base64.b64encode(imgCompact)

    documento = {"_id": codigo, "name": name,
                    "base64": "{}".format(encodedImg).replace("b'", "").replace("'", "")}
    x = mycol.insert_one(documento)

    os.remove(new_arquivo)

    response = buscaImg(codigo, name)

    return response