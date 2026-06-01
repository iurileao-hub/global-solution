# Antonsen, Myers et al. 2022 — *Estimating medical risk in human spaceflight* (deep dive)

**Referência completa:** Antonsen, E. L.; Myers, J. G.; Boley, L.; Arellano, J.; Kerstman, E.; Kadwa, B.; Buckland, D. M.; Van Baalen, M. (2022). *Estimating medical risk in human spaceflight*. **npj Microgravity** 8, 8. DOI: 10.1038/s41526-022-00193-9. PMC8971481. Publicado 31/03/2022.

**Afiliações:** NASA Johnson Space Center (Antonsen e maioria), NASA Glenn (Myers), KBR (operador do IMM em contrato com NASA).

**Confiança:** alta — paper open access, lido em detalhe via WebFetch.

## Por que esta nota está em deep dive

Antonsen 2022 é o **paper-fonte do framework de risco médico** que Russell 2023 cita para fundamentar o CHI. É também o **único PRA (Probabilistic Risk Assessment) quantitativo** publicado para missão de Marte em humanos. Conhecer seus números em detalhe é base empírica direta pro P1 — dá o universo de teste, define a magnitude do problema, e expõe o ponto exato onde o P1 ocupa: a *"100% effective"* assumption do IMM.

## 1. O argumento central

A NASA precisava de **estimativa quantificada de risco médico** comparável entre durações de missão, mas até 2022 não existia. O Integrated Medical Model (IMM) é uma simulação Monte-Carlo de Probabilistic Risk Assessment que produz essa estimativa. O paper compara 7 Design Reference Missions (DRMs) de 14 a 1.195 dias e mostra que **risco médico cresce não-linearmente com duração** e que **capacidade médica importa muito mais em missões longas**.

> *"To date, there have been no reliable estimates of how much [risk]."*

## 2. O Integrated Medical Model (IMM) — arquitetura

### Inputs
- **100 condições médicas** modeladas (catálogo completo em Extended Data, Table 2).
- Base de dados: **Integrated Medical Evidence Database (iMED)** — Apollo, Skylab, Mir, Shuttle, ISS.
- Recursos médicos baseline = ISS medical system.
- Atributos de tripulação considerados: sexo, coronary artery calcium score, dental crowns, contact lens use, prior abdominal surgery.

### 7 Design Reference Missions

| DRM | Duração (dias) | Tripulação |
|---|---|---|
| 1 | 14 | 7 |
| 2 | 21 | 4 |
| 3 | 42 | 4 |
| 4 | 180 | 6 |
| 5 | 365 | 4 |
| 6 | 730 | 4 |
| 7 | **1.195** | 4 (cenário Marte) |

### Capacidades modeladas (3 cenários)
1. **No Medical Capability** — pior caso.
2. **Unlimited ISS Medical Capability** — melhor caso (com resupply infinito).
3. **Limited ISS Medical Capability** — realista (sem resupply, meds podem acabar).

### Monte-Carlo
- **100.000 trials** por simulação.
- Convergência: <5% mudança em desvio padrão de CHI, EVAC, LOCL.

### Outputs
- **TME** (Total Medical Events) — número de eventos.
- **CHI** (Crew Health Index) — % de funcionalidade da tripulação.
- **EVAC** — probabilidade de evacuação médica.
- **LOCL** (Loss of Crew Life) — probabilidade de morte.

## 3. CHI — definição operacional e a frase importante

### Fórmula
> **CHI = (1 − QAMTL/MissionLength) × 100**

QAMTL = Quality-Adjusted Mission Time Lost = soma do impairment funcional × duração em **três fases clínicas**:
1. Diagnóstico e tratamento inicial.
2. Tratamento contínuo.
3. End-state (resolução, incapacidade permanente ou morte).

### Escala
- 0 = tripulação totalmente incapacitada.
- 100 = tripulação totalmente funcional.

### Limitação **brutal** declarada
> *"Note that the AMA Guides estimate permanent impairment based on terrestrial norms. Application of these assessments in estimating functional impairment in a spaceflight environment likely overpredict impairment in some outcomes (i.e., lower limbs) and underpredict impairment in other instances (i.e., eyes, hands)."*

Tradução: o CHI **superestima** dano em membros inferiores (porque microgravidade neutraliza muito do uso terrestre) e **subestima** dano em olhos e mãos (porque em microgravidade essas são via principal de operação). Esse é o tipo de gap que P1 captura via `cognitive_state_proxy` + `outcome_followup`.

## 4. Resultados quantitativos para Marte (DRM 7, 1.195 dias, 4 tripulantes)

| Cenário | CHI | LOCL | EVAC |
|---|---|---|---|
| No Medical | ~15% | ~4-6% | ~95%+ |
| Limited ISS Medical | ~70-75% | ~1-2% | ~20-30% |
| Unlimited ISS Medical | ~85-88% | ~1-2% | ~15-25% |

**Comparação histórica de tolerância de risco:** LOC aceito no fim do Space Shuttle Program = **1/90 (~1.1%)**. Em DRM 6 (730 dias) e DRM 7 (1.195 dias), **LOCL excede 1.1% mesmo com Unlimited ISS Medical Capability** — ou seja, missão Marte sob protocolo atual estaria **acima do nível de risco historicamente aceito**.

