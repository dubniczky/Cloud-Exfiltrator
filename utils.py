
def request_success(response):
    return response['ResponseMetadata']['HTTPStatusCode'] == 200