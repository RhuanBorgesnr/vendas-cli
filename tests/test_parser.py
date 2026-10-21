import logging
from decimal import Decimal
from pathlib import Path

import pytest

from tests.conftest import CriarCSV
from vendas_cli.parser import CSVInvalidoError, ler_vendas

CABECALHO = "data,produto,quantidade,preco_unitario\n"


def test_le_vendas_validas(criar_csv: CriarCSV) -> None:
    caminho = criar_csv(CABECALHO + "2025-01-15,Notebook,2,3500.00\n")

    vendas = ler_vendas(caminho)

    assert len(vendas) == 1
    assert vendas[0].produto == "Notebook"
    assert vendas[0].total == Decimal("7000.00")


def test_aceita_cabecalho_flexivel(criar_csv: CriarCSV) -> None:
    caminho = criar_csv(" PRODUTO ,Data,preco_unitario,quantidade,obs\nMouse,2025-01-01,10,3,x\n")

    vendas = ler_vendas(caminho)

    assert vendas[0].produto == "Mouse"
    assert vendas[0].quantidade == 3


@pytest.mark.parametrize(
    ("linha", "motivo"),
    [
        ("2025-13-01,Mouse,1,10", "data inválida"),
        ("2025-01-01,Mouse,abc,10", "quantidade inválida"),
        ("2025-01-01,Mouse,0,10", "quantidade deve ser positiva"),
        ("2025-01-01,Mouse,1,abc", "preço inválido"),
        ("2025-01-01,Mouse,1,-5", "preço não pode ser negativo"),
        ("2025-01-01,,1,10", "produto vazio"),
        ("2025-01-01,Mouse", "Linha 2 ignorada"),
    ],
)
def test_ignora_linha_invalida_e_registra_aviso(
    criar_csv: CriarCSV, caplog: pytest.LogCaptureFixture, linha: str, motivo: str
) -> None:
    caminho = criar_csv(CABECALHO + linha + "\n2025-01-01,Teclado,1,10\n")

    with caplog.at_level(logging.WARNING):
        vendas = ler_vendas(caminho)

    assert [v.produto for v in vendas] == ["Teclado"]
    assert motivo in caplog.text


def test_arquivo_inexistente(tmp_path: Path) -> None:
    with pytest.raises(CSVInvalidoError, match="não encontrado"):
        ler_vendas(tmp_path / "nao_existe.csv")


def test_arquivo_vazio(criar_csv: CriarCSV) -> None:
    with pytest.raises(CSVInvalidoError, match="vazio"):
        ler_vendas(criar_csv(""))


def test_coluna_obrigatoria_ausente(criar_csv: CriarCSV) -> None:
    with pytest.raises(CSVInvalidoError, match="preco_unitario, quantidade"):
        ler_vendas(criar_csv("data,produto\n2025-01-01,Mouse\n"))
