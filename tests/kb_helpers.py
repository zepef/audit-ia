"""Aides de test partagées pour la base de connaissances."""

import shutil
from datetime import date
from pathlib import Path

import yaml

from audit_ia.kb.loader import load_kb
from audit_ia.kb.models import Benchmark, Confidence, Provenance, Rule, RuleStatus

KB_MIN = Path(__file__).resolve().parent / "fixtures" / "kb_min"

_BASE = load_kb(KB_MIN)
# Base de test où seul le repère « construction » subsiste (aucun repère générique).
KB_SECTOR_ONLY = _BASE.model_copy(
    update={"benchmarks": {"repere-construction": _BASE.benchmarks["repere-construction"]}}
)


def _edit(root: Path, name: str, fn) -> None:
    path = root / name
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    fn(data)
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


def _by_id(data: list, entry_id: str) -> dict:
    return next(e for e in data if e["id"] == entry_id)


def _duplicate_rule_id(data):
    data.append(dict(_by_id(data, "regle-a")))


def _bad_problem_id(data):
    _by_id(data, "HUM-S1")["id"] = "hum_s1"


MUTATIONS = {
    "duplicate_rule_id": ("rules.yaml", _duplicate_rule_id),
    "condition_unknown_fact": (
        "problems.yaml",
        lambda d: _by_id(d, "HUM-S1")["triggers"].update(fact="fait_inconnu"),
    ),
    "unknown_source": (
        "benchmarks.yaml",
        lambda d: _by_id(d, "repere-a")["provenance"].update(source_id="src-inconnue"),
    ),
    "problem_unknown_action": (
        "problems.yaml",
        lambda d: _by_id(d, "HUM-S1").update(action_ids=["action-inconnue"]),
    ),
    "problem_unknown_benchmark": (
        "problems.yaml",
        lambda d: _by_id(d, "HUM-S1").update(evidence_benchmark_ids=["repere-inconnu"]),
    ),
    "bad_problem_id": ("problems.yaml", _bad_problem_id),
    "verified_without_date": (
        "rules.yaml",
        lambda d: _by_id(d, "regle-a")["provenance"].update(verified_on=None),
    ),
    "evidence_is_unverified": (
        "benchmarks.yaml",
        lambda d: _by_id(d, "repere-a")["provenance"].update(confidence="B"),
    ),
}


def mutated_copy(src: Path, tmp_path: Path, mutation: str) -> Path:
    """Copie la base dans tmp_path et applique la mutation nommée au YAML."""
    root = tmp_path / "kb"
    shutil.copytree(src, root)
    name, fn = MUTATIONS[mutation]
    _edit(root, name, fn)
    return root


def rule(*, verified_on: date | None = date(2026, 11, 13), **overrides) -> Rule:
    fields = dict(
        id="regle-t",
        statement="Règle de test.",
        status=RuleStatus.APPLICABLE,
        effective_on=date(2025, 2, 2),
        bounds=None,
        applies_when=None,
        provenance=Provenance(
            source_id="src-a", verified_on=verified_on, confidence=Confidence.V
        ),
    )
    fields.update(overrides)
    return Rule(**fields)


def benchmark(
    *,
    expires_on: date = date(2027, 6, 30),
    verified_on: date | None = date(2026, 11, 13),
    **overrides,
) -> Benchmark:
    fields = dict(
        id="repere-t",
        indicator="adoption",
        value="40 %",
        headcount_min=None,
        headcount_max=None,
        sectors=[],
        population="Entreprises de 1 à 249 salariés",
        fieldwork="T1 2026",
        expires_on=expires_on,
        provenance=Provenance(
            source_id="src-a", verified_on=verified_on, confidence=Confidence.V
        ),
    )
    fields.update(overrides)
    return Benchmark(**fields)


def state(headcount: int = 45, sector: str = "commerce", stage: str = "usage_individuel", **facts):
    """Construit un AuditState ; chaque fait est une valeur (constatée) ou un couple (certitude, valeur)."""
    from audit_ia.audit.models import AuditState, CompanyProfile, Fact

    built = {}
    for fact_id, raw in facts.items():
        certainty, value = raw if isinstance(raw, tuple) else ("constate", raw)
        built[fact_id] = Fact(fact_id=fact_id, value=value, certainty=certainty)
    profile = CompanyProfile(
        headcount=headcount, sector=sector, stage=stage, respondent_role="dirigeant"
    )
    return AuditState(profile=profile, facts=built)
