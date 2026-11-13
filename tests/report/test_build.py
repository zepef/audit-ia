from datetime import date

from kb_helpers import KB, KB_SECTOR_ONLY, S_FULL, TODAY, report_for, state

from audit_ia.audit.models import Dimension
from audit_ia.diagnostic.engine import diagnose
from audit_ia.kb.models import Horizon
from audit_ia.report.build import ESTIMATED_NOTE, STALE_NOTE, build_report
from audit_ia.report.check import check_report


def test_sections_always_present():
    r = build_report(state(), diagnose(state(), KB, TODAY), KB, TODAY)
    assert set(r.by_dimension) == set(Dimension) and set(r.plan) == set(Horizon)


def test_empty_audit_report():
    r = report_for(state())
    assert all(len(v) == 1 and v[0].refs == [] for v in r.by_dimension.values())
    assert r.verifications and check_report(r, state(), KB) == []


def test_estimated_finding_is_flagged():
    r = report_for(state(comptes_perso=("estime", True)))
    assert r.by_dimension[Dimension.SECURITE][0].note == ESTIMATED_NOTE


def test_upcoming_rule_shows_its_date():
    assert "2 décembre 2027" in report_for(state()).upcoming[0].text


def test_stale_rule_is_flagged_not_hidden():
    r = report_for(state(), today=date(2027, 12, 3))
    assert r.obligations and all(i.note == STALE_NOTE for i in r.obligations)
    assert all(s.stale for i in r.obligations for s in i.sources)


def test_every_kb_backed_item_has_a_source():
    r = report_for(S_FULL)
    assert r.obligations and r.upcoming and r.aids
    for item in r.obligations + r.upcoming + r.aids:
        assert item.sources and all(s.url and s.confidence for s in item.sources)


def test_no_benchmark_statement():
    assert report_for(state(sector="peche"), kb=KB_SECTOR_ONLY).not_measured


def test_built_report_is_always_clean():
    for s in (state(), S_FULL):
        assert check_report(report_for(s), s, KB) == []


def test_summary_and_plan_and_annex():
    r = report_for(S_FULL)
    assert len(r.summary) == 4
    assert [i.refs[0].id for i in r.plan[Horizon.J30]] == ["action-outil-officiel"]
    ids = [s.source_id for s in r.sources]
    assert ids == sorted(ids) and len(set(map(tuple, (s.model_dump().values() for s in r.sources)))) == len(ids)
    finding = r.by_dimension[Dimension.SECURITE][0]
    assert [s.source_id for s in finding.sources] == ["src-a"]
