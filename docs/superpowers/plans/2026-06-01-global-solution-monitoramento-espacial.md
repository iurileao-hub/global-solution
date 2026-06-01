# Global Solution — Sistema de Monitoramento Espacial — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Entregar o repo GS-compliant `global-solution` reaproveitando o motor `operations` da Fase 3 do Aurora SIGER (vendado em `src/engine/`) + uma camada nova `src/monitor/` (alertas, fila/pilha, matriz, I/O de telemetria), atingindo nota 10 da rubrica exceto o vídeo.

**Architecture:** `src/engine/` é cópia fiel dos módulos `aurora_siger.operations` (imports reescritos para `engine.*`). `src/monitor/` é código novo, stdlib-only, testado em TDD. `src/sistema.py` orquestra: lê `data/dados.csv` → matriz/previsão/alertas → imprime relatório textual. `pytest` com `pythonpath=["src"]` torna `import engine` / `import monitor` resolvíveis.

**Tech Stack:** Python 3.12 stdlib (`csv`, `dataclasses`, `typing`); `pytest` (dev); pandoc/xelatex (relatório). Sem numpy/sklearn no runtime.

**Fonte do motor:** `~/projects/FIAP-Aurora-Siger/aurora_siger/operations/` e `~/projects/FIAP-Aurora-Siger/tests/`.
**Workspace de trabalho:** `~/projects/global-solution-fiap/` (este repo). O conteúdo final será o repo público `iurileao-hub/global-solution`.

---

## Task 1: Scaffold do repositório

**Files:**
- Create: `src/engine/__init__.py`, `src/monitor/__init__.py`, `tests/__init__.py`
- Create: `pyproject.toml`
- Create: `data/.gitkeep`

- [ ] **Step 1: Criar a árvore de diretórios**

Run:
```bash
cd ~/projects/global-solution-fiap
mkdir -p src/engine src/monitor data tests
touch src/engine/__init__.py src/monitor/__init__.py tests/__init__.py data/.gitkeep
```

- [ ] **Step 2: Criar `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "global-solution"
version = "1.0.0"
description = "Sistema inteligente de monitoramento de missão espacial — Global Solution FIAP 2026-1"
requires-python = ">=3.10"

[project.optional-dependencies]
dev = ["pytest>=8"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

- [ ] **Step 3: Verificar que o pytest coleta (sem testes ainda)**

Run: `cd ~/projects/global-solution-fiap && python -m pytest -q`
Expected: "no tests ran" (exit 5) — confirma que `pyproject.toml` é válido e o `pythonpath` foi aceito.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml src tests data
git commit -m "chore: scaffold do repo global-solution (src/engine, src/monitor, tests)"
```

---

## Task 2: Vendoring do motor `operations` + testes de regressão

**Files:**
- Create: `src/engine/{allocation,climate,constants,consumption,decision,energy_levels,failures,generation,hierarchies,modules,prediction,rng,simulator,state,tree}.py`
- Create: `tests/engine/` (subconjunto dos testes de operations)

- [ ] **Step 1: Copiar os 15 módulos do motor (sem dashboard/cli/simsnapshot/analysis)**

Run:
```bash
cd ~/projects/global-solution-fiap
SRC=~/projects/FIAP-Aurora-Siger/aurora_siger/operations
for m in allocation climate constants consumption decision energy_levels \
         failures generation hierarchies modules prediction rng simulator state tree; do
  cp "$SRC/$m.py" "src/engine/$m.py"
done
ls src/engine/
```
Expected: os 15 arquivos + `__init__.py`.

- [ ] **Step 2: Reescrever os imports `aurora_siger.operations` → `engine`**

Run:
```bash
cd ~/projects/global-solution-fiap
sed -i 's/aurora_siger\.operations/engine/g' src/engine/*.py
grep -rl 'aurora_siger' src/engine/ || echo "OK: nenhuma referência a aurora_siger restante"
```
Expected: "OK: nenhuma referência a aurora_siger restante".

- [ ] **Step 3: Verificar que o motor importa e simula (smoke manual)**

Run:
```bash
cd ~/projects/global-solution-fiap
PYTHONPATH=src python -c "from engine.simulator import run_simulation; c,b,h=run_simulation(seed=42); print('steps:', len(h['total_generation_kw']), 'battery:', round(h['battery_charge_kwh'][-1],1))"
```
Expected: `steps: 168 battery: <algum número>`. Se der `ModuleNotFoundError` para um módulo não-vendado, copie-o também (mesma sed) e repita.

