# src/monitor/structures.py
"""Estruturas lineares genéricas, escritas à mão (GS §8.2).

Queue (FIFO) e Stack (LIFO) sobre uma list, implementadas explicitamente
em vez de collections.deque para que a estrutura fique visível e
defensável — a rubrica (§14) pontua a estrutura aplicada e justificada.
Espelha aurora_siger/landing/structures.py da Fase 2.
"""
from typing import Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """Fila First-In-First-Out."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if self.is_empty():
            raise IndexError("dequeue de fila vazia")
        return self._items.pop(0)

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek de fila vazia")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class Stack(Generic[T]):
    """Pilha Last-In-First-Out."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if self.is_empty():
            raise IndexError("pop de pilha vazia")
        return self._items.pop()

    def peek(self) -> T:
        if self.is_empty():
            raise IndexError("peek de pilha vazia")
        return self._items[-1]

    def top_n(self, n: int) -> list[T]:
        """Os n itens mais recentes, do mais novo ao mais antigo (não-destrutivo)."""
        return list(reversed(self._items[-n:]))

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)
