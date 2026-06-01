# Síntese divergente — tríade médico-integrador × exploração espacial

**Data:** 2026-05-21
**Função:** mapear o estado da arte na interseção saúde × espaço, identificar lacunas onde a tríade clínico+gestor+educador tem vantagem competitiva, e propor produtos candidatos de escopo claro pra Global Solution FIAP 2026-1.

---

## 1. Como ler este documento

Este arquivo é o ponto de entrada da pesquisa divergente. Cada seção abaixo resume um eixo coberto em arquivo próprio nesta mesma pasta (`01-*.md` até `09-*.md`). Aqui o trabalho é **integrar** — onde estão as lacunas que conectam dois ou mais eixos e abrem espaço pra produto autoral.

---

## 2. Achados consolidados em uma página

### Estado da arte de IA médica espacial (2025-2026)

- **CMO-DA** (NASA + Google Cloud Vertex AI, ago/2025): assistente multimodal, **88% accuracy** diagnóstica em 250 condições, treinado em dados abertos. Roadmap: detectar condições microgravidade-específicas, operar ultrassom, administrar medicação. **É o competidor de referência.** [`01-cmo-da-google-nasa-2025.md`]
- **Latência Terra-Marte**: 18-20 min one-way, ante 1-2s da ISS. Telemedicina síncrona morre na transição ISS → Marte. CDSS local autônomo pode reduzir mortalidade em **34%** em LDEM (Russell et al. 2023). [`02-latencia-autonomia-medica.md`]

### Formação humana atual

- **CMO típico não é médico** — recebe ~40h de CPR/emergência em 18 meses pré-missão. Funciona em ISS com Terra de retaguarda; insuficiente em Marte. Programas acadêmicos (NASA Aerospace Medicine Clerkship; UC Irvine Space MED) existem mas não treinam CMOs em larga escala. [`03-formacao-cmo-estado-atual.md`]

### Análogos terrestres

- HI-SEAS, MDRS, MARS-500, Concordia, 2MARS rodam estudos com N=6 típico. Brasil **não tem análogo certificado**, mas tem condições naturais (Amazônia, Antártica via Comte. Ferraz, submarinos da Marinha, fronteira PMDF). [`04-analogos-terrestres.md`]

### Brasil — ativos institucionais subexplorados

- AEB existe (1994), opera Alcântara/CLBI. Programa de astronautas limitado (Marcos Pontes, 2006, único). **Sem programa estruturado de medicina aeroespacial.** Mas três ativos articuláveis: SUS, medicina militar, LGPD. [`05-brasil-aeb-lacuna.md`]

### Pediatria e reprodução

- **Zero gravidezes/partos** em 60+ anos de voo. Pesquisa em reprodução, gestação e pediatria espacial é pré-paradigmática. Colonização sem isso é ficção biomédica. **Território autoral aberto.** [`06-pediatria-reproducao-gap-colonial.md`]

### Governança de dados

- HIPAA não se aplica a astronautas. NASA usa Privacy Act 1974 + princípios HIPAA por afinidade. Tripulações internacionais geram colisão de jurisdições. **Turismo espacial: vácuo legal explícito.** LGPD brasileira tem dispositivos (Art. 18, 33, 38 RIPD) que poderiam ser exportados como framework. [`07-governanca-dados-saude.md`]

### Framework ético consolidado

- IOM/National Academies: **avoid harm, beneficence, favourable risk-benefit, respect for autonomy, fairness, fidelity**. Principal tensão: **consentimento sob coerção implícita** (competição por missão). Framework atual pensado para astronauta adulto selecionado — não cobre turista, família, trabalhador. [`08-etica-medicina-espacial.md`]

### O análogo brasileiro mais maduro (e ignorado)

- Telessaúde Brasil Redes, Conexão Povos da Floresta, FAS Eirunepé, TELEMEDIC 1.0 já operam medicina remota em condições análogas a missão longa, **com pediatria e saúde da família incluídas**. Amazônia é análogo **mais completo** do que HI-SEAS porque tem família, criança, idoso — coisas que faltam totalmente nos análogos formais. [`09-telemedicina-amazonia-analogo.md`]

