import logging
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from vendas_cli.models import Venda

logger = logging.getLogger(__name__)

__all__ = ["Relatorio", "ResumoProduto", "filtrar_por_data", "gerar_relatorio"]


@dataclass(frozen=True)
class ResumoProduto:
    produto: str
    quantidade: int
    total: Decimal


@dataclass(frozen=True)
class Relatorio:
    produtos: list[ResumoProduto]
    total_geral: Decimal
    mais_vendido: ResumoProduto | None


def filtrar_por_data(
    vendas: Iterable[Venda], inicio: date | None = None, fim: date | None = None
) -> list[Venda]:
    """Mantém as vendas dentro do intervalo [inicio, fim], com as duas pontas inclusas."""
    if inicio and fim and inicio > fim:
        raise ValueError(f"Data inicial {inicio} é posterior à final {fim}")

    filtradas = [
        v
        for v in vendas
        if (inicio is None or v.data >= inicio) and (fim is None or v.data <= fim)
    ]
    logger.info("%d vendas no período", len(filtradas))
    return filtradas


def gerar_relatorio(vendas: Iterable[Venda]) -> Relatorio:
    """Agrupa por produto e calcula total geral e produto mais vendido."""
    quantidades: dict[str, int] = defaultdict(int)
    totais: dict[str, Decimal] = defaultdict(Decimal)

    for venda in vendas:
        quantidades[venda.produto] += venda.quantidade
        totais[venda.produto] += venda.total

    produtos = sorted(
        (ResumoProduto(p, quantidades[p], totais[p]) for p in totais),
        key=lambda r: r.total,
        reverse=True,
    )
    total_geral = sum((r.total for r in produtos), Decimal("0"))
    mais_vendido = max(produtos, key=lambda r: (r.quantidade, r.total), default=None)

    return Relatorio(produtos=produtos, total_geral=total_geral, mais_vendido=mais_vendido)
