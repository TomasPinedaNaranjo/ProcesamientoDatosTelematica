# Fake Store API Bot con AWS S3

Este proyecto consiste en un bot que consume datos de la Fake Store API y los sube automáticamente a Amazon S3.

## Estructura del Proyecto

- **fake_store_bot.py**: Clase principal para consumir la API de Fake Store.
- **s3_uploader.py**: Clase para gestionar la subida de archivos a Amazon S3.
- **main.py**: Script principal que utiliza las clases anteriores para obtener datos y subirlos a S3.

## Requisitos previos

1. Python 3.6 o superior
2. Paquetes de Python:
   - requests
   - boto3

## Instalación

1. Clone este repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd fake-store-s3-bot
```

2. Instale las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de AWS

Hay dos formas de proporcionar credenciales de AWS:

1. **A través de argumentos de línea de comandos**:
   ```bash
   python main.py --aws-key=YOUR_ACCESS_KEY --aws-secret=YOUR_SECRET_KEY --bucket=YOUR_BUCKET_NAME
   ```

2. **A través de configuración de AWS**:
   - Configure sus credenciales de AWS usando `aws configure` o
   - Configure las variables de entorno `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`

## Uso

Para ejecutar el bot y subir datos a S3:

```bash
python main.py --bucket=nombre-de-tu-bucket
```

### Parámetros disponibles:

- `--aws-key`: AWS Access Key ID (opcional si está configurado en el entorno)
- `--aws-secret`: AWS Secret Access Key (opcional si está configurado en el entorno)
- `--region`: Región de AWS (por defecto: us-east-1)
- `--bucket`: Nombre del bucket S3 (requerido)
- `--prefix`: Prefijo de ruta en S3 (por defecto: fakestore/)

## Flujo de ejecución

1. El bot obtiene todos los productos disponibles en Fake Store API
2. Consulta las categorías de productos
3. Obtiene productos para cada categoría
4. Guarda todos los datos en archivos de texto en el directorio `temp_data/`
5. Sube todos los archivos a Amazon S3 en carpetas organizadas por fecha/hora

## Ejemplo de uso

```bash
# Con credenciales en línea de comandos
python main.py --aws-key=AKIAXXXXXXXX --aws-secret=xxxxxxx --bucket=my-fake-store-data

# Con credenciales en entorno o perfil AWS
python main.py --bucket=my-fake-store-data --prefix=datos/tienda/
```

## Estructura de archivos en S3

Los archivos se organizan en S3 de la siguiente manera:

```
{prefix}/{timestamp}/todos_los_productos.txt
{prefix}/{timestamp}/categorias.txt
{prefix}/{timestamp}/productos_{categoria}.txt
...
```

Donde:
- `{prefix}` es el prefijo proporcionado (por defecto: "fakestore/")
- `{timestamp}` es la fecha y hora de ejecución en formato "YYYYMMDD_HHMMSS"