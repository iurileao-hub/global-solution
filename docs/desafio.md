# Global Solution FIAP 2026-1 — Sistema Inteligente de Monitoramento Espacial

> Brief oficial do desafio. Fonte: enunciado FIAP (2026). Transcrito e formatado em 2026-06-01 como documento de referência do projeto.

---

## 1. Introdução

O Global Solution desafia os estudantes a desenvolverem soluções tecnológicas para os desafios da indústria espacial moderna. O foco é transformar problemas relacionados à exploração espacial, sobrevivência fora da Terra, comunicação entre planetas, automação autônoma, sustentabilidade e segurança aeroespacial em oportunidades de inovação e avanço tecnológico.

A indústria espacial representa um dos maiores desafios tecnológicos da humanidade. Desde os primeiros voos orbitais até as ambições de colonização de Marte, cada fase da exploração espacial demanda soluções inovadoras em engenharia, computação e gestão de riscos. As missões espaciais não apenas expandem nosso conhecimento sobre o universo, mas também criam tecnologias que transformam a vida na Terra em áreas como comunicação, energia renovável, materiais avançados e sistemas inteligentes.

Nesse contexto, sistemas inteligentes de monitoramento, controle e análise de dados são essenciais. As operações espaciais dependem de plataformas computacionais capazes de interpretar dados em tempo real, identificar problemas, gerar alertas automáticos e fornecer recomendações técnicas que protejam a vida dos astronautas, a integridade dos equipamentos e o sucesso da missão. Esse desafio propõe que você desenvolva uma solução de software que simule os elementos críticos de um sistema de monitoramento operacional, aplicando lógica, estruturas de dados, algoritmos e pensamento computacional.

A oportunidade é dupla: adquirir competências técnicas relevantes para a indústria aeroespacial e refletir sobre como a computação pode ser usada de forma responsável e ética em operações críticas que impactam a segurança humana.

---

## 2. Período e formato de participação

- **Período de realização:** 25 de maio a **09 de junho de 2026**.
- **Formato:** individual ou em grupo de até 5 pessoas. Recomenda-se grupo (trabalho em equipe, distribuição de responsabilidades técnicas, dinâmica profissional).
- **Lives:**
  - Abertura — **25/05/2026 à noite** (apresentação do tema + dúvidas iniciais; presença recomendada).
  - Tira-dúvidas com tutores — **26/05/2026**.
  - Links divulgados em breve.

---

## 3. Contexto do desafio

As missões espaciais modernas dependem de sistemas inteligentes de monitoramento contínuo para garantir a segurança operacional e a eficiência dos recursos. Em ambientes em que a comunicação é limitada, os dados gerados pelos sensores e módulos da operação se tornam a fonte primária de informação para tomar decisões.

A equipe será responsável por desenvolver um sistema inteligente capaz de **receber, interpretar e exibir** dados de uma missão espacial experimental. O sistema deverá identificar situações críticas, gerar alertas automáticos e fornecer recomendações para manter a operação em condições normais ou de crise.

A dificuldade não está apenas na programação, mas também na capacidade de **interpretar dados incompletos ou conflitantes**, organizar informações de forma clara e comunicar decisões de maneira justificada.

---

## 4. Objetivo geral

Desenvolver um sistema inteligente de monitoramento para controle básico de uma missão espacial experimental, aplicando conceitos de programação, algoritmos, pensamento computacional e inteligência artificial, capaz de interpretar dados operacionais, gerar alertas automáticos e fornecer análises de situações críticas.

---

## 5. Conteúdos integrados

Reúne conteúdos das três primeiras fases do curso, aplicados a um cenário realista de operação espacial:

| Fase | Conteúdos mobilizados |
|---|---|
| **Fase 1** | Sistemas numéricos, lógica inicial, algoritmos e fluxogramas, Python básico, IA como apoio, pensamento computacional, eficiência energética, ética e sustentabilidade. |
| **Fase 2** | Portas lógicas, funções booleanas, listas, filas, pilhas, busca, ordenação, funções matemáticas, evolução da computação e sustentabilidade. |
| **Fase 3** | Lógica booleana, dicionários e tabelas hash, árvores e hierarquias, matrizes e vetores, sistemas operacionais, análise de dados simples, energia e sustentabilidade. |

*Quadro 1 – Conteúdos mobilizados. Fonte: Elaborado pelo autor (2026).*

---

## 6. Missão da equipe

O sistema de monitoramento operacional deve executar as seguintes tarefas:

