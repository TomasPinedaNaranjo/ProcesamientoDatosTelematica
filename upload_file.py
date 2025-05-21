import boto3

s3 = boto3.client('s3')
s3.meta.client.upload_file('C:\Users\tomas\OneDrive\Escritorio\Aprendizaje\2025-1\TE Telematica\ProcesamientoDatos\todos_los_productos.txt', 'emurielrdatalake', 'todos_los_productos.txt')