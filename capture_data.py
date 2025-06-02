import requests
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

# URL de la API de productos
url = "https://fakestoreapi.com/products"

# Conexión a Azure Blob Storage (pon aquí tu connection string)
connection_string = os.getenv("CONNECTION_STRING")

# Nombre del contenedor y blob donde guardarás el JSON
container_name = os.getenv("CONTAINER_RAW")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

# URLs de la API Fake Store
api_urls = {
    "products": "https://fakestoreapi.com/products",
    "carts": "https://fakestoreapi.com/carts",
    "users": "https://fakestoreapi.com/users"
}

def download_and_upload(name, url):
    print(f"Descargando {name}...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.text  # texto JSON
    
    # Guardar localmente
    filename = f"{name}.json"
    with open(filename, "w") as f:
        f.write(data)
    print(f"{filename} guardado localmente.")
    
    # Subir a Azure Blob Storage
    blob_client = container_client.get_blob_client(f"api/{filename}")
    with open(filename, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
    print(f"{filename} subido a Blob Storage en la ruta api/{filename}.")
    
    # Opcional: eliminar archivo local para no acumular
    os.remove(filename)

for name, url in api_urls.items():
    download_and_upload(name, url)

print("Proceso terminado.")