---

## 3. Mapa de lacunas — onde a tríade tem vantagem competitiva

Identifico **seis lacunas** que conectam pelo menos dois eixos e onde o perfil do Iúri (pediatra + gestor médico militar + educador) tem ângulo de ataque inalcançável a quem domina apenas um dos papéis.

| # | Lacuna | Eixos conectados | Vantagem da tríade |
|---|---|---|---|
| **L1** | **Inspecionabilidade clínica do CMO-DA** — IA tem 88% accuracy; ninguém auditou como ela falha nos 12% restantes nem como o clínico humano pode contestá-la | IA (01) + latência (02) + ética (08) + governança (07) | Clínico vê a interface no momento da decisão; gestor entende governança de adoção; educador treina uso crítico. Aurora SIGER já é arquitetura compatível. |
| **L2** | **Formação distribuída e continuada do CMO** — 40h em 18 meses é insuficiente pra missão de 2-3 anos. Não há currículo modular in-flight | Formação (03) + análogos (04) + Brasil (05) | Educador é o protagonista. Iúri já tem prática (PMDF Resiliência, apostilas, mentor). |
| **L3** | **Pediatria e saúde da família espacial** — território virgem; colônia futura precisa, NASA não tem | Reprodução/pediatria (06) + ética (08) + Amazônia (09) | Pediatra é o protagonista; Iúri é pediatra praticante. Ângulo autoral único globalmente. |
| **L4** | **Análogo terrestre brasileiro certificado** — Brasil vive as condições, não as nomeia | Análogos (04) + Brasil (05) + Amazônia (09) | Gestor articula HRT/PMDF + SUS amazônico. Não é proposta abstrata — é institucional concreta. |
| **L5** | **Soberania LGPD-derived de dados de saúde em missões internacionais** — vácuo legislativo, Brasil tem framework regulatório forte | Governança (07) + Brasil (05) + IA (01) | Gestor já trabalhou RIPD em AeroPed. Arquitetura é portável. |
| **L6** | **Ética pós-astronauta** — framework para turistas, famílias e trabalhadores, não só adultos selecionados | Ética (08) + reprodução (06) + governança (07) | Os três papéis da tríade convergem aqui. Tradição bioética brasileira (Lei 14.874/2024) tem instrumentos. |

---

## 4. Quatro produtos candidatos de escopo claro

Cada produto cobre 2-4 das lacunas acima. Apresento em ordem decrescente de prontidão pra implementação num semestre FIAP.

### P1 — **AuditCMO**: framework de auditoria clínica para CDSS espacial

**O que é:** especificação técnica + protótipo de log auditável de decisões IA-assistidas em medicina espacial autônoma. Cada output do CDSS é registrado com (a) input clínico, (b) inferência da IA, (c) intervalo de confiança, (d) decisão humana final, (e) discordância se houver, (f) outcome.

**Lacunas cobertas:** L1, L5.

**Vantagem competitiva:** continuidade direta com Aurora SIGER (Fase 1 Isolation Forest + Fase 2 lógica booleana auditável). **A frase do post — "para quem funciona, com que transparência, sob qual governança?" — vira artefato técnico.**

**Cabe num semestre FIAP?** Sim. Stack viável: Python + SQLite + Streamlit/Django mínimo. Pode chegar a protótipo funcional.

**Riscos:** se a edição 2026-1 da Global Solution não permitir foco espacial direto, precisa ser reenquadrado como auditoria de IA-assistiva em qualquer cenário operacional (incluindo telemedicina amazônica — aplicação dual natural).

---

### P2 — **AeroSUS**: análogo brasileiro certificado + ferramentas de cuidado familiar

