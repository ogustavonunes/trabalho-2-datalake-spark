from minio import Minio

client = Minio(
    "localhost:9020", 
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

buckets = ["landing-zone", "bronze"]

for bucket in buckets:
    try:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"Bucket '{bucket}' criado com sucesso!")
        else:
            print(f"Bucket '{bucket}' já existe.")
    except Exception as err:
        print(f"Erro ao falar com o MinIO: {err}")