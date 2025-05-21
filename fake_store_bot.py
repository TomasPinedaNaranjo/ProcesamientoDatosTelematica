import requests
import json
from datetime import datetime

class FakeStoreBot:
    """
    Bot para consumir datos de la Fake Store API y guardarlos en archivos de texto.
    """
    
    def __init__(self, base_url="https://fakestoreapi.com"):
        """Inicializa el bot con la URL base de la API."""
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_all_products(self):
        """Obtiene todos los productos disponibles."""
        endpoint = f"{self.base_url}/products"
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener productos: {response.status_code}")
            return None
    
    def get_single_product(self, product_id):
        """Obtiene un producto específico por su ID."""
        endpoint = f"{self.base_url}/products/{product_id}"
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener el producto {product_id}: {response.status_code}")
            return None
    
    def get_products_by_category(self, category):
        """Obtiene productos por categoría."""
        endpoint = f"{self.base_url}/products/category/{category}"
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener productos de la categoría {category}: {response.status_code}")
            return None
    
    def get_all_categories(self):
        """Obtiene todas las categorías disponibles."""
        endpoint = f"{self.base_url}/products/categories"
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener categorías: {response.status_code}")
            return None
    
    def get_cart(self, cart_id):
        """Obtiene información de un carrito de compras por ID."""
        endpoint = f"{self.base_url}/carts/{cart_id}"
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener el carrito {cart_id}: {response.status_code}")
            return None
    
    def get_user(self, user_id):
        """Obtiene información de un usuario por ID."""
        endpoint = f"{self.base_url}/users/{user_id}"
        response = self.session.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener el usuario {user_id}: {response.status_code}")
            return None
    
    def save_to_file(self, data, filename=None):
        """Guarda los datos en un archivo de texto con formato JSON."""
        if filename is None:
            # Generar un nombre de archivo con la fecha y hora actual
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fakestore_data_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        print(f"Los datos se han guardado exitosamente en '{filename}'")
        return filename