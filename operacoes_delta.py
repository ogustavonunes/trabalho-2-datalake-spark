from pyspark.sql import SparkSession
from delta.tables import DeltaTable

# 1. Configurando a sessão com suporte total ao Delta
spark = SparkSession.builder \
    .appName("Operacoes Delta Lake") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9020") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

path_bronze_clientes = "s3a://bronze/Clientes"

print("\n--- 1. Lendo a Tabela Delta de Clientes ---")
dt_clientes = DeltaTable.forPath(spark, path_bronze_clientes)
dt_clientes.toDF().show()

print("\n--- 2. Simulando um UPDATE (Mudando nome do Gustavo) ---")
dt_clientes.update(
    condition = "id = 1",
    set = { "nome": "'Gustavo Nunes Teixeira'" }
)

print("\n--- 3. Simulando um DELETE (Removendo o id 2 se existir) ---")
dt_clientes.delete("id = 2")

print("\n--- 4. Visualizando os dados atualizados ---")
dt_clientes.toDF().show()

print("\n--- 5. Verificando o Histórico da Tabela (Time Travel) ---")
dt_clientes.history().select("version", "timestamp", "operation", "operationParameters").show(truncate=False)

spark.stop()