from pyspark.sql import SparkSession
from delta import *
import os

# 1. Configuração da Sessão (Mantendo o padrão que funcionou)
jars_path = os.path.join(os.getcwd(), "jars")
all_jars = [os.path.join(jars_path, f) for f in os.listdir(jars_path) if f.endswith(".jar")]

builder = SparkSession.builder \
    .appName("Operacoes DML Delta") \
    .config("spark.jars", ",".join(all_jars)) \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9020") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

# 2. Caminho da tabela Bronze
path_produtos = "s3a://bronze/Produtos"

# Criar uma view temporária para facilitar o uso de SQL
spark.read.format("delta").load(path_produtos).createOrReplaceTempView("v_produtos")

print("\n--- Dados Originais na Bronze ---")
spark.sql("SELECT * FROM v_produtos").show()

# A. INSERT usando SQL (Evita o erro de serialização/stack overflow)
print("Executando INSERT via SQL...")
spark.sql("""
    INSERT INTO delta.`{path}` 
    VALUES (103, 'Monitor 144hz', 1200.00)
""".format(path=path_produtos))

# B. UPDATE e C. DELETE usando a DeltaTable API (Mais estável)
delta_table = DeltaTable.forPath(spark, path_produtos)

print("Executando UPDATE...")
delta_table.update("id = 101", { "preco": "300.00" })

print("Executando DELETE...")
delta_table.delete("id = 102")

# 3. Exibição dos resultados finais
print("\n--- Dados após operações DML (Insert, Update, Delete) ---")
delta_table.toDF().show()

print("\n--- Histórico de Versões ---")
delta_table.history().select("version", "timestamp", "operation").show()

spark.stop()