# Uso de Inteligência Artificial

Este projeto foi desenvolvido com apoio de IA (Claude Code), em diálogo constante com a
equipe e sob suas decisões de arquitetura e implementação — conforme o §13 do enunciado,
cuja exigência central é que a solução reflita o entendimento da equipe.

## Como a IA foi usada
- **Brainstorming, especificação e implementação assistida** da camada de monitoramento e
  apresentação (`src/monitor/`), a partir das decisões de projeto da equipe e em ciclos de
  teste-primeiro (TDD).
- **Revisão e redação** de código, do README e do relatório técnico.
- A **telemetria não foi gerada por IA**: vem do simulador determinístico próprio da equipe
  (Fase 3), também origem do motor científico incorporado em `src/engine/`.

## Autoria e validação
A equipe está integrada às decisões de arquitetura e implementação e é capaz de explicar e
defender a solução. A validação incluiu a conferência dos números do relatório contra os
dados reais (`data/dados.csv`), a verificação de determinismo (mesma seed ⇒ `dados.csv`
idêntico) e uma suíte de testes automatizados.
