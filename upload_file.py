import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar cliente S3 con credenciales desde .env
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# Parámetros
bucket_name = 'emurielrdatalake'
file_path = 'todos_los_productos.txt'
s3_key = 'raw/todos_los_productos.txt'  # Ruta en S3

# Subir archivo
def upload_to_s3(file_path, bucket_name, s3_key):
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"Archivo {file_path} subido exitosamente a {bucket_name}/{s3_key}")