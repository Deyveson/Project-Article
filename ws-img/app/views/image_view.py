from flask import send_file
from flask_restplus import Resource

from app.py_image import app, ns, api
from app.services import imageService


@ns.route('/version')
class Version(Resource):
    def get(self):
        """
            Version project.
        """
        return api.version


@ns.route('/get_image/<id>')
class ImageDefault(Resource):

    def get(self, id):
        if id == '1':
            filename = app.config['DIRETORIO']+'ok.jpg'
        else:
            filename = app.config['DIRETORIO']+'error.jpg'
        return send_file(filename, mimetype='image/jpg')


@ns.route('/findImage/<name>/<codigo>')
class Compact(Resource):
    def get(self, name, codigo):

        response = imageService.compactImage(name, codigo)

        return response
