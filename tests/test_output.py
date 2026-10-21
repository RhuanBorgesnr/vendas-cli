import json

from vendas_cli.core import gerar_relatorio
from vendas_cli.models import Venda
from vendas_cli.output import formatar


def test_saida_json(vendas: list[Venda]) -> None:
    dados = json.loads(formatar(gerar_relatorio(vendas), "json"))

    assert dados["total_geral"] == "12055.00"
    assert dados["mais_vendido"] == {"produto": "Mouse", "quantidade": 10}
    assert dados["produtos"][0] == {"produto": "Notebook", "quantidade": 3, "total": "10500.00"}


def test_saida_json_sem_vendas() -> None:
    dados = json.loads(formatar(gerar_relatorio([]), "json"))

    assert dados == {"produtos": [], "total_geral": "0.00", "mais_vendido": None}


def test_saida_texto(vendas: list[Venda]) -> None:
    texto = formatar(gerar_relatorio(vendas), "text")

    assert "Notebook |          3 |   10500.00" in texto
    assert "Total geral: R$ 12055.00" in texto
    assert "Produto mais vendido: Mouse (10 unidades)" in texto


def test_saida_texto_sem_vendas() -> None:
    assert formatar(gerar_relatorio([]), "text") == "Nenhuma venda encontrada no período."
