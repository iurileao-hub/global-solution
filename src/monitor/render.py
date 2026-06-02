"""Primitivas de apresentação do relatório (GS — camada de UI, §8/§12).

Puras e sem domínio: recebem dados, devolvem str/list[str]; nada imprime.
ANSI escrito à mão (stdlib-only). Cor desligada sob não-TTY / NO_COLOR; os
glifos de desenho e matemática caem para ASCII quando o encoding do stdout
não os suporta (evita UnicodeEncodeError → protege "executa sem erros").
"""
import os
import re
import sys

ESC = "\033"
RESET = f"{ESC}[0m"

# nome → código SGR (cores ANSI básicas + bold; portáteis em qualquer terminal)
_COLORS = {
    "red": "31", "green": "32", "yellow": "33", "blue": "34",
    "magenta": "35", "cyan": "36", "gray": "90", "bold": "1",
}

# Conjunto de glifos: Unicode (padrão) e fallback ASCII puro.
_UNICODE = {
    "tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│",
    "bar_f": "█", "bar_e": "░", "dot_ok": "●", "dot_bad": "✕", "check": "✓",
    "and": "∧", "or": "∨", "not": "¬", "arrow": "⇒", "hook": "↳",
    "middot": "·", "times": "×", "ellipsis": "…",
    "ramp": "▁▂▃▄▅▆▇█",
}
_ASCII = {
    "tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|",
    "bar_f": "#", "bar_e": "-", "dot_ok": "o", "dot_bad": "x", "check": "OK",
    "and": "AND", "or": "OR", "not": "NOT", "arrow": "=>", "hook": ">",
    "middot": "-", "times": "x", "ellipsis": "..",
    "ramp": ".:-=+*#%@",
}

# Probe: se o encoding do stdout codifica TODOS estes, usamos Unicode.
_PROBE = "┌█░▁✓●✕∧∨¬⇒↳·×…"


def supports_color() -> bool:
    """True só num TTY interativo que não opte por sair (NO_COLOR / TERM=dumb)."""
    if "NO_COLOR" in os.environ or "GS_NO_COLOR" in os.environ:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    isatty = getattr(sys.stdout, "isatty", None)
    return bool(isatty()) if callable(isatty) else False


def unicode_ok() -> bool:
    """True se o encoding do stdout consegue representar os glifos de desenho."""
    enc = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        _PROBE.encode(enc)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


def glyphs() -> dict:
    return _UNICODE if unicode_ok() else _ASCII


def c(text: str, color: str) -> str:
    """Embrulha em cor ANSI se o terminal suportar; senão devolve cru."""
    if not supports_color():
        return text
    code = _COLORS.get(color)
    return f"{ESC}[{code}m{text}{RESET}" if code else text


_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def visible_len(text: str) -> int:
    return len(strip_ansi(text))


def padto(text: str, width: int) -> str:
    diff = width - visible_len(text)
    return text + " " * diff if diff > 0 else text
