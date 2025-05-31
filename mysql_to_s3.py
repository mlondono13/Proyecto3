import pymysql
import json

# Conexión a MySQL
conn = pymysql.connect(
    host="proyecto3-db.ctkwuucka690.us-east-1.rds.amazonaws.com",
    user="user",
    password="admin123",
    db="proyecto3"
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