# Leer datos limpios de trusted
from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

load_dotenv()

storage_account_name = "proyecto3bigdata"
container_name_trusted = "trusted"

spark = SparkSession.builder.appName("ETL_FakeStore") \
    .config(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", os.getenv("AZURE_KEY")) \
    .getOrCreate()

base_path_trusted = f"wasbs://{container_name_trusted}@{storage_account_name}.blob.core.windows.net/processed"
products_df = spark.read.parquet(f"{base_path_trusted}/products")
users_df = spark.read.parquet(f"{base_path_trusted}/users")
carts_df = spark.read.parquet(f"{base_path_trusted}/carts")

# Crear vistas temporales para usar SQL
products_df.createOrReplaceTempView("products")
users_df.createOrReplaceTempView("users")
carts_df.createOrReplaceTempView("carts")

# Ejemplo análisis: promedio de precio de productos por categoría
avg_price_by_category = spark.sql("""
  SELECT category, AVG(price) as avg_price
  FROM products
  GROUP BY category
""")

avg_price_by_category.show()

# Guardar resultados en Refined
container_name_refined = "refined"
base_path_refined = f"wasbs://{container_name_refined}@{storage_account_name}.blob.core.windows.net/"

avg_price_by_category.write.mode("overwrite").parquet(f"{base_path_refined}/avg_price_by_category")

print("Análisis guardado en zona Refined")