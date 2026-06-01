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
