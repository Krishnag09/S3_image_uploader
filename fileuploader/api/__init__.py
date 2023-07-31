from flask import Blueprint
from flask_restful import Api

from .resources import HelloWorld, ImageUpload

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(HelloWorld, '/hello')
api.add_resource(ImageUpload, '/upload')
