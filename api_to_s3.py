import requests
import os
from datetime import datetime

# Carpeta local donde se guardarán los archivos
OUTPUT_DIR = "raw_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Descargar y guardar los datos de la API
endpoints = ["products", "users", "carts"]
for endpoint in endpoints:
    url = f"https://fakestoreapi.com/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{endpoint}_{date}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w") as f:
            f.write(response.text)
        print(f"[✓] {endpoint} guardado como {filepath}")
    else:
        print(f"[✗] Error al descargar {endpoint}")