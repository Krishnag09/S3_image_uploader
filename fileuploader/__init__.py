import os
import boto3
import random
from flask import Flask, request,jsonify
from werkzeug.utils import secure_filename
import redis
from fileuploader.config import Config
from flask_restful import Api
from fileuploader.helpers import Helpers
import asyncio
import aiohttp

AWS_ACCESS_KEY_ID = Config.AWS_ACCESS_KEY_ID
AWS_ACCESS_KEY_SECRET = Config.AWS_ACCESS_KEY_SECRET
S3_BUCKET_NAME = Config.S3_BUCKET_NAME
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


s3_client = boto3.client('s3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_ACCESS_KEY_SECRET)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # from fileuploader.api.routes import api, back
    # app.register_blueprint(back)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    
   # 20% of 200= 40mbps divided by 250 kb image size = 160*60 = 9600 images per min / 60 = 160 images per sec
    
    @app.route('/upload', methods=['POST'])
    def upload():
        user_ip = request.remote_addr
        rate_limit_key = 'upload:' + user_ip
        if Helpers.is_rate_limited(rate_limit_key, Config.LIMIT, Config.PERIOD):
            return 'Rate limit exceeded', 429
        try:
          file = request.files['file']
          if file:
                randomfileindex = random.randint(1, 100000)
                filename = secure_filename(file.filename)
                if not Helpers.is_valid_image(file):
                    return 'Invalid image', 400
                file.save(os.path.join(Config.UPLOAD_FOLDER, str(randomfileindex) + filename))
                Helpers.increment_rate_limit(rate_limit_key)
                # s3upload(filename)
                
                # loop = asyncio.new_event_loop()
                # asyncio.set_event_loop(loop)
                # task = s3upload(filename)
                # image_upload_response = loop.run_until_complete(task)
                # loop.close()
                return 'File uploaded successfully'
          else:
                return 'No file provided', 400
        except Exception as e:
            return jsonify({'error': str("Error uploading file: " + str(e))}), 500
            
    # def s3upload(filename):
    #     max_upload_speed= 40 #configurable max upload speed in mbps
    #     file = open("uploads/filename", "rb")
    #     try:
    #         s3_client.upload_fileobj(file, S3_BUCKET_NAME,
    #                              file.filename, ExtraArgs={'ACL': 'public-read'})
    #         return jsonify({'message': 'File uploaded successfully'}), 200
    #     except Exception as e:
    #         return jsonify({'error': str("Error uploading file: " + str(e))}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
