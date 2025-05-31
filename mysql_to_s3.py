import json
import mysql.connector

conn = mysql.connector.connect(
    host='tu-endpoint-rds',
    user='admin',
    password='admin123',
    database='nombre_de_tu_db'
)
cursor = conn.cursor()

# Ejecutar query
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Convertir resultados a una lista de diccionarios
data = [dict(zip(columns, row)) for row in rows]

# Guardar como archivo JSON local
with open("products.json", "w") as f:
    json.dump(data, f, indent=2)

print("Archivo 'products.json' generado exitosamente.")