import base64
import os

import pymongo
from PIL import Image
from flask import jsonify

from app.py_image import app

myclient = pymongo.MongoClient(app.config['MONGOADDR'])
mybd = myclient["bd_img"]
mycol = mybd["Imagens"]


def compactImage(name, codigo):
    data = []
    response = {}

    data.append(buscaImg(int(codigo), name))

    if data[0] != None:

        return jsonify(data)

    elif data[0] == None:


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

    path = app.config['DIRETORIO'] + name

    print(path)

    arquivo = app.config['DIRETORIO'] + name + "/" + str(codigo) + ".JPG"

    basewidth = 400
    img = Image.open(arquivo)

    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    new_img.save(app.config['DIRETORIO'] + name + "/newImg" + str(codigo) + ".JPG", optimize=True)
    new_arquivo = app.config['DIRETORIO'] + name + "/newImg" + str(codigo) + ".JPG"

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