- [ ] **Step 4: Vendorar os testes de regressão do motor**

Run:
```bash
cd ~/projects/global-solution-fiap
mkdir -p tests/engine
touch tests/engine/__init__.py
TSRC=~/projects/FIAP-Aurora-Siger/tests
for t in prediction decision energy_levels tree hierarchies failures \
         simulator climate consumption generation allocation constants rng state modules; do
  cp "$TSRC/test_operations_$t.py" "tests/engine/test_$t.py" 2>/dev/null || true
done
sed -i 's/aurora_siger\.operations/engine/g' tests/engine/*.py
ls tests/engine/
```

- [ ] **Step 5: Rodar os testes do motor**

Run: `cd ~/projects/global-solution-fiap && python -m pytest tests/engine -q`
Expected: todos PASS. Se algum teste importar um módulo não-vendado (dashboard/cli/simsnapshot/analysis), **delete esse arquivo de teste** (`rm tests/engine/test_<x>.py`) — esses módulos estão fora de escopo — e rode de novo até verde.

- [ ] **Step 6: Commit**

```bash
git add src/engine tests/engine
git commit -m "feat(engine): vendoring do motor operations (Fase 3) + testes de regressão"
```

---

## Task 3: `monitor/structures.py` — Fila e Pilha à mão (§8.2)

**Files:**
- Create: `src/monitor/structures.py`
- Test: `tests/test_structures.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_structures.py
import pytest
from monitor.structures import Queue, Stack


def test_queue_is_fifo():
    q = Queue()
    q.enqueue("a"); q.enqueue("b"); q.enqueue("c")
    assert len(q) == 3
    assert q.dequeue() == "a"
    assert q.dequeue() == "b"
    assert q.peek() == "c"
    assert len(q) == 1


def test_queue_empty_raises():
    q = Queue()
    assert q.is_empty()
    with pytest.raises(IndexError):
        q.dequeue()


def test_stack_is_lifo():
    s = Stack()
    s.push(1); s.push(2); s.push(3)
    assert s.pop() == 3
    assert s.peek() == 2
    assert len(s) == 2


def test_stack_top_n_most_recent_first():
    s = Stack()
    for i in range(5):
        s.push(i)
    assert s.top_n(3) == [4, 3, 2]   # não-destrutivo, mais recente primeiro
    assert len(s) == 5


def test_stack_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()
```

- [ ] **Step 2: Rodar — deve falhar**

Run: `python -m pytest tests/test_structures.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'monitor.structures'`.

- [ ] **Step 3: Implementar**

```python
# src/monitor/structures.py
"""Estruturas lineares genéricas, escritas à mão (GS §8.2).

Queue (FIFO) e Stack (LIFO) sobre uma list, implementadas explicitamente
em vez de collections.deque para que a estrutura fique visível e
defensável — a rubrica (§14) pontua a estrutura aplicada e justificada.
Espelha aurora_siger/landing/structures.py da Fase 2.
"""
from typing import Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """Fila First-In-First-Out."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue de fila vazia")
        return self._items.pop(0)

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek de fila vazia")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class Stack(Generic[T]):
    """Pilha Last-In-First-Out."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop de pilha vazia")
        return self._items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek de pilha vazia")
        return self._items[-1]

    def top_n(self, n: int) -> list[T]:
        """Os n itens mais recentes, do mais novo ao mais antigo (não-destrutivo)."""
        return list(reversed(self._items[-n:]))

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)
```

- [ ] **Step 4: Rodar — deve passar**

Run: `python -m pytest tests/test_structures.py -q`
Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add src/monitor/structures.py tests/test_structures.py
git commit -m "feat(monitor): Queue (fila) e Stack (pilha) genéricas à mão"
```

---

## Task 4: `monitor/matrix.py` — Matriz [hora × variável] (§8.2)

**Files:**
- Create: `src/monitor/matrix.py`
- Test: `tests/test_matrix.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_matrix.py
import pytest
from monitor.matrix import ReadingsMatrix

TELEMETRY = [
    {"temperature_c": -60.0, "wind_ms": 3.0, "battery_pct": 50.0},
    {"temperature_c": -55.0, "wind_ms": 5.0, "battery_pct": 48.0},
    {"temperature_c": -58.0, "wind_ms": 4.0, "battery_pct": 47.0},
]


