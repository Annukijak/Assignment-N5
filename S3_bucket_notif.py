import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
client = boto3.client('lambda')

def add_permision(aws_name, bucket_name):
    client.add_permission(
        FunctionName=aws_name,
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket_name}',
    )


def s3_trigger(bucket_name, aws_name):
    try:
        add_permision(aws_name, bucket_name)
        s3.put_bucket_notification_configuration(
            Bucket=bucket_name,
            NotificationConfiguration={
            'LambdaFunctionConfigurations':[{
            'LambdaFunctionArn': client.get_function(
                FunctionName=aws_name)['Configuration']['FunctionArn'],
            'Events': [
                's3:ObjectCreated:*'
            ],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': '.jpeg'
                        },
                    ]
                }
            }
            }],
            }
        )
        print(f'{aws_name} has been added to {bucket_name}')
    except ClientError as e:
        print(e)


if __name__ == '__main__':
    s3_trigger('devops-image-storage',
               'devops-image-processor',
               )