import boto3
from pathlib import Path
from botocore.exceptions import ClientError

client = boto3.client('lambda')
iam = boto3.client('iam')

def convert_to_bytes(zip_file):
    with open(zip_file, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content


def create_function(aws_name, aws_role, handler, archive):
    try:
        client.create_function(
            FunctionName=aws_name,
            Runtime='python3.8',
            Role=aws_role,
            Handler=f'{Path(archive).stem}.{handler}',
            Code={
                'ZipFile': convert_to_bytes(archive)
            },
        )
        print(f'function {aws_name} has been created')
    except ClientError as e:
        print(e)


if __name__ == '__main__':
    create_function('devops-image-processor', 'arn:aws:iam::560714147739:role/LabRole',
                    'lambda_handler', './devops-image-processor.zip')
