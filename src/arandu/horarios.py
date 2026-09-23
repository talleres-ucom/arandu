
from collections.abc import Iterable

from .modelo import Franja


def se_solapan(a: Franja, b: Franja) -> bool:
    if a.dia != b.dia:
        return False
    return a.inicio < b.fin and b.inicio < a.fin


def chocan(unas: Iterable[Franja], otras: Iterable[Franja]) -> bool:
    """True si alguna franja de `unas` se solapa con alguna de `otras`."""
    otras = tuple(otras)
    return any(se_solapan(a, b) for a in unas for b in otras)
