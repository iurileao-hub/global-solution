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
    "ramp": ".:-=+*#@",
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


def glyphs() -> dict[str, str]:
    return _UNICODE if unicode_ok() else _ASCII


def c(text: str, color: str) -> str:
    """Embrulha em cor ANSI se o terminal suportar; senão devolve cru."""
    if not supports_color():
        return text
    code = _COLORS[color]  # KeyError intencional em nome desconhecido
    return f"{ESC}[{code}m{text}{RESET}"


_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def visible_len(text: str) -> int:
    return len(strip_ansi(text))


def padto(text: str, width: int) -> str:
    diff = width - visible_len(text)
    return text + " " * diff if diff > 0 else text


def clip(text: str, width: int) -> str:
    """Trunca para `width` caracteres VISÍVEIS, preservando escapes ANSI."""
    if visible_len(text) <= width:
        return text
    ell = glyphs()["ellipsis"]
    keep = max(0, width - len(ell))
    out, count, i = [], 0, 0
    while i < len(text) and count < keep:
        m = _ANSI_RE.match(text, i)
        if m:
            out.append(m.group())
            i = m.end()
            continue
        out.append(text[i])
        count += 1
        i += 1
    tail = RESET if "\033" in text else ""
    return "".join(out) + ell + tail


def rule(width: int) -> str:
    return c(glyphs()["h"] * width, "gray")


def kv(label: str, value: str, color: str | None = None, label_w: int = 16) -> str:
    lab = c(f"{label:<{label_w}}", "gray")
    val = c(value, color) if color else value
    return f"  {lab}{val}"


def badge(text: str, color: str) -> str:
    return c(f"[ {text} ]", color)


def hbar(val: float, mx: float, width: int, color: str = "green") -> str:
    g = glyphs()
    filled = int((val / mx) * width) if mx > 0 else 0
    filled = max(0, min(width, filled))
    return c(g["bar_f"] * filled, color) + c(g["bar_e"] * (width - filled), "gray")


def sparkline(vals: list[float], width: int) -> str:
    ramp = glyphs()["ramp"]
    if not vals:
        return ""
    series = vals[-width:]
    lo, hi = min(series), max(series)
    span = (hi - lo) or 1.0
    chars = []
    for v in series:
        idx = int((v - lo) / span * (len(ramp) - 1))
        chars.append(ramp[max(0, min(len(ramp) - 1, idx))])
    return c("".join(chars), "cyan")


def box(title: str, lines: list[str], tag: str | None = None, width: int = 64) -> list[str]:
    """Moldura: título à esquerda, `tag` (critério) à direita no topo.

    Largura total = `width` em TODAS as linhas (corpo é clipado + padded).
    Borda e título em cinza; corpo passa com suas próprias cores.
    """
    g = glyphs()
    inner = width - 2  # espaço entre as duas bordas verticais
    left = f"{g['h']} {title} "
    right = f" {tag} {g['h']}" if tag else ""
    fill = max(0, inner - len(left) - len(right))
    top = g["tl"] + left + g["h"] * fill + right + g["tr"]
    bottom = g["bl"] + g["h"] * inner + g["br"]
    out = [c(top, "gray")]
    for ln in lines:
        body = padto(clip(ln, inner), inner)
        out.append(c(g["v"], "gray") + body + c(g["v"], "gray"))
    out.append(c(bottom, "gray"))
    return out
