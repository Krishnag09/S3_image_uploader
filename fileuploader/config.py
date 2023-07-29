import json
with open('fileuploader/config.json') as config_file:
    config = json.load(config_file)

class Config:
    UPLOAD_FOLDER = config.get('UPLOAD_FOLDER')
    AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID')
    AWS_ACCESS_KEY_SECRET = config.get('AWS_ACCESS_KEY_SECRET')
    S3_BUCKET_NAME = config.get('S3_BUCKET_NAME')
    PERIOD = config.get('PERIOD')
    LIMIT = config.get('LIMIT')
