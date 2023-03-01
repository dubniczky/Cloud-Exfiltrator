import os
import boto3

import utils


config = utils.read_config()
s3 = boto3.client('s3')
object_size_limit = config['s3']['size_limit']


def get_buckets():
    response = s3.list_buckets()
    if utils.request_success(response):
        utils.save_json(response, 's3/buckets.json')
        print("Buckets found:", len(response['Buckets']))
        bucket_names = [bucket['Name'] for bucket in response['Buckets']]
        print("Buckets:", bucket_names)
        return bucket_names
    
    print('No permission to list buckets')
    return []
    
def bucket_details(bucket):
    return s3.get_bucket_acl(Bucket=bucket)

def list_all_objects(bucket_name):
    # This sends requests until all objects are returned, because only 1000 can be listed at once
    response = s3.list_objects_v2(Bucket=bucket_name)
    if not utils.request_success(response):
        print(f'No permission to list objects in bucket {bucket_name}')
        return []
    objects = response['Contents']
    
    while response['IsTruncated']:
        response = s3.list_objects_v2(
            Bucket=bucket_name,
            ContinuationToken=response['NextContinuationToken']
        )
        print(objects)
        objects += response['Contents']
        
    return objects

def save_objects(bucket, objects):
    print(f'Saving {len(objects)} objects from bucket {bucket}')
    for o in objects:
        key = o['Key']
        if object_size_limit and object_size_limit != 0 and o['Size'] > object_size_limit:
            continue
        path = utils.datapath(f's3/objects/{bucket}/{key}')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        print(f'Downloading s3://{bucket}/{key} -> {path}')
        s3.download_file(bucket, key, path)

def main():
    # Auto discover buckets if enabled in config
    buckets = config['s3']['include']
    if config['s3']['discover']:
        buckets += get_buckets()
    for b in config['s3']['exclude']:
        buckets.remove(b)
        
    # Get details and list of objects for each bucket
    objects = {}
    for bucket in buckets:
        response = bucket_details(bucket)
        if utils.request_success(response):
            utils.save_json(response, f's3/{bucket}.details.json')
        else:
            print(f'No permission to get details for bucket {bucket}')
            
        objects[bucket] = list_all_objects(bucket)
        utils.save_json(objects[bucket], f's3/object_lists/{bucket}.objects.json')
        print(f'Found {len(objects[bucket])} objects in bucket {bucket}')
        
    # Save all objects
    os.makedirs(utils.datapath('s3/objects'), exist_ok=True)
    for b in buckets:
        save_objects(b, objects[b])
            
        

if __name__ == '__main__':
    main()