1. Receber e interpretar um pacote de dados simulados de uma missão espacial experimental;
2. Organizar os dados em estruturas computacionais adequadas (listas, filas, pilhas, dicionários, matrizes);
3. Implementar regras lógicas para classificar a situação operacional em **normal, alerta ou crítico**;
4. Gerar alertas automáticos baseados em condições críticas simuladas;
5. Aplicar uma técnica simples de análise/previsão para estimar o comportamento de uma variável crítica;
6. Fornecer recomendações técnicas para manutenção ou recuperação operacional.

---

## 7. Dados simulados obrigatórios

A equipe pode criar seus próprios dados, desde que coerentes com um cenário realista. Pacote mínimo de telemetria:

- **Status binários de ≥ 6 módulos críticos** (ex.: suporte à vida, energia, comunicação, habitat, laboratório, armazenamento);
- **Leituras de geração e consumo de energia em ≥ 6 horários**, incluindo reservas energéticas;
- **Variáveis ambientais** (temperatura externa/interna, nível de radiação, qualidade de comunicação, velocidade do vento);
- **Log de eventos com ≥ 8 registros** (alertas, reinicializações, falhas de sensor, mudanças de prioridade, modos de economia);
- **Ao menos uma inconsistência proposital** nos dados, para testar a capacidade de diagnóstico.

---

## 8. Requisitos técnicos do sistema

### 8.1 Leitura e interpretação de dados

Ler dados de arquivo externo (**CSV, JSON ou TXT simples**) ou embutidos no código (claramente documentados).

- Definir claramente quais dados representam o estado da missão;
- Usar variáveis booleanas ou valores 0/1 para módulos críticos;
- Criar tabela simples de status (normal / alerta / crítico);
- Incluir ≥ 1 regra de interpretação baseada em sistemas numéricos, estados binários ou faixas de segurança.

### 8.2 Organização dos dados

- **Listas** — séries temporais (geração, consumo, temperatura);
- **Fila** — alertas pendentes por ordem de chegada ou prioridade;
- **Pilha** — últimos eventos críticos analisados;
- **Dicionário / tabela hash** — acesso rápido a dados de módulos pelo nome;
- **Hierarquia da missão** — ex.: energia (solar/eólica/baterias), habitat (oxigênio/temperatura/comunicação);
- **Matriz / lista de listas** — leituras por horário × variável.

### 8.3 Regras lógicas

- `IF` / `ELIF` / `ELSE` para classificar a situação da missão;
- `AND` / `OR` / `NOT` em ≥ 3 regras distintas;
- Apresentar no README **uma expressão booleana principal** do diagnóstico;
- Explicar em linguagem simples o motivo de cada regra gerar determinada ação.

### 8.4 Alertas automáticos

- Gerar alertas para situações críticas (falha de módulos essenciais, energia baixa, comunicação comprometida);
- Classificar por severidade (normal / alerta / crítico);
- Exibir de forma clara, organizada e **priorizando os mais críticos**;
- Fornecer recomendações automáticas de ação por alerta.

### 8.5 Análise e previsão de dados

- Técnica simples **sem bibliotecas avançadas**: regressão linear, média móvel ou extrapolação de tendência;
- Variável: energia disponível, consumo, geração renovável, temperatura ou qualidade de comunicação;
- Mostrar dados usados, metodologia e resultado previsto;
- A previsão deve **influenciar ≥ 1 recomendação ou decisão** do sistema.

---

## 9. Exemplo de funcionamento

> Referência apenas — a equipe pode criar solução diferente, desde que atenda aos requisitos.

**Entrada simulada:** `energia_reserva = 32%`, `consumo = 78 kWh`, `geracao_solar = 25 kWh`, `suporte_vida = 1`, `comunicacao = 0`, `radiacao = alta`.

**Diagnóstico:** alerta crítico — energia baixa, comunicação instável e radiação elevada detectada.

**Previsão:** se o consumo continuar no mesmo ritmo, a reserva poderá cair para **24% no próximo ciclo**.

| Prioridade | Ação |
|---|---|
| Crítica | Manter suporte à vida e comunicação de emergência. |
| Alta | Desligar o laboratório e sistemas não essenciais. |
| Alta | Redirecionar energia para habitat e carregamento de baterias. |

---

## 10. Entregáveis obrigatórios

Enviar um arquivo **`.TXT`** via plataforma FIAP ON contendo **apenas dois links**:

1. Link direto do repositório GitHub **público** da equipe;
2. Link do vídeo de apresentação no YouTube como **"Não Listado"**.

Estrutura exata do repositório GitHub:

