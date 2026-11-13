"""Base de connaissances initiale : tailles minimales, provenance, valeurs épinglées."""

from datetime import date
from pathlib import Path

from audit_ia.audit.models import Dimension
from audit_ia.kb.loader import load_kb

ROOT = Path(__file__).resolve().parents[1]
KB = load_kb(ROOT / "kb", verified_only=True)


def test_minimum_sizes():
    assert len(KB.rules) >= 10 and len(KB.benchmarks) >= 15 and len(KB.problems) >= 15
    assert (
        len(KB.facts) >= 40
        and len(KB.actions) >= 20
        and len(KB.aids) >= 3
        and len(KB.use_cases) >= 8
    )


def test_every_dimension_has_facts_and_a_problem():
    for d in Dimension:
        assert sum(f.dimension == d for f in KB.facts.values()) >= 4
        assert any(p.dimension == d for p in KB.problems.values())


def test_only_verified_entries():
    for e in [*KB.rules.values(), *KB.benchmarks.values(), *KB.aids.values()]:
        assert e.provenance.confidence in (
            "V",
            "V2",
        ) and e.provenance.verified_on == date(2026, 11, 13)


def test_pinned_values_from_corpus():
    r = KB.rules["ai-act-annexe-iii"]
    assert (r.status, r.effective_on) == ("adopte_non_applicable", date(2027, 12, 2))
    assert KB.rules["ai-act-annexe-i"].effective_on == date(2028, 8, 2)
    assert KB.rules["ai-act-art-50-transparence"].effective_on == date(2026, 8, 2)
    assert KB.rules["facturation-electronique-reception"].effective_on == date(
        2026, 9, 1
    )
    assert KB.rules["facturation-electronique-emission-pme"].effective_on == date(
        2027, 9, 1
    )
    b = KB.benchmarks["insee-2025-adoption"]
    assert b.value.startswith("18 %") and b.headcount_min == 10
    assert KB.benchmarks["francenum-2026-adoption"].value.startswith("40 %")
    assert KB.benchmarks["bdf-2026-gain-productivite"].value.startswith("31 %")
    assert {"HUM-S1", "HUM-G2", "CYB-C4", "FON-RH"} <= set(KB.problems)


def test_diagnostic_data_ia_excludes_under_ten():
    a = KB.aids["diagnostic-data-ia"]
    assert a.headcount_min == 10 and "40 %" in a.amount


def test_every_problem_has_an_action():
    assert all(p.action_ids for p in KB.problems.values())


def test_no_forbidden_term_in_kb_texts():
    texts = [a.title for a in KB.actions.values()] + [
        u.title + u.first_step for u in KB.use_cases.values()
    ]
    assert not [t for t in texts for w in KB.forbidden_terms if w.lower() in t.lower()]
