from kb_helpers import KB, S_FULL, report_for, state

from audit_ia.audit.models import Dimension
from audit_ia.report.build import Ref
from audit_ia.report.check import check_report


def test_check_catches_dangling_ref():
    r = report_for(S_FULL)
    r.obligations[0].refs.append(Ref(kind="rule", id="absente"))
    assert any("absente" in v for v in check_report(r, S_FULL, KB))


def test_check_catches_forbidden_term():
    r = report_for(S_FULL)
    r.summary[0].text += " Contactez tckc."
    assert any("tckc" in v.lower() for v in check_report(r, S_FULL, KB))  # terme interdit : "TCKC"


def test_check_catches_forbidden_term_in_note():
    r = report_for(S_FULL)
    r.obligations[0].note = "Voir TCKC"
    assert check_report(r, S_FULL, KB)


def test_check_catches_missing_source_and_url():
    r = report_for(S_FULL)
    r.aids[0].sources = []
    r.obligations[0].sources[0].url = ""
    v = check_report(r, S_FULL, KB)
    assert any("sans ligne de source" in x for x in v) and any("sans URL" in x for x in v)


def test_check_catches_missing_keys():
    r = report_for(state())
    del r.by_dimension[Dimension.SI]
    r.plan.pop(next(iter(r.plan)))
    assert len(check_report(r, state(), KB)) == 2


def test_check_catches_benchmark_item_without_source():
    r = report_for(S_FULL)
    r.benchmarks[0].sources = []
    assert any("benchmarks" in v and "sans ligne de source" in v for v in check_report(r, S_FULL, KB))
