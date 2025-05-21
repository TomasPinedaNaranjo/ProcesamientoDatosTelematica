from fake_store_bot import FakeStoreBot
from s3_uploader import S3Uploader
import os
import argparse
import time

def parse_arguments():
    """Procesa los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description='Fake Store API Bot con subida a S3')
    
    parser.add_argument('--aws-key', dest='aws_key', help='AWS Access Key ID')
    parser.add_argument('--aws-secret', dest='aws_secret', help='AWS Secret Access Key')
    parser.add_argument('--region', dest='region', default='us-east-1', help='AWS Region')
    parser.add_argument('--bucket', dest='bucket_name', required=True, help='Nombre del bucket S3')
    parser.add_argument('--prefix', dest='prefix', default='fakestore/', 
                        help='Prefijo de ruta en S3 (por defecto: fakestore/)')
    
    return parser.parse_args()

def main():
    """Función principal para demostrar el uso del bot y subir datos a S3."""
    # Obtener argumentos
    args = parse_arguments()
    
    # Inicializar bot de FakeStore
    print("Inicializando bot de Fake Store API...")
    bot = FakeStoreBot()
    
    # Crear directorio temporal para archivos si no existe
    temp_dir = "temp_data"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    created_files = []  # Lista para almacenar las rutas de los archivos creados
    
    # Obtener todos los productos
    print("Obteniendo todos los productos...")
    all_products = bot.get_all_products()
    
    if all_products:
        # Guardar todos los productos en un archivo
        products_file = os.path.join(temp_dir, "todos_los_productos.txt")
        bot.save_to_file(all_products, products_file)
        created_files.append(products_file)
        
        # Mostrar cuántos productos se obtuvieron
        print(f"Se obtuvieron {len(all_products)} productos en total")
        
        # Mostrar los nombres de los primeros 5 productos (o menos si hay menos de 5)
        print("\nPrimeros productos obtenidos:")
        for i, product in enumerate(all_products[:5]):
            print(f"{i+1}. {product['title']} - ${product['price']}")
    
    # Obtener categorías
    print("\nObteniendo categorías...")
    categories = bot.get_all_categories()
    
    if categories:
        # Guardar las categorías en un archivo
        categories_file = os.path.join(temp_dir, "categorias.txt")
        bot.save_to_file(categories, categories_file)
        created_files.append(categories_file)
        
        print("Categorías disponibles:")
        for i, category in enumerate(categories):
            print(f"{i+1}. {category}")
        
        # Obtener y guardar productos por categoría
        for category in categories:
            print(f"\nObteniendo productos de la categoría '{category}'...")
            category_products = bot.get_products_by_category(category)
            
            if category_products:
                category_file = os.path.join(temp_dir, f"productos_{category.replace(' ', '_')}.txt")
                bot.save_to_file(category_products, category_file)
                created_files.append(category_file)
                print(f"Se obtuvieron {len(category_products)} productos de la categoría '{category}'")
    
    # Inicializar el uploader de S3
    print("\nInicializando conexión con AWS S3...")
    s3_uploader = S3Uploader(
        aws_access_key_id=args.aws_key,
        aws_secret_access_key=args.aws_secret,
        region_name=args.region
    )
    
    # Verificar que el bucket existe, si no, crearlo
    print(f"Verificando bucket '{args.bucket_name}'...")
    s3_uploader.create_bucket(args.bucket_name, args.region)
    
    # Subir archivos a S3
    print("\nSubiendo archivos a S3...")
    timestamp_folder = time.strftime("%Y%m%d_%H%M%S")
    uploaded_count = 0
    
    for file_path in created_files:
        file_name = os.path.basename(file_path)
        s3_path = f"{args.prefix}{timestamp_folder}/{file_name}"
        
        print(f"Subiendo {file_name} a s3://{args.bucket_name}/{s3_path}...")
        if s3_uploader.upload_file(file_path, args.bucket_name, s3_path):
            uploaded_count += 1
    
    print(f"\nProceso completado. {uploaded_count} de {len(created_files)} archivos subidos a S3.")


if __name__ == "__main__":
    main()


