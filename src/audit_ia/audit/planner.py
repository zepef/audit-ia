"""Planificateur d'entretien : choisit déterministement le prochain fait à recueillir."""

from pydantic import BaseModel

from audit_ia.audit.models import AuditState, Dimension
from audit_ia.kb.models import KnowledgeBase

MIN_FACTS_PER_DIMENSION = 3


class Objective(BaseModel):
    fact_id: str
    dimension: Dimension


def coverage(state: AuditState, kb: KnowledgeBase) -> dict[Dimension, int]:
    """Nombre de faits recueillis par dimension, réponses « inconnu » comprises."""
    counts = {dimension: 0 for dimension in Dimension}
    for fact_id in state.facts:
        fact_def = kb.facts.get(fact_id)
        if fact_def is not None:
            counts[fact_def.dimension] += 1
    return counts


def next_objective(
    state: AuditState, kb: KnowledgeBase, *, asked: frozenset[str] = frozenset()
) -> Objective | None:
    """Prochain fait à recueillir, ou None si l'entretien est complet.

    Candidats : faits non recueillis, non déjà posés, valables pour le stade.
    Choix : dimension la moins couverte (ordre de l'énumération en cas
    d'égalité), puis priorité décroissante, puis identifiant.
    """
    stage = state.profile.stage
    candidates = [
        f
        for f in kb.facts.values()
        if f.id not in state.facts
        and f.id not in asked
        and (not f.stages or stage in f.stages)
    ]
    if not candidates:
        return None
    counts = coverage(state, kb)
    order = {dimension: i for i, dimension in enumerate(Dimension)}
    best = min(
        candidates,
        key=lambda f: (counts[f.dimension], order[f.dimension], -f.priority, f.id),
    )
    if counts[best.dimension] >= MIN_FACTS_PER_DIMENSION:
        return None
    return Objective(fact_id=best.id, dimension=best.dimension)
