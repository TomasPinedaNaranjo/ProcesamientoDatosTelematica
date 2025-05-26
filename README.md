#  Proyecto 3 Tópicos E. Telemática


Asignatura: 
Tópicos especiales en Telemática


Docente: 

Edwin Montoya Munera


Por:
Emanuel Patiño
Esteban Muriel
 Tomás Pineda



Escuela de ciencias e ingeniería
Universidad EAFIT, sede Medellín
2025-1

# Introducción

Este proyecto tiene como propósito implementar una arquitectura batch automatizada para Big Data, que abarque todo el ciclo de vida de los datos: captura desde múltiples fuentes (archivos, APIs y bases de datos), ingesta hacía S3, procesamiento con Spark en clústeres EMR y entrega de resultados para su consulta mediante Athena o API Gateway.
A través de esta solución, se busca simular un entorno real de ingeniería de datos, integrando herramientas en la nube y automatizando cada etapa del proceso, desde la obtención hasta la explotación de los datos. Con ello, se pretende cerrar la brecha entre los ejercicios académicos y los escenarios reales del análisis de datos en entornos empresariales.

# Objetivo general

Implementar una arquitectura batch automatizada para capturar, procesar y analizar datos desde múltiples fuentes, utilizando servicios en la nube orientados a Big Data.

# Objetivos específicos

Automatizar la captura e ingesta de datos desde archivos en línea, APIs y bases de datos relacionales hacia un bucket S3 en la zona Raw.

Diseñar e implementar un flujo ETL automático utilizando Spark sobre un clúster EMR.

Almacenar los datos transformados en la zona Trusted de S3, listos para su análisis.

## Requisitos funcionales
RF1: El sistema debe permitir la descarga automática de archivos desde URLs externas y almacenamiento en la zona Raw de S3.

RF2: El sistema debe consumir datos desde APIs públicas y almacenarlos automáticamente en la zona Raw de S3.

RF3: El sistema debe extraer datos desde una base de datos relacional (MySQL o PostgreSQL) y cargarlos en la zona Raw de S3 de forma automatizada.

RF4: El sistema debe crear automáticamente un clúster EMR en AWS para ejecutar tareas de procesamiento.

RF5: El sistema debe ejecutar procesos ETL con Spark para limpiar, transformar y unir los datos provenientes de distintas fuentes.

RF6: El sistema debe almacenar los resultados procesados en la zona Trusted del bucket S3.

RF7: El sistema debe aplicar análisis descriptivos y/o modelos de machine learning usando SparkML sobre los datos en la zona Trusted.

RF8: El sistema debe guardar los resultados finales del análisis en la zona Refined de S3.

RF9: El sistema debe exponer los resultados mediante consultas en Amazon Athena y vía una API REST usando API Gateway.


## Requisitos no funcionales

RNF1: Todos los procesos del flujo de datos (ingesta, procesamiento, análisis y consulta) deben ejecutarse de forma automática sin intervención humana.

RNF2: El sistema debe ser escalable y soportar incrementos en el volumen de datos sin necesidad de rediseñar la arquitectura.

RNF3: El sistema debe estar desarrollado sobre servicios en la nube con alta disponibilidad, priorizando el uso de AWS, GCP o Azure según la viabilidad técnica.


# Ingesta de datos

La ingesta de datos es el proceso mediante el cual se recolectan y trasladan datos desde múltiples fuentes hacia un sistema centralizado para su almacenamiento y posterior análisis. En el contexto de la telemática y la nube (como AWS), este proceso permite capturar información en tiempo real desde sensores, dispositivos IoT o bases de datos, y enviarla a servicios como Amazon S3 para posteriormente continuar con el ciclo de vida. El proceso para lograr esto fue:

