import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class Constraint:
    type: str
    a: tuple[str, str]
    b: tuple[str, str] | int