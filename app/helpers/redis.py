import json
from redis import Redis
from flask import current_app

def delete_multiple(keys):
    keys = tuple(keys)
    redis_host = current_app.config.get("REDIS_HOST")
    redis_port = current_app.config.get("REDIS_PORT")
    redis_db = current_app.config.get("REDIS_DB")
    r = Redis(host=redis_host, port=redis_port, db=redis_db)
    r.delete(*keys)