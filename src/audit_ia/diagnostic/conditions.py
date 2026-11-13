"""Évaluation des conditions de la base de connaissances en logique à trois valeurs."""

from collections.abc import Mapping
from enum import Enum

from audit_ia.audit.models import Certainty, Fact
from audit_ia.kb.models import All, AnyOf, Condition, Not, Test


class Tri(Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


def _known_value(test: Test, facts: Mapping[str, Fact]) -> tuple[bool, object]:
    fact = facts.get(test.fact)
    if fact is None or fact.certainty == Certainty.INCONNU:
        return False, None
    return True, fact.value


def _is_number(x: object) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _compare(op: str, left: object, right: object) -> Tri:
    if op == "eq":
        return Tri.TRUE if left == right else Tri.FALSE
    if op == "ne":
        return Tri.TRUE if left != right else Tri.FALSE
    if op == "in":
        if not isinstance(right, (list, tuple, set, frozenset)):
            return Tri.UNKNOWN
        return Tri.TRUE if left in right else Tri.FALSE
    comparable = (_is_number(left) and _is_number(right)) or (
        isinstance(left, str) and isinstance(right, str)
    )
    if not comparable:
        return Tri.UNKNOWN
    result = {
        "lt": left < right,
        "lte": left <= right,
        "gt": left > right,
        "gte": left >= right,
    }[op]
    return Tri.TRUE if result else Tri.FALSE


def _children(cond: All | AnyOf) -> list[Condition]:
    return cond.all if isinstance(cond, All) else cond.any


def evaluate(cond: Condition, facts: Mapping[str, Fact]) -> Tri:
    match cond:
        case Test():
            known, value = _known_value(cond, facts)
            return _compare(cond.op, value, cond.value) if known else Tri.UNKNOWN
        case All():
            results = [evaluate(c, facts) for c in cond.all]
            if Tri.FALSE in results:
                return Tri.FALSE
            return Tri.UNKNOWN if Tri.UNKNOWN in results else Tri.TRUE
        case AnyOf():
            results = [evaluate(c, facts) for c in cond.any]
            if Tri.TRUE in results:
                return Tri.TRUE
            return Tri.UNKNOWN if Tri.UNKNOWN in results else Tri.FALSE
        case Not():
            inner = evaluate(cond.not_, facts)
            if inner is Tri.UNKNOWN:
                return Tri.UNKNOWN
            return Tri.FALSE if inner is Tri.TRUE else Tri.TRUE
        case _:
            raise TypeError(f"condition inconnue : {cond!r}")


def undecided_facts(cond: Condition, facts: Mapping[str, Fact]) -> set[str]:
    """Faits absents ou inconnus qui empêchent de trancher ; vide si le résultat n'est pas UNKNOWN."""
    if evaluate(cond, facts) is not Tri.UNKNOWN:
        return set()
    match cond:
        case Test():
            known, _ = _known_value(cond, facts)
            return set() if known else {cond.fact}
        case All() | AnyOf():
            return set().union(*(undecided_facts(c, facts) for c in _children(cond)))
        case Not():
            return undecided_facts(cond.not_, facts)
        case _:
            raise TypeError(f"condition inconnue : {cond!r}")
