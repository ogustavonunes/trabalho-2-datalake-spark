from pyspark.sql import SparkSession
from delta import *
import os

# Caminho para a sua pasta de jars
jars_path = os.path.join(os.getcwd(), "jars")
all_jars = [os.path.join(jars_path, f) for f in os.listdir(jars_path) if f.endswith(".jar")]

# 1. Configurando a sessão Spark para usar os Jars LOCAIS
builder = SparkSession.builder \
    .appName("Landing para Bronze - Local Jars") \
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

# 2. Processamento
tabelas = ["Clientes", "Produtos"]

for tabela in tabelas:
    try:
        print(f"\n--- Processando {tabela} ---")
        df = spark.read.option("header", "true").csv(f"s3a://landing-zone/{tabela}")
        df.write.format("delta").mode("overwrite").save(f"s3a://bronze/{tabela}")
        print(f"Sucesso! Tabela {tabela} salva como Delta na Bronze.")
    except Exception as e:
        print(f"Erro em {tabela}: {e}")

spark.stop()