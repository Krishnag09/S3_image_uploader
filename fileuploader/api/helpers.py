import redis
import boto3
from PIL import Image
from fileuploader.config import Config
from flask import jsonify
from boto3.s3.transfer import TransferConfig

s3_config = TransferConfig(multipart_threshold=Config.S3_UPLOAD_LIMIT, use_threads=Config.S3_USE_THREADS)


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

s3_client = boto3.client('s3',
                         aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.AWS_ACCESS_KEY_SECRET)

class Helpers:
    def __init__(self):
        pass
    def is_valid_image(filename):
        try:
            image = Image.open(filename)
            return image.format.lower() in ALLOWED_IMAGE_EXTENSIONS
        except Exception as e:
            return False
        
    def is_rate_limited(key, limit, period):
        current_count = redis_client.get(key)
        if current_count is None:
            return False
        return int(current_count) >= limit
    
    def increment_rate_limit(key):
        redis_client.incr(key)
        
    def s3upload(filepath):
        file = (filepath, "rb")
        try:
            s3_client.upload_fileobj(file, Config.S3_BUCKET_NAME,
                                        file.filename, CONFIG=s3_config)
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str("Error uploading file: " + str(e))}), 500


        
        
        