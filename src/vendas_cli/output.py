import json
from decimal import Decimal
from typing import Any, Literal

from vendas_cli.core import Relatorio

__all__ = ["Formato", "formatar", "formatar_json", "formatar_texto", "para_dict"]

Formato = Literal["text", "json"]


def _dinheiro(valor: Decimal) -> str:
    return str(valor.quantize(Decimal("0.01")))


def para_dict(relatorio: Relatorio) -> dict[str, Any]:
    mais = relatorio.mais_vendido
    return {
        "produtos": [
            {"produto": p.produto, "quantidade": p.quantidade, "total": _dinheiro(p.total)}
            for p in relatorio.produtos
        ],
        "total_geral": _dinheiro(relatorio.total_geral),
        "mais_vendido": (
            {"produto": mais.produto, "quantidade": mais.quantidade} if mais else None
        ),
    }


def formatar_json(relatorio: Relatorio) -> str:
    return json.dumps(para_dict(relatorio), ensure_ascii=False, indent=2)


def formatar_texto(relatorio: Relatorio) -> str:
    if not relatorio.produtos:
        return "Nenhuma venda encontrada no período."

    cabecalho = ("Produto", "Quantidade", "Total (R$)")
    linhas = [(p.produto, str(p.quantidade), _dinheiro(p.total)) for p in relatorio.produtos]

    larguras = [max(len(c) for c in coluna) for coluna in zip(cabecalho, *linhas)]

    def formatar_linha(celulas: tuple[str, ...]) -> str:
        return " | ".join(
            f"{c:<{w}}" if i == 0 else f"{c:>{w}}"
            for i, (c, w) in enumerate(zip(celulas, larguras))
        )

    separador = "-+-".join("-" * w for w in larguras)
    partes = [formatar_linha(cabecalho), separador, *map(formatar_linha, linhas), separador]
    partes.append(f"Total geral: R$ {_dinheiro(relatorio.total_geral)}")
    if relatorio.mais_vendido:
        mv = relatorio.mais_vendido
        partes.append(f"Produto mais vendido: {mv.produto} ({mv.quantidade} unidades)")
    return "\n".join(partes)


def formatar(relatorio: Relatorio, formato: Formato) -> str:
    if formato == "json":
        return formatar_json(relatorio)
    return formatar_texto(relatorio)
