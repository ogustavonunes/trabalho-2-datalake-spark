from pyspark.sql import SparkSession

# 1. Configurando a sessão do Spark com download automático de pacotes
spark = SparkSession.builder \
    .appName("Extração SQL para Landing Zone") \
    .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262,com.microsoft.sqlserver:mssql-jdbc:12.8.1.jre11") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9020") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()


# 2. Dados de conexão com o SQL Server (exatamente como no seu Docker)
jdbc_url = "jdbc:sqlserver://localhost:1433;databaseName=trabalho2;encrypt=false"
db_properties = {
    "user": "sa",
    "password": "SqlServer@2025!",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# 3. Lista das tabelas que vamos extrair
tabelas = ["Clientes", "Produtos"]

for tabela in tabelas:
    print(f"Lendo tabela {tabela} do SQL Server...")
    
    # Lendo os dados do banco
    df = spark.read.jdbc(url=jdbc_url, table=tabela, properties=db_properties)
    
    # Salvando no MinIO (bucket landing-zone) no formato CSV
    # O modo 'overwrite' apaga o que tinha antes e coloca o novo
    df.write.mode("overwrite").option("header", "true").csv(f"s3a://landing-zone/{tabela}")
    
    print(f"Sucesso! Tabela {tabela} salva na Landing Zone.")

spark.stop()