def test_dimensions():
    m = ReadingsMatrix.from_telemetry(TELEMETRY, ["temperature_c", "wind_ms"])
    assert m.n_hours() == 3
    assert m.n_variables() == 2


def test_get_cell():
    m = ReadingsMatrix.from_telemetry(TELEMETRY, ["temperature_c", "wind_ms"])
    assert m.get(1, "wind_ms") == 5.0
    assert m.get(0, "temperature_c") == -60.0


def test_column():
    m = ReadingsMatrix.from_telemetry(TELEMETRY, ["battery_pct"])
    assert m.column("battery_pct") == [50.0, 48.0, 47.0]


def test_rows_is_list_of_lists():
    m = ReadingsMatrix.from_telemetry(TELEMETRY, ["temperature_c", "wind_ms"])
    assert m.rows == [[-60.0, 3.0], [-55.0, 5.0], [-58.0, 4.0]]
```

- [ ] **Step 2: Rodar — deve falhar**

Run: `python -m pytest tests/test_matrix.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'monitor.matrix'`.

- [ ] **Step 3: Implementar**

```python
# src/monitor/matrix.py
"""Matriz [hora × variável] — GS §8.2 (matriz / lista de listas).

Constrói uma matriz 2-D a partir das leituras horárias de telemetria:
uma linha por hora, uma coluna por variável selecionada. Lista-de-listas
pura, sem numpy.
"""


class ReadingsMatrix:
    """Matriz de leituras: rows[hora][variável]."""

    def __init__(self, variables: list[str], rows: list[list[float]]) -> None:
        self.variables = variables
        self.rows = rows

    @classmethod
    def from_telemetry(cls, telemetry: list[dict], variables: list[str]) -> "ReadingsMatrix":
        rows = [[float(rec[v]) for v in variables] for rec in telemetry]
        return cls(variables, rows)

    def get(self, hour_index: int, variable: str) -> float:
        return self.rows[hour_index][self.variables.index(variable)]

    def column(self, variable: str) -> list[float]:
        j = self.variables.index(variable)
        return [row[j] for row in self.rows]

    def n_hours(self) -> int:
        return len(self.rows)

    def n_variables(self) -> int:
        return len(self.variables)
```

- [ ] **Step 4: Rodar — deve passar**

Run: `python -m pytest tests/test_matrix.py -q`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/monitor/matrix.py tests/test_matrix.py
git commit -m "feat(monitor): ReadingsMatrix [hora × variável]"
```

---

## Task 5: `monitor/telemetry_io.py` — I/O, inconsistência e log de eventos (§7, §8.1)

**Files:**
- Create: `src/monitor/telemetry_io.py`
- Test: `tests/test_telemetry_io.py`

**Esquema do CSV (colunas):** `step, sol, hour, temperature_c, wind_ms, tau, storm, solar_kw, wind_kw, nuclear_kw, generation_kw, consumption_kw, battery_kwh, battery_pct, broken_count, energy_level, slope, predicted_delta, mod1_ok, mod2_ok, mod3_ok, mod7_ok, mod6_ok, mod8_ok`.

Os 6 módulos críticos para o status binário (§7) são ids **1, 2, 3, 7, 6, 8**.

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_telemetry_io.py
import pytest
from monitor.telemetry_io import (
    export_run, read_telemetry, detect_inconsistencies, build_event_log,
    CRITICAL_MODULE_IDS,
)


@pytest.fixture
def csv_path(tmp_path):
    p = tmp_path / "dados.csv"
    export_run(str(p), seed=42)
    return str(p)


def test_export_creates_168_rows(csv_path):
    rows = read_telemetry(csv_path)
    assert len(rows) == 168


def test_types_are_coerced(csv_path):
    rows = read_telemetry(csv_path)
    r = rows[0]
    assert isinstance(r["step"], int)
    assert isinstance(r["battery_pct"], float)
    assert isinstance(r["storm"], str)
    assert isinstance(r["mod1_ok"], int)


def test_six_critical_module_columns_present(csv_path):
    rows = read_telemetry(csv_path)
    for mid in CRITICAL_MODULE_IDS:
        assert f"mod{mid}_ok" in rows[0]
        assert rows[0][f"mod{mid}_ok"] in (0, 1)


def test_planted_inconsistency_is_detected(csv_path):
    rows = read_telemetry(csv_path)
    issues = detect_inconsistencies(rows)
    assert len(issues) >= 1
    # a anomalia plantada é uma bateria% fisicamente impossível (>100)
    assert any(i["field"] == "battery_pct" for i in issues)


