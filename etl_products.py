from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_date, year, month, dayofmonth, to_timestamp

# Configuración de S3 (se pasarán como argumentos o se infieren de la ejecución en EMR)
S3_RAW_BUCKET = "proyecto3-s3/raw" # ¡CAMBIA ESTO!
S3_TRUSTED_BUCKET = "proyecto3-s3/trusted" # ¡CAMBIA ESTO!

def create_spark_session():
    return SparkSession.builder \
        .appName("ETLProducts") \
        .getOrCreate()

def etl_process(spark):
    print("Iniciando proceso ETL...")

    # Obtener la fecha de ejecución actual para la lectura de datos más recientes
    # En un entorno real, puedes pasar la fecha como argumento o inferirla de la partición
    processing_date = datetime.now() # O usar una fecha específica si es una ejecución de un día anterior
    raw_products_path = f"s3a://{S3_RAW_BUCKET}/api/products/{processing_date.strftime('%Y/%m/%d')}/"
    raw_clientes_path = f"s3a://{S3_RAW_BUCKET}/api/users/{processing_date.strftime('%Y/%m/%d')}/"

    try:
        # Cargar datos de productos (JSON Lines)
        # Asegúrate de que el path apunte a los archivos JSON reales, no solo a la carpeta
        df_products = spark.read.json(raw_products_path)
        print(f"Productos leídos de: {raw_products_path}")
        df_products.printSchema()

        # Cargar datos de clientes (Parquet)
        df_clientes = spark.read.parquet(raw_clientes_path)
        print(f"Clientes leídos de: {raw_clientes_path}")
        df_clientes.printSchema()

        # Preparación de datos de productos:
        # - Renombrar columnas si es necesario (ej., para evitar conflictos al unir)
        # - Convertir tipos de datos
        # - Seleccionar columnas relevantes
        df_products_clean = df_products.select(
            col("id").alias("product_id"),
            col("title"),
            col("price"),
            col("description"),
            col("category"),
            col("image"),
            col("rating.rate").alias("rating_rate"),
            col("rating.count").alias("rating_count")
        )
        print("Esquema de productos después de la limpieza:")
        df_products_clean.printSchema()

        # Simular una unión (la API no tiene ID de cliente, así que la unión es lógica o simulada)
        # Para esta demo, asignaremos un 'id_cliente' aleatorio o basado en un rango
        # En un caso real, la unión sería por una columna común (ej., ID de pedido, ID de usuario)
        # Aquí, vamos a simular que cada producto podría ser "comprado" por un cliente.
        # Esto es un ejemplo, la lógica real de unión dependerá de tus datos de clientes y API.
        
        # Primero, crea un DF con el número de filas de productos para generar IDs aleatorios
        from pyspark.sql.functions import monotonically_increasing_id, ceil, rand
        
        # Añade un ID de fila temporal a ambos DataFrames para simular un JOIN.
        # Esto es solo un ejemplo de cómo podrías "cruzar" datos sin una clave directa.
        # En un escenario real, buscarías una clave de negocio (ej. order_id, user_id).
        df_products_with_row_id = df_products_clean.withColumn("temp_row_id_prod", monotonically_increasing_id())
        df_clientes_with_row_id = df_clientes.withColumn("temp_row_id_cli", monotonically_increasing_id())

        # Unir por un ID temporal generado. Esto no es una unión lógica de negocio.
        # Se hace para tener ambas informaciones en un mismo DataFrame.
        # Una forma más realista sería si la API tuviera, por ejemplo, "user_id" para cada compra,
        # o si simularas transacciones.
        # Para este ejercicio, vamos a 'unir' un cliente aleatorio a cada producto.
        # Esto NO es una unión de negocio, sino una forma de combinar los DataFrames.
        # En un escenario real, tendrías una tabla de transacciones que une productos y clientes.
        
        # Una forma sencilla de simular la unión es haciendo un crossJoin y luego filtrando
        # o muestreando, pero un crossJoin es muy costoso para Big Data.
        # Para simplificar y dado que no hay una clave de unión directa, vamos a
        # añadir una columna 'cliente_id' aleatoria a los productos que exista en la tabla de clientes.
        
        # Obtenemos los IDs de clientes existentes para asignarlos aleatoriamente
        cliente_ids = [row.id_cliente for row in df_clientes.select("id_cliente").collect()]
        
        if cliente_ids:
            from pyspark.sql.functions import udf, array, explode, floor, lit
            from pyspark.sql.types import IntegerType
            import random

            # UDF para seleccionar un cliente ID aleatorio
            @udf(IntegerType())
            def get_random_client_id():
                return random.choice(cliente_ids)

            df_joined = df_products_clean.withColumn("id_cliente", get_random_client_id())
            # Ahora, unir df_joined con df_clientes por 'id_cliente'
            df_final = df_joined.join(df_clientes, on="id_cliente", how="left")
        else:
            print("Advertencia: No se encontraron IDs de clientes para la unión. Procediendo sin unión.")
            df_final = df_products_clean.withColumn("id_cliente", lit(None)) # Añadir columna de cliente vacía
            df_final = df_final.withColumn("nombre_cliente", lit(None))
            df_final = df_final.withColumn("ciudad", lit(None))
            df_final = df_final.withColumn("antiguedad_meses", lit(None))


        print("Esquema de datos después de la unión:")
        df_final.printSchema()
        df_final.show(5, truncate=False) # Mostrar algunas filas para verificar

        # Añadir columnas de partición (año, mes, día)
        df_final = df_final.withColumn("load_year", year(current_date())) \
                           .withColumn("load_month", month(current_date())) \
                           .withColumn("load_day", dayofmonth(current_date()))

        # Guardar datos procesados en la zona Trusted (Parquet particionado)
        trusted_path = f"s3a://{S3_TRUSTED_BUCKET}/processed_data/"
        df_final.write \
            .mode("overwrite") \
            .partitionBy("load_year", "load_month", "load_day") \
            .parquet(trusted_path)
        print(f"Datos procesados guardados en s3a://{S3_TRUSTED_BUCKET}/processed_data/")

    except Exception as e:
        print(f"Error durante el proceso ETL: {e}")
        raise # Relanzar la excepción para que el Step de EMR falle

    finally:
        spark.stop()
        print("Proceso ETL finalizado.")

if __name__ == "__main__":
    from datetime import datetime # Importar aquí para uso en el script
    spark_session = create_spark_session()
    etl_process(spark_session)