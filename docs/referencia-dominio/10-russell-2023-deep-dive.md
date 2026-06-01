# Russell et al. 2023 — Clinical Decision Support System para Earth-Independent Medical Operations (deep dive)

**Referência completa:** Russell, B. K.; Burian, B. K.; Hilmers, D. C.; Beard, B. L.; Martin, K.; Pletcher, D. L.; Easter, B.; Lehnhardt, K.; Levin, D. (2023). *The value of a spaceflight clinical decision support system for earth-independent medical operations*. **npj Microgravity** 9, 46. DOI: 10.1038/s41526-023-00284-1. PMC10284846. Publicado em 21/06/2023.

**Afiliações:** NASA Ames Research Center (5 autores), NASA Johnson Space Center (3 autores), Auckland University of Technology, Baylor College of Medicine, Columbia University.

**Confiança:** alta — paper open access PMC, lido em detalhe via WebFetch.

## Por que esta nota está em deep dive e não em síntese curta

Russell 2023 é o **paper-âncora** para o produto P1 AuditCMO e qualquer protótipo de CDSS espacial. A leitura cuidadosa identifica simultaneamente o framework conceitual a herdar **e** os gaps específicos a preencher. Vale o esforço extra.

---

## 1. O argumento central

A NASA prepara missões lunares e marcianas que mudarão o paradigma de suporte médico a astronautas — de telemedicina síncrona com a Terra para **Earth-Independent Medical Operations (EIMO)**. O Exploration Medical Capability (ExMC), elemento do Human Research Program (HRP), investiga viabilidade de capacidades avançadas para promover EIMO. A proposta central é um **Clinical Decision Support System (CDSS)** embarcado que amplie cognitiva e proceduralmente o tripulante não-médico.

## 2. O framework C-SoP / P-SoP — o que merece ser importado

A inovação conceitual mais útil do paper é a separação entre **Scope of Practice cognitivo (C-SoP)** e **procedural (P-SoP)**, ambos numa escala 0-5:

| Nível | Equivalência terrestre |
|---|---|
| 0 | Leigo sem treinamento |
| 1 | EMT-B (técnico em emergência básico) — equivale ao treinamento atual do CMO da ISS |
| 2 | Paramédico |
| 3 | Enfermeiro de emergência |
| 4 | Médico PGY-1 |
| 5 | Médico Attending experiente |

**Achado crítico:** as habilidades **cognitivas** têm efeito maior nos desfechos do que as procedurais — o que muda o foco do CDSS para apoio ao raciocínio, não execução de tarefa.

> *"Cognitive skills had a greater effect on outcomes than procedural skills, as demonstrated in the use case below where lack of early diagnosis could be the difference between an untreated severe condition or a quick resolution."*

Para um produto da tríade, isso valida o eixo educador: a competência cognitiva é alavanca maior que a procedural.

## 3. Resultados quantitativos — leitura crítica

Cenário simulado: missão de referência de **26 meses** em deep space.

**Achado principal:**
> *"With a C-SoP of 1 and P-SoP of 1, roughly equivalent to ISS CMO training, our simulation reference mission of 26 months had up to 3 deaths, but if CDSS can increase C-SoP and P-SoP to level 5, preliminary results show this can be reduced by a minimum of 34%."*

Tradução: 3 mortes → ~2 mortes em 26 meses, redução mínima de 34%.

**Variação do Crew Health Index (CHI):** 15-88%, dependendo da capacidade médica (citação de Antonsen & Myers 2022, missão de 1195 dias).

**Honestidade metodológica dos autores:**
> *"Although the mathematical approach is straightforward, the clinical and operational validity of this proposed approach has yet to be peer reviewed."*

Conclusão metodológica: o paper é **documento de posicionamento estratégico**, não estudo empírico. Os 34% são simulação teórica via Probabilistic Risk Analysis (PRA) sobre o programa NASA **IMPACT-MD** (Informing Mission Planning via Analysis of Complex Trade-spaces Medical Database). Não há p-valores, IC, validação prospectiva — e os autores reconhecem isso explicitamente.

## 4. Funções recomendadas para o CDSS (Tabela 1 reconstituída)

| Domínio | Função |
|---|---|
| **Emergência** | Protocolos ABCDE pré-determinados; vital signs em tempo real |
| **Rotina-Diagnóstico** | Engine probabilístico bayesiano; próxima pergunta com maior valor preditivo positivo |
| **Rotina-Tratamento** | Opções terapêuticas ordenadas; checagem automática de alergias; localização de medicamentos |
| **Prevenção** | Ambient monitoring (movimento, timing de teclado para detectar fadiga cognitiva) |

Pontos a destacar:
- O **ambient monitoring** (keyboard timing como proxy de fadiga cognitiva) é exemplo interessante de instrumento passivo — pode inspirar feature do P1 AuditCMO.
- O **bayesian engine** é caixa-preta no paper — abertura para o que P1 propõe (auditabilidade do raciocínio probabilístico).

## 5. Gaps técnicos declarados