def test_event_log_has_at_least_8(csv_path):
    rows = read_telemetry(csv_path)
    events = build_event_log(rows)
    assert len(events) >= 8
    assert all({"step", "type", "message"} <= set(e) for e in events)


def test_roundtrip_is_stable(tmp_path):
    p1 = tmp_path / "a.csv"
    p2 = tmp_path / "b.csv"
    export_run(str(p1), seed=42)
    export_run(str(p2), seed=42)
    assert p1.read_text() == p2.read_text()   # determinismo bit-a-bit
```

- [ ] **Step 2: Rodar — deve falhar**

Run: `python -m pytest tests/test_telemetry_io.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'monitor.telemetry_io'`.

- [ ] **Step 3: Implementar**

```python
# src/monitor/telemetry_io.py
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

# Faixas de segurança / invariantes para o validador.
STORM_LEVELS = ("clear", "light", "moderate", "severe")
INCONSISTENCY_STEP = 50            # linha onde a anomalia é plantada
INCONSISTENCY_BATTERY_PCT = 142.0  # bateria% fisicamente impossível (>100)


def _record(history, idx):
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
        "battery_kwh": round(history["battery_charge_kwh"][idx], 3),
        "battery_pct": round(history["battery_charge_kwh"][idx] / BATTERY_CAPACITY_KWH * 100.0, 2),
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
    """Roda a simulação hora a hora, monta as linhas e grava o CSV."""
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
    """Lê o CSV com coerção de tipos (§8.1: leitura de arquivo externo)."""
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
    """Valida faixas de segurança e invariantes; retorna a lista de violações."""
    issues = []
    for r in rows:
        if not (0.0 <= r["battery_pct"] <= 100.0):
            issues.append({"step": r["step"], "field": "battery_pct",
                           "value": r["battery_pct"], "reason": "fora de [0, 100] %"})
        if r["generation_kw"] < 0 or r["consumption_kw"] < 0:
            issues.append({"step": r["step"], "field": "energia",
                           "value": (r["generation_kw"], r["consumption_kw"]),
                           "reason": "geração/consumo negativo"})
        if r["storm"] not in STORM_LEVELS:
            issues.append({"step": r["step"], "field": "storm",
                           "value": r["storm"], "reason": "nível de tempestade inválido"})
    return issues


def build_event_log(rows: list[dict]) -> list[dict]:
    """Deriva eventos da operação (§7: ≥8 registros): falhas, auto-reparos,
    início de tempestade e mudanças de nível de energia."""
    events = []
    prev = None
    for r in rows:
        if prev is not None:
            for mid in CRITICAL_MODULE_IDS:
                col = f"mod{mid}_ok"
                if prev[col] == 1 and r[col] == 0:
                    events.append({"step": r["step"], "type": "FALHA",
                                   "message": f"Módulo {mid} ({find_module(mid)['name']}) fora de operação"})
                elif prev[col] == 0 and r[col] == 1:
                    events.append({"step": r["step"], "type": "AUTO-REPARO",
                                   "message": f"Módulo {mid} ({find_module(mid)['name']}) restaurado"})
            if prev["storm"] == "clear" and r["storm"] != "clear":
                events.append({"step": r["step"], "type": "CLIMA",
                               "message": f"Tempestade iniciada (nível {r['storm']})"})
            if prev["energy_level"] != r["energy_level"] and r["energy_level"] in ("LOW", "CRITICAL"):
                events.append({"step": r["step"], "type": "ENERGIA",
                               "message": f"Nível de energia rebaixado para {r['energy_level']}"})
        prev = r
    return events
```

- [ ] **Step 4: Rodar — deve passar**

Run: `python -m pytest tests/test_telemetry_io.py -q`
Expected: 6 passed. Se `test_event_log_has_at_least_8` falhar (seed produziu <8 eventos), amplie `build_event_log` para também registrar mudanças de nível para `NOMINAL/HIGH/SURPLUS` (recuperações), e rode de novo.

- [ ] **Step 5: Commit**

```bash
git add src/monitor/telemetry_io.py tests/test_telemetry_io.py
git commit -m "feat(monitor): I/O de telemetria, inconsistência proposital e log de eventos"
```

---

## Task 6: `monitor/alerts.py` — Alertas, severidade, fila de prioridade e pilha (§8.3, §8.4)

**Files:**
- Create: `src/monitor/alerts.py`
- Test: `tests/test_alerts.py`

**Expressão booleana principal (vai pro README):**
`CRÍTICO = (consumo > geração) ∧ (bateria_baixa ∨ vital_quebrado) ∧ ¬em_recuperação`, onde `em_recuperação ≡ slope > 0`.

- [ ] **Step 1: Escrever o teste que falha**

```python
# tests/test_alerts.py
from monitor.alerts import Alert, evaluate_alerts, AlertQueue, CriticalEventStack


