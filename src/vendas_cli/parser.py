import csv
import logging
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from vendas_cli.models import Venda

logger = logging.getLogger(__name__)

__all__ = ["CSVInvalidoError", "ler_vendas"]

COLUNAS_OBRIGATORIAS: frozenset[str] = frozenset(
    {"data", "produto", "quantidade", "preco_unitario"}
)


class CSVInvalidoError(Exception):
    """Erro fatal: o arquivo não pode ser processado."""


def _normalizar(nome: str) -> str:
    return nome.strip().lower()


def _converter_linha(linha: dict[str, str]) -> Venda:
    """Converte uma linha do CSV em Venda. Lança ValueError se inválida."""
    produto = linha["produto"].strip()
    if not produto:
        raise ValueError("produto vazio")

    try:
        data = date.fromisoformat(linha["data"].strip())
    except ValueError as exc:
        raise ValueError(f"data inválida (use AAAA-MM-DD): {linha['data']!r}") from exc

    try:
        quantidade = int(linha["quantidade"].strip())
    except ValueError as exc:
        raise ValueError(f"quantidade inválida: {linha['quantidade']!r}") from exc
    if quantidade <= 0:
        raise ValueError(f"quantidade deve ser positiva: {quantidade}")

    try:
        preco = Decimal(linha["preco_unitario"].strip())
    except InvalidOperation as exc:
        raise ValueError(f"preço inválido: {linha['preco_unitario']!r}") from exc
    if preco < 0:
        raise ValueError(f"preço não pode ser negativo: {preco}")

    return Venda(data=data, produto=produto, quantidade=quantidade, preco_unitario=preco)


def ler_vendas(caminho: Path) -> list[Venda]:
    """Lê o CSV e devolve as vendas válidas.

    Linhas inválidas são ignoradas com um aviso no log.
    Problemas no arquivo como um todo lançam CSVInvalidoError.
    """
    if not caminho.is_file():
        raise CSVInvalidoError(f"Arquivo não encontrado: {caminho}")

    logger.info("Lendo arquivo %s", caminho)
    vendas: list[Venda] = []

    with caminho.open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        if leitor.fieldnames is None:
            raise CSVInvalidoError("Arquivo vazio ou sem cabeçalho")

        leitor.fieldnames = [_normalizar(c) for c in leitor.fieldnames]
        ausentes = COLUNAS_OBRIGATORIAS - set(leitor.fieldnames)
        if ausentes:
            raise CSVInvalidoError(
                f"Colunas obrigatórias ausentes: {', '.join(sorted(ausentes))}"
            )

        for numero, linha in enumerate(leitor, start=2):
            try:
                vendas.append(_converter_linha(linha))
            except (ValueError, TypeError, AttributeError) as exc:
                logger.warning("Linha %d ignorada: %s", numero, exc)

    logger.info("%d vendas válidas lidas", len(vendas))
    return vendas
