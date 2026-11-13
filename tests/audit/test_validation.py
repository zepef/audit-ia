"""Contrôle des faits d'audit contre la base de connaissances (F2)."""

import pytest
from kb_helpers import KB, state

from audit_ia.audit.validation import FactValidationError, validate_state
from audit_ia.kb.models import FactDef

KB_KINDS = KB.model_copy(
    update={
        "facts": {
            **KB.facts,
            "n_entier": FactDef(id="n_entier", dimension="si", kind="int", prompt_hint="?"),
            "n_reel": FactDef(id="n_reel", dimension="si", kind="float", prompt_hint="?"),
            "choix": FactDef(id="choix", dimension="si", kind="enum", choices=["a", "b"], prompt_hint="?"),
            "texte": FactDef(id="texte", dimension="si", kind="text", prompt_hint="?"),
        }
    }
)


def test_valid_state_passes():
    validate_state(state(comptes_perso=True, charte_ia=("inconnu", None)), KB)
    validate_state(state(n_entier=3, n_reel=2, choix="a", texte="libre"), KB_KINDS)
    validate_state(state(n_reel=2.5), KB_KINDS)


@pytest.mark.parametrize(
    "facts",
    [
        {"comptes_perso": "true"},     # chaîne pour un booléen
        {"comptes_perso": 1},
        {"n_entier": True},            # un booléen n'est pas un entier
        {"n_entier": 2.0},
        {"n_reel": False},
        {"choix": "c"},                # hors des choix
        {"choix": 1},
        {"texte": 3},
    ],
)
def test_value_of_wrong_kind_is_rejected(facts):
    with pytest.raises(FactValidationError) as e:
        validate_state(state(**facts), KB_KINDS)
    assert e.value.fact_id == next(iter(facts))
    assert next(iter(facts)) in str(e.value)


def test_unknown_fact_is_rejected():
    with pytest.raises(FactValidationError) as e:
        validate_state(state(fait_absent=True), KB)
    assert e.value.fact_id == "fait_absent"


def test_unknown_sector_is_rejected():
    with pytest.raises(FactValidationError) as e:
        validate_state(state(sector="aeronautique"), KB)
    assert e.value.fact_id is None and "aeronautique" in e.value.message