def _snap(**kw):
    base = {"step": 0, "consumption_kw": 50.0, "generation_kw": 60.0,
            "battery_pct": 70.0, "slope": 0.0, "storm": "clear",
            "modules_ok": {1: 1, 2: 1, 3: 1, 7: 1, 6: 1, 8: 1}}
    base.update(kw)
    return base


def test_nominal_yields_normal_only():
    alerts = evaluate_alerts(_snap())
    assert len(alerts) == 1
    assert alerts[0].severity == "NORMAL"


def test_energy_deficit_is_critical():
    alerts = evaluate_alerts(_snap(consumption_kw=80.0, generation_kw=40.0,
                                   battery_pct=25.0, slope=-1.0))
    codes = {a.code for a in alerts}
    assert "ENERGY_DEFICIT" in codes
    assert any(a.severity == "CRÍTICO" and a.code == "ENERGY_DEFICIT" for a in alerts)


def test_recovery_suppresses_energy_deficit():
    # slope > 0 ⇒ em recuperação ⇒ NOT em_recuperação é falso ⇒ sem ENERGY_DEFICIT
    alerts = evaluate_alerts(_snap(consumption_kw=80.0, generation_kw=40.0,
                                   battery_pct=25.0, slope=1.5))
    assert "ENERGY_DEFICIT" not in {a.code for a in alerts}


def test_vital_failure_is_critical():
    alerts = evaluate_alerts(_snap(modules_ok={1: 1, 2: 0, 3: 1, 7: 1, 6: 1, 8: 1}))
    assert any(a.severity == "CRÍTICO" and a.code == "VITAL_FAILURE" for a in alerts)


def test_storm_alert():
    alerts = evaluate_alerts(_snap(storm="severe"))
    assert any(a.code == "CLIMATE" for a in alerts)


def test_queue_drains_by_priority():
    q = AlertQueue()
    q.add(Alert("NORMAL", "OK", "", "", "system", 0))
    q.add(Alert("CRÍTICO", "X", "", "", "energy", 1))
    q.add(Alert("ALERTA", "Y", "", "", "climate", 2))
    drained = q.drain()
    assert [a.severity for a in drained] == ["CRÍTICO", "ALERTA", "NORMAL"]


def test_queue_fifo_within_severity():
    q = AlertQueue()
    q.add(Alert("ALERTA", "first", "", "", "a", 0))
    q.add(Alert("ALERTA", "second", "", "", "b", 1))
    drained = q.drain()
    assert [a.code for a in drained] == ["first", "second"]


def test_critical_stack_is_lifo():
    s = CriticalEventStack()
    s.push_event(Alert("CRÍTICO", "a", "", "", "x", 0))
    s.push_event(Alert("CRÍTICO", "b", "", "", "x", 1))
    assert [a.code for a in s.recent(2)] == ["b", "a"]
```

- [ ] **Step 2: Rodar — deve falhar**

Run: `python -m pytest tests/test_alerts.py -q`
Expected: FAIL com `ModuleNotFoundError: No module named 'monitor.alerts'`.

- [ ] **Step 3: Implementar**

```python
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


def evaluate_alerts(snapshot: dict) -> list:
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

    def add_all(self, alerts: list) -> None:
        for a in alerts:
            self.add(a)

    def drain(self) -> list:
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

    def recent(self, n: int) -> list:
        return self._stack.top_n(n)

    def __len__(self) -> int:
        return len(self._stack)
```

- [ ] **Step 4: Rodar — deve passar**

Run: `python -m pytest tests/test_alerts.py -q`
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
git add src/monitor/alerts.py tests/test_alerts.py
git commit -m "feat(monitor): alertas com severidade, fila de prioridade e pilha de eventos críticos"
```

---

## Task 7: `src/sistema.py` — Orquestrador + smoke E2E

**Files:**
- Create: `src/sistema.py`
- Test: `tests/test_sistema_smoke.py`

- [ ] **Step 1: Escrever o smoke test que falha**