**O que é:** proposta institucional para certificar uma unidade SUS amazônica (e/ou o HRT) como análogo terrestre certificado de missão espacial de longa duração, com:
- protocolo clínico pediátrico-familiar adaptado,
- IA copiloto auditável (re-uso do AuditCMO),
- governança LGPD-derived,
- plataforma de formação distribuída para profissional único na ponta.

**Lacunas cobertas:** L2, L3, L4, L5 (com pedaço de L1).

**Vantagem competitiva:** **inversão da assimetria Norte-Sul**. Brasil deixa de importar análogos e oferece análogo mais completo (com família, pediatria, gestação) — o que falta nos análogos do Norte. Aplicação imediata terrestre: melhoria real de cuidado a populações isoladas.

**Cabe num semestre FIAP?** Versão completa não, mas **MVP de uma vertical** sim — ex: módulo pediátrico de IA copiloto auditável testado em cenário simulado de comunidade ribeirinha.

**Riscos:** ambicioso. Risco de "guarda-chuva conceitual sem entrega" se mal escopado. Mitigação: começar pela vertical pediátrica que tem o Iúri como dono natural.

---

### P3 — **KidSpace**: framework de risk-benefit pediátrico para colônia espacial

**O que é:** paper-position robusto + ferramenta computacional de risk-benefit assessment para cuidado pediátrico em ambiente análogo / colônia espacial precoce, baseado em dados de pediatria amazônica como proxy.

**Lacunas cobertas:** L3, L6 (com pedaço de L4).

**Vantagem competitiva:** território virgem globalmente; pediatra brasileiro com experiência HRT é perfil raríssimo nesse campo.

**Cabe num semestre FIAP?** O paper-position sim. A ferramenta computacional só em MVP simples (assistente de decisão em web app).

**Riscos:** mais ensaístico que prototípivel. Risco de virar trabalho de filosofia sem o componente de tecnologia que a FIAP costuma valorizar.

---

### P4 — **EduCMO**: plataforma de educação médica distribuída para ambiente extremo

**O que é:** plataforma de microlearning + simulação interativa + IA-tutora baseada em casos clínicos, desenhada para formação continuada de profissional único na ponta (CMO espacial ou médico de unidade isolada SUS).

**Lacunas cobertas:** L2, L4 (com pedaço de L3).

**Vantagem competitiva:** Iúri já produz material formativo de qualidade (apostilas, curso PMDF Resiliência, mentor). Esta é a forma natural de transformar isso em produto digital.

**Cabe num semestre FIAP?** Sim, em escopo enxuto: 1 módulo clínico (ex: respiratório pediátrico) + simulação adaptativa.

**Riscos:** corre risco de competir com produtos comerciais maduros (Osmosis, AMBOSS) se não tiver ângulo bem diferenciado. O ângulo precisa ser **especificidade do ambiente extremo** — não "mais um app de medicina".

---

## 5. Critérios de decisão entre os candidatos

| Critério | P1 AuditCMO | P2 AeroSUS | P3 KidSpace | P4 EduCMO |
|---|---|---|---|---|
| Continuidade com Aurora SIGER | **Alta** | Média | Baixa | Baixa |
| Ataca diretamente a tese do post | **Alta** | Média | Média | Baixa |
| Originalidade autoral | Média | **Alta** | **Alta** | Média |
| Prototipável num semestre | **Alta** | Média | Média | **Alta** |
| Aplicação dual (espaço + Brasil) | **Alta** | **Alta** | Média | **Alta** |
| Risco de virar bagagem morta se GS pivotar | Baixa | Baixa | Média | Baixa |
| Equilibra os 3 papéis da tríade | **Alta** | **Alta** | Média | Média |

**Recomendação operacional:**

> **P1 AuditCMO como núcleo, com gancho explícito para crescer em P2 AeroSUS** quando o tema oficial da Global Solution for revelado em 25/05.

Justificativa: P1 é o que tem a melhor combinação de (a) continuidade com o trabalho anterior do Iúri, (b) fidelidade à tese do post, (c) prototipabilidade dentro do semestre, (d) flexibilidade pra pivotar. P2 é a evolução natural se o tema permitir ambição maior.

