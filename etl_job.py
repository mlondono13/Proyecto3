import pandas as pd
import requests
import pyarrow as pa
import pyarrow.parquet as pq
import os

# URLs públicas de tus JSONs en S3 (ajusta a tus archivos reales)
urls = [
    "https://proyecto3-bigdata.s3.amazonaws.com/raw/api/products/product1.json",
    # Agrega más archivos según necesites
]

# Descargar y leer archivos JSON
dataframes = []
for url in urls:
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_json(response.content)
    dataframes.append(df)

# Unir todos los DataFrames
if dataframes:
    final_df = pd.concat(dataframes, ignore_index=True)
    print(f"Total registros: {len(final_df)}")

    # Guardar en Parquet localmente
    table = pa.Table.from_pandas(final_df)
    pq.write_table(table, "products.parquet")
    print("Archivo 'products.parquet' generado localmente.")
else:
    print("No se encontraron datos para procesar.")