```python
# tests/test_sistema_smoke.py
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SISTEMA = REPO / "src" / "sistema.py"


def test_sistema_runs_without_error(tmp_path, monkeypatch):
    # roda num diretório de dados temporário para forçar a geração do CSV
    env = {"GS_DATA_PATH": str(tmp_path / "dados.csv")}
    result = subprocess.run(
        [sys.executable, str(SISTEMA)],
        capture_output=True, text=True, cwd=str(REPO),
        env={**__import__("os").environ, **env},
    )
    assert result.returncode == 0, result.stderr
    out = result.stdout
    # seções esperadas do relatório
    for marca in ("DIAGNÓSTICO", "ALERTAS", "PREVISÃO", "LOG DE EVENTOS", "INCONSISTÊNCIA"):
        assert marca in out, f"faltou a seção {marca}\n{out}"
```

- [ ] **Step 2: Rodar — deve falhar**

Run: `python -m pytest tests/test_sistema_smoke.py -q`
Expected: FAIL (returncode ≠ 0, `sistema.py` não existe / sem saída).

- [ ] **Step 3: Implementar**

```python
# src/sistema.py
"""Sistema inteligente de monitoramento — Global Solution FIAP 2026-1.

Ponto único de execução: lê a telemetria de data/dados.csv (gerando-a na
primeira execução), organiza em estruturas (matriz, fila, pilha), aplica
regras lógicas + previsão OLS e imprime o relatório operacional textual.

Uso: python src/sistema.py
"""
import os
import sys

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
    """OLS sobre battery_pct vs step na janela recente → reserva no próximo ciclo."""
    window = telemetry[-PREDICTION_WINDOW:]
    xs = [r["step"] for r in window]
    ys = [r["battery_pct"] for r in window]
    a, b = linear_regression(xs, ys)
    next_step = telemetry[-1]["step"] + 1
    return predict(a, b, next_step), a


def _status_tier(level: str) -> str:
    if level in ("CRITICAL",):
        return "CRÍTICO"
    if level in ("LOW",):
        return "ALERTA"
    return "NORMAL"


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
    print(f"\n[LOG DE EVENTOS]  {len(events)} registros:")
    for e in events[:12]:
        print(f"  passo {e['step']} [{e['type']}] {e['message']}")

    print("\n" + "=" * 64)


def main() -> None:
    telemetry = load_telemetry()
    print_report(telemetry)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Rodar — deve passar**

Run: `python -m pytest tests/test_sistema_smoke.py -q`
Expected: 1 passed.

- [ ] **Step 5: Rodar o sistema manualmente e conferir a saída**

Run: `cd ~/projects/global-solution-fiap && python src/sistema.py | head -40`
Expected: relatório com as seções; a inconsistência do passo 50 (battery_pct=142.0) aparece em `[INCONSISTÊNCIA NOS DADOS]`.

- [ ] **Step 6: Commit**

```bash
git add src/sistema.py tests/test_sistema_smoke.py
git commit -m "feat: sistema.py orquestrador + smoke test E2E"
```

---

## Task 8: Gerar e versionar `data/dados.csv`

**Files:**
- Create: `data/dados.csv`
- Remove: `data/.gitkeep`

- [ ] **Step 1: Gerar o CSV canônico (seed 42)**

Run:
```bash
cd ~/projects/global-solution-fiap
rm -f data/dados.csv data/.gitkeep
PYTHONPATH=src python -c "from monitor.telemetry_io import export_run; export_run('data/dados.csv')"
wc -l data/dados.csv && head -1 data/dados.csv
```
Expected: 169 linhas (cabeçalho + 168), cabeçalho com as 24 colunas.

- [ ] **Step 2: Confirmar a inconsistência plantada**

Run: `cd ~/projects/global-solution-fiap && sed -n '52p' data/dados.csv`
Expected: a linha do passo 50 com `battery_pct` = `142.0` (linha 52 = cabeçalho + step 0..50).

- [ ] **Step 3: Rodar toda a suíte**

Run: `cd ~/projects/global-solution-fiap && python -m pytest -q`
Expected: todos os testes PASS (motor + monitor + smoke).

- [ ] **Step 4: Commit**

```bash
git add data/dados.csv
git commit -m "data: telemetria canônica (seed 42) com inconsistência proposital"
```

---

## Task 9: `README.md` (10 seções do §11)

**Files:**
- Create: `README.md`

- [ ] **Step 1: Escrever o README**

Conteúdo completo (preencher a saída de exemplo com um trecho real de `python src/sistema.py`):

```markdown
# Global Solution FIAP 2026-1 — Sistema Inteligente de Monitoramento Espacial