Se a edição 2026-1 da Global Solution focar especificamente em **profissões do amanhã + IA + saúde**, P1 reenquadrado para qualquer contexto clínico (não necessariamente espacial) atende perfeitamente.

---

## 6. Próximos passos sugeridos (dependentes de validação do Iúri)

1. **Decisão prévia**: Iúri valida (ou pivota) a recomendação P1+P2 acima.
2. **22-24/05**: aprofundar uma das 4 referências-chave pendentes — provavelmente Russell et al. 2023 (CDSS espacial) e Heath et al. 2025 (reprodução em espaço), porque são os "papers de produto" diretamente acionáveis. Notas em `notes/divergente-saude-espaco/`.
3. **25/05**: capturar briefing oficial da Global Solution. Confrontar com a recomendação. Pivotar se necessário.
4. **Pós-25/05**: a depender do tema, criar `essay/` com proposta articulada ou `code/` para protótipo.

---

## 7. Frase-âncora pra qualquer entregável

> *"Eficiência sem ética é apenas uma forma mais sofisticada de desperdício."*
>
> *"Para quem essa tecnologia funciona, com que transparência e sob qual governança?"*

Ambas vão da Terra ao espaço sem perder peso.

---

## 8. Atualização pós-deep-dive (2026-05-21)

Após leitura aprofundada de **Russell et al. 2023** (CDSS espacial) e do conjunto **Heath/Palmer/Karouia 2025 + Cutigni 2025 + Sharma 2024** (reprodução em espaço), três achados modificam o quadro acima. Detalhes em [`10-russell-2023-deep-dive.md`] e [`11-reproducao-pediatria-2025-deep-dive.md`].

### 8.1 P1 AuditCMO sai validado e ganha v0 de especificação

Russell 2023 confirma **por ausência** o terreno do P1: o paper-âncora do CDSS espacial não tem protocolo de auditoria formal, não tem framework de governança ética/regulatória, não tem transparência de modelo bayesiano, não tem cenários de falha, e não tem população não-adulta. Os próprios autores reconhecem que *"the clinical and operational validity of this proposed approach has yet to be peer reviewed."*

O framework **C-SoP / P-SoP** (Cognitive vs Procedural Scope of Practice, escala 0-5) é importável diretamente como vocabulário do P1. O achado central — *"cognitive skills had a greater effect on outcomes than procedural skills"* — valida o eixo educador da tríade.

Especificação v0 do P1 agora existe em `10-russell-2023-deep-dive.md §8` — schema do log auditável com 9 campos (timestamp, clinical_input, cdss_inference, cdss_confidence, crew_decision, crew_rationale, divergence_flag, cognitive_state_proxy, outcome_followup).

### 8.2 P3 KidSpace ganha força — campo é literalmente pré-paradigmático

Heath 2025 (Karouia/NASA): *"reproductive health can no longer remain a policy blind spot. International collaboration is urgently needed."* Palmer: tecnologias reprodutivas espaciais entram *"incrementally, quietly and often justified after the fact."*

**Pediatria espacial** está ausente de **todas** as três revisões recentes sobre reprodução em espaço. Sharma 2024, Cutigni 2025 e Heath 2025 cobrem gameta, embrião e gestante — não cobrem criança. Iúri é pediatra. Vantagem competitiva por ausência sistemática nas referências do campo, não por especulação.

Quantitativos consolidados: 60+ anos de voo humano, 0 partos, 0 intercursos sexuais reportados, 11-22,7% astronautas mulheres, oocyte maturation cai de 73% para 8,94% em microgravidade simulada, dose de radiação interplanetária até 1.070 mSv (vs 54-108 em LEO).

Refinamento sugerido para P3: tese passa a ser *"Pediatria espacial precoce: framework de risk-benefit derivado de pediatria amazônica brasileira como análogo terrestre mais completo."* Combina L3 + L4 + L6 numa frase autoral.

