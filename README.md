# vendas-cli

CLI que lê um CSV de vendas e mostra o total por produto, o valor total vendido e o produto mais vendido. A saída pode ser em tabela ou em JSON, e dá para filtrar por período.

## Como rodar

Precisa de Python 3.10 ou mais novo. Não tem dependência externa, só a biblioteca padrão.

```bash
git clone https://github.com/RhuanBorgesnr/vendas-cli.git
cd vendas-cli
python -m venv .venv
source .venv/bin/activate   # no Windows: .venv\Scripts\activate
pip install .
```

Depois disso o comando `vendas-cli` fica disponível no terminal. O repositório já tem um `vendas.csv` de exemplo para testar:

```bash
vendas-cli vendas.csv
vendas-cli vendas.csv --format json --start 2025-01-01 --end 2025-03-31
```

Opções disponíveis:

- `--format text|json`: formato da saída (o padrão é `text`)
- `--start` e `--end`: período no formato `AAAA-MM-DD`, pode usar só um dos dois
- `-v`: mostra os logs de processamento

Para salvar o resultado num arquivo (os logs vão para o stderr e não se misturam):

```bash
vendas-cli vendas.csv --format json > relatorio.json
```

## Formato do CSV

```csv
data,produto,quantidade,preco_unitario
2025-01-15,Notebook,2,3500.00
```

A ordem das colunas não importa. Linhas com dados inválidos são puladas e aparecem no log. O produto mais vendido é o de maior quantidade.

## Testes

```bash
pip install -e ".[dev]"
pytest
mypy src tests
```