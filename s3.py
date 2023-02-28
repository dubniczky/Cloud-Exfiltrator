import boto3

import utils


config = utils.read_config()
s3 = boto3.client('s3')
discovered_buckets = None


def get_buckets():
    response = s3.list_buckets()
    if utils.request_success(response):
        utils.save_json(response, 's3/buckets.json')
        print("Buckets found:", len(response['Buckets']))
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        print("Buckets:", bucket_names)
        return bucket_names
    else:
        print('No permission to list buckets')
        return []


# Auto discover buckets if enabled in config
if config['s3']['discover_buckets']:
    discovered_buckets = get_buckets()
