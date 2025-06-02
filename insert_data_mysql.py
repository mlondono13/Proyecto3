import requests
import json
import pymysql
from datetime import datetime

# URLs API
urls = {
    "products": "https://fakestoreapi.com/products",
    "users": "https://fakestoreapi.com/users",
    "carts": "https://fakestoreapi.com/carts"
}

# Descargar y guardar JSON localmente
for key, url in urls.items():
    response = requests.get(url)
    data = response.json()
    with open(f"{key}.json", "w") as f:
        json.dump(data, f, indent=4)
    print(f"{key.capitalize()} descargados y guardados en {key}.json")

# Conexión a MySQL
conn = pymysql.connect(
    host="20.15.106.113",      # Cambia por IP/host de tu BD
    user="root",
    password="root",
    database="proyecto3"
)
cursor = conn.cursor()

# Insertar productos
with open("products.json") as f:
    products = json.load(f)

sql_products = """
INSERT INTO products (title, price, description, category, image)
VALUES (%s, %s, %s, %s, %s)
"""
for p in products:
    cursor.execute(sql_products, (p["title"], p["price"], p["description"], p["category"], p["image"]))
conn.commit()
print(f"{cursor.rowcount} productos insertados")

# Insertar usuarios
with open("users.json") as f:
    users = json.load(f)

sql_users = """
INSERT INTO users (id, email, username, password, name_first, name_last, phone)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
for u in users:
    cursor.execute(sql_users, (
        u["id"], u["email"], u["username"], u["password"],
        u["name"]["firstname"], u["name"]["lastname"], u["phone"]
    ))
conn.commit()
print(f"{cursor.rowcount} usuarios insertados")

# Insertar carritos y sus items
with open("carts.json") as f:
    carts = json.load(f)

sql_carts = "INSERT INTO carts (id, userId, date) VALUES (%s, %s, %s)"
sql_cart_items = "INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)"

for c in carts:
    date_obj = datetime.strptime(c["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    cursor.execute(sql_carts, (c["id"], c["userId"], date_obj))
    for item in c["products"]:
        cursor.execute(sql_cart_items, (c["id"], item["productId"], item["quantity"]))

conn.commit()
print(f"{len(carts)} carritos y sus items insertados")

cursor.close()
conn.close()
