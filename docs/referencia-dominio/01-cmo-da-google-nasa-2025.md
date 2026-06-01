# CMO-DA — Crew Medical Officer Digital Assistant (NASA + Google Cloud)

**Referências:**
- TechCrunch (08/08/2025). *NASA and Google are building an AI medical assistant to keep Mars-bound astronauts healthy*. https://techcrunch.com/2025/08/08/nasa-and-google-are-building-an-ai-medical-assistant-to-keep-mars-bound-astronauts-healthy/
- Google Cloud Blog. *How Google and NASA are Testing AI for Medical Care in Space*. https://cloud.google.com/blog/topics/public-sector/how-google-and-nasa-are-testing-ai-for-medical-care-in-space
- Space.com. *NASA and Google test AI medical assistant for astronaut missions to the moon and Mars*. https://www.space.com/technology/nasa-and-google-test-ai-medical-assistant-for-astronaut-missions-to-the-moon-and-mars

**Confiança:** alta para fatos básicos (cobertura jornalística múltipla); média para detalhes técnicos (papers de validação não publicados até esta data).

## Argumento (≤ 3 frases)

CMO-DA é um assistente médico multimodal (voz, texto, imagem) construído sobre Google Cloud Vertex AI, treinado em open data cobrindo 250 condições médicas comuns no espaço, com accuracy diagnóstica de até 88% em cenários simulados. O projeto representa o **estado da arte de IA médica espacial em agosto de 2025** e ataca diretamente o problema da latência Terra-Marte (18-20 min one-way), que torna telemedicina síncrona inviável. Roadmap declarado: ingestão de dados de devices médicos a bordo, detecção de condições microgravidade-específicas e capacidade de operar equipamentos (ultrassom, administração de medicamentos).

## Implicação pra Global Solution

CMO-DA define o **competidor de referência**. Qualquer produto que a tríade proponha precisa pelo menos saber em quê NÃO compete. Onde ele não chega:
- **Inspecionabilidade pelo paciente** (o astronauta-paciente vê o raciocínio?).
- **Mecanismo de contestação** (o CMO humano pode discordar de forma auditável?).
- **Governança de dados** (Google Cloud detém amostras de saúde de astronautas de várias nacionalidades?).
- **Pediatria e saúde da família** (250 condições "comuns no espaço" foram derivadas de população de astronautas adultos selecionados).

## Gancho com a tríade

- **Clínico:** o produto-rival da IA precisa preservar agência clínica — não é um problema de "performar melhor que 88%", é de "como o CMO usa criticamente os 88%".
- **Gestor médico:** a aquisição de um CMO-DA-equivalente pra Brasil exigiria framework de governança de dados que ainda não existe.
- **Educador:** treinar o profissional pra "modo ativo" no uso do copiloto (cf. Throuvala 2023) é a interface entre IA-espacial e cognição protegida.

## Gancho com o ângulo crítico

A pergunta do post — "para quem funciona, com que transparência e sob qual governança?" — ataca CMO-DA em todas as frentes: para Mars-bound astronauts da NASA (escopo restrito), com transparência limitada (Vertex AI é caixa-preta operada por empresa privada), sob governança bilateral NASA+Google que não cobre cenário internacional ou colonial.