### 8.3 Insight farmacológico-translacional (Cutigni 2025)

Cutigni observa que o padrão endócrino de microgravidade *"looks like the picture observed in PCOS"* (Síndrome dos Ovários Policísticos). Implicação: tratamentos PCOS desenvolvidos para uso terrestre podem ser aproveitáveis como countermeasure espacial. Esse é um **vetor de pesquisa reverso** interessante (Terra → espaço), mas escapa do escopo de um semestre FIAP. Vale guardar como referência para a tese de longo prazo (eixo IA & florescimento humano, projeto `eixo_ia_florescimento`).

### 8.4 Correção factual

A referência prévia como "Goyal et al. 2024" está errada. Autores corretos do PMC11646162: **Sharma P., Malik S., Sarkar A.** (Cureus, 14/11/2024, ESIC Medical College, Faridabad/Índia). Corrigido em `11-reproducao-pediatria-2025-deep-dive.md`.

### 8.5 Matriz de produtos atualizada

| Critério | P1 AuditCMO | P2 AeroSUS | P3 KidSpace | P4 EduCMO |
|---|---|---|---|---|
| Continuidade com Aurora SIGER | **Alta** | Média | Baixa | Baixa |
| Ataca diretamente a tese do post | **Alta** | Média | Média | Baixa |
| Originalidade autoral | Média | **Alta** | **Alta ↑** | Média |
| Prototipável num semestre | **Alta ↑** (v0 já esboçada) | Média | Média | **Alta** |
| Validação do campo (literatura confirma o gap) | **Alta ↑** | Média | **Alta ↑** | Baixa |
| Aplicação dual (espaço + Brasil) | **Alta** | **Alta** | **Média ↑** | **Alta** |
| Risco de virar bagagem morta se GS pivotar | Baixa | Baixa | Média | Baixa |
| Equilibra os 3 papéis da tríade | **Alta** | **Alta** | Média | Média |

(↑ = ganho relativo após deep-dive.)

### 8.6 Recomendação operacional refinada

A recomendação P1 + P2 (núcleo + extensão) permanece, mas com modulação:

- **P1 AuditCMO** agora tem v0 esboçada. Pode começar protótipo (Aurora-SIGER-style, Python + SQLite + dashboard mínimo) já em **22-24/05** sem esperar 25/05.
- **P3 KidSpace** subiu como alternativa forte para a vertical pediátrica de P2, com tese reformulada acima. Se o tema de 25/05 favorecer ângulo de **políticas / governança** em vez de **protótipo técnico**, P3 + P2-pediátrico pode passar a ser o eixo principal.

### 8.7 Frases-âncora adicionais

> Russell 2023: *"The system's role is not to react perfectly but to aid the clinician with a second opinion."* — defesa de design contra IA-substitutiva.

> Karouia 2025: *"Reproductive health can no longer remain a policy blind spot."* — janela de governança aplicada à reprodução espacial.

> Palmer 2025: tecnologias reprodutivas espaciais entram *"incrementally, quietly and often justified after the fact."* — espelha o argumento do post sobre IA terrestre, no campo reprodutivo espacial.

Os três autores convergem no diagnóstico — campo avança sem governança — que é exatamente a tese do post.

---

## 9. Pivot 2026-05-21: P3 descontinuado, P1 expandido como foco único

**Decisão do Iúri:** pediatria espacial (P3 KidSpace) é remota demais para ser produto da Global Solution 2026-1. A nota de pesquisa `11-reproducao-pediatria-2025-deep-dive.md` permanece como referência histórica/futura, mas P3 sai do trilho ativo.

**P1 AuditCMO passa a ser foco único**, expandido com interface explícita em:
- **Ética operacional de IA em saúde** (frameworks regulatórios e de auditoria)
- **Moral em edge cases extremos** (filosofia aplicada a decisão sob escassez, latência e isolamento)

