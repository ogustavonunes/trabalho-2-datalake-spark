from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

# 1. Configurando a sessão do Spark (Padrão Linux com download automático)
spark = SparkSession.builder \
    .appName("Processamento Landing para Bronze") \
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9020") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

# 2. Lista de tabelas para processar
tabelas = ["Clientes", "Produtos"]

for tabela in tabelas:
    try:
        print(f"--- Processando {tabela}: Landing -> Bronze ---")
        
        # Lendo os dados da Landing (CSV)
        path_landing = f"s3a://landing-zone/{tabela}"
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(path_landing)
        
        # Adicionando metadados (Data de processamento)
        df_bronze = df.withColumn("_data_processamento", current_timestamp())
        
        # Salvando na Bronze em formato DELTA
        path_bronze = f"s3a://bronze/{tabela}"
        df_bronze.write.format("delta").mode("overwrite").save(path_bronze)
        
        print(f"✅ Tabela {tabela} salva com sucesso na camada Bronze (Delta)!")
    except Exception as e:
        print(f"❌ Erro ao processar {tabela}: {str(e)}")

spark.stop()