1. **Escassez de dados LDEM** — Apollo voou no máximo 12 dias lunares; missões longas de espaço profundo não têm precedente clínico.
2. **Restrições computacionais** — massa, volume, energia limitados a bordo.
3. **Stressors cognitivos da tripulação** — CO₂ elevado, auditory overload, dor musculoesquelética, disrupção circadiana, isolamento, diferenças culturais, fadiga.
4. **Condições nunca observadas** — eventos clínicos sem precedente em terra ou no espaço.

## 6. **Gaps NÃO declarados — onde o P1 AuditCMO entra**

A análise crítica do paper revela **ausências sistemáticas** que abrem espaço para produto autoral:

### 6.1 Auditoria formal — NENHUMA
- Log é mencionado en passant: *"CDSS closes the encounter and logs the data in the patient's chart."*
- Não há protocolo de auditoria, format de log padronizado, política de retenção, ou mecanismo de revisão pós-fato.
- **P1 AuditCMO endereça isso.**

### 6.2 Governança ética/regulatória — NENHUMA
- Sem discussão de comissão de ética, validação clínica formal, homologação regulatória.
- Sem framework para falha do CDSS (quem é responsável?).
- Sem discussão de consentimento informado em emergência autônoma.
- **L1 e L6 da síntese se confirmam como brutalmente reais.**

### 6.3 Transparência do modelo — NENHUMA
- O *bayesian engine* é apresentado como caixa-preta funcional.
- Sem discussão de explainable AI, intervalos de confiança apresentados ao usuário, ou contestação humana estruturada.
- **A frase do post — "para quem, com que transparência, sob qual governança?" — é especificação técnica direta aqui.**

### 6.4 Populações fora do "adulto saudável selecionado" — NENHUMA
- O texto trata exclusivamente de "exploration crew", "astronauts", "CMO".
- **AUSÊNCIA TOTAL** de menção a:
  - Crianças / pediatria
  - Mulheres grávidas
  - Idosos
  - Comorbidades pré-existentes
  - Diversidade de composição
- **L3 da síntese se confirma — P3 KidSpace tem terreno aberto.**

### 6.5 Cenários de falha — NENHUMA
- Não há análise de modos de falha do CDSS (false positive, false negative, deriva de modelo, ataque adversarial).
- Sem playbook para "quando ignorar o CDSS".

## 7. Frase para guardar como âncora

> *"The system's role is not to react perfectly but to aid the clinician with a second opinion and provide reassurance that their approach is logical in the face of limited data."*

Essa frase **é defesa de design** contra o paradigma de IA-substitutiva. Útil pra fundamentar P1 (que preserva agência clínica) contra um CMO-DA-style (que mais cedo ou mais tarde substitui).

## 8. Implicação para o P1 AuditCMO — especificação

A leitura aprofundada permite escrever a v0 da especificação do P1:

**P1 AuditCMO v0** — sistema de auditoria embarcado para CDSS de medicina espacial autônoma. Cada interação CDSS↔tripulante gera registro auditável contendo:

| Campo | O que captura |
|---|---|
| `timestamp_utc` | momento da interação |
| `clinical_input` | sinais vitais, sintomas, imagens, voz capturados |
| `cdss_inference` | hipóteses diagnósticas + probabilidades posteriores |
| `cdss_confidence` | intervalo de confiança ou medida equivalente |
| `crew_decision` | decisão final do tripulante |
| `crew_rationale` | justificativa registrada (texto, voz) |
| `divergence_flag` | true se decisão divergir da recomendação top-1 |
| `cognitive_state_proxy` | CO₂, hora do dia, fadiga estimada por ambient monitor |
| `outcome_followup` | desfecho clínico em T+24h, T+72h, T+30d |

Operação:
- O log é local-first (latência), sincronizado com Terra quando possível.
- Estrutura inspirada em **Aurora SIGER Fase 2**: tabela-verdade da decisão exposta + faixas seguras documentadas + histórico empilhado.
- Auditável on-demand: tripulante e Terra podem inspecionar qualquer decisão.

Aplicação dual:
- **Espacial**: missão de longa duração, EIMO.
- **Terrestre**: hospital de pequeno porte com IA-assistiva, telemedicina amazônica, UTI sob plantão único.

## 9. O que ainda preciso saber

- A NASA IMPACT-MD database é aberta? Se sim, dá base empírica ao protótipo.
- A versão 3001-Vol2 do **NASA-STD-3001** (Crew Health) tem requisitos explícitos sobre logging de CDSS? Vale checar.
- Hay paper de follow-up de Russell et al. (2024-2025) com validação prospectiva? Buscar.

## 10. Gancho final com o post de 07/04

Russell 2023 confirma, sem usar essas palavras: o CMO-DA-style está sendo desenhado **sem** governança, **sem** auditoria, **sem** mecanismo de contestação, e **sem** população não-adulta. A pergunta do post — *para quem essa tecnologia funciona, com que transparência e sob qual governança?* — recebe três respostas vazias quando aplicada ao estado da arte. Esse vazio **é** a oportunidade.
