import requests
import boto3
from datetime import datetime

BUCKET = "proyecto3-s3"

def upload_to_s3(data, endpoint):
    s3 = boto3.client('s3')
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    key = f"raw/api/{endpoint}/{date}.json"
    s3.put_object(Bucket=BUCKET, Key=key, Body=data)

# Descargar datos de la API
endpoints = ["products", "users", "carts"]
for endpoint in endpoints:
    url = f"https://fakestoreapi.com/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        upload_to_s3(response.text, endpoint)