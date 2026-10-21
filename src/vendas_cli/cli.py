import argparse
import logging
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from vendas_cli.core import filtrar_por_data, gerar_relatorio
from vendas_cli.output import formatar
from vendas_cli.parser import CSVInvalidoError, ler_vendas

logger = logging.getLogger(__name__)

__all__ = ["criar_parser", "main"]


def _data(texto: str) -> date:
    try:
        return date.fromisoformat(texto)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"data inválida: {texto!r} (use AAAA-MM-DD)"
        ) from exc


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vendas-cli",
        description="Gera relatórios de vendas a partir de um arquivo CSV.",
    )
    parser.add_argument("arquivo", type=Path, help="caminho do arquivo CSV de vendas")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="formato de saída (padrão: text)"
    )
    parser.add_argument("--start", type=_data, help="data inicial, inclusiva (AAAA-MM-DD)")
    parser.add_argument("--end", type=_data, help="data final, inclusiva (AAAA-MM-DD)")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="mostra logs detalhados (nível INFO)"
    )
    return parser


def _configurar_log(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(levelname)s [%(name)s] %(message)s",
        stream=sys.stderr,
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = criar_parser().parse_args(argv)
    _configurar_log(args.verbose)

    try:
        vendas = ler_vendas(args.arquivo)
        vendas = filtrar_por_data(vendas, args.start, args.end)
    except (CSVInvalidoError, ValueError) as exc:
        logger.error("%s", exc)
        return 1

    print(formatar(gerar_relatorio(vendas), args.format))
    return 0


if __name__ == "__main__":
    sys.exit(main())
