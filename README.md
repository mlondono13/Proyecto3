# ST0263 - TÓPICOS ESPECIALES DE TELEMÁTICA
## Estudiantes:
## Luis Fernando Posada Cano - lfposadac@eafit.edu.co
## Jose Miguel Burgos Cuartas - jmburgoc@eafit.edu.co
## Marcela Londoño Leon - mlondonol@eafit.edu.co
## Juanmartin Betancur Arango - jbetancur5@eafit.edu.co
## Proyecto3: Automatización de un proceso batch de datos big data en azure

- - -
## 1. Breve descripción de la actividad

Este proyecto consiste en la automatización completa de un flujo de procesamiento de datos tipo batch usando tecnologías de la nube. Se trabajó con datos de comercio electrónico simulados provenientes de la Fake Store API y una base de datos relacional MySQL alojada en una máquina virtual (VM) en Azure.

El pipeline incluye la captura de datos, su ingesta en almacenamiento tipo data lake, procesamiento ETL y análisis de datos descriptivos y avanzados, utilizando herramientas como **Azure Blob Storage**, **Azure Databricks** y **Python**. La ejecución del flujo completo se automatizó mediante un **Job en Databricks**.

### 1.1 Aspectos cumplidos de la actividad propuesta por el profesor

- Uso de dos fuentes de datos reales: una API pública (Fake Store API) y una base de datos relacional simulada (MySQL en VM).
- Ingesta automática a contenedores tipo "raw" en Blob Storage.
- Procesamiento automático con Spark (ETL y análisis) sobre Databricks.
- Almacenamiento de resultados en zona “refined” del data lake.
- Automatización del proceso con Jobs en Databricks.
- Video de sustentación mostrando el funcionamiento del pipeline automatizado.

### 1.2 Aspectos no cumplidos de la actividad propuesta por el profesor

- No se usó Athena para consulta de datos, ya que la implementación fue en Azure.

---

## 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas

- **Arquitectura por zonas:** datos se almacenan en contenedores `raw`, `trusted`, y `refined` en Azure Blob Storage.
- **Separación por scripts modulares** para cada etapa: captura, ingesta, procesamiento, análisis.
- **Automatización con Azure Databricks Jobs**: el flujo completo corre automáticamente sin intervención manual.
- **Persistencia estructurada y formatos estándar** (`JSON`, `Parquet`) para almacenamiento intermedio y final.
- **Notebooks en Databricks** para facilitar pruebas, desarrollo y seguimiento del procesamiento.

---

## 3. Descripción del ambiente de desarrollo y técnico
### 3.1 Cómo se compila y ejecuta

1. **Captura de datos desde la API**
   - Script: `capture_data.py`
   - Descarga datos de `/products`, `/users` y `/carts` desde https://fakestoreapi.com y los guarda en archivos `.json`.

2. **Ingesta a base de datos relacional simulada**
   - Script: `insert_data_mysql.py`
   - Carga los archivos `.json` a una base de datos MySQL ejecutándose en una VM de Azure.

3. **Extracción desde la base de datos a Azure Blob Storage**
   - Script: `mysql_to_blobstorage.py`
   - Extrae los datos desde la base MySQL y los sube a la zona `raw/relational/` de Blob Storage.

4. **Procesamiento ETL**
   - Script: `etl.py` (Notebook en Databricks)
   - Limpia y une datos de la API con la base relacional y los guarda en la zona `trusted`.

5. **Análisis de datos**
   - Script: `analysis.py` (Notebook en Databricks)
   - Realiza análisis descriptivo sobre los datos procesados.
   - Resultados almacenados en `refined`.

6. **Automatización**
   - Se creó un **Job en Databricks** que ejecuta en secuencia los notebooks de ETL y análisis.

### 3.2 Detalles del desarrollo

- Lenguaje principal: **Python 3**
- Desarrollo distribuido entre scripts locales y notebooks en Databricks.
- Organización modular: cada etapa tiene su propio script/notebook independiente.

### 3.3 Detalles técnicos

- **Azure Blob Storage:**
  - `raw/` → Datos crudos desde API y MySQL
  - `trusted/` → Datos procesados
  - `refined/` → Resultados del análisis

- **Base de datos relacional:**
  - MySQL 8.0 corriendo en una VM Ubuntu en Azure.
  - Tablas simuladas de usuarios, carritos, y productos.

- **Cluster de procesamiento:**
  - Azure Databricks (clúster autoservicio)

### 3.4 Descripción y configuración de parámetros del proyecto

- Variables de entorno requeridas:
  - `AZURE_STORAGE_CONNECTION_STRING`
  - Credenciales de conexión a MySQL (host, puerto, usuario, contraseña)
- Configuración del Job en Databricks:
  - Secuencia de tareas:
    1. `etl.py`
    2. `analysis.py`
  - Programado para ejecución manual o periódica.

---

## 4. Video de sustentación

🎥 Video disponible en:  
[https://www.youtube.com/watch?v=gv8I-KAUOxU&feature=youtu.be](https://www.youtube.com/watch?v=gv8I-KAUOxU&feature=youtu.be)

## 5. Otra información que considere relevante para esta actividad

Durante el desarrollo de este proyecto se exploraron herramientas modernas para procesamiento batch de datos en la nube. Se destaca lo siguiente:

La automatización con Databricks Jobs simplificó la orquestación sin necesidad de herramientas adicionales como Airflow.

El uso de Azure Blob Storage como Data Lake permitió mantener una arquitectura limpia separando las zonas de datos (raw, trusted, refined).

La simulación de una base de datos relacional en una VM fue útil para replicar escenarios reales de integración de múltiples fuentes.

La elección de la Fake Store API resultó apropiada para simular un entorno de ecommerce, y permitió integrar datos con estructura variada (productos, carritos, usuarios).

🔗 Referencias y créditos
Fake Store API – https://fakestoreapi.com/

Video de referencia para EMR con Spark (como guía inicial del enfoque):
https://www.youtube.com/watch?v=ZFns7fvBCH4

Documentación oficial de:

Azure Databricks: https://learn.microsoft.com/en-us/azure/databricks/

Azure Blob Storage: https://learn.microsoft.com/en-us/azure/storage/blobs/

Curso ST0263 - Recursos compartidos por el profesor

Stack Overflow – Soluciones a errores con conexión a MySQL y scripts en Python

---
Video: https://youtu.be/gv8I-KAUOxU
