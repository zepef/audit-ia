import pytest

from audit_ia.audit.models import Fact
from audit_ia.diagnostic.conditions import Tri, deciding_facts, evaluate, undecided_facts
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


# --- faits décisifs (F1)

def _fon_rh():
    """Forme de FON-RH : a ET (b = faux OU c = faux)."""
    return All(all=[
        Test(fact="a", op="eq", value=True),
        AnyOf(any=[Test(fact="b", op="eq", value=False), Test(fact="c", op="eq", value=False)]),
    ])  # fmt: skip


def test_deciding_facts_skip_false_branch_of_any():
    f = facts(a=("constate", True), b=("constate", False), c=("estime", True))
    assert evaluate(_fon_rh(), f) is T
    assert deciding_facts(_fon_rh(), f) == {"a", "b"}


def test_deciding_facts_mirror_only_estimated_branch_true():
    f = facts(a=("constate", True), b=("constate", True), c=("estime", False))
    assert deciding_facts(_fon_rh(), f) == {"a", "c"}


def test_deciding_facts_prefers_constated_true_branch():
    f = facts(a=("constate", True), b=("estime", False), c=("constate", False))
    assert deciding_facts(_fon_rh(), f) == {"a", "c"}
    f = facts(a=("constate", True), b=("estime", False), c=("estime", False))
    assert deciding_facts(_fon_rh(), f) == {"a", "b"}      # aucune branche constatée : la première


def test_deciding_facts_through_not():
    a, b = Test(fact="a", op="eq", value=True), Test(fact="b", op="eq", value=True)
    # NON(a ET b) vrai : une des branches fausses suffit, de préférence constatée
    f = facts(a=("estime", False), b=("constate", False))
    assert deciding_facts(Not(not_=All(all=[a, b])), f) == {"b"}
    # NON(a OU b) vrai : toutes les branches fausses comptent
    f = facts(a=("estime", False), b=("constate", False))
    assert deciding_facts(Not(not_=AnyOf(any=[a, b])), f) == {"a", "b"}


def test_deciding_facts_empty_when_unknown():
    assert deciding_facts(_fon_rh(), facts(a=("inconnu", None))) == set()


def test_type_mismatch_lists_fact_to_verify():
    # une incohérence de type ne peut plus venir de l'entrée ; si elle survient,
    # l'UNKNOWN a toujours un fait à vérifier
    assert undecided_facts(Test(fact="s", op="gt", value=3), facts(s=("constate", "texte"))) == {"s"}
