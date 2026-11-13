"""Chargement de la base de connaissances YAML, avec contrôles croisés."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ValidationError

from audit_ia.kb.models import (
    PROFILE_FACTS,
    Action,
    Aid,
    Benchmark,
    Confidence,
    FactDef,
    KnowledgeBase,
    Problem,
    Rule,
    Sector,
    Source,
    UseCase,
    referenced_facts,
)

VERIFIED_CONFIDENCES = {Confidence.V, Confidence.V2}


class KBError(Exception):
    def __init__(self, file: str, entry_id: str | None, message: str):
        self.file = file
        self.entry_id = entry_id
        self.message = message
        where = f"{file}" + (f" [{entry_id}]" if entry_id else "")
        super().__init__(f"{where} : {message}")


def validation_summary(exc: ValidationError) -> str:
    """Erreurs de validation pydantic sur une seule ligne : « emplacement : message »."""
    return " ; ".join(
        f"{'.'.join(str(p) for p in err['loc']) or 'document'} : {err['msg']}"
        for err in exc.errors()
    )


def _read_text(root: Path, name: str) -> str:
    try:
        return (root / name).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise KBError(name, None, "fichier manquant") from None
    except UnicodeDecodeError:
        raise KBError(name, None, "encodage invalide, UTF-8 attendu") from None
    except OSError as exc:
        raise KBError(name, None, f"lecture impossible ({exc.strerror})") from None


def _read_yaml(root: Path, name: str) -> Any:
    text = _read_text(root, name)
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        detail = " ".join(str(exc).split())
        raise KBError(name, None, f"YAML invalide : {detail}") from None


def _load_entries(root: Path, name: str, model: type[BaseModel]) -> dict[str, Any]:
    raw = _read_yaml(root, name)
    if not isinstance(raw, list):
        raise KBError(name, None, "le fichier doit contenir une liste d'entrées")
    entries: dict[str, Any] = {}
    for item in raw:
        entry_id = item.get("id") if isinstance(item, dict) else None
        try:
            entry = model.model_validate(item)
        except ValidationError as exc:
            raise KBError(name, entry_id, validation_summary(exc)) from None
        if entry.id in entries:
            raise KBError(name, entry.id, "identifiant en double")
        entries[entry.id] = entry
    return entries


def load_kb(
    root: Path, *, verified_only: bool = False, require_review: bool = False
) -> KnowledgeBase:
    root = Path(root)
    if not root.exists():
        raise KBError(str(root), None, "base de connaissances introuvable")
    if not root.is_dir():
        raise KBError(str(root), None, "un répertoire de base de connaissances est attendu")
    version = _read_text(root, "VERSION").strip()

    neutrality = _read_yaml(root, "neutrality.yaml")
    if not isinstance(neutrality, dict) or not isinstance(
        neutrality.get("forbidden_terms"), list
    ):
        raise KBError("neutrality.yaml", None, "clé forbidden_terms (liste) attendue")

    files = {
        "sources": ("sources.yaml", Source),
        "sectors": ("sectors.yaml", Sector),
        "facts": ("facts.yaml", FactDef),
        "rules": ("rules.yaml", Rule),
        "benchmarks": ("benchmarks.yaml", Benchmark),
        "problems": ("problems.yaml", Problem),
        "use_cases": ("use_cases.yaml", UseCase),
        "actions": ("actions.yaml", Action),
        "aids": ("aids.yaml", Aid),
    }
    tables = {key: _load_entries(root, *spec) for key, spec in files.items()}

    _cross_check(tables, files)

    if require_review:
        for key in ("rules", "benchmarks", "aids"):
            for entry in tables[key].values():
                if not entry.provenance.human_reviewed:
                    raise KBError(
                        files[key][0], entry.id, "entrée non relue par un humain"
                    )

    if verified_only:
        for key in ("rules", "benchmarks", "aids"):
            tables[key] = {
                i: e
                for i, e in tables[key].items()
                if e.provenance.confidence in VERIFIED_CONFIDENCES
            }
        _check_problem_dependencies(tables, files, after_filter=True)

    return KnowledgeBase(
        version=version, forbidden_terms=list(neutrality["forbidden_terms"]), **tables
    )


def _cross_check(tables: dict[str, dict[str, Any]], files: dict) -> None:
    fact_ids = set(tables["facts"])
    source_ids = set(tables["sources"])

    conditions = (
        [("rules", r.id, r.applies_when) for r in tables["rules"].values()]
        + [("problems", p.id, p.triggers) for p in tables["problems"].values()]
        + [("use_cases", u.id, u.applies_when) for u in tables["use_cases"].values()]
        + [("aids", a.id, a.eligibility) for a in tables["aids"].values()]
    )
    for key, entry_id, cond in conditions:
        if cond is None:
            continue
        unknown = referenced_facts(cond) - fact_ids - PROFILE_FACTS
        if unknown:
            raise KBError(
                files[key][0], entry_id, f"fait inconnu : {', '.join(sorted(unknown))}"
            )

    for key in ("rules", "benchmarks", "aids"):
        for entry in tables[key].values():
            if entry.provenance.source_id not in source_ids:
                raise KBError(
                    files[key][0],
                    entry.id,
                    f"source inconnue : {entry.provenance.source_id}",
                )

    for bench in tables["benchmarks"].values():
        unknown = [s for s in bench.sectors if s not in tables["sectors"]]
        if unknown:
            raise KBError(
                files["benchmarks"][0], bench.id, f"secteur inconnu : {', '.join(unknown)}"
            )

    _check_problem_dependencies(tables, files, after_filter=False)

    for key in ("rules", "benchmarks", "aids"):
        for entry in tables[key].values():
            prov = entry.provenance
            if prov.confidence in VERIFIED_CONFIDENCES and prov.verified_on is None:
                raise KBError(
                    files[key][0],
                    entry.id,
                    f"confiance {prov.confidence} sans date de vérification",
                )


def _check_problem_dependencies(
    tables: dict[str, dict[str, Any]], files: dict, *, after_filter: bool
) -> None:
    suffix = " (écartée par verified_only)" if after_filter else ""
    for problem in tables["problems"].values():
        if not after_filter:
            for action_id in problem.action_ids:
                if action_id not in tables["actions"]:
                    raise KBError(
                        files["problems"][0], problem.id, f"action inconnue : {action_id}"
                    )
        for bench_id in problem.evidence_benchmark_ids:
            if bench_id not in tables["benchmarks"]:
                raise KBError(
                    files["problems"][0],
                    problem.id,
                    f"repère inconnu : {bench_id}{suffix}",
                )
