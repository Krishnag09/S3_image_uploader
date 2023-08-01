from flask import request, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename
import os
import random
import boto3
from flask import Flask

from fileuploader.api.helpers import Helpers
from fileuploader.config import Config


s3_client = boto3.client('s3',
                         aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.AWS_ACCESS_KEY_SECRET)

app = Flask(__name__)

class HelloWorld(Resource):
    def get(self):
        return 'Hello, World! This is the File Uploader API!'


class ImageUpload(Resource):
    def post(self):
        user_ip = request.remote_addr
        rate_limit_key = 'upload:' + user_ip
        if Helpers.is_rate_limited(rate_limit_key, Config.LIMIT, Config.PERIOD):
            return 'Rate limit exceeded', 429
        try:
            file = request.files['file']
            if file:
                randomfileindex = random.randint(1, 100000)
                filename = secure_filename(file.filename)
                processed_filename = str(randomfileindex) + str(filename)
                print (processed_filename)
                if not Helpers.is_valid_image(file):
                    return 'Invalid image', 400
                processed_filepath= os.path.join(Config.UPLOAD_FOLDER, processed_filename)
                file.save(processed_filepath)
                Helpers.increment_rate_limit(rate_limit_key)
                Helpers.s3upload(processed_filepath)
                return 'File processed successfully'
            else:
                return 'No file provided', 400
        except Exception as e:
            return {'error': f"Error uploading file: {str(e)}"}, 500

        

