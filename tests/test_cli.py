import pytest
from kb_helpers import KB_MIN, S_FULL, mutated_copy, state

from audit_ia.cli import main


@pytest.fixture
def audit_json(tmp_path):
    path = tmp_path / "audit.json"
    path.write_text(S_FULL.model_dump_json(), encoding="utf-8")
    return path


@pytest.fixture
def audit_250(tmp_path):
    path = tmp_path / "audit250.json"
    path.write_text(state(headcount=45).model_dump_json().replace('"headcount":45', '"headcount":250'), encoding="utf-8")
    return path


@pytest.fixture
def broken_kb(tmp_path):
    return mutated_copy(KB_MIN, tmp_path, "duplicate_rule_id")


def test_cli_report_writes_file(tmp_path, audit_json):
    out = tmp_path / "r.html"
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(audit_json), "--out", str(out),
                 "--today", "2026-11-13", "--all-confidence"]) == 0  # fmt: skip
    assert out.read_text(encoding="utf-8").startswith("<!doctype html>")


def test_cli_exit_codes(tmp_path, capsys, broken_kb, audit_250):
    assert main(["validate-kb", "--kb", str(broken_kb)]) == 1
    assert "rules.yaml: regle-a:" in capsys.readouterr().err
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(audit_250), "--out", str(tmp_path / "x")]) == 2  # fmt: skip
    assert "1 à 249 salariés" in capsys.readouterr().err
    assert not (tmp_path / "x").exists()


def test_cli_validate_kb_ok(capsys):
    assert main(["validate-kb", "--kb", str(KB_MIN)]) == 0


def test_cli_invalid_audit_file_exits_1(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("pas du json", encoding="utf-8")
    out = tmp_path / "x"
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(bad), "--out", str(out)]) == 1
    assert capsys.readouterr().err.strip() and not out.exists()


def test_cli_missing_inputs_exit_1(tmp_path, audit_json, capsys):
    out = str(tmp_path / "x")
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(tmp_path / "nope.json"), "--out", out]) == 1
    assert main(["report", "--kb", str(tmp_path / "nokb"), "--facts", str(audit_json), "--out", out]) == 1
    assert main(["validate-kb", "--kb", str(tmp_path / "nokb")]) == 1


def test_cli_check_failure_exits_3(tmp_path, audit_json, monkeypatch, capsys):
    monkeypatch.setattr("audit_ia.cli.check_report", lambda *a: ["violation test"])
    out = tmp_path / "x"
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(audit_json), "--out", str(out),
                 "--all-confidence"]) == 3  # fmt: skip
    assert "violation test" in capsys.readouterr().err and not out.exists()
