# ❓ Perguntas Frequentes (FAQ)

---

## 🎯 Sobre o Projeto

### O que é Data Lakehouse?

**Data Lakehouse** é uma arquitetura que combina as melhores características de Data Lakes e Data Warehouses:

- **Data Lake:** Armazenamento flexível, escalável, de baixo custo
- **Data Warehouse:** Queries rápidas, ACID compliance, governança

**Benefícios:**
- ✅ ACID transactions no Data Lake
- ✅ Schema enforcement e data quality
- ✅ Performance otimizada
- ✅ Escalabilidade ilimitada
- ✅ Suporte a múltiplos formatos (Parquet, CSV, JSON)

---

### Qual é a diferença entre Landing e Bronze?

| Aspecto | Landing | Bronze |
|---------|---------|--------|
| **Formato** | CSV | Delta Lake (Parquet) |
| **Schema** | Nenhum | Definido |
| **Otimização** | Não | Sim |
| **Transações ACID** | Não | Sim |
| **Particionamento** | Não | Sim |
| **Caso de uso** | Backup raw | Processamento |

**Analogia:**
- **Landing Zone** = Área de desembarque (dados brutos)
- **Bronze Layer** = Depósito refinado (dados processados)

---

### Por que usar Delta Lake em vez de Parquet puro?

**Delta Lake adiciona:**
- ✅ Transaction log (_delta_log)
- ✅ ACID compliance
- ✅ Time Travel
- ✅ Schema enforcement
- ✅ Data versioning
- ✅ Unified batch and streaming

**Parquet puro não oferece essas garantias!**

---

## 🛠 Sobre Tecnologias

### Qual versão de Python devo usar?

Recomendamos **Python 3.11 ou superior**.

```bash
# Verificar versão
python --version

# Python 3.11+ suporta melhor features recentes
```

---

### MinIO é seguro? Posso usar em produção?

**MinIO é seguro**, mas com ressalvas:

- ✅ Em desenvolvimento/testes: Seguro
- ✅ Em staging: Com boas práticas de segurança
- ⚠️ Em produção: Recomenda-se AWS S3 ou Azure Blob

**Para produção:**
- Use autenticação SSL/TLS
- Configure firewalls
- Implemente RBAC (Role-Based Access Control)
- Habilite audit logging
- Use versioning e backups

---

### Posso usar cloud storage (AWS S3, Azure Blob)?

**Sim!** Spark + Delta Lake suportam qualquer S3-compatible storage:

```python
# AWS S3
df.write.format("delta") \
    .save("s3://seu-bucket/tabela/")

# Azure Blob
df.write.format("delta") \
    .save("wasbs://container@storage.blob.core.windows.net/tabela/")

# GCS (Google Cloud Storage)
df.write.format("delta") \
    .save("gs://seu-bucket/tabela/")
```

---

### Preciso de um cluster Spark distribuído?

**Para este projeto:** Não, uso local é suficiente.

**Para produção:**
- Dados < 10GB: Spark local/single-node
- Dados 10GB-1TB: Cluster de 3-5 nodes
- Dados > 1TB: Cluster com 10+ nodes

---

## 📊 Sobre Dados

### Quantos dados o pipeline pode processar?

**Capacidade teórica:**
- Landing Zone: Ilimitado (storage S3)
- Processing: ~100MB/s por core Spark
- Bronze Layer: Ilimitado com particionamento

**Exemplo:**
- 1GB de dados: ~10 segundos
- 100GB de dados: ~16 minutos
- 1TB de dados: ~2-3 horas

---

### Posso adicionar novos dados sem reprocessar tudo?

**Sim!** Use modo append:

```python
# Modo append (não sobrescreve)
df_novo.write.format("delta") \
    .mode("append") \
    .save("s3a://bronze/Produtos/")

# Modo overwrite (sobrescreve tudo)
df.write.format("delta") \
    .mode("overwrite") \
    .save("s3a://bronze/Produtos/")
```

---

### Como lidar com dados nulos?

Delta Lake oferece opções:

```python
# Rejeitar nulos
df.write.format("delta") \
    .option("mergeSchema", "false") \
    .save(path)

# Preencher com valores padrão
df = df.fillna({"preco": 0.0, "categoria": "Sem categoria"})

# Remover registros nulos
df = df.dropna(subset=["id", "nome"])
```

---

## 🔄 Sobre Pipeline

### Posso executar scripts em paralelo?

**Não é recomendado.** Ordem correta:

1. `extracao_landing.py` (extrai dados)
2. `processamento_bronze.py` (transforma dados)
3. `operacoes_delta.py` (testa operações)

Executar em paralelo pode causar:
- ❌ Condições de corrida
- ❌ Conflitos de escrita
- ❌ Corrupção de dados

---

### Posso pular um script?

**Não:**
- ❌ Pular `extracao_landing.py`: Sem dados brutos
- ❌ Pular `processamento_bronze.py`: Sem Delta tables
- ❌ Pular `operacoes_delta.py`: Sem testes ACID

