import boto3

# # Авторизация
# s3 = boto3.client(
#    service_name='s3',
#    endpoint_url='https://storage.yandexcloud.net',
#    aws_access_key_id='YCAJEjb20gvLY9NtOX2XizTGR',
#    region_name = 'ru-central1',
#    aws_secret_access_key='YCPmNOS7t_39fmaRztJJeHgbim42AUFhdKdPO7NB',
# )

# Название бакета
BUCKET_NAME = 'rtf-video-bucket'

ACCESS_KEY = "YCAJEjb20gvLY9NtOX2XizTGR"
REGION_NAME = "ru-central1"
SECRET_ACCESS_KEY = "YCPmNOS7t_39fmaRztJJeHgbim42AUFhdKdPO7NB"

# URL доступа
# URL_ACCESS = f'https://{BUCKET_NAME}.s3.yandexcloud.net/'
URL_ACCESS = f'https://storage.yandexcloud.net/{BUCKET_NAME}/'
ENDPOINT_URL = 'https://storage.yandexcloud.net'