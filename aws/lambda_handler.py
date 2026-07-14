import json
import boto3
from datetime import datetime

error_bucket_name = 'real-time-scd1-error-bucket'
target_bucket_name = 'real-time-scd1-data-bucket'
s3_client = boto3.client('s3')
kinesis_client = boto3.client('kinesis')

def lambda_handler(event, context):
    try:
        data = json.loads(event['body'])
        print(type(event))
        error_count = 0
        success_count = 0
        error_data = []
        success_data = []

        for record in data:
            print(type(record))
            print(record)
            if 'employee_id' not in record or record['employee_id'] in [None,'']:
                error_count += 1
                error_data.append(record)
            else:
                success_data.append(record)
                success_count += 1
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        
        if error_data:
            object_key = f'error_{timestamp}.json'
            print(f'error_count is {error_count}')
            s3_client.put_object(Bucket=error_bucket_name,Key=object_key,Body=json.dumps(error_data))
        if success_data:
            object_key = f'data_{timestamp}.json'
            print(f'success_count is {success_count}')
            s3_client.put_object(Bucket=target_bucket_name,Key=object_key,Body=json.dumps(success_data))
        response = {
            'statusCode': 200,
            'body': json.dumps({'message':'Data Processing Completed','Sucess records':success_count,'Error_records':error_count})
        }
        print(response)
        return response
    except Exception as e:
        error_response = {'statusCode': 500,
                            'body': json.dumps(f'Error processing event {e}')}
        return error_response