Justificativa do escopo expandido: o ângulo crítico do post — *"para quem essa tecnologia funciona, com que transparência e sob qual governança?"* — exige fundamentação dupla. O lado **operacional** (FDA SaMD, EU AI Act, WHO 2021, NIST AI RMF, ISO/IEC 42001) responde *como auditar*. O lado **filosófico** (Beauchamp & Childress, NASEM, Scanlon, Williams, triagem em catástrofe) responde *o que vale auditar e por quê*. Sem os dois, P1 vira ou ferramenta sem alma, ou ensaio sem código.

P2 AeroSUS (análogo brasileiro) e P4 EduCMO permanecem como **extensões opcionais pós-25/05** caso o tema oficial demande.

Próxima etapa registrada em `notes/etica-ia-edge-cases/` (nova pasta) — mix ~60% operacional + ~40% filosófico, aprovado em 21/05/2026.

---

## 10. Pós-expansão (Fase 3) — P1 AuditCMO v0.3 consolidado

Síntese completa em [`notes/etica-ia-edge-cases/00-sintese-etica-edge-cases.md`]. Resumo do que mudou:

### 10.1 Descoberta crítica
**Alu & Oluwadare 2026** (Frontiers in AI, 04/02/2026, PMC12913532) publicaram framework **quase idêntico** ao P1 — mas para CDSS clínico **terrestre comum**, em forma **puramente conceitual** (sem implementação, sem teste, sem validação empírica declarada pelos próprios autores).

**Implicação:** P1 deixa de ser "invenção" e passa a ser **especialização do framework Alu/Oluwadare para edge cases extremos** (espacial + austero). Posicionamento autoral fica mais claro, ganha aliado canônico recente.

### 10.2 Cinco princípios convergentes adotados como espinha normativa

B&C + Floridi/Cowls + WHO 2021 + NASEM convergem em: **autonomy, beneficence, non-maleficence, justice, explicability**. P1 v0.3 obriga o registro de qual princípio prevaleceu em cada decisão crítica.

### 10.3 Vocabulário de ambientes austeros importado

Pingree et al. 2020 (HEC Forum) — *"princípios imutáveis, aplicação variável"*. Conceitos centrais incorporados ao P1:
- Triagem militar (Immediate/Delayed/Minimal/Expectant).
- "Physician first, officer second" → "Clínico first, AI-operator second".
- Minimal necessary standard → como o CDSS espacial revela info à Terra.
- Treinamento a priori + protocolo desenhado antes da crise.
- Lessons learned publicadas → log do P1 alimenta isso.

### 10.4 Backbone regulatório explícito

- **EU AI Act 2024** (Articles 12, 13, 14, 15) — entrada em vigor 02/08/2026.
- **WHO 2021** — 6 princípios.
- **ISO/IEC 42001:2023** — AIMS, PDCA adaptado para missão isolada.

### 10.5 Schema do log v0.3 — campos adicionados

- `cognitive_state_proxy` (CO₂, fadiga, latência de teclado).
- `principle_prioritized` (qual dos 5 prevaleceu).
- `principle_conflict_acknowledged` + `notes`.
- `mode` (routine/isolated/emergency) com regras de override diferentes.
- `ledger_hash_prev` + `ledger_hash_self` (cadeia hash sem necessidade de Hyperledger online).

### 10.6 Tese-âncora final do P1

> Em ambiente espacial autônomo (EIMO), a pergunta *"para quem essa tecnologia funciona, com que transparência e sob qual governança?"* não pode ser respondida em tempo real. O CDSS decide, o humano confirma, e a única governança possível é **diferida** — exercida em revisão pós-fato sobre registros que precisam ser densos o suficiente para reconstituir o estado mental do operador, o estado da máquina e o estado moral da decisão.
>
> P1 AuditCMO é a engenharia dessa **governança diferida**: não impede más decisões; garante que cada decisão deixe um rastro auditável o bastante para deliberação ética posterior, proteção legal/moral do operador (contra moral injury, Pingree 2020), e aprendizado institucional.

