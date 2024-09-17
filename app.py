from flask import Flask, abort, make_response, jsonify
from dotenv import load_dotenv, dotenv_values
from flask_cors import CORS
import copy
import json
import os
import redis
import requests

app = Flask(__name__)

load_dotenv()
REDIS_HOST = os.environ.get('REDIS_HOST') or dotenv_values()['REDIS_HOST']
REDIS_PORT = os.environ.get('REDIS_PORT') or dotenv_values()['REDIS_PORT']
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or dotenv_values()['REDIS_PASSWORD']

redis_instance = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

app.config['CORS_HEADERS'] = 'Content-Type' # TODO: Only enable for local development
CORS(app, resources=r'/*', supports_credentials=True) # TODO: Only enable for local development

AIVEN_CLOUDS_API_URL = 'https://api.aiven.io/v1/clouds'

@app.route("/ping")
def ping():
    return "pong"

@app.route("/api/clouds")
def clouds():
    cached_response = redis_instance.get(AIVEN_CLOUDS_API_URL)
    if cached_response:
        app.logger.debug(f'Found cached {AIVEN_CLOUDS_API_URL} response in Redis')
        return json.loads(cached_response)

    response = requests.get(AIVEN_CLOUDS_API_URL)
    if response.status_code != requests.codes.ok:
        abort(make_response(jsonify(message=response.status_code), response.status_code))

    response_body = response.json()
    extended_response_body = {
        'clouds': list(
            map(
                lambda cloud: extend_cloud_item(cloud),
                response_body['clouds']
            )
        )
    }
    # Cache the response for 1 minute
    redis_instance.set(AIVEN_CLOUDS_API_URL, json.dumps(extended_response_body))
    redis_instance.expire(AIVEN_CLOUDS_API_URL, 60)
    app.logger.debug(f'Cached {AIVEN_CLOUDS_API_URL} response to Redis')

    return extended_response_body

def parse_cloud_provider_from_cloud_name(cloud_name):
    return cloud_name.split('-')[0]

def extend_cloud_item(cloud):
    extended_cloud = copy.deepcopy(cloud)
    extended_cloud['cloud_provider'] = parse_cloud_provider_from_cloud_name(cloud['cloud_name'])
    return extended_cloud
