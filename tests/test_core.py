from datetime import date
from decimal import Decimal

import pytest

from vendas_cli.core import filtrar_por_data, gerar_relatorio
from vendas_cli.models import Venda


def test_total_por_produto_e_geral(vendas: list[Venda]) -> None:
    relatorio = gerar_relatorio(vendas)

    totais = {p.produto: p.total for p in relatorio.produtos}
    assert totais == {
        "Notebook": Decimal("10500.00"),
        "Mouse": Decimal("805.00"),
        "Teclado": Decimal("750.00"),
    }
    assert relatorio.total_geral == Decimal("12055.00")


def test_mais_vendido_por_quantidade(vendas: list[Venda]) -> None:
    relatorio = gerar_relatorio(vendas)

    assert relatorio.mais_vendido is not None
    assert relatorio.mais_vendido.produto == "Mouse"
    assert relatorio.produtos[0].produto == "Notebook"


def test_empate_desempata_pelo_valor() -> None:
    vendas = [
        Venda(date(2025, 1, 1), "Barato", 5, Decimal("1")),
        Venda(date(2025, 1, 1), "Caro", 5, Decimal("100")),
    ]

    relatorio = gerar_relatorio(vendas)

    assert relatorio.mais_vendido is not None
    assert relatorio.mais_vendido.produto == "Caro"


def test_sem_vendas() -> None:
    relatorio = gerar_relatorio([])

    assert relatorio.produtos == []
    assert relatorio.total_geral == Decimal("0")
    assert relatorio.mais_vendido is None


@pytest.mark.parametrize(
    ("inicio", "fim", "esperado"),
    [
        (date(2025, 1, 15), date(2025, 3, 20), 3),
        (date(2025, 3, 1), None, 2),
        (None, date(2025, 1, 31), 1),
        (None, None, 4),
    ],
)
def test_filtro_por_data(
    vendas: list[Venda], inicio: date | None, fim: date | None, esperado: int
) -> None:
    assert len(filtrar_por_data(vendas, inicio, fim)) == esperado


def test_filtro_com_inicio_depois_do_fim(vendas: list[Venda]) -> None:
    with pytest.raises(ValueError, match="posterior"):
        filtrar_por_data(vendas, date(2025, 5, 1), date(2025, 1, 1))
