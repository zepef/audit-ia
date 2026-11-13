"""Règle de péremption : une entrée périmée est signalée, jamais masquée."""

from datetime import date, timedelta

from audit_ia.kb.models import Aid, Benchmark, Rule

RULE_MAX_AGE_DAYS = 180


def _verification_too_old(verified_on: date | None, today: date) -> bool:
    if verified_on is None:
        return True
    return today - verified_on > timedelta(days=RULE_MAX_AGE_DAYS)


def is_stale(entry: Rule | Benchmark | Aid, today: date) -> bool:
    """Un repère est périmé après `expires_on` ou si sa vérification date de
    plus de RULE_MAX_AGE_DAYS ; une règle ou une aide, sur la seule ancienneté
    de `verified_on` (absente = périmée)."""
    if isinstance(entry, Benchmark) and today > entry.expires_on:
        return True
    return _verification_too_old(entry.provenance.verified_on, today)