![Captura de pantalla (178)](https://github.com/user-attachments/assets/f9dc5d69-dd8a-4ea8-8c64-46438c94093a)

### 1. Extraer datos de la API

Uso de un bot automatizado: Implementar una clase (FakeStoreBot) que gestione las solicitudes HTTP a la API y facilite la extracción de datos.
Manejo de errores: Validar las respuestas de la API y gestionar adecuadamente los posibles errores o códigos de estado inesperados.
Flexibilidad en la extracción: Permitir la obtención de todos los productos, productos por categoría o por ID, según las necesidades del proceso.

Para lograr esto hacemos uso del método get_all_products() de la clase FakeStoreBot para realizar una solicitud HTTP a la API y obtener todos los productos en formato JSON.

### 2. Guardar datos

Formato estructurado: Almacenar los datos extraídos en archivos de texto con formato JSON para facilitar su posterior procesamiento.
Nombres de archivo claros: Utilizar nombres de archivo descriptivos y, si es necesario, incluir marcas de tiempo para identificar diferentes lotes de datos.
Para lograr está tarea tenemos el método save_to_file(data, filename) de la clase FakeStoreBot para guardar los datos extraídos en un archivo de texto con formato JSON y codificación UTF-8.

### 3. Montar datos a S3

Automatización del proceso: Implementar scripts o funciones que suban automáticamente los archivos generados a un bucket de S3.

Gestión de credenciales: Utilizar variables de entorno y buenas prácticas de seguridad para manejar las credenciales de AWS.

Control de versiones y organización: Definir rutas y carpetas en S3 para organizar los archivos subidos y facilitar su acceso y gestión futura.

Como último objetivo de este fragmento hacemos uso de la función upload_to_s3(file_path, bucket_name, s3_key) definida en upload_file.py para subir el archivo generado a un bucket de S3, utilizando credenciales seguras cargadas desde variables de entorno.

Para montar este proceso crearemos una máquina EC2 donde montaremos nuestro proyecto para que el bot se pueda ejecutar eventualmente en la hora establecida periódicamente y asi obtener los dato actualizados para todo el proceso que estamos realizando.

# 1. Creación de la Instancia EC2

1.1 Configuración Básica
Ingresar a AWS Console y navegar al servicio EC2
Lanzar Nueva Instancia:
Nombre: procesamiento-datos-telematica (o el nombre que prefieras)
AMI: Ubuntu Server 22.04 LTS (Free tier eligible)
Tipo de Instancia: t2.micro (Free tier) o t3.small según necesidades
Key Pair: Crear nueva o usar existente para acceso SSH
1.2 Configuración de Seguridad
Security Group:
Permitir SSH (puerto 22) desde tu IP
Opcional: HTTP (80) y HTTPS (443)

# 2. Nos conectamos a la máquina y ejecutamos
   
#Actualizar paquetes del sistema 

sudo apt update && sudo apt upgrade -y

#Instalar pip si no está disponible

sudo apt install -y python3-pip 

sudo apt install -y git

### 3. Clonar repositorio

git clone https://github.com/TomasPinedaNaranjo/ProcesamientoDatosTelematica.git

#Navegar al directorio del proyecto 

cd ProcesamientoDatosTelematica

### 4. Entorno Virtual 

#Crear entorno virtual 
python3 -m venv venv 
#Activar entorno virtual
 source venv/bin/activate

### 5. Instalar dependencias

pip install -r requirements.txt

#Instalar AWS CLI 

sudo apt install -y awscli

### 6. Configurar credenciales AWS

En este paso es clave la extracción de las credenciales correspondientes para poder ejecutar la tarea del bot. En un entorno normal obtendremos las credenciales usando el servicio IAM para crear un usuario y darle un rol específico con la posibilidad de montar datos a S3, dado que estamos en una cuenta de Academia no tenemos la posibilidad de lograr esto por ende obtenemos las credenciales temporales de nuestro laboratorio, al correr este hacemos 

cat ~/.aws/credentials

Copiamos las credenciales y las pegamos en nuestro .env usando 

nano .venv

Hacer un cron para ejecutar periódicamente el bot

Para lograr esta tarea realizaremos los siguientes pasos

Creamos un script ya cuando estemos en nuestra máquina EC2

nano run_daily_task.sh

Agregamos este contenido:

#!/bin/bash

#Activar el entorno virtual

source /home/ubuntu/ProcesamientoDatosTelematica/venv/bin/activate

#Directorio del proyecto

cd /home/ubuntu/ProcesamientoDatosTelematica

#Crear directorio de logs si no existe
mkdir -p logs

#Ejecutar el script Python con logging
echo "$(date): Iniciando tarea cada 5 minutos" >> logs/task.log
python3 main.py >> logs/task.log 2>&1
echo "$(date): Tarea completada" >> logs/task.log
echo "----------------------------------------" >> logs/task.log

Le damos permisos de ejecución

chmod +x run_daily_task.sh

Para probar el script manualmente

./run_daily_task.sh

cat logs/task.log

Usamos cron para automatizar el proceso en el periodo que lo deseemos

crontab -e

Agregamos: 

*/5 * * * * /home/ubuntu/ProcesamientoDatosTelematica/run_daily_task.sh

Finalmente verificamos la configuración:

crontab -l

sudo systemctl status cron

