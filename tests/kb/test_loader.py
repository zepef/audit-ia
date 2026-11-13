import shutil

import pytest
import yaml
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
        ("rule_without_label", "rules.yaml", "regle-a"),
        ("aid_without_label", "aids.yaml", "aide-a"),
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


@pytest.mark.parametrize(
    "file, entry_id, edit",
    [
        ("rules.yaml", "regle-a", lambda e: e.update(applies_whn=None)),
        ("problems.yaml", "HUM-S1", lambda e: e["triggers"].update(vlaue=True)),
        (
            "benchmarks.yaml",
            "repere-a",
            lambda e: e["provenance"].update(confidance="V"),
        ),
    ],
)
def test_unknown_key_fails_with_file_and_entry(tmp_path, file, entry_id, edit):
    root = tmp_path / "kb"
    shutil.copytree(KB_MIN, root)
    data = yaml.safe_load((root / file).read_text(encoding="utf-8"))
    edit(next(e for e in data if e["id"] == entry_id))
    (root / file).write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    with pytest.raises(KBError) as e:
        load_kb(root)
    assert (e.value.file, e.value.entry_id) == (file, entry_id)


def test_sectors_are_loaded():
    kb = load_kb(KB_MIN)
    assert {"commerce", "construction", "peche", "autre"} <= set(kb.sectors)
    assert kb.sectors["construction"].label


def test_benchmark_with_unknown_sector_is_rejected(tmp_path):
    root = mutated_copy(KB_MIN, tmp_path, "benchmark_unknown_sector")
    with pytest.raises(KBError) as e:
        load_kb(root)
    assert (e.value.file, e.value.entry_id) == ("benchmarks.yaml", "repere-construction")
    assert "secteur inconnu" in e.value.message


def _set_trigger(root, fact):
    path = root / "problems.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    next(e for e in data if e["id"] == "HUM-S1")["triggers"] = {"fact": fact, "op": "eq", "value": "x"}
    path.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")


@pytest.mark.parametrize("fact", ["profile.stage", "profile.headcount", "profile.sector"])
def test_profile_pseudo_facts_accepted_in_conditions(tmp_path, fact):
    root = tmp_path / "kb"
    shutil.copytree(KB_MIN, root)
    _set_trigger(root, fact)
    assert "HUM-S1" in load_kb(root).problems


def test_other_profile_name_is_rejected(tmp_path):
    root = tmp_path / "kb"
    shutil.copytree(KB_MIN, root)
    _set_trigger(root, "profile.respondent_role")
    with pytest.raises(KBError) as e:
        load_kb(root)
    assert e.value.entry_id == "HUM-S1"
