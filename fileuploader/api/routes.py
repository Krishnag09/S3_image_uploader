from flask_restful import Api
from .resources.ImageFarm import ImageFarm


def initialize_routes(api):
    api.add_resource(ImageFarm, '/upload')
    api.add_resource(ImageFarm, '/s3upload')
