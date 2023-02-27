import boto3
import json

import utils

s3 = boto3.client('s3')

response = s3.list_buckets()
if utils.request_success(response):
    print(response['Buckets'])
else:
    print('No permission to list buckets')
