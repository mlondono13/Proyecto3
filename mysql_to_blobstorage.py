import pymysql
import json
from decimal import Decimal
from datetime import datetime, date
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

# Configuración MySQL
MYSQL_HOST = os.getenv("DB_HOST")
MYSQL_USER = os.getenv("DB_USER")
MYSQL_PASS = os.getenv("DB_PASSWORD")
MYSQL_DB = os.getenv("DB_NAME")

# Configuración Azure Blob Storage
AZURE_CONN_STR = os.getenv("CONNECTION_STRING")
CONTAINER_NAME = "raw"

def convertir_tipos(obj):
    if isinstance(obj, list):
        return [convertir_tipos(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convertir_tipos(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        return obj

def extraer_datos_y_guardar_json(cursor, tabla):
    cursor.execute(f"SELECT * FROM {tabla}")
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()

    datos = [dict(zip(columnas, fila)) for fila in filas]
    datos = convertir_tipos(datos)  # convierte Decimal y datetime

    archivo_json = f"{tabla}.json"
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    print(f"{tabla.capitalize()} descargados y guardados en {archivo_json}")
    return archivo_json

def subir_archivo_blob(ruta_local, nombre_blob, container_client):
    with open(ruta_local, "rb") as data:
        container_client.upload_blob(name=nombre_blob, data=data, overwrite=True)
    print(f"Archivo {ruta_local} subido a {nombre_blob} en contenedor {container_client.container_name}")

def main():
    # Conexión a MySQL
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        database=MYSQL_DB,
        cursorclass=pymysql.cursors.Cursor
    )

    # Cliente Azure Blob
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    tablas = ["products", "users", "carts"]
    with conn:
        with conn.cursor() as cursor:
            for tabla in tablas:
                archivo_json = extraer_datos_y_guardar_json(cursor, tabla)
                nombre_blob = f"mysql/{archivo_json}"
                subir_archivo_blob(archivo_json, nombre_blob, container_client)

if __name__ == "__main__":
    main()