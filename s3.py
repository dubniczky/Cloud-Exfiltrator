import boto3

import utils


config = utils.read_config()
s3 = boto3.client('s3')


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

def main():
    # Auto discover buckets if enabled in config
    buckets = config['s3']['include']
    if config['s3']['discover']:
        buckets += get_buckets()
    for b in config['s3']['exclude']:
        buckets.remove(b)
        
    for bucket in buckets:
        response = bucket_details(bucket)
        if utils.request_success(response):
            utils.save_json(response, f's3/{bucket}.details.json')
        else:
            print(f'No permission to get details for bucket {bucket}')
            
        objects = list_all_objects(bucket)
        utils.save_json(objects, f's3/object_lists/{bucket}.objects.json')
        print(f'Found {len(objects)} objects in bucket {bucket}')
        

if __name__ == '__main__':
    main()
