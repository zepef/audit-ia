"""Contrôle d'un état d'audit contre la base de connaissances.

Un fait inconnu de la base, une valeur d'un type autre que celui du fait ou un
secteur absent de la base serait sinon ignoré sans trace par le moteur.
"""

from audit_ia.audit.models import AuditState, Certainty
from audit_ia.kb.models import FactDef, KnowledgeBase


class FactValidationError(ValueError):
    def __init__(self, fact_id: str | None, message: str):
        self.fact_id = fact_id
        self.message = message
        super().__init__(f"{fact_id} : {message}" if fact_id else message)


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _matches(value: object, fact_def: FactDef) -> bool:
    match fact_def.kind:
        case "bool":
            return isinstance(value, bool)
        case "int":
            return _is_int(value)
        case "float":
            return _is_int(value) or isinstance(value, float)
        case "enum":
            return isinstance(value, str) and value in (fact_def.choices or [])
        case "text":
            return isinstance(value, str)
    return False


_EXPECTED = {
    "bool": "un booléen (true ou false)",
    "int": "un nombre entier",
    "float": "un nombre",
    "text": "un texte",
}


def validate_state(state: AuditState, kb: KnowledgeBase) -> None:
    """Lève FactValidationError à la première incohérence relevée."""
    sector = state.profile.sector
    if sector not in kb.sectors:
        raise FactValidationError(
            None, f"secteur inconnu de la base de connaissances : « {sector} »"
        )
    for fact_id, fact in state.facts.items():
        fact_def = kb.facts.get(fact_id)
        if fact_def is None:
            raise FactValidationError(fact_id, "fait inconnu de la base de connaissances")
        if fact.certainty is Certainty.INCONNU:
            continue
        if not _matches(fact.value, fact_def):
            expected = (
                f"une valeur parmi {', '.join(fact_def.choices or [])}"
                if fact_def.kind == "enum"
                else _EXPECTED[fact_def.kind]
            )
            raise FactValidationError(
                fact_id, f"valeur {fact.value!r} invalide, attendu {expected}"
            )
