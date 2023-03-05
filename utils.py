import os
import json
import datetime

import yaml


BASE_DATA_DIR = 'data/'
CONFIG_PATH = 'config.yaml'


def request_success(response):
    '''Check if a boto3 request was successful'''
    return response['ResponseMetadata']['HTTPStatusCode'] == 200

def to_json(data):
    '''Convert object to human readable json'''
    return json.dumps(data, indent=2, sort_keys=True, default=str)

def now_str():
    '''Get current date and time as string in format YYYY-MM-DDTHH-MM-SS'''
    return datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

def datapath(filename):
    '''Append filename to extracted data directory'''
    return BASE_DATA_DIR + filename

def msec(ms):
    '''Convert millisecond int to second float'''
    return float(int(ms / 1000))

def save_json(obj, filename):
    '''Save object as json file, also manage backups'''
    filename = BASE_DATA_DIR + filename
    # If file exists, back it up
    if os.path.exists(filename):
        os.rename(filename, filename + '.' + now_str())
    # Create directory if it doesn't exist
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    # Write file
    with open(filename, 'w', encoding='utf8') as f:
        f.write(to_json(obj))
    print(f'Saved json: {filename}')

def read_config():
    '''Read config.yaml file'''
    with open(CONFIG_PATH, 'r', encoding='utf8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
