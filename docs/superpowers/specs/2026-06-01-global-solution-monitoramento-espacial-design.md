# Global Solution FIAP 2026-1 — Sistema Inteligente de Monitoramento Espacial

**Design / Spec** · 2026-06-01 · equipe Aurora SIGER (Gabriel Carmona Bittencourt, Iúri Leão de Almeida, Márcio Francisco dos Santos Júnior)

> Brief oficial: [`docs/desafio.md`](../../desafio.md). Referência de domínio: [`docs/referencia-dominio/`](../../referencia-dominio/).

---

## 1. Contexto e objetivo

O Global Solution pede um **sistema inteligente de monitoramento operacional** de uma missão espacial experimental: recebe telemetria, organiza em estruturas de dados, classifica a situação (normal/alerta/crítico), gera alertas automáticos priorizados, aplica uma técnica simples de previsão e emite recomendações técnicas (ver `docs/desafio.md` §4, §6).

A equipe já possui o **Aurora SIGER** (`~/projects/FIAP-Aurora-Siger`, repo `iurileao-hub/FIAP-Aurora-Siger`), a integradora de Fases 1-3 do curso, cujo módulo `operations/` (Fase 3, "colônia operando") é um simulador determinístico de operação energética de uma colônia em Marte — geração (solar/eólica/nuclear), consumo térmico, bateria, clima, regressão OLS à mão, dashboard TUI. O motor científico do GS **já existe e é de autoria da própria equipe**.

**Objetivo deste projeto:** empacotar e completar essa base num repositório de entrega GS-compliant, construindo a camada fina de monitoramento/alertas que falta, com qualidade de **padrão de referência** para o desenvolvimento continuado do grupo.

## 2. Premissas e restrições

- **Alvo:** nota **10,0/10,0** da rubrica (§14 do brief), **com exceção do vídeo** (2,0 pts), que ficará pendente para gravação posterior pela equipe. Todo o resto — código, estruturas, lógica, previsão, documentação — deve ser entregue completo.
- **Reaproveitamento legítimo:** o código do motor é da equipe (Fase 3). O GS é desenhado para integrar conteúdos das Fases 1-3 (§5 do brief), então reusar a integradora é exatamente o pedido — não fere o §13 (proibição de copiar código de IA).
- **Stdlib-only no caminho de execução** (§12): `sistema.py` e tudo que ele importa rodam sem `pip install`, só biblioteca padrão. OLS escrita à mão (sem numpy/sklearn no runtime). `pytest` é dependência só de desenvolvimento.
- **Determinismo:** toda aleatoriedade passa por um LCG seed-aware; mesma seed ⇒ mesmo `dados.csv`.
- **Repo público dedicado** (decisão de brainstorming): novo repo `iurileao-hub/global-solution` (recriado após exclusão do rascunho antigo). `src/` enxuto reaproveitando o motor; não expõe o portfólio das 7 fases.
- **Reference standard:** código legível, comentado, testado e defensável; serve de molde para a equipe estender.

## 3. Escopo

**Dentro:**
- Repo de entrega com estrutura do §10 do brief.
- Vendoring do subconjunto necessário do motor `aurora_siger.operations` em `src/engine/`.
- Camada nova `src/monitor/` (alertas, I/O de telemetria, matriz).
- `src/sistema.py` orquestrador executável.
- `data/dados.csv` (run canônico + inconsistência proposital + base do log de eventos).
- README (10 seções), `docs/relatorio.pdf` (4-8 pp), `docs/uso_ia.md`, `docs/link_video.txt` (placeholder até o vídeo existir).
- Testes pytest da camada nova + testes relevantes do motor transplantado.

**Fora:**
- O **vídeo** (gravação posterior; `docs/link_video.txt` fica como placeholder documentado).
- Divisão de trabalho entre os 3 integrantes (desenvolvemos o projeto inteiro; coordenação fica a cargo da equipe).
- Dashboard TUI ao vivo no `src/` — **bônus opcional**, só se sobrar tempo; a entrega principal é a saída textual do `sistema.py`.
- Reescrita do motor: transplante fiel, sem refatorar a física já validada.

