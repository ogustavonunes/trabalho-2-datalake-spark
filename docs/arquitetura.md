# Arquitetura de Dados

O projeto segue uma estrutura de camadas para garantir a organização e rastreabilidade dos dados.



## Fluxo de Dados
1. **Extração (SQL Server → Landing):** Os dados são extraídos das tabelas originais e gravados como arquivos CSV no bucket `landing-zone`. O CSV é o formato padrão escolhido para dados relacionais nesta etapa.
2. **Processamento (Landing → Bronze):** O Spark lê os CSVs brutos, infere o esquema e converte os dados para o formato **Delta Lake** no bucket `bronze`.
3. **Operações ACID:** Com os dados em formato Delta, realizamos operações de Insert, Update e Delete diretamente no armazenamento de objetos, mantendo a consistência dos dados.

## Diferenças de Tabelas
Neste laboratório, utilizamos **Tabelas Não Gerenciadas (Externas)**.
* **Tabelas Gerenciadas:** O Spark gerencia tanto os metadados quanto os arquivos físicos. Se a tabela for deletada, os dados somem.
* **Tabelas Não Gerenciadas:** O Spark apenas aponta para o local no MinIO. Se deletarmos a tabela no Spark, os dados continuam seguros no MinIO. Esta é a prática recomendada para ambientes multi-ferramentas.