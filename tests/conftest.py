from collections.abc import Callable
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from vendas_cli.models import Venda

CriarCSV = Callable[[str], Path]


@pytest.fixture
def criar_csv(tmp_path: Path) -> CriarCSV:
    def _criar(conteudo: str) -> Path:
        caminho = tmp_path / "vendas.csv"
        caminho.write_text(conteudo, encoding="utf-8")
        return caminho

    return _criar


@pytest.fixture
def vendas() -> list[Venda]:
    return [
        Venda(date(2025, 1, 15), "Notebook", 2, Decimal("3500.00")),
        Venda(date(2025, 2, 3), "Mouse", 10, Decimal("80.50")),
        Venda(date(2025, 3, 20), "Notebook", 1, Decimal("3500.00")),
        Venda(date(2025, 4, 10), "Teclado", 5, Decimal("150.00")),
    ]
