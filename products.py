import pymysql
import requests

# Conexión a tu base de datos MySQL
conn = pymysql.connect(
    host="proyecto3-db.ctkwuucka690.us-east-1.rds.amazonaws.com",
    user="user",
    password="admin123",
    db="proyecto3"
)
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    price FLOAT,
    description TEXT,
    category VARCHAR(255),
    image TEXT
)
""")

# Obtener productos desde la API
response = requests.get("https://fakestoreapi.com/products")
products = response.json()

# Insertar productos en la base de datos
for product in products:
    cursor.execute("""
    INSERT INTO products (id, title, price, description, category, image)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title=VALUES(title),
        price=VALUES(price),
        description=VALUES(description),
        category=VALUES(category),
        image=VALUES(image)
    """, (
        product["id"],
        product["title"],
        product["price"],
        product["description"],
        product["category"],
        product["image"]
    ))

conn.commit()
cursor.close()
conn.close()