# 🚀 Data Lakehouse com Apache Spark & Delta Lake

Este repositório contém a implementação do **Trabalho 2** da disciplina de Engenharia de Dados. O projeto consiste em construir um pipeline de dados seguindo a arquitetura Lakehouse, realizando a extração de dados de um banco relacional, processamento em camadas no MinIO e execução de operações transacionais com Delta Lake.

## 📊 Visão Geral
O projeto implementa um pipeline de processamento de dados com as seguintes características:
- ✅ **Extração** de dados de SQL Server para formato CSV
- ✅ **Transformação** de CSV para Delta Lake com schema validado
- ✅ **Operações transacionais** (INSERT, UPDATE, DELETE) com ACID compliance
- ✅ **Time Travel** para auditoria e recuperação de dados históricos
- ✅ **Armazenamento distribuído** utilizando MinIO como solução S3-compatível

## 🏗 Arquitetura do Projeto
O projeto segue o fluxo de dados dividido em camadas para garantir organização e governança:

```
SQL Server (Source)
    ↓
Landing Zone (CSV no MinIO)
    ↓
Bronze Layer (Delta Lake no MinIO)
    ↓
Operações DML & Análise
```

1. **Source:** SQL Server (Banco transacional executando via Docker).
2. **Landing Zone:** Dados brutos extraídos em formato CSV e armazenados no bucket `landing-zone` do MinIO.
3. **Bronze Layer:** Dados convertidos para formato Delta Lake no bucket `bronze`, permitindo transações ACID e Time Travel.

## 🛠 Tecnologias Utilizadas
| Categoria | Tecnologia | Versão |
|-----------|-----------|--------|
| **Linguagem** | Python | 3.11+ |
| **Processamento** | Apache Spark | 3.5.3 |
| **Storage (S3)** | MinIO | Latest |
| **Tabelas** | Delta Lake | 3.2.0 |
| **Banco de Dados** | Microsoft SQL Server | 2025 Dev |
| **Containerização** | Docker & Docker Compose | Latest |
| **Documentação** | MkDocs + Material Theme | 1.6.1+ |
| **Gerenciador de Pacotes** | uv | Latest |

