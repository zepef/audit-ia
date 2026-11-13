"""Modèles de la base de connaissances : sources, règles, repères, problèmes."""

from datetime import date
from enum import StrEnum
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from audit_ia.audit.models import Dimension, Stage


class Confidence(StrEnum):
    V = "V"
    V2 = "V2"
    A = "A"
    B = "B"
    C = "C"


class RuleStatus(StrEnum):
    APPLICABLE = "applicable"
    ADOPTE_NON_APPLICABLE = "adopte_non_applicable"
    PROJET = "projet"
    PROPOSITION = "proposition"
    RECOMMANDATION = "recommandation"
    JURISPRUDENCE = "jurisprudence"


class Horizon(StrEnum):
    J30 = "j30"
    J90 = "j90"
    M12 = "m12"


class _Strict(BaseModel):
    """Base commune : une clé inconnue (faute de frappe) est une erreur."""

    model_config = ConfigDict(extra="forbid")


class Source(_Strict):
    id: str
    title: str
    publisher: str
    url: str = Field(pattern=r"^https?://")
    published_on: date | None = None


class Sector(_Strict):
    id: str
    label: str


class Provenance(_Strict):
    source_id: str
    verified_on: date | None
    confidence: Confidence
    human_reviewed: bool = False


# Condition : arbre récursif de tests sur les faits.
class Test(_Strict):
    __test__: ClassVar[bool] = False  # ne pas collecter par pytest

    fact: str
    op: Literal["eq", "ne", "lt", "lte", "gt", "gte", "in"]
    value: Any


class All(_Strict):
    all: list["Condition"]


class AnyOf(_Strict):
    any: list["Condition"]


class Not(_Strict):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    not_: "Condition" = Field(alias="not")


Condition = Test | All | AnyOf | Not

All.model_rebuild()
AnyOf.model_rebuild()
Not.model_rebuild()


class FactDef(_Strict):
    id: str
    dimension: Dimension
    kind: Literal["bool", "int", "float", "enum", "text"]
    choices: list[str] | None = None
    prompt_hint: str
    stages: list[Stage] = []  # vide = tous les stades
    priority: int = 0


class Rule(_Strict):
    id: str
    label: str  # nom court affiché au lecteur (vérifications)
    statement: str
    status: RuleStatus
    effective_on: date | None = None
    bounds: str | None = None
    applies_when: Condition | None = None
    provenance: Provenance


class Benchmark(_Strict):
    id: str
    indicator: str
    value: str
    headcount_min: int | None = None
    headcount_max: int | None = None
    sectors: list[str] = []  # vide = tous secteurs
    # False : la source ne publie pas la taille des entreprises interrogées
    # (headcount_min/max nuls ne veulent alors pas dire « toutes tailles »).
    scope_published: bool = True
    stages: list[Stage] = []  # vide = tous les stades
    population: str
    fieldwork: str
    expires_on: date
    provenance: Provenance


class Problem(_Strict):
    id: str = Field(pattern=r"^(HUM|DAT|SI|GEN|CYB|COU|ENV|FON)-[A-Z0-9]+$")
    symptom: str
    dimension: Dimension
    triggers: Condition
    evidence_benchmark_ids: list[str] = []
    action_ids: list[str] = []


class UseCase(_Strict):
    id: str
    function: str
    title: str
    prerequisites: list[str]
    obstacles: list[str]
    risks: list[str]
    first_step: str
    applies_when: Condition | None = None
    priority: int = 0


class Action(_Strict):
    id: str
    title: str
    horizon: Horizon
    effort: Literal["faible", "moyen", "fort"]
    prerequisites: list[str] = []
    success_check: str


class Aid(_Strict):
    id: str
    label: str  # nom court affiché au lecteur (vérifications)
    name: str
    eligibility: Condition | None = None
    headcount_min: int | None = None
    headcount_max: int | None = None
    amount: str
    provenance: Provenance


class KnowledgeBase(_Strict):
    version: str
    sources: dict[str, Source]
    sectors: dict[str, Sector]
    facts: dict[str, FactDef]
    rules: dict[str, Rule]
    benchmarks: dict[str, Benchmark]
    problems: dict[str, Problem]
    use_cases: dict[str, UseCase]
    actions: dict[str, Action]
    aids: dict[str, Aid]
    forbidden_terms: list[str]


# Pseudo-faits toujours constatés, tirés du profil : une condition peut les lire
# sans définition dans facts.yaml ; ils ne sont jamais une vérification ni la
# preuve d'un constat.
PROFILE_FACTS = frozenset({"profile.stage", "profile.headcount", "profile.sector"})


def referenced_facts(cond: Condition) -> set[str]:
    """Identifiants de faits cités par une condition (récursivement)."""
    match cond:
        case Test():
            return {cond.fact}
        case All():
            children = cond.all
        case AnyOf():
            children = cond.any
        case Not():
            return referenced_facts(cond.not_)
        case _:
            raise TypeError(f"condition inconnue : {cond!r}")
    return set().union(*(referenced_facts(c) for c in children)) if children else set()
