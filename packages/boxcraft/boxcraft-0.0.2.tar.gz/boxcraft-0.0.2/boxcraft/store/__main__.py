import redis
import json
from boxcraft.exceptions import *

class RedisStore:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        try:
            self.connection = redis.Redis(host=host, port=port, db=db, password=password)
            self.connection.get('test_connection')
        except redis.ConnectionError as err:
            raise MissingGenericException

    def get_json(self, key):
        while True:
            try:
                with self.connection.pipeline() as pipe:
                    pipe.watch(key)
                    json_value = pipe.get(key)
                    pipe.reset()
                    return json.loads(json_value) if json_value else None
            except redis.WatchError:
                continue

    def set_json(self, key, value):
        while True:
            try:
                with self.connection.pipeline() as pipe:
                    pipe.watch(key)
                    pipe.multi()
                    pipe.set(key, json.dumps(value))
                    pipe.execute()
                    break
            except redis.WatchError:
                continue