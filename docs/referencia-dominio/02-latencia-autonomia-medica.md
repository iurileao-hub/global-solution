# Latência de comunicação e o imperativo da autonomia médica

**Referências:**
- Hamilton, D. R. et al. (2007). *Autonomous Medical Care for Exploration Class Space Missions*. NASA Technical Reports Server. https://ntrs.nasa.gov/api/citations/20070032039/downloads/20070032039.pdf
- Russell, B. K. et al. (2023). *The value of a spaceflight clinical decision support system for earth-independent medical operations*. PMC10284846. https://pmc.ncbi.nlm.nih.gov/articles/PMC10284846/
- Modern Retina / Ophthalmology Times — entrevista com Steven Laurie, PhD (NASA). *Extreme telemedicine during long-duration spaceflight*.

**Confiança:** alta — fontes técnicas primárias da NASA.

## Argumento (≤ 3 frases)

A latência de comunicação na ISS (~250 milhas) é de 1-2 segundos, permitindo telemedicina síncrona em tempo real; para Marte, a latência salta para 18-20 minutos one-way em sinal de áudio, tornando qualquer "tirar dúvida com a Terra" impraticável em emergências. O paradigma migra de **telemedicina assistida → autonomia médica suportada por CDSS local**. Russell et al. (2023) estimam que um CDSS bem desenhado pode reduzir mortalidade em missões de longa duração em até 34% ao elevar o "escopo de prática cognitivo" do tripulante não-médico ao nível 3+ (enfermeira certificada).

## Gaps técnicos identificados (Russell 2023)

1. **Dados limitados de LDEM** (Long-Duration Exploration Missions) — não há base empírica robusta.
2. **Restrição computacional, massa e energia** a bordo.
3. **Adaptabilidade a déficits cognitivos da tripulação** (CO₂, isolamento, fadiga).
4. **Eventos clínicos nunca observados nem na Terra nem no espaço** (multi-órgão, micro-gravidade aguda).

## Gaps éticos (implícitos)

- Qualificação de tripulantes não-médicos para decisões críticas.
- Autonomia × responsabilidade em cenários de vida-ou-morte.
- Consentimento informado em emergência (não há tempo de contatar familiar/comitê).

## Gancho com a tríade

- **Clínico:** a interface humano-IA em ambiente latente é o **núcleo do problema**: como tomar decisão crítica em até 20 min sem feedback externo, sem virar refém da sugestão?
- **Gestor médico:** governança de "escopo de prática cognitiva ampliado por IA" é o equivalente clínico do que Aurora SIGER faz com decisões Go/No-Go de pouso — auditabilidade necessária por design.
- **Educador:** o tripulante CMO precisa de treinamento continuado in-flight, porque competência decai em isolamento. Currículo distribuído + IA tutora.

## Gancho com o ângulo crítico

Esse é o caso-limite do *"quem decide quando a máquina decide"*: numa emergência marciana, com 20 min de delay, **a máquina decide quase tudo no minuto que importa**. A governança não pode ser síncrona — tem que ser embarcada na arquitetura do sistema.
