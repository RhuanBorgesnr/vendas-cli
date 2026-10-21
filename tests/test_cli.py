import json
import logging

import pytest

from tests.conftest import CriarCSV
from vendas_cli.cli import main

CSV = (
    "data,produto,quantidade,preco_unitario\n"
    "2025-01-15,Notebook,2,3500.00\n"
    "2025-04-10,Teclado,5,150.00\n"
)


def test_cli_texto(criar_csv: CriarCSV, capsys: pytest.CaptureFixture[str]) -> None:
    codigo = main([str(criar_csv(CSV))])

    assert codigo == 0
    assert "Total geral: R$ 7750.00" in capsys.readouterr().out


def test_cli_json_com_filtro(criar_csv: CriarCSV, capsys: pytest.CaptureFixture[str]) -> None:
    codigo = main(
        [str(criar_csv(CSV)), "--format", "json", "--start", "2025-01-01", "--end", "2025-03-31"]
    )

    dados = json.loads(capsys.readouterr().out)
    assert codigo == 0
    assert dados["total_geral"] == "7000.00"


def test_cli_log_nao_suja_saida(
    criar_csv: CriarCSV, capsys: pytest.CaptureFixture[str], caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        main([str(criar_csv(CSV)), "--format", "json", "-v"])

    json.loads(capsys.readouterr().out)
    assert "vendas válidas lidas" in caplog.text


def test_cli_arquivo_inexistente(caplog: pytest.LogCaptureFixture) -> None:
    assert main(["nao_existe.csv"]) == 1
    assert "não encontrado" in caplog.text


def test_cli_intervalo_invertido(criar_csv: CriarCSV) -> None:
    assert main([str(criar_csv(CSV)), "--start", "2025-05-01", "--end", "2025-01-01"]) == 1


@pytest.mark.parametrize("args", [["--start", "2025-99-01"], ["--format", "xml"]])
def test_cli_parametro_invalido(criar_csv: CriarCSV, args: list[str]) -> None:
    with pytest.raises(SystemExit) as erro:
        main([str(criar_csv(CSV)), *args])

    assert erro.value.code == 2
