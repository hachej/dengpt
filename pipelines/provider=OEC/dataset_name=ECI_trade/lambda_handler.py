import os
import hashlib
import json
import boto3
import requests
from datetime import datetime

def lambda_handler(event, context):
    endpoint = os.environ['OEC_ECI_trade_ENDPOINT']
    response = requests.get(endpoint)
    data = response.content

    md5_hash = hashlib.md5(data).hexdigest()
    request_day = datetime.utcnow().strftime('%Y-%m-%d')
    file_path = f"data_profile=raw/provider_name=OEC/dataset_name=ECI_trade/request_time={request_day}/{md5_hash}.json"

    s3 = boto3.client('s3')
    s3.put_object(
        Bucket='sumeo-OEC',
        Key=file_path,
        Body=data,
        Metadata={
            'RequestTime': request_day,
            'Provider': 'OEC',
            'DatasetName': 'ECI_trade'
        }
    )

    return {
        'statusCode': 200
    }