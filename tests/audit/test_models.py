import pytest
from pydantic import ValidationError

from audit_ia.audit.models import AuditState, CompanyProfile, Fact, OutOfScopeError

PROFILE = CompanyProfile(
    headcount=40, sector="construction", stage="usage_individuel",
    respondent_role="dirigeant",
)
STATE = AuditState(
    profile=PROFILE,
    facts={
        "a": Fact(fact_id="a", value=True, certainty="constate", quote="oui"),
        "b": Fact(fact_id="b", value=None, certainty="inconnu"),
    },
)


def test_headcount_bounds():
    for n in (0, 250):
        with pytest.raises(OutOfScopeError) as e:
            CompanyProfile(headcount=n, sector="construction",
                           stage="usage_individuel", respondent_role="dirigeant")
        assert "1 à 249 salariés" in str(e.value)


def test_unknown_fact_has_no_value():
    with pytest.raises(ValidationError):
        Fact(fact_id="x", value=True, certainty="inconnu")
    with pytest.raises(ValidationError):
        Fact(fact_id="x", value=None, certainty="constate")


def test_record_replaces():
    s = AuditState(profile=PROFILE)
    s.record(Fact(fact_id="a", value=1, certainty="estime"))
    s.record(Fact(fact_id="a", value=2, certainty="constate"))
    assert s.facts["a"].value == 2


def test_state_roundtrips_json():
    assert AuditState.model_validate_json(STATE.model_dump_json()) == STATE
