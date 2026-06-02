# src/monitor/report.py
"""Composição do relatório operacional (camada de view).

Monta o view-model a partir da telemetria (motor + estruturas) e renderiza
cada seção via render.py. Nenhuma função imprime: compose_report() devolve a
string final; sistema.main() faz o único print.
"""
from collections import Counter

from engine.hierarchies import build_criticality_tree
from engine.prediction import linear_regression, predict
from monitor import render as r
from monitor.alerts import (
    AlertQueue, CriticalEventStack, VITAL_MODULE_IDS,
    diagnostic_terms, evaluate_alerts,
)
from monitor.matrix import ReadingsMatrix
from monitor.rubric import CRITERIOS, por_id
from monitor.telemetry_io import (
    CRITICAL_MODULE_IDS, build_event_log, detect_inconsistencies,
)

WIDTH = 64
PREDICTION_WINDOW = 12
MATRIX_VARS = ["temperature_c", "wind_ms", "generation_kw", "consumption_kw", "battery_pct"]

_TIER_COLOR = {"CRÍTICO": "red", "ALERTA": "yellow", "NORMAL": "green"}
_NIVEL_PT = {"Vital": "Vital", "Sustenance": "Sustento", "Expansion": "Expansão"}


def _status_tier(energy_level: str) -> str:
    return {"CRITICAL": "CRÍTICO", "LOW": "ALERTA"}.get(energy_level, "NORMAL")


# --- view-model (montagem; não imprime) ---

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


def predict_next_reserve(telemetry: list[dict]) -> tuple[float, float]:
    """OLS de battery_pct vs step na janela recente → (reserva_prevista, slope).

    Pré-condição: telemetry deve ter pelo menos 2 registros (linear_regression
    levanta ValueError caso contrário). No fluxo real a telemetria tem 336
    registros, portanto essa condição é sempre satisfeita.
    """
    window = telemetry[-PREDICTION_WINDOW:]
    xs = [rec["step"] for rec in window]
    ys = [rec["battery_pct"] for rec in window]
    a, b = linear_regression(xs, ys)
    next_step = telemetry[-1]["step"] + 1
    return predict(a, b, next_step), a


# --- seções A ---

def render_header(final: dict) -> list[str]:
    tier = _status_tier(final["energy_level"])
    title = "AURORA SIGER · MONITORAMENTO OPERACIONAL DA COLÔNIA"
    sub = f"sol {final['sol']} · {final['hour']:02d}h · passo {final['step']}   status: "
    line = r.rule(WIDTH)
    return [line, "  " + r.c(title, "bold"),
            "  " + r.c(sub, "gray") + r.badge(tier, _TIER_COLOR[tier]), line]


def render_interpretacao(issues: list[dict], matrix: ReadingsMatrix) -> list[str]:
    cr = por_id("interpretacao")
    lines = []
    if issues:
        for i in issues:
            lines.append(r.c("  anomalia:", "yellow")
                         + f" passo {i['step']} · {i['field']}={i['value']} — {i['reason']}")
    else:
        lines.append("  nenhuma anomalia detectada")
    lines.append(r.kv("matriz", f"{matrix.n_hours()} horas {r.glyphs()['times']} "
                                 f"{matrix.n_variables()} variáveis"))
    sep = r.glyphs()["middot"]
    lines.append(r.kv("variáveis", sep.join(
        ["temp", "vento", "geração", "consumo", "bateria"])))
    return r.box("INTERPRETAÇÃO", lines, tag=cr.tag, width=WIDTH)


def render_estruturas(matrix: ReadingsMatrix, queue_len: int, stack_len: int,
                      tree) -> list[str]:
    cr = por_id("estruturas")
    g = r.glyphs()
    niveis = g["middot"].join(_NIVEL_PT.get(ch.name, ch.name) for ch in tree.children)
    lines = [
        r.kv("matriz", f"{matrix.n_hours()}{g['times']}{matrix.n_variables()} (lista de listas)"),
        r.kv("fila (Queue)", f"{queue_len} alertas — FIFO por severidade"),
        r.kv("pilha (Stack)", f"{stack_len} eventos críticos — LIFO"),
        r.kv("dicionário", f"{len(tree.leaves())} módulos — acesso O(1) por id"),
        r.kv("árvore N-ária", f"criticidade: {niveis} (profund. {tree.depth()})"),
    ]
    return r.box("ESTRUTURAS", lines, tag=cr.tag, width=WIDTH)
