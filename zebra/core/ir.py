"""Canonical Constraint IR — the single contract between the neural and symbolic
layers. Every clue, whether parsed from text, generated, or fed to the solver,
is a `Constraint`. Its linearized string form (`to_str` / `parse_constraint`) is
exactly what the M2 parser emits and the M4 renderer consumes.

Five clue kinds (roadmap):
    pos       attribute is at a fixed house     b: int in [1..N]
    eq        two attributes share a house      b: Attr
    neq       two attributes differ in house    b: Attr
    imm_left  a is immediately left of b        b: Attr   (pos_a == pos_b - 1)
    next      a is adjacent to b                b: Attr   (|pos_a - pos_b| == 1)

String form:
    pos(color:red, 1)
    imm_left(nation:swede, color:red)
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal, Union, get_args

ClueKind = Literal["pos", "eq", "neq", "imm_left", "next"]
Attr = tuple[str, str]  # (category, value), e.g. ("nation", "swede")

_KINDS: tuple[str, ...] = get_args(ClueKind)
_RELATIONAL: frozenset[str] = frozenset({"eq", "neq", "imm_left", "next"})  # b is an Attr


@dataclass(frozen=True)
class Constraint:
    """An immutable, hashable formal clue. `b` is an int for `pos`, else an Attr."""

    type: ClueKind
    a: Attr
    b: Union[Attr, int]

    # -- serialization ---------------------------------------------------------
    def to_str(self) -> str:
        """Linearize to the canonical string form."""
        if self.type == "pos":
            return f"pos({_attr_to_str(self.a)}, {int(self.b)})"
        return f"{self.type}({_attr_to_str(self.a)}, {_attr_to_str(self.b)})"  # type: ignore[arg-type]

    # -- tuple interop (backward-compat with M0 internals) ---------------------
    def to_tuple(self) -> tuple:
        return (self.type, self.a, self.b)

    @staticmethod
    def from_tuple(t: tuple) -> "Constraint":
        kind, a, b = t[0], t[1], t[2]
        return Constraint(kind, tuple(a), b if isinstance(b, int) else tuple(b))  # type: ignore[arg-type]


def _attr_to_str(a: Attr) -> str:
    return f"{a[0]}:{a[1]}"


def _parse_attr(s: str) -> Attr:
    cat, _, val = s.partition(":")
    if not cat or not val or ":" in val:
        raise ValueError(f"malformed attribute {s!r} (expected 'category:value')")
    return (cat.strip(), val.strip())


_RE = re.compile(r"^\s*([A-Za-z_]+)\s*\((.+)\)\s*$")


def parse_constraint(s: str) -> Constraint:
    """Inverse of `Constraint.to_str`. Raises ValueError on malformed input.

    Used both directly and as the round-trip guard for generation (re-parse a
    rendered sentence's target string and compare to the original constraint).
    """
    m = _RE.match(s)
    if not m:
        raise ValueError(f"not a constraint string: {s!r}")
    kind, inner = m.group(1), m.group(2)
    if kind not in _KINDS:
        raise ValueError(f"unknown clue kind {kind!r}; expected one of {_KINDS}")
    parts = [p.strip() for p in inner.split(",")]
    if len(parts) != 2:
        raise ValueError(f"expected 2 arguments in {s!r}, got {len(parts)}")
    a = _parse_attr(parts[0])
    if kind == "pos":
        try:
            b: Union[Attr, int] = int(parts[1])
        except ValueError as e:
            raise ValueError(f"pos position must be an int, got {parts[1]!r}") from e
    else:
        b = _parse_attr(parts[1])
    return Constraint(kind, a, b)  # type: ignore[arg-type]


def is_valid(c: Constraint, categories: dict[str, list[str]]) -> bool:
    """Structural validity: known kind, attributes exist in `categories`, and a
    `pos` position lies in [1..N]. Does not judge logical satisfiability."""
    from .. import config  # local import avoids a cycle at module import time

    if c.type not in _KINDS:
        return False
    if not _attr_in(c.a, categories):
        return False
    if c.type == "pos":
        n = config.n_houses(categories)
        return isinstance(c.b, int) and 1 <= c.b <= n
    return isinstance(c.b, tuple) and _attr_in(c.b, categories)


def _attr_in(a: Attr, categories: dict[str, list[str]]) -> bool:
    return (
        isinstance(a, tuple)
        and len(a) == 2
        and a[0] in categories
        and a[1] in categories[a[0]]
    )
