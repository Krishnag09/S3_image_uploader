import time
import redis
from PIL import Image

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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


        
        
        