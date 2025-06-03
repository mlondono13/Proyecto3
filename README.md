# ST0263 - TÓPICOS ESPECIALES DE TELEMÁTICA
## Estudiantes:
## Luis Fernando Posada Cano - lfposadac@eafit.edu.co
## Juan Martin Betancur Rios - jbetan56@eafit.edu.co
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


Video: https://youtu.be/gv8I-KAUOxU
