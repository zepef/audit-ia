from audit_ia.audit.models import Dimension, Fact
from audit_ia.audit.planner import MIN_FACTS_PER_DIMENSION, coverage, next_objective
from audit_ia.kb.loader import load_kb
from audit_ia.kb.models import FactDef
from kb_helpers import KB_MIN, state


def _fd(fact_id: str, dimension: Dimension, priority: int = 0) -> FactDef:
    return FactDef(
        id=fact_id, dimension=dimension, kind="bool", prompt_hint=fact_id, priority=priority
    )


_BASE = load_kb(KB_MIN)
_EXTRA = [
    _fd("strat_b", Dimension.STRATEGIE, priority=5),
    _fd("strat_c", Dimension.STRATEGIE, priority=5),
    _fd("strat_d", Dimension.STRATEGIE, priority=1),
    _fd("secu_b", Dimension.SECURITE),
    _fd("secu_c", Dimension.SECURITE),
    _fd("secu_d", Dimension.SECURITE),
    _fd("gouv_b", Dimension.GOUVERNANCE),
    _fd("gouv_c", Dimension.GOUVERNANCE),
    _fd("valeur_b", Dimension.VALEUR),
    _fd("valeur_c", Dimension.VALEUR),
    _fd("valeur_d", Dimension.VALEUR),
]
KB = _BASE.model_copy(update={"facts": {**_BASE.facts, **{f.id: f for f in _EXTRA}}})


def all_objectives(s, kb, *, ids: bool = True):
    out = []
    while (obj := next_objective(s, kb)) is not None:
        out.append(obj.fact_id if ids else obj)
        s.record(Fact(fact_id=obj.fact_id, value=None, certainty="inconnu"))
    return out


def fully_covered_state(kb):
    """Chaque dimension a exactement MIN_FACTS_PER_DIMENSION faits recueillis (ou tous, s'il y en a moins)."""
    s = state()
    by_dim: dict[Dimension, list[str]] = {}
    for fid in sorted(kb.facts):
        by_dim.setdefault(kb.facts[fid].dimension, []).append(fid)
    for fids in by_dim.values():
        for fid in fids[:MIN_FACTS_PER_DIMENSION]:
            s.record(Fact(fact_id=fid, value=True, certainty="constate"))
    return s


def test_starts_with_least_covered_dimension_in_enum_order():
    assert next_objective(state(), KB).dimension == Dimension.STRATEGIE


def test_skips_facts_of_other_stages():
    ids = all_objectives(state(stage="non_utilisatrice"), KB)
    assert "automatisation.validation_humaine" not in ids


def test_includes_facts_of_matching_stage():
    ids = all_objectives(state(stage="processus_transforme"), KB)
    assert "automatisation.validation_humaine" in ids


def test_unknown_answer_counts_as_covered():
    s = state()
    s.record(Fact(fact_id="f1", value=None, certainty="inconnu"))
    assert coverage(s, KB)[Dimension.STRATEGIE] == 1


def test_coverage_lists_every_dimension():
    assert coverage(state(), KB) == {d: 0 for d in Dimension}


def test_asked_but_unanswered_is_not_asked_again():
    first = next_objective(state(), KB)
    assert next_objective(state(), KB, asked=frozenset({first.fact_id})).fact_id != first.fact_id


def test_stops_when_every_dimension_is_covered():
    assert next_objective(fully_covered_state(KB), KB) is None


def test_terminates():
    assert len(all_objectives(state(), KB)) <= len(KB.facts)


def test_priority_then_id_within_dimension():
    ids = all_objectives(state(), KB)
    strat = [i for i in ids if KB.facts[i].dimension == Dimension.STRATEGIE]
    assert strat[:2] == ["strat_b", "strat_c"]


def test_alternates_dimensions_by_least_coverage():
    objs = all_objectives(state(), KB, ids=False)
    assert [o.dimension for o in objs[:3]] == [
        Dimension.STRATEGIE,
        Dimension.GOUVERNANCE,
        Dimension.SECURITE,
    ]


def test_no_dimension_exceeds_minimum_when_stopping():
    s = state()
    all_objectives(s, KB)
    cov = coverage(s, KB)
    assert all(n <= MIN_FACTS_PER_DIMENSION for n in cov.values())
