import boto3
import logging
from botocore.exceptions import ClientError
import os

class S3Uploader:
    """
    Clase para gestionar la subida de archivos a Amazon S3.
    """
    
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, region_name='us-east-1'):
        """
        Inicializa el cliente S3 con las credenciales proporcionadas o del entorno.
        
        Args:
            aws_access_key_id (str, opcional): Clave de acceso de AWS.
            aws_secret_access_key (str, opcional): Clave secreta de AWS.
            region_name (str, opcional): Región de AWS. Por defecto 'us-east-1'.
        """
        # Si no se proporcionan credenciales, boto3 buscará en las variables de entorno
        # o en ~/.aws/credentials
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        
        # Configuración de logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def upload_file(self, file_path, bucket_name, object_name=None):
        """
        Sube un archivo a un bucket de S3.
        
        Args:
            file_path (str): Ruta al archivo local que se va a subir.
            bucket_name (str): Nombre del bucket de S3.
            object_name (str, opcional): Nombre del objeto S3 (ruta dentro del bucket).
                                         Si no se especifica, se usará el nombre del archivo.
                                        
        Returns:
            bool: True si la subida es exitosa, False en caso contrario.
        """
        # Si no se proporciona object_name, usar el nombre base del archivo
        if object_name is None:
            object_name = os.path.basename(file_path)
            
        try:
            self.logger.info(f"Intentando subir {file_path} a {bucket_name}/{object_name}")
            self.s3_client.upload_file(file_path, bucket_name, object_name)
            self.logger.info(f"Archivo subido exitosamente a {bucket_name}/{object_name}")
            return True
        except ClientError as e:
            self.logger.error(f"Error al subir archivo a S3: {e}")
            return False
    
    def create_bucket(self, bucket_name, region=None):
        """
        Crea un nuevo bucket de S3 si no existe.
        
        Args:
            bucket_name (str): Nombre del bucket a crear.
            region (str, opcional): Región donde crear el bucket.
                                    Si es None, se usará la región configurada en el cliente.
                                    
        Returns:
            bool: True si el bucket fue creado o ya existe, False en caso de error.
        """
        try:
            if region is None:
                # Crear bucket en la región actual del cliente
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                # Para regiones distintas a us-east-1, se necesita una configuración especial
                if region == 'us-east-1':
                    self.s3_client.create_bucket(Bucket=bucket_name)
                else:
                    location = {'LocationConstraint': region}
                    self.s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration=location
                    )
            self.logger.info(f"Bucket '{bucket_name}' creado o ya existente.")
            return True
        except ClientError as e:
            self.logger.error(f"Error al crear bucket: {e}")
            return False
    
    def list_buckets(self):
        """
        Lista todos los buckets disponibles en la cuenta.
        
        Returns:
            list: Lista de nombres de buckets o None en caso de error.
        """
        try:
            response = self.s3_client.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            self.logger.info(f"Buckets disponibles: {buckets}")
            return buckets
        except ClientError as e:
            self.logger.error(f"Error al listar buckets: {e}")
            return None
    
    def list_objects(self, bucket_name, prefix=''):
        """
        Lista objetos en un bucket con un prefijo opcional.
        
        Args:
            bucket_name (str): Nombre del bucket.
            prefix (str, opcional): Prefijo para filtrar objetos.
            
        Returns:
            list: Lista de nombres de objetos o None en caso de error.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            
            if 'Contents' in response:
                objects = [obj['Key'] for obj in response['Contents']]
                self.logger.info(f"Objetos en {bucket_name}/{prefix}: {objects}")
                return objects
            else:
                self.logger.info(f"No se encontraron objetos en {bucket_name}/{prefix}")
                return []
        except ClientError as e:
            self.logger.error(f"Error al listar objetos: {e}")
            return None