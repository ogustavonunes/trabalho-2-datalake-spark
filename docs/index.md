# Trabalho 2 - Data Lakehouse com Apache Spark

Este projeto consiste na implementação de uma arquitetura de **Data Lakehouse** utilizando Apache Spark, MinIO (armazenamento de objetos) e SQL Server (banco de dados relacional).

O objetivo principal é demonstrar o fluxo de dados desde a extração de um banco transacional até a persistência em tabelas **Delta Lake**, permitindo operações transacionais ACID e versionamento de dados.

## Tecnologias Utilizadas
* **Apache Spark:** Processamento distribuído de dados.
* **MinIO:** Armazenamento compatível com S3 (Camadas Landing e Bronze).
* **Delta Lake:** Formato de tabela que traz confiabilidade para o Data Lake.
* **SQL Server:** Fonte dos dados transacionais.
* **Python/uv:** Linguagem de script e gerenciamento de ambiente.