## 1. Equipe
- Gabriel Carmona Bittencourt — RM <preencher>
- Iúri Leão de Almeida — RM <preencher>
- Márcio Francisco dos Santos Júnior — RM <preencher>

## 2. Problema e cenário
Colônia Aurora Siger em Marte, em operação. Sob comunicação limitada, a telemetria é a fonte primária de decisão. O sistema lê a telemetria horária, classifica a situação (normal/alerta/crítico), gera alertas priorizados, prevê a reserva de energia e recomenda ações.

## 3. Estruturas de dados (e por quê)
- **Lista** — séries horárias (geração, consumo, bateria).
- **Fila** (`monitor/structures.Queue`) — alertas pendentes por prioridade (`AlertQueue`).
- **Pilha** (`monitor/structures.Stack`) — últimos eventos críticos analisados (`CriticalEventStack`).
- **Dicionário** — módulos e snapshots (acesso O(1) por chave).
- **Árvore N-ária** (`engine/tree.Node`) — hierarquia de criticidade (Vital→Sustento→Expansão).
- **Matriz** (`monitor/matrix.ReadingsMatrix`) — leituras [hora × variável].

## 4. Regras lógicas do diagnóstico
Expressão booleana principal:
`CRÍTICO = (consumo > geração) ∧ (bateria_baixa ∨ vital_quebrado) ∧ ¬em_recuperação`
(`em_recuperação ≡ slope OLS > 0`). Regras com AND/OR/NOT em `monitor/alerts.evaluate_alerts`.

## 5. Técnica de previsão
Regressão linear OLS de forma fechada, escrita à mão (`engine/prediction.linear_regression`), sem numpy/sklearn. Extrapola a reserva de bateria do próximo ciclo; um slope negativo aciona recomendação de economia preventiva.

## 6. Como executar
```bash
python src/sistema.py          # gera data/dados.csv na 1ª execução e imprime o relatório
python -m pytest               # roda a suíte de testes (requer pip install -e ".[dev]")
```

## 7. Exemplo de entrada e saída
Entrada: `data/dados.csv` (telemetria horária de 7 sóis, seed 42).
Saída (trecho):
<colar aqui ~20 linhas reais de `python src/sistema.py`>

## 8. Recomendações geradas
O sistema emite recomendações por alerta (manter Vital, ativar economia, priorizar nuclear+bateria em tempestade) e uma recomendação preventiva quando a previsão projeta reserva < 40%.

## 9. Link do vídeo
<TBD — vídeo pendente de gravação> (YouTube "Não Listado").

## 10. Conclusões e aprendizados
<2-3 parágrafos: evolução reativo→preditivo; valor de separar regra de apresentação; limites da automação.>
```

- [ ] **Step 2: Preencher a saída de exemplo (seção 7) com saída real**

Run: `cd ~/projects/global-solution-fiap && python src/sistema.py | sed -n '1,22p'`
Cole o resultado na seção 7 do README.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: README com as 10 seções do §11 (RMs e vídeo como TBD)"
```

---

## Task 10: `docs/uso_ia.md` e `docs/link_video.txt`

**Files:**
- Create: `docs/uso_ia.md`, `docs/link_video.txt`

- [ ] **Step 1: Criar `docs/link_video.txt` (placeholder)**

```text
VÍDEO PENDENTE DE GRAVAÇÃO.
Publicar no YouTube como "Não Listado" (≤4 min) e substituir esta linha pelo link exato.
```

- [ ] **Step 2: Criar `docs/uso_ia.md` (relato honesto, §13)**

```markdown
# Uso de Inteligência Artificial

## Onde a IA foi usada (permitido — §13)
- **Organização e revisão**: estruturação do design, revisão de redação do README e do relatório.
- **Geração de dados simulados**: a telemetria é gerada por simulador determinístico próprio da equipe (Fase 3), não por IA.
- **Apoio à arquitetura**: discussão de alternativas (vendoring vs. dependência; fila/pilha à mão vs. builtins).

## O que é autoria da equipe
- O **motor científico** (`src/engine/`) é o módulo `operations` da Fase 3 do Aurora SIGER, escrito pela própria equipe (regressão OLS à mão, simulação determinística, árvores, controle de carga).
- A **camada de monitoramento** (`src/monitor/`) foi co-desenvolvida com validação crítica linha a linha pela equipe.

## Validação crítica feita
- Suíte de testes (`pytest`) cobrindo estruturas, alertas, I/O e o motor transplantado.
- Smoke test E2E garantindo que `python src/sistema.py` executa sem erros.
- Determinismo verificado (mesma seed ⇒ mesmo `dados.csv`).
```

