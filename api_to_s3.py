import requests
import subprocess
import os

BUCKET = "proyecto3-bigdata"
BASE_PATH = "raw/api"

# Crear archivos y subirlos
endpoints = ["products", "users", "carts"]
for endpoint in endpoints:
    url = f"https://fakestoreapi.com/{endpoint}"
    response = requests.get(url)

    if response.status_code == 200:
        filename = f"{endpoint}.json"
        
        # Guardar archivo localmente
        with open(filename, "w") as f:
            f.write(response.text)
        
        # Subir a S3 usando AWS CLI
        s3_key = f"s3://{BUCKET}/{BASE_PATH}/{endpoint}/{filename}"
        subprocess.run(["aws", "s3", "cp", filename, s3_key], check=True)
        print(f"Subido a: {s3_key}")
        
        # (Opcional) eliminar archivo local
        os.remove(filename)
    else:
        print(f"Error al obtener datos de {endpoint}")
