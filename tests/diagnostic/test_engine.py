from datetime import date

from kb_helpers import KB_MIN, state

from audit_ia.diagnostic.engine import Finding, diagnose
from audit_ia.kb.loader import load_kb
from audit_ia.kb.models import Test, UseCase

TODAY = date(2026, 11, 13)
KB = load_kb(KB_MIN)
S = state(comptes_perso=("estime", True), charte_ia=False)


def _kb_with(**changes):
    return KB.model_copy(update=changes)


KB_SECTOR_ONLY = _kb_with(
    benchmarks={"repere-construction": KB.benchmarks["repere-construction"]}
)
KB_MANY_USE_CASES = _kb_with(
    use_cases={
        f"cas-priorite-{p}": UseCase(
            id=f"cas-priorite-{p}",
            function="administration",
            title=f"Cas {p}",
            prerequisites=[],
            obstacles=[],
            risks=[],
            first_step="Démarrer.",
            priority=p,
        )
        for p in range(1, 10)
    }
)


def timing(d, rule_id):
    return next(h.timing for h in d.rules if h.rule_id == rule_id)


def aids(d):
    return [h.aid_id for h in d.aids]


def test_finding_with_estimated_fact():
    d = diagnose(state(comptes_perso=("estime", True)), KB, TODAY)
    assert d.findings == [Finding(problem_id="HUM-S1", fact_ids=["comptes_perso"], certainty="estime")]
    assert d.action_ids == ["action-outil-officiel"]


def test_empty_audit_invents_nothing():
    d = diagnose(state(), KB, TODAY)
    assert d.findings == [] and d.action_ids == []
    assert {v.fact_id for v in d.verifications} >= {"comptes_perso"}
    assert "HUM-S1" in next(v for v in d.verifications if v.fact_id == "comptes_perso").blocks


def test_rule_timing():
    d = diagnose(state(), KB, date(2026, 11, 13))
    assert timing(d, "regle-a") == "applicable"     # effective_on 2025-02-02
    assert timing(d, "regle-b") == "a_venir"        # adopte_non_applicable, 2027-12-02
    assert timing(diagnose(state(), KB, date(2027, 12, 2)), "regle-b") == "applicable"


def test_stale_entries_are_kept_and_flagged():
    d = diagnose(state(), KB, date(2027, 12, 1))
    assert all(h.stale for h in d.rules) and len(d.rules) == 2


def test_sector_benchmark_replaces_generic():
    d = diagnose(state(sector="construction"), KB, TODAY)
    assert [h.benchmark_id for h in d.benchmarks] == ["repere-construction"]


def test_generic_benchmark_when_no_sector_one():
    d = diagnose(state(sector="commerce"), KB, TODAY)
    assert [h.benchmark_id for h in d.benchmarks] == ["repere-a"]


def test_no_benchmark_for_segment_is_reported():
    d = diagnose(state(headcount=5, sector="peche"), KB_SECTOR_ONLY, TODAY)
    assert d.benchmarks == [] and d.indicators_without_benchmark == ["adoption"]


def test_use_cases_capped_and_ordered():
    d = diagnose(state(), KB_MANY_USE_CASES, TODAY)
    assert len(d.use_case_ids) == 5 and d.use_case_ids[0] == "cas-priorite-9"


def test_aid_headcount_bounds():
    assert aids(diagnose(state(headcount=9), KB, TODAY)) == []          # aide 10..249
    assert aids(diagnose(state(headcount=10), KB, TODAY)) == ["aide-a"]


def test_actions_deduplicated_in_finding_order():
    d = diagnose(S, KB, TODAY)
    assert [f.problem_id for f in d.findings] == ["HUM-G1", "HUM-S1"]
    assert d.action_ids == ["action-charte", "action-outil-officiel"]


def test_diagnosis_is_deterministic():
    assert diagnose(S, KB, TODAY) == diagnose(S, KB, TODAY)


def _blocks(d, fact_id):
    return next(v.blocks for v in d.verifications if v.fact_id == fact_id)


def test_undecided_use_case_becomes_verification():
    uc = KB.use_cases["cas-a"].model_copy(
        update={"applies_when": Test(fact="charte_ia", op="eq", value=True)}
    )
    kb = _kb_with(use_cases={"cas-a": uc})
    d = diagnose(state(), kb, TODAY)
    assert d.use_case_ids == []
    assert "cas-a" in _blocks(d, "charte_ia")


def test_undecided_rule_is_excluded_and_verified():
    rule = KB.rules["regle-a"].model_copy(
        update={"applies_when": Test(fact="f1", op="eq", value=True)}
    )
    kb = _kb_with(rules={"regle-a": rule})
    d = diagnose(state(), kb, TODAY)
    assert [h.rule_id for h in d.rules] == []
    assert "regle-a" in _blocks(d, "f1")


def test_stale_aid_and_benchmark_are_kept_and_flagged():
    d = diagnose(state(), KB, date(2027, 12, 1))
    assert [h.aid_id for h in d.aids] == ["aide-a"] and d.aids[0].stale
    assert d.benchmarks and all(h.stale for h in d.benchmarks)
