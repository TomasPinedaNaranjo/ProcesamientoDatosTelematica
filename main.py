from fake_store_bot import FakeStoreBot
import upload_file

def main():
    # Extraer productos usando FakeStoreBot
    bot = FakeStoreBot()
    productos = bot.get_all_products()
    if productos is None:
        print("No se pudieron obtener los productos.")
        return

    # Guardar productos en archivo
    filename = bot.save_to_file(productos, filename="todos_los_productos.txt")

    # Subir archivo a S3 usando upload_file.py
    s3_key = f"raw/{filename}"  # O la ruta que desees
    upload_file.upload_to_s3(filename, upload_file.bucket_name, s3_key)
    print(f"Archivo {filename} subido exitosamente a {upload_file.bucket_name}/{s3_key}")

if __name__ == "__main__":
    main()