# Global Solution FIAP 2026-1 — Sistema Inteligente de Monitoramento Espacial

## 1. Equipe
- Gabriel Carmona Bittencourt — RM569239
- Iúri Leão de Almeida — RM570215
- Márcio Francisco dos Santos Júnior — RM570758

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
```
================================================================
AURORA SIGER — MONITORAMENTO OPERACIONAL DA COLÔNIA
================================================================

[INCONSISTÊNCIA NOS DADOS]
  passo 50: battery_pct=142.0 — fora de [0, 100] %

[MATRIZ DE LEITURAS]  168 horas × 5 variáveis
  variáveis: temperature_c, wind_ms, generation_kw, consumption_kw, battery_pct

[DIAGNÓSTICO]
  passo 167 (sol 6, hora 23h)
  bateria: 65.6%  |  nível de energia: HIGH  ⇒  NORMAL
  geração: 81.0 kW  |  consumo: 107.5 kW
    módulo 1 Command and Control: OK
    módulo 2 Life Support (ECLSS): OK
    módulo 3 Habitat: OK
    módulo 7 Medical Support: OK
    módulo 6 Communications: OK
    módulo 8 Food Production: OK

[PREVISÃO]
  tendência (slope OLS): -3.289 %/passo
  reserva prevista no próximo ciclo: 68.0%
```

## 8. Recomendações geradas
O sistema emite recomendações por alerta (manter Vital, ativar economia, priorizar nuclear+bateria em tempestade) e uma recomendação preventiva quando a previsão projeta reserva < 40%.

## 9. Link do vídeo
<TBD — vídeo pendente de gravação> (YouTube "Não Listado").

## 10. Conclusões e aprendizados

A maior virada de paradigma neste projeto foi a passagem do monitoramento **reativo** para o **preditivo**. Um sistema reativo espera o limiar de bateria ser ultrapassado para soar o alarme; o critério booleano `¬em_recuperação` inverte esse comportamento: se o slope OLS da série de bateria é positivo, a colônia está se recuperando e o alerta crítico é suprimido, mesmo que os demais limites estejam no vermelho. Essa decisão — fazer a regressão linear participar diretamente da condição de disparo — faz com que o sistema não apenas descreva o estado presente, mas incorpore a trajetória como parte do diagnóstico.

A separação entre regra de negócio e apresentação mostrou seu valor ao longo de todo o desenvolvimento. `evaluate_alerts` é uma função pura: recebe um dicionário de snapshot e devolve uma lista de alertas; ela não sabe nada de filas, pilhas ou impressão. Isso tornou cada regra testável de forma isolada (os 110 testes passam sem nenhum efeito colateral) e deixou a camada de apresentação — `AlertQueue` e `CriticalEventStack` — livre para priorizar, ordenar e exibir sem jamais misturar lógica de diagnóstico com lógica de interface. Em sistemas críticos, essa separação não é elegância acadêmica: é o que permite auditar e modificar uma regra sem risco de efeito colateral silencioso em outra parte do sistema.

Por fim, o sistema reconhece seus próprios limites. A inconsistência plantada deliberadamente (`battery_pct=142.0` no passo 50) e capturada por `detect_inconsistencies` é um lembrete concreto de que telemetria pode mentir — sensor com defeito, corrupção de transmissão, overflow de registrador. A função verifica invariantes físicos, mas não pode detectar erros plausíveis dentro da faixa válida. Em uma colônia real, o relatório gerado é insumo para decisão humana, não substituto dela. Automação cuida do volume; julgamento humano cuida dos casos nos quais os dados parecem corretos mas o contexto diz o contrário.
