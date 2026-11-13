"""Moteur de diagnostic : déduit constats, règles, repères, aides et vérifications.

Déterministe : mêmes entrées, même sortie ; ni réseau ni modèle de langage.
Une condition indécidable produit une vérification, jamais un constat.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel

from collections.abc import Mapping

from audit_ia.audit.models import AuditState, Certainty, Fact
from audit_ia.diagnostic.conditions import Tri, deciding_facts, evaluate, undecided_facts
from audit_ia.kb.freshness import is_stale
from audit_ia.kb.models import PROFILE_FACTS, Condition, KnowledgeBase, RuleStatus

MAX_USE_CASES = 5

Timing = Literal["applicable", "a_venir", "en_projet", "reference"]


class Finding(BaseModel):
    problem_id: str
    fact_ids: list[str]
    certainty: Certainty


class RuleHit(BaseModel):
    rule_id: str
    timing: Timing
    stale: bool


class BenchmarkHit(BaseModel):
    benchmark_id: str
    stale: bool


class AidHit(BaseModel):
    aid_id: str
    stale: bool


class Verification(BaseModel):
    fact_id: str
    blocks: list[str]  # identifiants des problèmes, règles, aides, cas d'usage


class Diagnosis(BaseModel):
    findings: list[Finding]
    rules: list[RuleHit]
    benchmarks: list[BenchmarkHit]
    aids: list[AidHit]
    action_ids: list[str]
    use_case_ids: list[str]
    verifications: list[Verification]
    indicators_without_benchmark: list[str]
    undecided_problem_ids: list[str] = []  # problèmes indécis faute de faits du stade


def _in_bounds(headcount: int, low: int | None, high: int | None) -> bool:
    return (low is None or headcount >= low) and (high is None or headcount <= high)


def _rule_timing(status: RuleStatus, effective_on: date | None, today: date) -> Timing:
    if status in (RuleStatus.PROJET, RuleStatus.PROPOSITION):
        return "en_projet"
    if status in (RuleStatus.RECOMMANDATION, RuleStatus.JURISPRUDENCE):
        return "reference"
    if effective_on is not None and effective_on > today:
        return "a_venir"
    return "applicable"


def profile_facts(state: AuditState) -> dict[str, Fact]:
    """Faits de l'audit, plus les pseudo-faits du profil (toujours constatés)."""
    profile = state.profile
    values = {
        "profile.stage": profile.stage.value,
        "profile.headcount": profile.headcount,
        "profile.sector": profile.sector,
    }
    facts: dict[str, Fact] = dict(state.facts)
    for fact_id, value in values.items():
        facts[fact_id] = Fact(fact_id=fact_id, value=value, certainty=Certainty.CONSTATE)
    return facts


def _outside_stage(fact_id: str, kb: KnowledgeBase, state: AuditState) -> bool:
    fact_def = kb.facts.get(fact_id)
    return (
        fact_def is not None
        and bool(fact_def.stages)
        and state.profile.stage not in fact_def.stages
    )


def diagnose(state: AuditState, kb: KnowledgeBase, today: date) -> Diagnosis:
    facts: Mapping[str, Fact] = profile_facts(state)
    profile = state.profile
    blocked: dict[str, set[str]] = {}
    undecided: set[str] = set()

    def track(entry_id: str, cond: Condition) -> Tri:
        """Évalue ; une condition indécise ne devient vérification que pour les
        faits que le planificateur pose au stade de l'entreprise. Indécise
        seulement faute de faits d'un autre stade, elle n'est pas retenue."""
        result = evaluate(cond, facts)
        if result is Tri.UNKNOWN:
            missing = {
                f for f in undecided_facts(cond, facts) if not _outside_stage(f, kb, state)
            }
            for fact_id in missing:
                blocked.setdefault(fact_id, set()).add(entry_id)
            if missing:
                undecided.add(entry_id)
        return result

    findings = []
    for problem_id in sorted(kb.problems):
        problem = kb.problems[problem_id]
        if track(problem_id, problem.triggers) is not Tri.TRUE:
            continue
        cited = sorted(deciding_facts(problem.triggers, facts) - PROFILE_FACTS)
        estimated = any(facts[f].certainty is Certainty.ESTIME for f in cited)
        findings.append(
            Finding(
                problem_id=problem_id,
                fact_ids=cited,
                certainty=Certainty.ESTIME if estimated else Certainty.CONSTATE,
            )
        )

    rules = []
    for rule_id in sorted(kb.rules):
        rule = kb.rules[rule_id]
        if rule.applies_when is not None and track(rule_id, rule.applies_when) is not Tri.TRUE:
            continue
        rules.append(
            RuleHit(
                rule_id=rule_id,
                timing=_rule_timing(rule.status, rule.effective_on, today),
                stale=is_stale(rule, today),
            )
        )

    compatible = {
        b.id: b
        for b in kb.benchmarks.values()
        if _in_bounds(profile.headcount, b.headcount_min, b.headcount_max)
        and (not b.sectors or profile.sector in b.sectors)
    }
    chosen: dict[str, list] = {}
    for b in compatible.values():
        chosen.setdefault(b.indicator, []).append(b)
    benchmarks = []
    for indicator, candidates in chosen.items():
        specific = [b for b in candidates if b.sectors]
        for b in specific or candidates:
            benchmarks.append(BenchmarkHit(benchmark_id=b.id, stale=is_stale(b, today)))
    benchmarks.sort(key=lambda h: h.benchmark_id)
    indicators_without_benchmark = sorted(
        {b.indicator for b in kb.benchmarks.values()} - set(chosen)
    )

    aids = []
    for aid_id in sorted(kb.aids):
        aid = kb.aids[aid_id]
        if not _in_bounds(profile.headcount, aid.headcount_min, aid.headcount_max):
            continue
        if aid.eligibility is not None and track(aid_id, aid.eligibility) is not Tri.TRUE:
            continue
        aids.append(AidHit(aid_id=aid_id, stale=is_stale(aid, today)))

    action_ids: list[str] = []
    for finding in findings:
        for action_id in kb.problems[finding.problem_id].action_ids:
            if action_id not in action_ids:
                action_ids.append(action_id)

    applicable_cases = [
        uc
        for uc in kb.use_cases.values()
        if uc.applies_when is None or track(uc.id, uc.applies_when) is Tri.TRUE
    ]
    applicable_cases.sort(key=lambda uc: (-uc.priority, uc.id))
    use_case_ids = [uc.id for uc in applicable_cases[:MAX_USE_CASES]]

    verifications = [
        Verification(fact_id=fact_id, blocks=sorted(blocked[fact_id]))
        for fact_id in sorted(blocked)
    ]

    return Diagnosis(
        findings=findings,
        rules=rules,
        benchmarks=benchmarks,
        aids=aids,
        action_ids=action_ids,
        use_case_ids=use_case_ids,
        verifications=verifications,
        indicators_without_benchmark=indicators_without_benchmark,
        undecided_problem_ids=sorted(undecided & set(kb.problems)),
    )
