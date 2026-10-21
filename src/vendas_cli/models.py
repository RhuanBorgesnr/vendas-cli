from dataclasses import dataclass
from datetime import date
from decimal import Decimal

__all__ = ["Venda"]


@dataclass(frozen=True)
class Venda:
    """Uma linha de venda já validada."""

    data: date
    produto: str
    quantidade: int
    preco_unitario: Decimal

    @property
    def total(self) -> Decimal:
        """Valor total da venda (quantidade x preço unitário)."""
        return self.preco_unitario * self.quantidade
