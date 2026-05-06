# 🚀 Data Lakehouse com Apache Spark & Delta Lake

Este repositório contém a implementação do **Trabalho 2** da disciplina de Engenharia de Dados. O projeto consiste em construir um pipeline de dados seguindo a arquitetura Lakehouse, realizando a extração de dados de um banco relacional, processamento em camadas no MinIO e execução de operações transacionais com Delta Lake.

## 🏗 Arquitetura do Projeto
O projeto segue o fluxo de dados dividido em camadas para garantir organização e governança:
1. **Source:** SQL Server (Banco transacional executando via Docker).
2. **Landing Zone:** Dados brutos extraídos em formato CSV e armazenados no bucket `landing-zone` do MinIO.
3. **Bronze Layer:** Dados convertidos para formato Delta Lake no bucket `bronze`, permitindo transações ACID e Time Travel.

## 🛠 Tecnologias Utilizadas
* **Linguagem:** Python 3.11+
* **Processamento:** Apache Spark 3.5.x
* **Storage (S3):** MinIO
* **Tabelas:** Delta Lake 3.2.0
* **Banco de Dados:** Microsoft SQL Server 2025 Dev
* **Containerização:** Docker & Docker Compose
* **Documentação:** MkDocs com tema Material

## 📋 Pré-requisitos
Antes de rodar o projeto, você precisará ter instalado:
* [Docker & Docker Compose](https://www.docker.com/)
* [Python 3.11+](https://www.python.org/) (Gerenciador `uv` recomendado)

### 📂 Bibliotecas Necessárias (Pasta `jars/`)
Devido ao limite de tamanho do GitHub, os arquivos `.jar` de driver e conectores devem ser baixados e colocados manualmente na pasta `/jars` na raiz do projeto:
1. `mssql-jdbc-12.8.1.jre11.jar` (Driver SQL Server)
2. `hadoop-aws-3.3.4.jar` (Conector S3A)
3. `aws-java-sdk-bundle-1.12.262.jar` (SDK AWS)

## 🚀 Como Executar

### 1. Subir o ambiente (Docker)
Inicie os serviços do SQL Server e MinIO:
```bash
docker-compose up -d
```

### 2. Configurar o ambiente Python
Utilizando o gerenciador **uv** para instalar as dependências:
```bash
uv sync
```

### 3. Executar o Pipeline de Dados
Execute os scripts na ordem lógica do fluxo para processar as tabelas:

**Extração: SQL Server para CSV (Landing Zone)**
```bash
uv run extracao_landing.py
```

**Processamento: CSV para Delta Lake (Bronze Layer)**
```bash
uv run processamento_bronze.py
```

**Operações DML: Teste de Insert, Update, Delete e Histórico**
```bash
uv run operacoes_delta.py
```

## 📖 Documentação Completa (MkDocs)
Para acessar a documentação detalhada da arquitetura, scripts e a discussão sobre tabelas gerenciadas vs não gerenciadas, execute:
```bash
uv run mkdocs serve
```
Acesse em: **http://127.0.0.1:8000**

## 👥 Grupo de Desenvolvimento
* **Gustavo Nunes Teixeira Teixeira** - [GitHub](https://github.com/ogustavonunes)
* **Frank Cardoso Serrano** - [GitHub](https://github.com/frank-cardoso)

---
*Este projeto foi desenvolvido para fins acadêmicos conforme os requisitos da Atividade Prática - Trabalho 2.*