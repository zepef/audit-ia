from datetime import date

from kb_helpers import benchmark, rule

from audit_ia.kb.freshness import is_stale


def test_staleness():
    today = date(2026, 11, 13)
    assert is_stale(rule(verified_on=date(2026, 5, 16)), today)  # 181 jours
    assert not is_stale(rule(verified_on=date(2026, 5, 17)), today)  # 180 jours
    assert is_stale(rule(verified_on=None), today)
    assert is_stale(benchmark(expires_on=date(2026, 11, 12)), today)
    assert not is_stale(benchmark(expires_on=date(2026, 11, 13)), today)
