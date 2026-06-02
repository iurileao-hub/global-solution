# src/sistema.py
"""Sistema inteligente de monitoramento — Global Solution FIAP 2026-1.

Ponto único de execução: lê a telemetria de data/dados.csv (gerando-a na
primeira execução) e imprime o relatório operacional rico. Toda a montagem do
relatório vive em monitor.report; este arquivo só orquestra (load → print).

Uso: python src/sistema.py
"""
import os
import sys

# Torna engine/ e monitor/ importáveis ao rodar o arquivo diretamente.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitor.report import compose_report          # noqa: E402
from monitor.telemetry_io import export_run, read_telemetry  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.environ.get("GS_DATA_PATH", os.path.join(_HERE, "..", "data", "dados.csv"))


def load_telemetry() -> list[dict]:
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        export_run(DATA_PATH)
    return read_telemetry(DATA_PATH)


def main() -> None:
    # Rede de segurança: em stdout não-UTF-8 (ex. cp1252), caracteres fora do
    # encoding viram '?' em vez de derrubar o programa (protege "roda sem erros").
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    print(compose_report(load_telemetry()))


if __name__ == "__main__":
    main()
