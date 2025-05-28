import requests
import boto3
import json
from datetime import datetime

# Configura el nombre de tu bucket y carpeta destino (zona raw)
BUCKET_NAME = 'proyecto3'
RAW_ZONE_PATH = 'raw/fakestore/products/'

# 1. Captura datos desde la API
url = "https://fakestoreapi.com/products"
response = requests.get(url)
data = response.json()

# 2. Guarda temporalmente en archivo local
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name = f"products_{timestamp}.json"

with open(file_name, 'w') as f:
    json.dump(data, f, indent=2)

# 3. Carga a S3
s3 = boto3.client('s3')
s3.upload_file(file_name, BUCKET_NAME, RAW_ZONE_PATH + file_name)

print(f"Archivo cargado exitosamente a s3://{BUCKET_NAME}/{RAW_ZONE_PATH}{file_name}")
