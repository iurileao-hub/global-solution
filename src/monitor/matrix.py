# src/monitor/matrix.py
"""Matriz [hora × variável] — GS §8.2 (matriz / lista de listas).

Constrói uma matriz 2-D a partir das leituras horárias de telemetria:
uma linha por hora, uma coluna por variável selecionada. Lista-de-listas
pura, sem numpy.
"""


class ReadingsMatrix:
    """Matriz de leituras: rows[hora][variável]."""

    def __init__(self, variables: list[str], rows: list[list[float]]) -> None:
        self.variables = variables
        self.rows = rows

    @classmethod
    def from_telemetry(cls, telemetry: list[dict], variables: list[str]) -> "ReadingsMatrix":
        rows = [[float(rec[v]) for v in variables] for rec in telemetry]
        return cls(variables, rows)

    def get(self, hour_index: int, variable: str) -> float:
        return self.rows[hour_index][self.variables.index(variable)]

    def column(self, variable: str) -> list[float]:
        j = self.variables.index(variable)
        return [row[j] for row in self.rows]

    def n_hours(self) -> int:
        return len(self.rows)

    def n_variables(self) -> int:
        return len(self.variables)