### 10.7 Próxima decisão pendente (do Iúri)

(a) Manda P1 v0.3 pra protótipo já agora (esqueleto Python em `code/`).
(b) Mais uma rodada de leitura (Antonsen 2022, Wakayama 2009, NASEM Health Standards 2014) — fecha o último 10% de pendências.
(c) Esboça paper-position em `essay/` reenquadrável quando o tema oficial sair em 25/05.

---

## 11. Rodada de fechamento 21/05/2026 — pendências resolvidas

Decisão prévia (b) executada. Resultado:

### 11.1 Antonsen & Myers 2022 — mantido como relevante, deep dive em [`12-antonsen-myers-2022-deep-dive.md`]

Justificativa: as 100 condições médicas do IMM são universo de teste acionável pro protótipo P1; assumption brutal *"every diagnosis and treatment 100% effective"* é exatamente o ponto que P1 ataca; LSDA é repositório público de dados; encadeamento Antonsen (medir) → Russell (resolver) → P1 (auditar) é defensável academicamente.

### 11.2 Wakayama 2009 — descontinuado junto com P3

Pendência removida. Nota `11-reproducao-pediatria-2025-deep-dive.md` recebeu cabeçalho marcando o status — conteúdo preservado como histórico (útil ao eixo IA-florescimento de longo prazo, se retomar o assunto).

### 11.3 Follow-up Alu/Oluwadare — ENCONTRADO

**Alu, Oluwadare, Halliday, Agwunobi 2026** (Frontiers in AI, aceito 11/03/2026, PMC13106396) implementou empiricamente em cenário controlado o framework conceitual de fev/2026. Achado contra-intuitivo notável: **logistic regression mostrou 57% mais bias que random forest** — *"interpretability does not guarantee fairness"*.

Importação direta: **AFPR (AI Fairness Provenance Record)** com 5 componentes, embutível no P1 v0.3 como módulo de fairness. Detalhes em [`../etica-ia-edge-cases/operacional/alu-et-al-2026-fairness-provenance-audit.md`].

### 11.4 ISO/IEC 42005:2025 — PUBLICADA

Não mais draft. Maio/2025. AI System Impact Assessment. Fecha a trinca **EU AI Act + ISO 42001 + ISO 42005**. Detalhes em [`../etica-ia-edge-cases/operacional/iso-iec-42005-2025.md`].

### 11.5 NASEM Health Standards 2014 cap 5 — LIDO

**Decision framework de 3 níveis** (categoria de missão → design específico → seleção individual). 6 princípios (incluindo **Fidelity** — ausente em B&C e Floridi/Cowls). Detalhes em [`../etica-ia-edge-cases/filosofico/nasem-health-standards-2014-cap5.md`].

Importação: o framework de 3 níveis vira **esqueleto do paper-position** do P1. Fidelity vira a justificativa filosófica do **log auditável de longa duração** — o sistema é a infraestrutura material do compromisso da sociedade com quem aceitou risco.

### 11.6 WHO 2021 §5-6 — leitura parcial completada

Texto integral ainda não acessado, mas adjacente consolidou: transparency virou **dever operacional** (não retórica), explainability é **task-appropriate** (graduável por modo do P1). Atualização em [`../etica-ia-edge-cases/operacional/who-2021-floridi-cowls-2019-principios-ia-saude.md`] §7.

### 11.7 Estado atual

Pendências de leitura pré-25/05 zeradas. Três caminhos abertos pro Iúri decidir:

- **(a)** Protótipo Python em `code/` — esqueleto Aurora-SIGER-style + AFPR + cenários sintéticos do IMM/LSDA. 1-2 dias ativos modo PI+Claude+Codex.
- **(b)** Paper-position em `essay/` — argumento articulado seguindo NASEM 3 níveis + pirâmide Antonsen-Russell-P1. ~1 dia ativo. Reenquadrável após 25/05.
- **(c)** Esperar 25/05 com quadro completo e pivotar pra dentro do tema oficial.
