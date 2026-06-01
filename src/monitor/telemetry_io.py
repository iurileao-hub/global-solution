"""I/O de telemetria, inconsistência proposital e log de eventos (GS §7, §8.1).

export_run() roda o simulador determinístico (Fase 3) hora a hora, captura o
status operacional binário dos módulos críticos e serializa tudo em CSV,
plantando UMA inconsistência proposital. read_telemetry() lê de volta com
coerção de tipos. detect_inconsistencies() valida faixas de segurança e
invariantes físicas. build_event_log() deriva os eventos da operação.
"""
import csv

from engine.constants import TOTAL_STEPS, HOURS_PER_SOL, BATTERY_CAPACITY_KWH
from engine.failures import is_operational
from engine.modules import find_module
from engine.simulator import init_simulation, step

# Módulos críticos cujo status binário entra no CSV (§7: ≥6 módulos).
# 1=Command, 2=Life Support, 3=Habitat, 7=Medical, 6=Communications, 8=Food.
CRITICAL_MODULE_IDS = (1, 2, 3, 7, 6, 8)

FIELDNAMES = [
    "step", "sol", "hour", "temperature_c", "wind_ms", "tau", "storm",
    "solar_kw", "wind_kw", "nuclear_kw", "generation_kw", "consumption_kw",
    "battery_kwh", "battery_pct", "broken_count", "energy_level",
    "slope", "predicted_delta",
] + [f"mod{mid}_ok" for mid in CRITICAL_MODULE_IDS]

_INT_FIELDS = {"step", "sol", "hour", "broken_count"} | {f"mod{m}_ok" for m in CRITICAL_MODULE_IDS}
_STR_FIELDS = {"storm", "energy_level"}

STORM_LEVELS = ("clear", "light", "moderate", "severe")
INCONSISTENCY_STEP = 50
INCONSISTENCY_BATTERY_PCT = 142.0


def _record(history, idx):
    """Extrai os campos de um passo do histórico pelo índice."""
    battery_kwh = history["battery_charge_kwh"][idx]
    return {
        "step": idx,
        "sol": idx // HOURS_PER_SOL,
        "hour": idx % HOURS_PER_SOL,
        "temperature_c": round(history["temperature_c"][idx], 3),
        "wind_ms": round(history["wind_ms"][idx], 3),
        "tau": round(history["tau"][idx], 3),
        "storm": history["storm"][idx],
        "solar_kw": round(history["solar_generation_kw"][idx], 3),
        "wind_kw": round(history["wind_generation_kw"][idx], 3),
        "nuclear_kw": round(history["nuclear_generation_kw"][idx], 3),
        "generation_kw": round(history["total_generation_kw"][idx], 3),
        "consumption_kw": round(history["total_consumption_kw"][idx], 3),
        "battery_kwh": round(battery_kwh, 3),
        "battery_pct": round(battery_kwh / BATTERY_CAPACITY_KWH * 100.0, 2),
        "broken_count": history["broken_count"][idx],
        "energy_level": history["energy_level"][idx],
        "slope": round(history["slope"][idx], 4),
        "predicted_delta": round(history["predicted_delta"][idx], 4),
    }


def inject_inconsistency(rows: list[dict]) -> list[dict]:
    """Planta UMA inconsistência proposital documentada (§7): bateria% > 100."""
    if len(rows) > INCONSISTENCY_STEP:
        rows[INCONSISTENCY_STEP]["battery_pct"] = INCONSISTENCY_BATTERY_PCT
    return rows


def export_run(path: str, seed: int = 42, horizon: int = TOTAL_STEPS) -> list[dict]:
    """Roda o simulador hora a hora, grava CSV com inconsistência plantada.

    Retorna a lista de dicts (rows) para uso imediato sem re-leitura.
    """
    state = init_simulation(seed)
    history = state["history"]
    rows = []
    for idx in range(horizon):
        step(state)
        rec = _record(history, idx)
        for mid in CRITICAL_MODULE_IDS:
            rec[f"mod{mid}_ok"] = 1 if is_operational(find_module(mid)) else 0
        rows.append(rec)
    rows = inject_inconsistency(rows)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return rows


def read_telemetry(path: str) -> list[dict]:
    """Lê o CSV de telemetria com coerção de tipos (int/float/str)."""
    rows = []
    with open(path, newline="") as f:
        for raw in csv.DictReader(f):
            rec = {}
            for k, v in raw.items():
                if k in _STR_FIELDS:
                    rec[k] = v
                elif k in _INT_FIELDS:
                    rec[k] = int(v)
                else:
                    rec[k] = float(v)
            rows.append(rec)
    return rows


def detect_inconsistencies(rows: list[dict]) -> list[dict]:
    """Valida faixas de segurança e invariantes físicas; retorna lista de issues."""
    issues = []
    for r in rows:
        if not (0.0 <= r["battery_pct"] <= 100.0):
            issues.append({
                "step": r["step"],
                "field": "battery_pct",
                "value": r["battery_pct"],
                "reason": "fora de [0, 100] %",
            })
        if r["generation_kw"] < 0 or r["consumption_kw"] < 0:
            issues.append({
                "step": r["step"],
                "field": "energia",
                "value": (r["generation_kw"], r["consumption_kw"]),
                "reason": "geração/consumo negativo",
            })
        if r["storm"] not in STORM_LEVELS:
            issues.append({
                "step": r["step"],
                "field": "storm",
                "value": r["storm"],
                "reason": "nível de tempestade inválido",
            })
    return issues


def build_event_log(rows: list[dict]) -> list[dict]:
    """Deriva eventos operacionais a partir das transições no histórico.

    Registra: falhas e auto-reparos de módulos críticos, início de tempestades,
    transições de nível de energia (degradações E recuperações).
    """
    events = []
    prev = None
    for r in rows:
        if prev is not None:
            # Falhas e auto-reparos de módulos críticos
            for mid in CRITICAL_MODULE_IDS:
                col = f"mod{mid}_ok"
                if prev[col] == 1 and r[col] == 0:
                    events.append({
                        "step": r["step"],
                        "type": "FALHA",
                        "message": f"Módulo {mid} ({find_module(mid)['name']}) fora de operação",
                    })
                elif prev[col] == 0 and r[col] == 1:
                    events.append({
                        "step": r["step"],
                        "type": "AUTO-REPARO",
                        "message": f"Módulo {mid} ({find_module(mid)['name']}) restaurado",
                    })
            # Início de tempestade
            if prev["storm"] == "clear" and r["storm"] != "clear":
                events.append({
                    "step": r["step"],
                    "type": "CLIMA",
                    "message": f"Tempestade iniciada (nível {r['storm']})",
                })
            # Transições de nível de energia (degradações E recuperações)
            if prev["energy_level"] != r["energy_level"]:
                events.append({
                    "step": r["step"],
                    "type": "ENERGIA",
                    "message": (
                        f"Nível de energia alterado: {prev['energy_level']}"
                        f" → {r['energy_level']}"
                    ),
                })
        prev = r
    return events
