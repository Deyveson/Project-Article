import base64
import json
import os
import sys

import pymongo
from PIL import Image
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_restplus import Api, Resource, Namespace
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
api = Api(app, version='1.0.1', title='Py-Image API', description='Image Controller')
app.wsgi_app = ProxyFix(app.wsgi_app)
ns = api.namespace('image', description='All operations  image')
CORS(app)


profile = os.environ['PROFILE']
properties = {}

# LOADING PROPERTIES
try:
    with open('./resources/profile-{}.properties'.format(profile)) as json_file:
        properties = json.load(json_file)
except FileNotFoundError:
    print('Profile não existe')
    sys.exit(4)

# CONNECT MONGODB
myclient = pymongo.MongoClient(properties['mongoAddr'])
mybd = myclient[properties['myclient']]
mycol = mybd[properties['mybd']]


@ns.route('/version')
class Version (Resource):
    def get(self):
        """
            Version project.
        """
        return api.version


@ns.route('/get_image/<id>')
class ImageDefault (Resource):

    def post(self, id):
        print(id)
        if id == '1':
           filename = 'ok.jpg'
        else:
           filename = 'error.gif'
        return send_file(filename, mimetype='image/jpg')


@ns.route('/findImage/<name>/<codigo>')
class Compact (Resource):
    def get(self, name, codigo):
        data = []
        response = {}

        data.append(buscaImg(int(codigo), name))

        if data[0] != None:

          return jsonify(data)

        elif data[0] == None:

          # data = mycol.find({})
          # response = []

          # for value in data:
          #     response.append(value)

          response = compactTransformImg(int(codigo), name)
          jsonify(response)

        else:
          response["menssage"] = "Imagem não existe no servidor"

        return jsonify(response)


def buscaImg(codigo, name):

    query1 = {"_id": codigo, "name": name}

    response = mycol.find_one(query1)

    return response


def compactTransformImg(codigo, name):

    """
        Função para compacta, redimensionar a imagem, tranforma em base64 e salvar no banco de dados.

        :argument:
           codigo, name
        :return:
            Json contendo um array com _id, base64 e name.
    """

    arquivo = properties['diretorioIMG'] + str(name) + "/" + str(codigo) + ".JPG"

    print("Param ~~~~~~~~~>", name, codigo)
    print("Diretorio: ", arquivo)

    basewidth = 400
    img = Image.open(arquivo)
   
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    new_img.save(properties['diretorioIMG'] + name + "/newImg" + str(codigo) + ".JPG", optimize=True)
    new_arquivo = properties['diretorioIMG'] + name + "/newImg" + str(codigo) + ".JPG"

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