## 📋 Pré-requisitos
Antes de rodar o projeto, você precisará ter instalado:
* [Docker & Docker Compose](https://www.docker.com/)
* [Python 3.11+](https://www.python.org/) (Gerenciador `uv` recomendado)
* Espaço em disco: ~5GB (para volumes Docker, dependências Python e dados)

### 📂 Arquivos JAR Necessários (Pasta `jars/`)
Devido ao limite de tamanho do GitHub, os arquivos `.jar` de driver e conectores devem ser baixados e colocados manualmente na pasta `/jars` na raiz do projeto:

| Arquivo | Versão | Propósito |
|---------|--------|----------|
| `mssql-jdbc-12.8.1.jre11.jar` | 12.8.1 | Driver JDBC para SQL Server |
| `hadoop-aws-3.3.4.jar` | 3.3.4 | Conector S3A (Hadoop) |
| `aws-java-sdk-bundle-1.12.262.jar` | 1.12.262 | SDK AWS para Java |

**Links de download:**
- [SQL Server JDBC Driver](https://learn.microsoft.com/en-us/sql/connect/jdbc/download-microsoft-jdbc-driver-for-sql-server)
- [Hadoop AWS JAR](https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-aws)
- [AWS Java SDK Bundle](https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-bundle)

## 🚀 Como Executar

### Passo 1: Preparar o ambiente
Clone o repositório e navegue até a pasta do projeto:
```bash
git clone https://github.com/ogustavonunes/trabalho-2-datalake-spark.git
cd trabalho-2-datalake-spark
```

### Passo 2: Subir os serviços (Docker)
Inicie os serviços do SQL Server e MinIO em background:
```bash
docker-compose up -d
```

Verifique se os serviços estão rodando:
```bash
docker-compose ps
```

**Acessos dos serviços:**
- **SQL Server:** `localhost:1433` (Usuário: `sa`, Senha: `SqlServer@2025!`)
- **MinIO Console:** `http://localhost:9021` (Usuário: `minioadmin`, Senha: `minioadmin`)
- **MinIO API:** `http://localhost:9020`

### Passo 3: Configurar o ambiente Python
Instale as dependências utilizando o gerenciador **uv**:
```bash
uv sync
```

### Passo 4: Download dos JARs necessários
Baixe os arquivos `.jar` listados na seção de pré-requisitos e coloque-os na pasta `jars/` da raiz do projeto.

### Passo 5: Executar o Pipeline de Dados
Execute os scripts na ordem lógica do fluxo:

#### 1️⃣ Extração: SQL Server → CSV (Landing Zone)
```bash
uv run extracao_landing.py
```
**O que faz:** Conecta ao SQL Server, extrai dados de tabelas transacionais e salva em CSV no bucket `landing-zone` do MinIO.

#### 2️⃣ Processamento: CSV → Delta Lake (Bronze Layer)
```bash
uv run processamento_bronze.py
```
**O que faz:** Lê CSVs da landing zone, valida schema, realiza transformações e salva como tabelas Delta Lake no bucket `bronze`.

#### 3️⃣ Operações DML: Testes de transações ACID
```bash
uv run operacoes_delta.py
```
**O que faz:** Executa operações INSERT, UPDATE, DELETE nas tabelas Delta, demonstra Time Travel e valida compliance ACID.

## 📖 Documentação Completa (MkDocs)
Para acessar a documentação detalhada sobre a arquitetura, scripts, decisões de design e discussão sobre tabelas gerenciadas vs não gerenciadas:
```bash
uv run mkdocs serve
```
Acesse em: **http://localhost:8000** (local)  
Versão publicada: **https://ogustavonunes.github.io/trabalho-2-datalake-spark/**

## 🛠 Estrutura do Projeto
```
trabalho-2-datalake-spark/
├── extracao_landing.py          # Script de extração SQL Server → CSV
├── processamento_bronze.py       # Script de processamento CSV → Delta
├── operacoes_delta.py            # Script de operações DML e testes
├── docker-compose.yml            # Orquestração de serviços (SQL Server + MinIO)
├── pyproject.toml                # Dependências do projeto
├── .gitignore                    # Configuração de versão
├── mkdocs.yml                    # Configuração da documentação
├── docs/                         # Arquivos de documentação
│   ├── index.md
│   ├── arquitetura.md
│   └── scripts.md
└── data/                         # Diretório para dados locais (não versionado)
```

## 📝 Descrição dos Scripts

### `extracao_landing.py`
- **Entrada:** SQL Server (database relacional)
- **Saída:** CSV no bucket `landing-zone` do MinIO
- **Responsabilidades:**
  - Conectar ao SQL Server via JDBC
  - Extrair dados de tabelas transacionais
  - Converter para formato CSV
  - Armazenar no MinIO com organização por tabela

### `processamento_bronze.py`
- **Entrada:** CSV do bucket `landing-zone`
- **Saída:** Delta Lake no bucket `bronze`
- **Responsabilidades:**
  - Ler arquivos CSV
  - Validar e aplicar schema
  - Realizar transformações básicas
  - Escrever em formato Delta com particionamento

### `operacoes_delta.py`
- **Entrada:** Tabelas Delta Lake
- **Saída:** Operações transacionais + relatórios
- **Responsabilidades:**
  - Executar INSERT de novos registros
  - Realizar UPDATE de dados existentes
  - Efetuar DELETE com compliance ACID
  - Demonstrar Time Travel e histórico

## 📦 Dependências Principais
```
delta-spark==3.2.0      # Delta Lake
pyspark==3.5.3          # Apache Spark
minio>=7.2.20           # Cliente MinIO
mkdocs>=1.6.1           # Documentação
mkdocs-material>=9.7.6  # Tema Material
```

Para atualizar dependências:
```bash
uv pip compile pyproject.toml -o requirements.txt
```

## 🧹 Limpeza

### Parar os serviços Docker
```bash
docker-compose down
```

### Parar e remover volumes (CUIDADO - apaga dados!)
```bash
docker-compose down -v
```

### Limpar cache Python
```bash
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

## ✅ Verificações e Validações

### Validar setup completo
```bash
# 1. Docker rodando
docker-compose ps

# 2. Python e uv instalados
python --version
uv --version

# 3. Dependências instaladas
uv pip list

# 4. JARs presentes
ls -la jars/
```

### Testar conectividade
```bash
# SQL Server
docker-compose exec sqlserver sqlcmd -S localhost -U sa -P SqlServer@2025! -Q "SELECT @@VERSION"

# MinIO
aws s3 --endpoint-url http://localhost:9020 ls --no-sign-request
```

## 👥 Grupo de Desenvolvimento
| Membro | GitHub | Papel |
|--------|--------|-------|
| **Gustavo Nunes Teixeira** | [@ogustavonunes](https://github.com/ogustavonunes)
| **Frank Cardoso Serrano** | [@frank-cardoso](https://github.com/frank-cardoso) 

## 📄 Licença
Este projeto é fornecido como está para fins acadêmicos. Consulte o arquivo LICENSE (se presente) para mais detalhes.

## 📞 Suporte
Para dúvidas ou issues:
1. Abra uma issue no repositório GitHub
2. Consulte a [documentação oficial](https://ogustavonunes.github.io/trabalho-2-datalake-spark/)
3. Verifique a seção de Troubleshooting acima

---
*Desenvolvido para fins acadêmicos conforme os requisitos da Atividade Prática - Trabalho 2 da disciplina de Engenharia de Dados.*