| Arquivo | O que deve conter |
|---|---|
| `README.md` | Nome da equipe e RMs, resumo do problema, estruturas de dados usadas, regras lógicas principais, técnica de previsão, como executar, exemplo de entrada/saída, link do vídeo. |
| `src/sistema.py` | Código Python completo, funcional e comentado. Deve executar sem erros. |
| `data/dados.csv` ou `.txt` | Dados simulados da telemetria. Se embutidos no código, incluir arquivo vazio como placeholder. |
| `docs/relatorio.pdf` | Relatório de **4 a 8 páginas**: análise, estruturas, lógica, previsão e decisões técnicas. |
| `docs/link_video.txt` | Link exato do vídeo no YouTube. |
| `docs/uso_ia.md` *(opcional)* | Se usaram IA: como, em quais partes, e a validação crítica feita. Se não usaram, podem omitir. |

*Quadro 2 – Arquivos e conteúdos. Fonte: Elaborado pelo autor (2026).*

---

## 11. Estrutura do README

1. Nome da equipe e RMs dos integrantes;
2. Resumo do problema e cenário analisado;
3. Estruturas de dados: quais foram usadas e por quê;
4. Regras lógicas principais do diagnóstico;
5. Técnica de previsão utilizada e resultado;
6. Como executar: `python src/sistema.py`;
7. Exemplo de entrada e saída do sistema;
8. Recomendações geradas pelo sistema;
9. Link do vídeo no YouTube;
10. Conclusões e aprendizados.

---

## 12. Regras técnicas

- Utilizar os conceitos das fases 1, 2 e 3;
- A solução pode rodar **diretamente no terminal**, sem interface gráfica;
- Priorizar estruturas fundamentais do Python (listas, dicionários, funções, laços, condicionais);
- Leitura/manipulação de CSV/TXT recomendada para organização dos dados;
- Bibliotecas (Pandas, NumPy, scikit-learn, Streamlit, frameworks web) **permitidas desde que** o projeto preserve a construção da lógica, a interpretação dos dados e as análises **feitas pelos próprios alunos**;
- A lógica de previsão deve demonstrar claramente o raciocínio adotado.

---

## 13. Uso de inteligência artificial

- **Permitido:** usar IA para organizar ideias, revisar texto, explicar conceitos ou gerar dados simulados.
- **Proibido:** copiar código ou análises direto de IA. A solução, código e conclusões devem refletir o entendimento da equipe.
- Se usarem IA, registrar em `docs/uso_ia.md` e explicar a validação crítica feita.

---

## 14. Rubrica de avaliação

**Total: 10,0 pontos.**

| Critério | Pontos | O que será observado |
|---|---|---|
| Interpretação de dados | 0–1,0 | Clareza do problema, dados coerentes, anomalias e riscos identificados. |
| Estruturas de dados | 0–1,5 | Listas, filas, pilhas, dicionários, hierarquias e matrizes bem aplicadas e justificadas. |
| Lógica e regras | 0–1,5 | IF/ELIF/ELSE, AND/OR/NOT, expressão booleana clara e decisões justificadas. |
| Análise e previsão | 0–1,5 | Técnica simples implementada, dados claros, resultado interpretado e influência na decisão. |
| Código Python | 0–2,0 | Funcional, sem erros, organizado em funções, comentado e compatível com a fase 3. |
| Vídeo de apresentação | 0–2,0 | Claro, sistema rodando ao vivo, diagnóstico explicado, decisões defendidas, **até 4 min**. |
| Documentação e organização | 0–0,5 | README claro, arquivos organizados, links funcionais e fácil executar. |

*Quadro 3 – Critérios de avaliação. Fonte: Elaborado pelo autor (2026).*

---

## 15. Checklist de entrega

- [ ] Repositório GitHub público e acessível?
- [ ] Arquivo `.TXT` enviado na plataforma com links corretos?
- [ ] Vídeo publicado no YouTube como "Não Listado"?
- [ ] Código Python executa sem erros?
- [ ] Exemplo de entrada/saída documentado?
- [ ] Estruturas de dados variadas e justificadas?
- [ ] Técnica de previsão implementada?
- [ ] Alertas automáticos funcionando?
- [ ] Recomendações priorizadas?
- [ ] Se usou IA, `docs/uso_ia.md` preenchido?

---

## 16. Objetivo final

Espera-se que a equipe demonstre capacidade de **pensar como profissionais de computação** em uma situação realista: interpretar dados operacionais, organizar informações de forma eficiente, construir regras lógicas de decisão, prever comportamentos e comunicar uma solução técnica de forma clara e justificada.

Mais do que entregar código funcional, a equipe deve demonstrar que **compreende o problema em profundidade**, sabe justificar suas escolhas técnicas e consegue transformar dados em recomendações úteis para a operação de uma missão espacial.

Busca-se aproximar os estudantes do desenvolvimento de sistemas inteligentes aplicados à indústria moderna, priorizando organização computacional, eficiência de código e clareza na comunicação técnica.
