# src/sistema.py
"""Sistema inteligente de monitoramento — Global Solution FIAP 2026-1.

Ponto único de execução: lê a telemetria de data/dados.csv (gerando-a na
primeira execução), organiza em estruturas (matriz, fila, pilha), aplica
regras lógicas + previsão OLS e imprime o relatório operacional textual.

Uso: python src/sistema.py
"""
import os
import sys
from collections import Counter

# Torna engine/ e monitor/ importáveis ao rodar o arquivo diretamente.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.modules import find_module                       # noqa: E402
from engine.prediction import linear_regression, predict     # noqa: E402
from monitor.alerts import evaluate_alerts, AlertQueue, CriticalEventStack  # noqa: E402
from monitor.matrix import ReadingsMatrix                     # noqa: E402
from monitor.telemetry_io import (                            # noqa: E402
    export_run, read_telemetry, detect_inconsistencies, build_event_log,
    CRITICAL_MODULE_IDS,
)

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.environ.get("GS_DATA_PATH", os.path.join(_HERE, "..", "data", "dados.csv"))
PREDICTION_WINDOW = 12


def load_telemetry() -> list:
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        export_run(DATA_PATH)
    return read_telemetry(DATA_PATH)


def build_snapshot(rec: dict) -> dict:
    return {
        "step": rec["step"],
        "consumption_kw": rec["consumption_kw"],
        "generation_kw": rec["generation_kw"],
        "battery_pct": rec["battery_pct"],
        "slope": rec["slope"],
        "storm": rec["storm"],
        "modules_ok": {mid: rec[f"mod{mid}_ok"] for mid in CRITICAL_MODULE_IDS},
    }


def predict_next_reserve(telemetry: list) -> tuple:
    """OLS sobre battery_pct vs step na janela recente → reserva no próximo ciclo.

    linear_regression(xs, ys) retorna (a, b) com a=slope, b=intercept (y=a*x+b).
    predict(a, b, x) = a*x + b.
    """
    window = telemetry[-PREDICTION_WINDOW:]
    xs = [r["step"] for r in window]
    ys = [r["battery_pct"] for r in window]
    a, b = linear_regression(xs, ys)
    next_step = telemetry[-1]["step"] + 1
    return predict(a, b, next_step), a


def _status_tier(level: str) -> str:
    if level == "CRITICAL":
        return "CRÍTICO"
    if level == "LOW":
        return "ALERTA"
    return "NORMAL"


def _representative_events(events: list, n: int = 12) -> list:
    """Seleciona até `n` eventos priorizando FALHA/AUTO-REPARO/CLIMA sobre
    ENERGIA, para um log mais informativo.  Preserva a ordem cronológica."""
    priority = [e for e in events if e["type"] in ("FALHA", "AUTO-REPARO", "CLIMA")]
    energia = [e for e in events if e["type"] == "ENERGIA"]
    # combina: priority primeiro, completa com ENERGIA na ordem cronológica
    combined = priority + energia
    # manter ordem cronológica dentro do resultado
    selected = sorted(combined[:n], key=lambda e: e["step"])
    return selected


def print_report(telemetry: list) -> None:
    final = telemetry[-1]

    print("=" * 64)
    print("AURORA SIGER — MONITORAMENTO OPERACIONAL DA COLÔNIA")
    print("=" * 64)

    # Inconsistência (§3/§8.1)
    issues = detect_inconsistencies(telemetry)
    print("\n[INCONSISTÊNCIA NOS DADOS]")
    if issues:
        for i in issues:
            print(f"  passo {i['step']}: {i['field']}={i['value']} — {i['reason']}")
    else:
        print("  nenhuma anomalia detectada")

    # Matriz [hora × variável] (§8.2)
    matrix = ReadingsMatrix.from_telemetry(
        telemetry, ["temperature_c", "wind_ms", "generation_kw", "consumption_kw", "battery_pct"])
    print(f"\n[MATRIZ DE LEITURAS]  {matrix.n_hours()} horas × {matrix.n_variables()} variáveis")
    print("  variáveis:", ", ".join(matrix.variables))

    # Diagnóstico atual (§8.3)
    tier = _status_tier(final["energy_level"])
    print("\n[DIAGNÓSTICO]")
    print(f"  passo {final['step']} (sol {final['sol']}, hora {final['hour']}h)")
    print(f"  bateria: {final['battery_pct']:.1f}%  |  nível de energia: {final['energy_level']}  ⇒  {tier}")
    print(f"  geração: {final['generation_kw']:.1f} kW  |  consumo: {final['consumption_kw']:.1f} kW")
    for mid in CRITICAL_MODULE_IDS:
        st = "OK" if final[f"mod{mid}_ok"] else "FALHA"
        print(f"    módulo {mid} {find_module(mid)['name']}: {st}")

    # Previsão (§8.5) — influencia a recomendação
    next_reserve, slope = predict_next_reserve(telemetry)
    print("\n[PREVISÃO]")
    print(f"  tendência (slope OLS): {slope:+.3f} %/passo")
    print(f"  reserva prevista no próximo ciclo: {next_reserve:.1f}%")
    if next_reserve < 40.0:
        print("  → previsão aciona recomendação: ativar modo economia preventivo")

    # Alertas priorizados (§8.4) — fila de prioridade
    queue = AlertQueue()
    queue.add_all(evaluate_alerts(build_snapshot(final)))
    print("\n[ALERTAS PRIORIZADOS]")
    for a in queue.drain():
        print(f"  [{a.severity}] {a.message}")
        print(f"        ↳ recomendação: {a.recommendation}")

    # Pilha dos últimos eventos críticos analisados (§8.2)
    stack = CriticalEventStack()
    for rec in telemetry:
        for a in evaluate_alerts(build_snapshot(rec)):
            if a.severity == "CRÍTICO":
                stack.push_event(a)
    print(f"\n[EVENTOS CRÍTICOS]  {len(stack)} no total — últimos analisados:")
    for a in stack.recent(5):
        print(f"  passo {a.step}: {a.code} — {a.message}")

    # Log de eventos da operação (§7)
    events = build_event_log(telemetry)
    shown = _representative_events(events, 12)
    # contagem por tipo para contexto
    counts = Counter(e["type"] for e in events)
    summary = "  ".join(f"{t}:{n}" for t, n in sorted(counts.items()))
    print(f"\n[LOG DE EVENTOS]  {len(events)} registros ({summary}):")
    for e in shown:
        print(f"  passo {e['step']} [{e['type']}] {e['message']}")

    print("\n" + "=" * 64)


def main() -> None:
    telemetry = load_telemetry()
    print_report(telemetry)


if __name__ == "__main__":
    main()