## 5. A frase que abre o nicho do P1

> *"For these simulations IMM assumes that every diagnosis and treatment are 100% effective."*

Essa é a assumption mais consequente do modelo, e a mais frágil. **CDSS reais (CMO-DA Google/NASA) têm 88% accuracy em casos simulados, não 100%.** Sob a assumption de 100%, o LOCL de ~1-2% representa o **piso teórico**. Sob accuracy realista, o LOCL pode ser substancialmente maior — e a fração derivada da **falha do sistema de IA** precisa ser auditável pra que melhorias sejam mensuráveis.

P1 AuditCMO ocupa exatamente esse intervalo entre a assumption (100%) e o real (88%). Sem auditoria, esse intervalo é invisível operacionalmente.

## 6. Lista exaustiva de limitações declaradas pelos autores

### Limitations declaradas
1. **CHI baseado em normas terrestres** (AMA Guides).
2. **Independência de condições** — UTI → sepse não modelada como progressão.
3. **100% effectiveness** assumido em diagnóstico/treatment.
4. **Sem failure modes** de instrumentos de monitoramento.
5. **Validação retroativa parcial**: modelo superpredisse missões >180d e subpredisse curtas.
6. **Base de dados pequena**: <600 pessoas em voo sob condições não-padronizadas.

### Capacidades não implementadas
1. **Saúde pós-missão** (efeitos terrestres pós-retorno).
2. **Perda de comunicações em tempo real** — efeito provavelmente negativo.
3. **Resupply limitado**.
4. **EVAs** (0.26 injuries/EVA, mãos e extremidades superiores).
5. **Deconditioning imunológico**.
6. **Degradação farmacêutica**.
7. **Efeitos psicológicos** (depressão, ansiedade, insônia crescem com duração).

### Conclusão metodológica dos próprios autores
> *"The net effect of these unimplemented capabilities and model limitations suggest that the LEO-specific estimates shown here are likely to underpredict the medical risk in real lunar or Mars missions."*

## 7. Repositório público — NASA LSDA

> *"The NASA Life Sciences Data Archive (LSDA) is the repository for all human and animal research data, including that associated with this study. LSDA has a public-facing portal where data requests can be initiated."*

URL: https://lsda.jsc.nasa.gov/

**Implicação pro P1:** o LSDA é a **fonte de dados acionável** pra protótipo. As 100 condições do IMM podem ser usadas como universo de teste sintético do AuditCMO sem precisar inventar cenários.

## 8. Sobre populações fora do "adulto saudável selecionado"

**AUSÊNCIA TOTAL.** Crianças, grávidas, idosos, comorbidades não modeladas.

> *"The model does not consider most crew attributes that are already attenuated by the astronaut selection standards and flight certification standards."*

Isso confirma o ponto da síntese: o estado da arte assume tripulante adulto selecionado. Para Global Solution 2026-1, isso é irrelevante (P3 KidSpace foi descontinuado); mas vale registrar como evidência adicional de que **o IMM herda exatamente o ponto cego da literatura toda**.

## 9. Sobre auditoria e governança no IMM

O paper declara:
- **Validação** com 4 anos de dados ISS + 20 missões Shuttle (subconjunto retido).
- **Transparência sobre pressupostos** — seção inteira dedicada a limitações.
- **Propriedade**: IMM v4.1 é do NASA Johnson, operado por KBR sob contrato.

**O que falta** (e que o P1 endereça): **transparência sobre falhas do CDSS em tempo de uso**, **mecanismo de contestação pelo CMO**, **registro de divergência humano × modelo**. O IMM é ferramenta de planejamento estratégico; o P1 é ferramenta de operação tática.

## 10. Implicação direta no P1

### O que importamos
- **Universo de teste**: as 100 condições do IMM ⇒ casos sintéticos para validação Phase 1 do P1.
- **Métricas baseline**: CHI, LOCL, EVAC ⇒ se P1 é eficaz, override rate humano deveria correlacionar com mudanças nessas métricas.
- **NASA LSDA**: fonte de dados pra calibração.

### O que estendemos
- **Adicionar fator "CDSS accuracy"** ao IMM — atualmente assumida 100%, deveria ser variável.
- **Adicionar fator "human override quality"** — quando o CMO discorda, qual é o outcome diferencial?
- **Logging das decisões individuais** preenche o que o IMM agrega.

## 11. Frase-âncora pro P1

> *"For these simulations IMM assumes that every diagnosis and treatment are 100% effective."*

Essa frase, no slide de abertura do entregável da Global Solution, justifica a existência do P1 em uma linha.

## 12. Validação cruzada com Russell 2023

Russell 2023 (`10-russell-2023-deep-dive.md`) cita Antonsen 2022 como referência principal pro CHI. A leitura cruzada confirma: Russell usa o CHI definido por Antonsen, propõe o CDSS para elevar C-SoP/P-SoP, mas **não fecha o loop** — não diz como auditar se o CDSS está performando como esperado. Antonsen mensura o problema; Russell propõe a solução; **P1 fecha o loop com auditabilidade contínua**.

Os três trabalhos formam pirâmide coerente: Antonsen (medir), Russell (resolver), P1 (auditar). Esse encadeamento é defensável academicamente.
