import pymysql
import boto3
import json

# Configuración de MySQL
conn = pymysql.connect(host="proyecto3-db.ctkwuucka690.us-east-1.rds.amazonaws.com", user="user", password="admin123", db="proyecto3")
cursor = conn.cursor()

# Ejecutar query y guardar en S3
cursor.execute("SELECT * FROM products")
data = cursor.fetchall()

s3 = boto3.client('s3')
s3.put_object(
    Bucket="proyecto3-s3",
    Key="raw/mysql/products.json",
    Body=json.dumps(data)
)