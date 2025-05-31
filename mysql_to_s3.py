import pymysql
import json
import requests

# Configuración de MySQL
conn = pymysql.connect(
    host="proyecto3-db.ctkwuucka690.us-east-1.rds.amazonaws.com",
    user="user",
    password="admin123",
    db="proyecto3"
)
cursor = conn.cursor()

# Ejecutar query
cursor.execute("SELECT * FROM products")
data = cursor.fetchall()

# Serializar a JSON
json_data = json.dumps(data)

# Ruta pública de subida (asegúrate que el bucket lo permita)
upload_url = "https://proyecto3-s3.s3.amazonaws.com/raw/mysql/products.json"

# Subir con PUT
response = requests.put(upload_url, data=json_data, headers={"Content-Type": "application/json"})

# Verificar respuesta
if response.status_code == 200:
    print("Archivo subido exitosamente a S3.")
else:
    print(f"Error al subir: {response.status_code} - {response.text}")