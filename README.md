# Global Solution FIAP 2026-1 — Sistema Inteligente de Monitoramento Espacial

## 1. Equipe
- Gabriel Carmona Bittencourt — RM569239
- Iúri Leão de Almeida — RM570215
- Márcio Francisco dos Santos Júnior — RM570758
- Maria Sophia Domingues dos Santos — RM571209

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
```
Runtime stdlib-only: não requer `pip install` nem dependências de terceiros.

## 7. Exemplo de entrada e saída
Entrada: `data/dados.csv` — telemetria horária de 7 sóis, seed 42.
Saída (relatório no terminal; cores degradam para texto puro quando redirecionado):
```
──────────────────────────────────────────────────────────────────────────
  AURORA SIGER · MONITORAMENTO OPERACIONAL DA COLÔNIA
  sol 6 · 23h · passo 167   status: [ NORMAL ]
──────────────────────────────────────────────────────────────────────────

┌─ INTERPRETAÇÃO ─────────────────────────────── interpretação de dados ─┐
│  anomalia: passo 50 · battery_pct=142.0 — fora de [0, 100] %           │
│  matriz          168 horas × 5 variáveis                               │
│  variáveis       temp·vento·geração·consumo·bateria                    │
└────────────────────────────────────────────────────────────────────────┘
┌─ ESTRUTURAS ───────────────────────────────────── estruturas de dados ─┐
│  matriz          168×5 (lista de listas)                               │
│  fila (Queue)    1 alertas — FIFO por severidade                       │
│  pilha (Stack)   65 eventos críticos — LIFO                            │
│  dicionário      13 módulos — acesso O(1) por id                       │
│  árvore N-ária   criticidade: Vital·Sustento·Expansão (profund. 3)     │
└────────────────────────────────────────────────────────────────────────┘
┌─ DIAGNÓSTICO ──────────────────────────────────────── lógica e regras ─┐
│  passo           167 · sol 6 · 23h                                     │
│  bateria  ██████████████░░░░░░░░  65.6%  [ NORMAL ]                    │
│  geração 81.0 kW   consumo 107.5 kW                                    │
│  vitais (1,2,3,7)  ● ● ● ●                                             │
│  CRÍTICO = (consumo>geração) ∧ (bat_baixa ∨ vital_quebr) ∧ ¬recuperação│
│  consumo>geração=V   bat_baixa=F   vital_quebr=F   ¬recuperação=F      │
│  ⇒ CRÍTICO = F                                                         │
└────────────────────────────────────────────────────────────────────────┘
┌─ PREVISÃO ──────────────────────────────────────── análise e previsão ─┐
│  tendência ▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▂▁▁▁▁▁▁▁▂▃▄▆█████▇▆▆▅▄▃▂                    │
│  slope (OLS)     -3.289 %/passo                                        │
│  reserva prev.   68.0% no próximo ciclo                                │
│  ⇒ reserva acima do limiar; sem economia preventiva                    │
└────────────────────────────────────────────────────────────────────────┘
  ...
┌─ COBERTURA DE REQUISITOS ──────────────────────────── rastreabilidade ─┐
│  ✓ Interpretação de dados  anomalia detectada + matriz de leituras     │
│  ✓ Estruturas de dados     fila·pilha·dict·árvore·matriz               │
│  ✓ Lógica e regras         AND/OR/NOT + expressão booleana avaliada    │
│  ✓ Análise e previsão      OLS ⇒ recomendação disparada                │
│  ✓ Código Python           stdlib · funções puras · sem dependências   │
└────────────────────────────────────────────────────────────────────────┘
```

## 8. Recomendações geradas
O sistema emite recomendações por alerta (manter Vital, ativar economia, priorizar nuclear+bateria em tempestade) e uma recomendação preventiva quando a previsão projeta reserva < 40%.

## 9. Link do vídeo
<TBD — vídeo pendente de gravação> (YouTube "Não Listado").

## 10. Conclusões e aprendizados

A maior virada de paradigma neste projeto foi a passagem do monitoramento **reativo** para o **preditivo**. Um sistema reativo espera o limiar de bateria ser ultrapassado para soar o alarme; o critério booleano `¬em_recuperação` inverte esse comportamento: se o slope OLS da série de bateria é positivo, a colônia está se recuperando e o alerta crítico é suprimido, mesmo que os demais limites estejam no vermelho. Essa decisão — fazer a regressão linear participar diretamente da condição de disparo — faz com que o sistema não apenas descreva o estado presente, mas incorpore a trajetória como parte do diagnóstico.

A separação entre regra de negócio e apresentação mostrou seu valor ao longo de todo o desenvolvimento. `evaluate_alerts` é uma função pura: recebe um dicionário de snapshot e devolve uma lista de alertas; ela não sabe nada de filas, pilhas ou impressão. Isso tornou cada regra testável e auditável de forma isolada e deixou a camada de apresentação — `AlertQueue` e `CriticalEventStack` — livre para priorizar, ordenar e exibir sem jamais misturar lógica de diagnóstico com lógica de interface. Em sistemas críticos, essa separação não é elegância acadêmica: é o que permite auditar e modificar uma regra sem risco de efeito colateral silencioso em outra parte do sistema.

Por fim, o sistema reconhece seus próprios limites. A inconsistência plantada deliberadamente (`battery_pct=142.0` no passo 50) e capturada por `detect_inconsistencies` é um lembrete concreto de que telemetria pode mentir — sensor com defeito, corrupção de transmissão, overflow de registrador. A função verifica invariantes físicos, mas não pode detectar erros plausíveis dentro da faixa válida. Em uma colônia real, o relatório gerado é insumo para decisão humana, não substituto dela. Automação cuida do volume; julgamento humano cuida dos casos nos quais os dados parecem corretos mas o contexto diz o contrário.
