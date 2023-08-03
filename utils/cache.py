import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()


class Cache:
    def __init__(self):
        self.client = redis.Redis(
            host=str(os.getenv("REDIS_HOST")),
            port=int(os.getenv("REDIS_PORT")),
            password=str(os.getenv("REDIS_PASSWORD")),
            db=0
        )

    def get(self, key):
        return json.loads(self.client.get(key))

    def set(self, key, value):
        return self.client.set(key, json.dumps(value))

    def delete(self, key):
        return self.client.delete(key)

    def exists(self, key):
        return self.client.exists(key)

    def keys(self):
        return self.client.keys()
