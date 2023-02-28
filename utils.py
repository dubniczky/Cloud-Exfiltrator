import os
import json
import datetime

import yaml


BASE_DATA_DIR = 'data/'
CONFIG_PATH = 'config.yaml'


def request_success(response):
    return response['ResponseMetadata']['HTTPStatusCode'] == 200

def to_json(data):
    return json.dumps(data, indent=2, sort_keys=True, default=str)

def now_str():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

def save_json(obj, filename):
    filename = BASE_DATA_DIR + filename
    # If file exists, back it up
    if os.path.exists(filename):
        os.rename(filename, filename + '.' + now_str())
    # Create directory if it doesn't exist
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    # Write file
    with open(filename, 'w') as f:
        f.write(to_json(obj))

def read_config():
    with open(CONFIG_PATH, 'r', encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
