"""Bout en bout sur la base réelle : trois audits de référence, rapport conforme."""

from datetime import date
from pathlib import Path

import pytest
from kb_helpers import all_objectives

from audit_ia.audit.models import AuditState, Dimension, load_audit_state
from audit_ia.diagnostic.engine import diagnose
from audit_ia.kb.loader import load_kb
from audit_ia.report.build import build_report
from audit_ia.report.check import check_report
from audit_ia.report.render import render_html

ROOT = Path(__file__).resolve().parents[1]
KB = load_kb(ROOT / "kb", verified_only=True)
AUDITS = Path(__file__).resolve().parent / "fixtures" / "audits"
TODAY = date(2026, 11, 13)


def load(name: str) -> AuditState:
    return load_audit_state((AUDITS / f"{name}.json").read_bytes())


@pytest.mark.parametrize(
    "name", ["tpe_non_utilisatrice", "pme_usage_individuel", "pme_usage_outille"]
)
def test_reference_audit_produces_clean_report(name):
    state = AuditState.model_validate_json(
        (AUDITS / f"{name}.json").read_text(encoding="utf-8")
    )
    report = build_report(state, diagnose(state, KB, TODAY), KB, TODAY)
    assert check_report(report, state, KB) == []
    assert render_html(report).startswith("<!doctype html>")


def test_pme_usage_individuel_expected_findings():
    d = diagnose(load("pme_usage_individuel"), KB, TODAY)
    assert {"HUM-S1", "CYB-C4"} <= {f.problem_id for f in d.findings}
    assert 3 <= len(d.use_case_ids) <= 5
    assert "diagnostic-data-ia" in {a.aid_id for a in d.aids}


def test_tpe_gets_no_diagnostic_data_ia():
    d = diagnose(load("tpe_non_utilisatrice"), KB, TODAY)  # 6 salariés
    assert "diagnostic-data-ia" not in {a.aid_id for a in d.aids}


def test_recruitment_screening_triggers_high_risk_deadline():
    d = diagnose(load("pme_usage_outille"), KB, TODAY)  # tri de candidatures par IA
    assert "FON-RH" in {f.problem_id for f in d.findings}
    assert ("ai-act-annexe-iii", "a_venir") in {(r.rule_id, r.timing) for r in d.rules}


def test_planner_covers_every_dimension_on_real_kb():
    s = load("tpe_non_utilisatrice").model_copy(update={"facts": {}})
    assert {o.dimension for o in all_objectives(s, KB, ids=False)} == set(Dimension)
