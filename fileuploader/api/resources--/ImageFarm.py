import os
import boto3
import random
from flask import Flask, request, jsonify
from flask_restful import Resource
from werkzeug.utils import secure_filename
from fileuploader.config import Config
from fileuploader.helpers import Helpers
import redis
from flask import Blueprint

image_farm = Blueprint('image_farm', __name__)

AWS_ACCESS_KEY_ID = Config.AWS_ACCESS_KEY_ID
AWS_ACCESS_KEY_SECRET = Config.AWS_ACCESS_KEY_SECRET
S3_BUCKET_NAME = Config.S3_BUCKET_NAME
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_ACCESS_KEY_SECRET)

class ImageFarm(Resource):
    def get(self):
        return 'Hello World'

    def post(self):
        period = Config.PERIOD
        limit = Config.LIMIT
        user_ip = request.remote_addr
        rate_limit_key = 'upload:' + user_ip
        if Helpers.is_rate_limited(rate_limit_key, limit, period):
            return 'Rate limit exceeded', 429
        try:
          file = request.files['file']
          if file:
                randomfileindex = random.randint(1, 100000)
                filename = secure_filename(file.filename)
                if not Helpers.is_valid_image(filename):
                    return 'Invalid image', 400
                file.save(os.path.join(Config.UPLOAD_FOLDER, str(randomfileindex) + filename))
                Helpers.increment_rate_limit(rate_limit_key)
                return 'File uploaded successfully'
          else:
                return 'No file provided', 400
        except Exception as e:
            return jsonify({'error': str("Error uploading file: " + str(e))}), 500

    def s3upload(filename):
        max_upload_speed = 40  # configurable max upload speed in mbps
        s3_client.meta.client.meta.events.register(
            'choose-signer.s3.PutObject', boto3.s3.transfer.create_transfer_speed_calculator(max_speed=max_upload_speed*1024))
        file = open("uploads/filename", "rb")
        try:
            s3_client.upload_fileobj(file, S3_BUCKET_NAME,
                                     file.filename, ExtraArgs={'ACL': 'public-read'})
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str("Error uploading file: " + str(e))}), 500
