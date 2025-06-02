from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os

load_dotenv()

storage_account_name = os.getenv("STORAGE_NAME")

spark = SparkSession.builder.appName("ETL_FakeStore") \
    .config(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", os.getenv("AZURE_KEY")) \
    .getOrCreate()
# Configuración conexión a Blob Storage (montaje o acceso directo con SAS o credenciales)
container_name_raw = os.getenv("CONTAINER_RAW")
container_name_trusted = os.getenv("CONTAINER_TRUSTED")
base_path_raw = f"wasbs://{container_name_raw}@{storage_account_name}.blob.core.windows.net/api"
base_path_trusted = f"wasbs://{container_name_trusted}@{storage_account_name}.blob.core.windows.net/processed"

# Cargar JSON
products_df = spark.read.json(f"{base_path_raw}/products.json")
users_df = spark.read.json(f"{base_path_raw}/users.json")
carts_df = spark.read.json(f"{base_path_raw}/carts.json")

# Limpieza básica: eliminar filas nulas
products_df = products_df.na.drop()
users_df = users_df.na.drop()
carts_df = carts_df.na.drop()

products_df = products_df.withColumn("price", col("price").cast("double"))

# Guardar en trusted (formato parquet para eficiencia)
products_df.write.mode("overwrite").parquet(f"{base_path_trusted}/products")
users_df.write.mode("overwrite").parquet(f"{base_path_trusted}/users")
carts_df.write.mode("overwrite").parquet(f"{base_path_trusted}/carts")

print("Datos ETL procesados y guardados en zona Trusted")