import requests
import os
from datetime import datetime
# Descargar y guardar los datos de la API
endpoints = ["products", "users", "carts"]
for endpoint in endpoints:
    url = f"https://fakestoreapi.com/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{endpoint}_{date}.json"
    else:
        print(f"[✗] Error al descargar {endpoint}")