## 4. Arquitetura

```
global-solution/
├── README.md                 # 10 seções (§11 do brief)
├── pyproject.toml            # metadados + pytest como dep de dev (opcional p/ rodar testes)
├── src/
│   ├── sistema.py            # ENTRYPOINT — `python src/sistema.py`
│   ├── engine/               # motor reaproveitado (código da equipe, atribuído)
│   │   ├── __init__.py
│   │   ├── constants.py, modules.py, rng.py
│   │   ├── climate.py, generation.py, consumption.py
│   │   ├── energy_levels.py, prediction.py, decision.py
│   │   ├── tree.py, hierarchies.py, failures.py
│   │   └── simulator.py, state.py
│   └── monitor/              # CÓDIGO NOVO
│       ├── __init__.py
│       ├── structures.py     # Queue (fila) + Stack (pilha) genéricos, à mão
│       ├── alerts.py         # Alert + evaluate_alerts + expressão booleana principal
│       ├── telemetry_io.py   # export_run / read_telemetry / inject + detect inconsistência / event_log
│       └── matrix.py         # readings_matrix [hora × variável]
├── data/
│   └── dados.csv             # telemetria do run canônico (seed fixa) + 1 inconsistência proposital
├── tests/
│   ├── test_alerts.py, test_structures.py, test_telemetry_io.py, test_matrix.py
│   ├── test_sistema_smoke.py # E2E: executa sem erro, emite seções esperadas
│   └── (testes transplantados do motor: prediction, decision, energy_levels, tree, failures)
└── docs/
    ├── relatorio.pdf         # 4-8 pp (pandoc/xelatex), adaptado da Fase 3
    ├── uso_ia.md
    └── link_video.txt        # placeholder até gravação
```

**Execução direta:** `sistema.py` insere `src/` no `sys.path` (ou usa imports relativos via `python -m`), de modo que `python src/sistema.py` funcione sem instalação — requisito do README (§11) e do checklist (§15).

**Vendoring:** os módulos de `src/engine/` são cópia fiel dos de `aurora_siger/operations/`, com cabeçalho de procedência (origem + autoria da equipe). Ficam de fora `dashboard.py`, `cli.py`, `simsnapshot.py`, `allocation.py`, `analysis.py` (não necessários ao caminho textual; reintroduzir só se o dashboard entrar no vídeo).

## 5. Fluxo de dados

```
[simulator.run_simulation(seed=42)]
        │  monitor.telemetry_io.export_run()  +  inject_inconsistency()
        ▼
data/dados.csv   (telemetria horária + 1 inconsistência proposital)
        │  read_telemetry()  — módulo csv (stdlib)
        ▼
linhas: list[dict]
        ├─ detect_inconsistencies(linhas)        → reporta a anomalia plantada      (§3, §6, §8.1)
        ├─ matrix.readings_matrix(linhas, vars)  → matriz [hora × variável]          (§8.2 matriz)
        ├─ prediction.linear_regression(série)   → slope + previsão próximo ciclo    (§8.5)
        ├─ energy_levels.energy_level(...)       → rótulo CRITICAL→SURPLUS            (§8.3)
        ├─ build_event_log(linhas)               → ≥8 eventos                        (§7)
        └─ alerts.evaluate_alerts(snapshot)      → [Alert] → AlertQueue (fila)        (§8.4, §8.2 fila)
                                                            → CriticalEventStack (pilha)(§8.2 pilha)
        ▼
sistema.py imprime: tabela de status (normal/alerta/crítico) · alertas priorizados + recomendações
                    · previsão e seu efeito numa decisão · log de eventos · inconsistência detectada
                    · árvore de criticidade
```

`sistema.py` **gera o CSV se ausente, lê o existente caso contrário** — documenta os dois caminhos que o §8.1 aceita (embutido-gerado e leitura de arquivo externo).

## 6. Componentes detalhados

