# src/monitor/rubric.py
"""Critérios TÉCNICOS da rubrica (§14) que o programa demonstra em runtime.

Fonte ÚNICA: alimenta tanto as tags de cabeçalho de seção quanto o painel
"COBERTURA DE REQUISITOS". Vídeo e Documentação/organização NÃO entram na
saída da CLI (não são requisitos técnicos do sistema em execução).
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Criterio:
    id: str       # chave estável
    nome: str     # rótulo do painel de cobertura
    pontos: float # peso na rubrica §14 (referência)
    tag: str      # rótulo curto no canto do cabeçalho de seção


CRITERIOS: list[Criterio] = [
    Criterio("interpretacao", "Interpretação de dados", 1.0, "interpretação de dados"),
    Criterio("estruturas",    "Estruturas de dados",    1.5, "estruturas de dados"),
    Criterio("logica",        "Lógica e regras",        1.5, "lógica e regras"),
    Criterio("previsao",      "Análise e previsão",     1.5, "análise e previsão"),
    Criterio("codigo",        "Código Python",          2.0, "código"),
]


def por_id(cid: str) -> Criterio:
    for cr in CRITERIOS:
        if cr.id == cid:
            return cr
    raise KeyError(cid)