- [ ] **Step 3: Commit**

```bash
git add docs/uso_ia.md docs/link_video.txt
git commit -m "docs: uso_ia.md (relato §13) + link_video.txt placeholder"
```

---

## Task 11: `docs/relatorio.pdf` (4-8 pp, adaptado da Fase 3)

**Files:**
- Create: `docs/relatorio.md`
- Create: `docs/relatorio.pdf` (build)

**Fonte:** `~/projects/FIAP-Aurora-Siger/fases/fase-3/relatorio.md` (relatório técnico já pronto da Fase 3; o pipeline pandoc/xelatex já é usado lá).

- [ ] **Step 1: Adaptar o relatório da Fase 3 para o escopo GS**

Copiar a base e enxugar para 4-8 páginas, focando nos 5 eixos da rubrica (§14): análise dos dados, estruturas de dados, lógica e regras, previsão, decisões técnicas.

Run:
```bash
cd ~/projects/global-solution-fiap
cp ~/projects/FIAP-Aurora-Siger/fases/fase-3/relatorio.md docs/relatorio.md
```
Edição manual de `docs/relatorio.md`: manter as seções de (1) análise dos dados e inconsistência, (2) estruturas (lista/fila/pilha/dict/árvore/matriz), (3) regras lógicas + expressão booleana, (4) previsão OLS e seu efeito na decisão, (5) decisões técnicas e arquitetura (vendoring, regra pura vs. apresentação). Remover o que for específico do dashboard TUI/Fase 3 fora do escopo GS. Atualizar título e autores.

- [ ] **Step 2: Gerar o PDF (pandoc/xelatex)**

Run:
```bash
cd ~/projects/global-solution-fiap/docs
pandoc relatorio.md -o relatorio.pdf --pdf-engine=xelatex -V geometry:margin=2.5cm
ls -la relatorio.pdf
```
Expected: `relatorio.pdf` gerado. Verifique que tem entre 4 e 8 páginas (`pdfinfo relatorio.pdf | grep Pages`); ajuste o conteúdo se passar de 8.

- [ ] **Step 3: Commit**

```bash
git add docs/relatorio.md docs/relatorio.pdf
git commit -m "docs: relatório técnico (4-8 pp) adaptado da Fase 3"
```

---

## Self-Review (preenchido na escrita do plano)

**1. Cobertura da spec:**
- §8.1 leitura de arquivo → Task 5 (`read_telemetry`) + Task 7 (`load_telemetry`). ✓
- §8.2 lista/fila/pilha/dict/árvore/matriz → Tasks 3, 4, 6 + engine.tree (Task 2). ✓
- §8.3 regras AND/OR/NOT + expressão booleana → Task 6 + README §4 (Task 9). ✓
- §8.4 alertas severidade/priorizados/recomendação → Task 6 + relatório no sistema.py (Task 7). ✓
- §8.5 previsão OLS influenciando decisão → Task 2 (prediction) + Task 7 (`predict_next_reserve`). ✓
- §7 ≥6 módulos binários, ≥8 eventos, inconsistência → Task 5. ✓
- Entregáveis §10 (README, src, data, relatório, uso_ia, link_video) → Tasks 9, 1-8, 8, 11, 10, 10. ✓
- Testes → Tasks 2-7. Determinismo → Task 5 (`test_roundtrip_is_stable`). ✓

**2. Placeholders:** os únicos "TBD/<preencher>" são RMs e link do vídeo no README — dados externos que a equipe fornece, não lacunas de implementação. OK.

**3. Consistência de tipos:** `evaluate_alerts(snapshot)` consome o dict produzido por `build_snapshot` (Task 7), cujas chaves casam com as lidas em `evaluate_alerts` (Task 6). `CRITICAL_MODULE_IDS` definido em `telemetry_io` (Task 5) e reusado em `sistema.py` (Task 7). `Alert`, `AlertQueue`, `CriticalEventStack` usados em Task 7 conforme definidos em Task 6. ✓

**Correção aplicada vs. spec:** o motor vendado inclui `allocation.py` (o `simulator` depende dele), embora a spec §4 o listasse como omitido.