### 6.1 `monitor/structures.py` (NOVO)
`Queue` (FIFO) e `Stack` (LIFO) genéricas escritas à mão sobre `list` (~15 linhas cada), com `enqueue`/`dequeue`/`peek`/`is_empty` e `push`/`pop`/`peek`. **Decisão:** implementação própria em vez de `collections.deque` — a rubrica (§14, Estruturas 0-1,5) pontua *ver a estrutura aplicada e justificada*. Espelha a filosofia do `landing/structures.py` da Fase 2.

### 6.2 `monitor/alerts.py` (NOVO)
- `Alert` (`@dataclass`): `severity` ∈ {`CRÍTICO`,`ALERTA`,`NORMAL`}, `code`, `message`, `recommendation`, `source`, `hour`.
- `evaluate_alerts(snapshot) -> list[Alert]`: **função pura** sobre um snapshot (dict). Compõe sinais existentes (energia baixa, módulo Vital quebrado, tempestade, consumo>geração, slope OLS negativo) com **AND/OR/NOT explícitos em ≥3 regras** (§8.3). Cada `Alert` carrega `recommendation` (§8.4).
- **Expressão booleana principal** (vai pro README, §8.3) — análoga operacional do `F∧A∧(L∨E)∧S` da Fase 2:
  ```
  CRÍTICO = (consumo > geração) ∧ (bateria_baixa ∨ vital_quebrado) ∧ ¬em_recuperação
  ```
- `AlertQueue` (usa `Queue`): insere por severidade, drena crít→alerta→normal (fila de prioridade).
- `CriticalEventStack` (usa `Stack`): empilha eventos críticos conforme analisados; expõe os últimos N.

### 6.3 `monitor/telemetry_io.py` (NOVO)
- `export_run(seed, hours, path)`: roda `simulator.run_simulation`, serializa linhas horárias (hora, status binário dos 13 módulos, geração por fonte, consumo, bateria%, temperatura, vento, tau, tempestade) em CSV.
- `inject_inconsistency(rows)`: planta **1 anomalia proposital documentada** (ex.: geração solar > 0 durante tempestade severa/noite, ou bateria% fora de [0,100]).
- `read_telemetry(path) -> list[dict]`: parse com módulo `csv` (stdlib), coerção de tipos.
- `build_event_log(rows) -> list[dict]`: deriva **≥8 eventos** (falha de módulo, auto-reparo, início/fim de tempestade, mudança de nível de energia, ativação de modo economia).
- `detect_inconsistencies(rows) -> list`: validador que captura a anomalia plantada (faixas de segurança + invariantes físicas).

### 6.4 `monitor/matrix.py` (NOVO)
`readings_matrix(rows, variables) -> list[list[float]]` — matriz [hora × variável] (lista-de-listas, §8.2) + acessores `get(hour, var)` e cabeçalhos.

### 6.5 `src/sistema.py` (NOVO — orquestrador)
Ponto único de execução. Sem lógica científica própria: lê dados, chama o motor + monitor, imprime o relatório textual operacional. Comentado para servir de leitura-guia ao grupo. Cobre o exemplo do §9 do brief (diagnóstico + previsão + ações priorizadas).

### 6.6 `src/engine/*` (TRANSPLANTE)
Cópia fiel dos módulos `operations` necessários, com cabeçalho de procedência. **Não refatorar** a física validada; ajustes só nos imports (`aurora_siger.operations.x` → `engine.x`).

## 7. Mapeamento da rubrica (alvo 10,0 − 2,0 vídeo = 8,0 entregues agora)

| Critério (§14) | Pts | Cobertura | Confiança |
|---|---|---|---|
| Interpretação de dados | 1,0 | inconsistência plantada + `detect_inconsistencies` + dados coerentes | alta |
| Estruturas de dados | 1,5 | lista, fila, pilha, dict, árvore, matriz — todas aplicadas e justificadas | alta |
| Lógica e regras | 1,5 | `evaluate_alerts` AND/OR/NOT (≥3) + expressão booleana no README | alta |
| Análise e previsão | 1,5 | OLS à mão, influencia o nível/decisão | muito alta |
| Código Python | 2,0 | motor testado + monitor TDD, sem erros, comentado | alta |
| **Vídeo** | **2,0** | **PENDENTE** (gravação posterior) | — |
| Documentação | 0,5 | README 10 seções + repo organizado + links | alta |

