# Governança de dados de saúde no espaço

**Referências:**
- HIPAATimes. *Does HIPAA apply to astronauts?* https://hipaatimes.com/does-hipaa-apply-to-astronauts
- *Developing an international database on long-term health effects of spaceflight*. ScienceDirect 2022. https://www.sciencedirect.com/science/article/abs/pii/S0094576522002855
- Maurer Global Forum (2024). *Data Privacy in Space Tourism: A New Frontier for an Adequate Legal Framework*. https://blogs.iu.edu/maurerglobalforum/2024/03/25/data-privacy-in-space-tourism-a-new-frontier-for-an-adequate-legal-framework/
- *The international data governance landscape*. PMC8977111.

**Confiança:** média-alta — fontes acadêmicas e jurídicas múltiplas.

## Argumento (≤ 3 frases)

HIPAA **não se aplica** diretamente a astronautas — a NASA não é Covered Entity no sentido legal, e dados de saúde de tripulantes são geridos sob o Privacy Act of 1974 **alinhados** com princípios HIPAA, sem obrigação legal vinculante. Para tripulações internacionais (ISS já hoje é multinacional; Lunar Gateway e missões marcianas serão ainda mais), há **colisão de jurisdições** — dados coletados em órbita pertencem ao operador? Ao país do astronauta? À empresa privada que lançou? Para turismo espacial comercial, há **vácuo legislativo** explícito: ainda não há framework adequado, e provavelmente cairá sob legislação estadual americana ou contratos privados não-padronizados.

## Pontos críticos identificados

1. **Acordos bilaterais ad hoc** (NASA-Roscosmos, NASA-ESA) cobrem casos específicos sem padronização global.
2. **Pesquisa longitudinal pós-missão** depende de coleta consistente — internacionais frequentemente saem do dataset.
3. **Turismo espacial** opera em zona cinzenta — consentimento de pessoas leigas sob condições experimentais.
4. **IA-assistida (CMO-DA)** introduz **terceiro ator** (Google Cloud) na cadeia de custódia — quem detém as transcrições das interações clínicas?

## Brasil — vantagem regulatória

LGPD (Lei 13.709/2018) tem mecanismos relevantes inexistentes em HIPAA:
- **Direitos do titular** mais explícitos (Art. 18).
- **Relatório de Impacto à Proteção de Dados** obrigatório para tratamentos de alto risco (Art. 38 — referenciado nas memórias do projeto AeroPed).
- **Transferência internacional** com hipóteses explícitas (Art. 33).

Aplicado a saúde espacial, LGPD-derived framework permitiria:
- Astronauta brasileiro mantém direitos sobre seus dados mesmo em ISS/Lunar Gateway.
- Operador estrangeiro precisa formalizar transferência internacional.
- IA-assistida exige RIPD antes de deploy.

## Gancho com a tríade

- **Clínico:** o astronauta-paciente brasileiro hoje não tem framework jurídico próprio para defender soberania sobre seu prontuário em órbita.
- **Gestor médico:** Iúri já trabalhou RIPD pra AeroPed (memória `feedback_supabase_django_gotchas` cita Art. 38 LGPD); arquitetura é portável conceitualmente.
- **Educador:** material formativo sobre soberania de dados de saúde em ambientes internacionais é diferencial pra qualquer profissional brasileiro embarcado em missão.

## Gancho com o ângulo crítico

A pergunta "sob qual governança?" do post tem aqui sua versão jurídica mais aguda. Sem framework explícito, governança é o que o operador (NASA, SpaceX, Axiom) decidir contratualmente. O Brasil pode entrar na conversa **com framework próprio já testado em saúde terrestre** (LGPD + RIPD + AeroPed-style audit).
