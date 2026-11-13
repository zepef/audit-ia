import pytest
from kb_helpers import KB_MIN, mutated_copy

from audit_ia.kb.loader import KBError, load_kb


def test_loads_minimal_kb():
    kb = load_kb(KB_MIN)
    assert set(kb.rules) == {"regle-a", "regle-b"} and kb.version == "test"


def test_verified_only_drops_unverified():
    assert set(load_kb(KB_MIN, verified_only=True).rules) == {"regle-a"}


def test_require_review_fails_on_unreviewed():
    with pytest.raises(KBError) as e:
        load_kb(KB_MIN, require_review=True)
    assert e.value.file == "rules.yaml" and e.value.entry_id == "regle-a"


@pytest.mark.parametrize(
    "mutation, file, entry_id",
    [
        ("duplicate_rule_id", "rules.yaml", "regle-a"),
        ("condition_unknown_fact", "problems.yaml", "HUM-S1"),
        ("unknown_source", "benchmarks.yaml", "repere-a"),
        ("problem_unknown_action", "problems.yaml", "HUM-S1"),
        ("problem_unknown_benchmark", "problems.yaml", "HUM-S1"),
        ("bad_problem_id", "problems.yaml", "hum_s1"),
        ("verified_without_date", "rules.yaml", "regle-a"),
    ],
)
def test_incoherent_kb_names_file_and_entry(tmp_path, mutation, file, entry_id):
    root = mutated_copy(KB_MIN, tmp_path, mutation)
    with pytest.raises(KBError) as e:
        load_kb(root)
    assert (e.value.file, e.value.entry_id) == (file, entry_id)


def test_verified_only_fails_if_dependency_dropped(tmp_path):
    with pytest.raises(KBError):
        load_kb(
            mutated_copy(KB_MIN, tmp_path, "evidence_is_unverified"), verified_only=True
        )
