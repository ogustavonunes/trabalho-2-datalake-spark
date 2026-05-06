# Scripts e Execução

Para reproduzir este ambiente, execute os scripts na ordem abaixo utilizando o comando `uv run <nome_do_arquivo>`.

### 1. `extracao_landing.py`
Realiza a conexão JDBC com o SQL Server e exporta as tabelas `Clientes` e `Produtos` para o MinIO em formato CSV.

### 2. `processamento_bronze.py`
Lê os CSVs da Landing Zone e realiza a carga na camada Bronze utilizando o formato Delta Lake. Este script carrega as dependências necessárias para que o Spark consiga ler e escrever no protocolo S3A.

### 3. `operacoes_delta.py`
Executa os testes de transações:
* **Insert:** Adiciona um novo monitor ao catálogo.
* **Update:** Atualiza o preço de produtos existentes.
* **Delete:** Remove itens obsoletos.
* **History:** Exibe o histórico de alterações (Time Travel) da tabela.