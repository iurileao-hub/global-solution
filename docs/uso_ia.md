# Uso de Inteligência Artificial

## Onde a IA foi usada (permitido — §13)
- **Organização e revisão**: estruturação do design, revisão de redação do README e do relatório.
- **Geração de dados simulados**: a telemetria é gerada por simulador determinístico próprio da equipe (Fase 3), não por IA.
- **Apoio à arquitetura**: discussão de alternativas (vendoring vs. dependência; fila/pilha à mão vs. builtins).

## O que é autoria da equipe
- O **motor científico** (`src/engine/`) é o módulo `operations` da Fase 3 do Aurora SIGER, escrito pela própria equipe (regressão OLS à mão, simulação determinística, árvores, controle de carga).
- A **camada de monitoramento** (`src/monitor/`) foi co-desenvolvida com validação crítica linha a linha pela equipe.

## Validação crítica feita
- Revisão linha a linha do motor transplantado e de toda a camada de monitoramento.
- Execução manual de `python src/sistema.py`, conferindo o relatório operacional gerado.
- Determinismo verificado (mesma seed ⇒ mesmo `dados.csv`).
