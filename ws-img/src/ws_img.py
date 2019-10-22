from flask import Flask, jsonify, request
from flask_cors import CORS
import base64
import pymongo
import requests
import os
import json
import sys
from PIL import Image

application = Flask(__name__)
CORS(application)

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


def buscaImg(cod_fornecedor: str, cod_produto: str):
    query = {"CodFornecedor": "{}".format(cod_fornecedor),
             "CodProduto": "{}".format(cod_produto)}
    return pdt_col.find_one(query, {'_id': 0})


def groupImgMatriz():
    """
            Função para compacta, redimensionar a imagem, tranforma em base64 e salvar no banco de dados.

            :argument:
                Array:
                        {
                            "CodFornecedor" : "111111",
                            "CodProduto" : "222222"
                        }
            :return:
                eson contendo um array com codFornecedor, codProduto e ImgBase64, imagem compactada em base64.
    """

    response = []
    existe = 0

    for req in request.json:
        mydoc = buscaImg(req["CodFornecedor"], req["CodProduto"])

        if mydoc:
            response.append(mydoc)
            existe += 1

    if existe == len(request.json):
        print("TODAS IMAGENS EXISTEM NO BANCO")
        return jsonify(response)

    elif existe < len(request.json) or existe == 0:
        print("NOVA IMAGEM, COMPACTAR & TRASFORMA EM BASE64")
        try:
            arquivo = properties['diretorio'] + req["CodFornecedor"] + "/" + req["CodProduto"] + ".JPG"
            basewidth = 400
            img = Image.open(arquivo)
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            new_img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            new_img.save(properties['diretorio'] + req["CodFornecedor"] + "/newImg" + req["CodProduto"] + ".JPG", optimize=True)

        except FileNotFoundError:

            print("UMA DAS IMAGEM NAO EXISTEM, DEVOLVER APENAS AS EXISTENTES")
            newResponse = []

            for req in request.json:
                mydoc = buscaImg(req["CodFornecedor"], req["CodProduto"])

                if mydoc:
                    newResponse.append(mydoc)

            return jsonify(newResponse)

        new_arquivo = properties['diretorio'] + req["CodFornecedor"] + "/newImg" + req["CodProduto"] + ".JPG"

        f = open(new_arquivo, 'rb')
        imgCompact = f.read()
        f.close()

        encodedImg = base64.b64encode(imgCompact)

        documento = {"CodFornecedor": req["CodFornecedor"], "CodProduto": req["CodProduto"],
                     "ImgBase64": "{}".format(encodedImg).replace("b'", "").replace("'", "")}
        x = pdt_col.insert_one(documento)

        os.remove(new_arquivo)

    newResponse = []

    for req in request.json:
        mydoc = buscaImg(req['CodFornecedor'], req['CodProduto'])

        if mydoc:
            newResponse.append(mydoc)

    return jsonify(newResponse)


def listarMatriz():
    """
        Função para consulta no banco de dados, de uma imagem especifica.

        :argument:
            codFornecedor: string
            codProduto: string
        :return:
            json contendo o codFornecedor, codProduto e ImgBase64.
    """

    codFornecedor = request.args.get('codFornecedor')
    codProduto = request.args.get('codProduto')

    response = {}
    value = []

    mydoc = buscaImg(codFornecedor, codProduto)

    if mydoc:
        value.append(mydoc)
        response = value
        return jsonify(response)
    response["menssage"] = "sem registro"
    return jsonify(response)


def groupImgFilial():
    """
            Função para consulta no banco de dados, de uma imagem especifica, se não achar ele faz uma requisição para o serviço da matriz.

            :argument:
                Array:
                        [{
                            "CodFornecedor" : "111111",
                            "CodProduto" : "222222"
                        }]
            :return:
                json contendo o codFornecedor, codProduto e ImgBase64.
    """

    response = []
    existe = 0
    searchmatriz = []

    for req in request.json:
        mydoc = buscaImg(req['CodFornecedor'], req['CodProduto'])

        if mydoc:
            existe += 1
            response.append(mydoc)
        else:
            searchmatriz.append(req)

    if existe == len(request.json):
        print("TODAS IMAGENS EXISTEM NO BANCO DA FILIAL")
        return jsonify(response)

    elif existe < len(request.json) or existe == 0:
        print("FAZENDO REQUISIÇÃO PARA MATRIZ")

        resposta = []
        resp = requests.post(properties['matrizUrl'] + '/imageGroup', data=None, json=searchmatriz)

        for resp in resp.json():
            pdt_col.insert_one(resp)

        for req in request.json:
            mydoc = buscaImg(req['CodFornecedor'], req['CodProduto'])

            if mydoc:
                resposta.append(mydoc)

        return jsonify(resposta)


def listarFilial():
    """
        Função para consulta no banco de dados, de uma imagem especifica.

        :argument:
            codFornecedor: string
            codProduto: string
        :return:
            json contendo o codFornecedor, codProduto e ImgBase64.
    """

    codFornecedor = request.args.get('codFornecedor')
    codProduto = request.args.get('codProduto')

    response = {}
    value = []

    mydoc = buscaImg(codFornecedor, codProduto)

    if mydoc:
        value.append(mydoc)
        response = value
        return jsonify(response)
    response["menssage"] = "sem registro"
    return jsonify(response)


searchGroup = searchImg = None
if os.environ['PROFILE'] == 'matriz':
    searchGroup = groupImgMatriz
    searchImg = listarMatriz
else:
    searchGroup = groupImgFilial
    searchImg = listarFilial


@application.route("/imageGroup", methods=['GET', 'POST'])
def searchGroupRoute():
    """
                Função para indetificar a variavel de ambiente e determina as suas rotas.

                :argument:
                    PROFILE
                :return:
                    a resposta das funções.
    """
    return searchGroup()


@application.route("/searchImg", methods=['GET'])
def searchImgRoute():
    return searchImg()