## 8. Entregáveis

1. **README.md** — 10 seções do §11 (inclui a expressão booleana principal e o link do vídeo, este último como TBD até a gravação).
2. **`src/sistema.py`** + `src/engine/` + `src/monitor/` — funcional, comentado, stdlib-only no runtime.
3. **`data/dados.csv`** — run canônico (seed 42) com inconsistência proposital.
4. **`docs/relatorio.pdf`** — 4-8 pp via pandoc/xelatex, adaptado do `relatorio.md` da Fase 3, focado em análise/estruturas/lógica/previsão/decisões.
5. **`docs/uso_ia.md`** — relato honesto do uso de IA (organização, revisão, geração de dados; código de autoria da equipe; validação crítica feita).
6. **`docs/link_video.txt`** — placeholder documentado ("vídeo pendente de gravação").

## 9. Testes

- **Camada nova (TDD, pytest):** `test_structures.py` (FIFO/LIFO), `test_alerts.py` (severidade por snapshot, ordem da fila, LIFO da pilha), `test_telemetry_io.py` (roundtrip CSV, detecção da inconsistência, log ≥8 eventos), `test_matrix.py` (dimensões e acessores).
- **Smoke E2E:** `test_sistema_smoke.py` — `python src/sistema.py` executa sem erro e emite as seções esperadas (cobre §15).
- **Determinismo:** mesma seed ⇒ `dados.csv` idêntico (diff de dois exports).
- **Motor transplantado:** trazer os testes verdes relevantes (prediction, decision, energy_levels, tree, failures) — garantem que o transplante não regrediu.

## 10. Decisões de design e justificativas

1. **Vendoring vs. dependência do pacote** — vendar garante `python src/sistema.py` sem `pip install` (stdlib pura), ao custo de duplicação entre repos; aceitável por ser entrega única.
2. **Queue/Stack à mão vs. `deque`** — a rubrica pontua a estrutura *visível e justificada*; builtins esconderiam o conceito.
3. **`evaluate_alerts` pura** — separar regra (snapshot→alertas) de apresentação (fila/pilha) torna o diagnóstico inspecionável e testável; é o argumento de "decisões justificadas" da rubrica.
4. **Gerar CSV + ler de volta** — cobre os dois caminhos do §8.1 num só fluxo e demonstra I/O de arquivo.
5. **Saída textual como entrega principal, dashboard como bônus** — protege o prazo (8 dias) sem arriscar a nota do código.
6. **Não refatorar o motor** — a física da Fase 3 já é validada por 276 testes; transplante fiel minimiza risco.

## 11. Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Vídeo (2,0 pts) ficar pendente indefinidamente | Spec já marca como item de continuação; `link_video.txt` placeholder; README sinaliza TBD. |
| Imports quebrarem com `python src/sistema.py` execução direta | `sys.path` insert no topo de `sistema.py` + smoke test E2E. |
| "Exatamente esses arquivos" (§10) lido de forma estrita pelo avaliador | Estrutura modular é defensável; plano B documentado: consolidar em `sistema.py` único se necessário. |
| Inconsistência plantada não detectável de forma robusta | `detect_inconsistencies` baseado em faixas de segurança + invariantes físicas explícitas, com teste dedicado. |

## 12. Continuação futura (pós-entrega)

- Gravar e publicar o **vídeo** (≤4 min, YouTube "Não Listado"); preencher `link_video.txt` e o README.
- Opcional: portar o **dashboard TUI ao vivo** para o `src/` e usá-lo no vídeo.
- O repo serve de **molde de referência** para o grupo nas próximas fases do Aurora SIGER.
