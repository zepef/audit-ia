import pytest

from audit_ia.audit.models import Fact
from audit_ia.diagnostic.conditions import Tri, evaluate, undecided_facts
from audit_ia.kb.models import All, AnyOf, Not, Test

T, F, U = Tri.TRUE, Tri.FALSE, Tri.UNKNOWN


def facts(**kwargs):
    return {
        name: Fact(fact_id=name, certainty=certainty, value=value)
        for name, (certainty, value) in kwargs.items()
    }


def facts_for(left, right):
    """Deux tests dont les résultats valent `left` et `right`."""
    spec = {
        T: ("constate", True),
        F: ("constate", False),
        U: ("inconnu", None),
    }
    f = facts(a=spec[left], b=spec[right])
    return f, Test(fact="a", op="eq", value=True), Test(fact="b", op="eq", value=True)


def test_ops():
    f = facts(n=("constate", 12), s=("estime", "sage"))
    assert evaluate(Test(fact="n", op="gte", value=10), f) is T
    assert evaluate(Test(fact="n", op="lt", value=10), f) is F
    assert evaluate(Test(fact="s", op="in", value=["sage", "ebp"]), f) is T


def test_missing_and_unknown_are_unknown():
    f = facts(a=("inconnu", None))
    assert evaluate(Test(fact="a", op="eq", value=True), f) is U
    assert evaluate(Test(fact="absent", op="eq", value=True), f) is U


@pytest.mark.parametrize("left, right, all_, any_", [
    (T, U, U, T), (F, U, F, U), (U, U, U, U), (T, F, F, T),
])
def test_kleene(left, right, all_, any_):
    f, a, b = facts_for(left, right)
    assert evaluate(All(all=[a, b]), f) is all_ and evaluate(All(all=[b, a]), f) is all_
    assert evaluate(AnyOf(any=[a, b]), f) is any_ and evaluate(AnyOf(any=[b, a]), f) is any_


def test_not():
    f, a, b = facts_for(T, U)
    assert evaluate(Not(not_=a), f) is F and evaluate(Not(not_=b), f) is U


def test_undecided_facts():
    c = All(all=[Test(fact="a", op="eq", value=True), Test(fact="b", op="eq", value=True)])
    assert undecided_facts(c, facts(a=("constate", True))) == {"b"}
    assert undecided_facts(c, facts(a=("constate", False))) == set()   # déjà FALSE


def test_type_mismatch_is_unknown():
    assert evaluate(Test(fact="s", op="gt", value=3), facts(s=("constate", "texte"))) is U
