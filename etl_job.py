import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

# Ruta local al archivo JSON que contiene todos los productos
filename = "products.json"

# Verifica que el archivo exista
if os.path.exists(filename):
    # Leer JSON local directamente a DataFrame
    df = pd.read_json(filename)

    print(f"Total registros: {len(df)}")

    # Guardar en Parquet localmente
    table = pa.Table.from_pandas(df)
    pq.write_table(table, "products.parquet")

    print("Archivo 'products.parquet' generado localmente.")
else:
    print(f"Archivo '{filename}' no encontrado.")
