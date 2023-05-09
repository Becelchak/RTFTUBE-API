import boto3

# # Авторизация
s3 = boto3.client(
   service_name='s3',
   endpoint_url='https://storage.yandexcloud.net',
   aws_access_key_id='YCAJEjb20gvLY9NtOX2XizTGR',
   region_name = 'us-east-1',
   aws_secret_access_key='YCPmNOS7t_39fmaRztJJeHgbim42AUFhdKdPO7NB',
)

# Название бакета
BUCKET_NAME = 'rtf-video-bucket'