Execute todos em ordem!

---

### Com que frequência devo executar o pipeline?

Depende do caso de uso:

- **Desenvolvimento:** Ad-hoc (quando necessário)
- **Testes:** Daily
- **Produção:** Hourly/Daily (conforme SLA)

Para automatizar, use:
- Apache Airflow
- Prefect
- dbt
- AWS Lambda/Step Functions

---

## 🐛 Sobre Problemas

### Perdi dados! Como recuperar?

**Time Travel ao resgate!**

```python
# Consultar versão anterior
df_v1 = spark.read.format("delta") \
    .option("versionAsOf", 1) \
    .load("s3a://bronze/Produtos/")

# Restaurar para versão anterior
spark.sql("""
    RESTORE TABLE delta.`s3a://bronze/Produtos/`
    TO VERSION AS OF 1
""")
```

---

### Tabela ficou corrompida. Posso limpar?

Sim, use VACUUM:

```sql
-- Listar arquivos não referenciados
SELECT * FROM delta.`s3a://bronze/Produtos/`

-- Limpar versões antigas (7+ dias)
VACUUM s3a://bronze/Produtos/ RETAIN 168 HOURS

-- Forçar limpeza (cuidado!)
-- DELETE FROM delta.`s3a://bronze/Produtos/`
```

---

## 💾 Sobre Armazenamento

### Quanto espaço em disco preciso?

**Mínimo:**
- Docker + SQL Server: 5GB
- Python dependências: 1GB
- Dados de teste: 500MB
- Total: ~7GB

**Recomendado:** 20-50GB para margem

---

### Como lidar com dados duplicados?

**Deduplicate:**

```python
# Remover linhas duplicadas
df_unique = df.dropDuplicates(["id"])

# Remover duplicatas considerando subset
df_unique = df.dropDuplicates(["nome", "email"])
```

---

## 🚀 Sobre Produção

### Como escalar para produção?

1. **Implementar CI/CD** (GitHub Actions, GitLab CI)
2. **Adicionar testes** (pytest, data quality checks)
3. **Monitorar pipeline** (Prometheus, Grafana)
4. **Usar orquestração** (Airflow, Prefect)
5. **Implementar alertas** (Slack, PagerDuty)
6. **Documentar SLAs** (tempo de processamento, RPO/RTO)

---

### Posso usar este projeto em produção?

**Este projeto é acadêmico.** Para produção:

- ✅ Conceitos e arquitetura: Excelentes
- ❌ Segurança: Precisa reforço
- ❌ Monitoramento: Precisa adicionar
- ❌ Error handling: Precisa melhorar
- ❌ Logging: Precisa estruturado

**Recomendação:** Use como base educacional e adapte para produção.

---

## 🤝 Contribuindo

### Como contribuir com o projeto?

1. Fork o repositório
2. Crie branch: `git checkout -b feature/sua-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push para branch: `git push origin feature/sua-feature`
5. Abra Pull Request

---

### Como reportar bugs?

1. Verifique se o bug já foi reportado
2. Descreva o problema claramente
3. Forneça passo a passo para reproduzir
4. Anexe logs e screenshots
5. Abra issue no GitHub

---

## 📚 Aprendizado

### Onde aprender mais sobre Data Lakes?

**Recursos:**
- [Delta Lake Docs](https://docs.delta.io/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Lakehouse Papers](https://www.cidrdb.org/)
- [Databricks Blog](https://databricks.com/blog)

---

### Qual é a roadmap do projeto?

Planejamos adicionar:

- [ ] Silver Layer (dados agregados)
- [ ] Gold Layer (insights finais)
- [ ] Streaming com Kafka
- [ ] ML pipeline integrada
- [ ] Governança com Apache Atlas
- [ ] Documentação em mais idiomas

---

## 💡 Dicas Extras

### Dica 1: Use modo "verbose" para debug

```python
spark.sparkContext.setLogLevel("DEBUG")
```

### Dica 2: Perfile seu código

```python
import cProfile
cProfile.run('seu_funcao()')
```

### Dica 3: Valide dados antes de escrever

```python
# Validação simples
assert df.count() > 0, "DataFrame vazio!"
assert "id" in df.columns, "Coluna 'id' faltando!"
```

### Dica 4: Documente transformações

```python
# Adicione comentários explicando transformações
df = df \
    .filter(col("preco") > 0) \  # Remover preços inválidos
    .drop("coluna_temporaria")    # Limpar colunas desnecessárias
```

---

## 📞 Ainda com dúvida?

- 📖 Consulte a [documentação completa](../documentation/architecture.md)
- 🐛 Veja o [Troubleshooting Guide](./troubleshooting.md)
- 💬 Abra uma [issue no GitHub](https://github.com/ogustavonunes/trabalho-2-datalake-spark/issues)
- 📧 Entre em contato com os autores
