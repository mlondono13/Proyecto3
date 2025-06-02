from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

load_dotenv()

storage_account_name = os.getenv("STORAGE_NAME")
storage_account_access_key = os.getenv("AZURE_KEY")
container_name = "refined"

spark = SparkSession.builder.appName("ETL_FakeStore") \
    .config(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_access_key) \
    .getOrCreate()

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_access_key)

# Leer datos desde Blob Storage
ruta_blob = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/avg_price_by_category"
df = spark.read.parquet(ruta_blob)

# Exploración
df.show(5)
df.printSchema()

# Crear vista para SQL
df.createOrReplaceTempView("resultados")

# Consulta SQL de ejemplo
df_agg = spark.sql("""
    SELECT category, AVG(avg_price) as promedio_valor
    FROM resultados
    GROUP BY category
    ORDER BY promedio_valor DESC
""")
df_agg.show()

# Convertir a Pandas y graficar
pdf = df_agg.toPandas()

plt.figure(figsize=(10,6))
sns.barplot(data=pdf, x='category', y='promedio_valor')
plt.title('Promedio de valor por categoría')
plt.xticks(rotation=45)
plt.show()
