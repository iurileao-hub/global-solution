# src/monitor/alerts.py
"""Alertas operacionais: regras lógicas, severidade, fila de prioridade e
pilha de eventos críticos (GS §8.3, §8.4).

evaluate_alerts() é PURA (snapshot dict → lista de Alert) e usa AND/OR/NOT
explícitos. Expressão booleana principal do diagnóstico crítico:

    CRÍTICO = (consumo > geração) ∧ (bateria_baixa ∨ vital_quebrado) ∧ ¬em_recuperação

com em_recuperação ≡ slope > 0. A fila/pilha apenas ordenam e exibem —
separar regra de apresentação torna o diagnóstico inspecionável.
"""
from dataclasses import dataclass

from monitor.structures import Queue, Stack

SEVERITY_ORDER = {"CRÍTICO": 0, "ALERTA": 1, "NORMAL": 2}

# Módulos Vital na árvore de criticidade da Fase 3: Command, ECLSS, Habitat, Medical.
VITAL_MODULE_IDS = (1, 2, 3, 7)
LOW_BATTERY_PCT = 40.0
STEEP_NEGATIVE_SLOPE = -2.0
STORM_ALERT_LEVELS = ("moderate", "severe")


@dataclass
class Alert:
    severity: str          # CRÍTICO | ALERTA | NORMAL
    code: str
    message: str
    recommendation: str
    source: str
    step: int


def _vital_broken(modules_ok: dict) -> bool:
    return any(modules_ok.get(mid, 1) == 0 for mid in VITAL_MODULE_IDS)


def evaluate_alerts(snapshot: dict) -> list[Alert]:
    """Snapshot → lista de Alert. Função pura, regras com AND/OR/NOT."""
    consumption = snapshot["consumption_kw"]
    generation = snapshot["generation_kw"]
    battery_pct = snapshot["battery_pct"]
    slope = snapshot["slope"]
    storm = snapshot["storm"]
    step = snapshot["step"]
    modules_ok = snapshot["modules_ok"]

    low_battery = battery_pct < LOW_BATTERY_PCT
    vital_broken = _vital_broken(modules_ok)
    in_recovery = slope > 0.0

    alerts = []

    # Regra 1 (CRÍTICO) — expressão booleana principal
    if (consumption > generation) and (low_battery or vital_broken) and (not in_recovery):
        alerts.append(Alert(
            "CRÍTICO", "ENERGY_DEFICIT",
            "Déficit energético com risco vital",
            "Manter Vital e Comunicação; desligar Expansão (Lab, Oficina, Logística)",
            "energy", step))

    # Regra 2 (ALERTA) — bateria baixa OU tendência fortemente negativa
    if low_battery or (slope <= STEEP_NEGATIVE_SLOPE):
        alerts.append(Alert(
            "ALERTA", "LOW_ENERGY",
            "Energia baixa ou tendência de queda acentuada",
            "Ativar modo economia; reduzir consumo dos módulos de Expansão",
            "prediction", step))

    # Regra 3 (ALERTA) — tempestade relevante E NÃO há falha vital concorrente
    if (storm in STORM_ALERT_LEVELS) and (not vital_broken):
        alerts.append(Alert(
            "ALERTA", "CLIMATE",
            f"Tempestade {storm}: geração solar comprometida",
            "Priorizar Vital e Sustento; apoiar-se em nuclear e bateria",
            "climate", step))

    # Regra 4 (CRÍTICO) — módulo vital fora de operação
    if vital_broken:
        alerts.append(Alert(
            "CRÍTICO", "VITAL_FAILURE",
            "Módulo vital fora de operação",
            "Acionar auto-reparo; redirecionar energia ao módulo vital afetado",
            "failure", step))

    if not alerts:
        alerts.append(Alert(
            "NORMAL", "OK", "Operação nominal",
            "Manter monitoramento", "system", step))
    return alerts


class AlertQueue:
    """Fila de prioridade sobre a Queue FIFO: uma raia por severidade,
    drenada CRÍTICO→ALERTA→NORMAL, preservando a ordem de chegada na raia."""

    def __init__(self) -> None:
        self._lanes = {sev: Queue() for sev in SEVERITY_ORDER}

    def add(self, alert: Alert) -> None:
        self._lanes[alert.severity].enqueue(alert)

    def add_all(self, alerts: list[Alert]) -> None:
        for a in alerts:
            self.add(a)

    def drain(self) -> list[Alert]:
        out = []
        for sev in sorted(self._lanes, key=lambda s: SEVERITY_ORDER[s]):
            lane = self._lanes[sev]
            while not lane.is_empty():
                out.append(lane.dequeue())
        return out

    def __len__(self) -> int:
        return sum(len(q) for q in self._lanes.values())


class CriticalEventStack:
    """Pilha LIFO dos últimos eventos críticos analisados."""

    def __init__(self) -> None:
        self._stack = Stack()

    def push_event(self, alert: Alert) -> None:
        self._stack.push(alert)

    def recent(self, n: int) -> list[Alert]:
        return self._stack.top_n(n)

    def __len__(self) -> int:
        return len(self._stack)
