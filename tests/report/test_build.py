from datetime import date

from kb_helpers import KB, KB_SECTOR_ONLY, S_FULL, TODAY, report_for, state

from audit_ia.audit.models import Dimension
from audit_ia.diagnostic.engine import diagnose
from audit_ia.kb.models import Horizon
from audit_ia.report.build import ESTIMATED_NOTE, STALE_NOTE, build_report
from audit_ia.report.check import check_report


def test_sections_always_present():
    r = build_report(state(), diagnose(state(), KB, TODAY), KB, TODAY)
    assert set(r.by_dimension) == set(Dimension) and set(r.plan) == set(Horizon)


def test_empty_audit_report():
    r = report_for(state())
    assert all(len(v) == 1 for v in r.by_dimension.values())
    assert r.verifications and check_report(r, state(), KB) == []


def test_estimated_finding_is_flagged():
    r = report_for(state(comptes_perso=("estime", True)))
    assert r.by_dimension[Dimension.SECURITE][0].note == ESTIMATED_NOTE


def test_upcoming_rule_shows_its_date():
    assert "2 décembre 2027" in report_for(state()).upcoming[0].text


def test_stale_rule_is_flagged_not_hidden():
    r = report_for(state(), today=date(2027, 12, 3))
    assert r.obligations and all(i.note == STALE_NOTE for i in r.obligations)
    assert all(s.stale for i in r.obligations for s in i.sources)


def test_every_kb_backed_item_has_a_source():
    r = report_for(S_FULL)
    assert r.obligations and r.upcoming and r.aids
    for item in r.obligations + r.upcoming + r.aids:
        assert item.sources and all(s.url and s.confidence for s in item.sources)


def test_no_benchmark_statement():
    assert report_for(state(sector="peche"), kb=KB_SECTOR_ONLY).not_measured


def test_built_report_is_always_clean():
    for s in (state(), S_FULL):
        assert check_report(report_for(s), s, KB) == []


def test_summary_and_plan_and_annex():
    r = report_for(S_FULL)
    assert len(r.summary) == 4
    assert [i.refs[0].id for i in r.plan[Horizon.J30]] == ["action-outil-officiel"]
    ids = [s.source_id for s in r.sources]
    assert ids == sorted(ids) and len(set(map(tuple, (s.model_dump().values() for s in r.sources)))) == len(ids)
    finding = r.by_dimension[Dimension.SECURITE][0]
    assert [s.source_id for s in finding.sources] == ["src-a"]


def test_use_case_shows_prerequisites_obstacles_risks_and_first_step():
    text = report_for(state()).use_cases[0].text
    assert text == (
        "Rédaction assistée de courriers. Prérequis : Un outil validé. "
        "Obstacles fréquents : Peur de l'erreur. Risques : Fuite de données. "
        "Première étape : Tester sur trois courriers types."
    )


def test_use_case_omits_empty_labels():
    uc = KB.use_cases["cas-a"].model_copy(
        update={"prerequisites": [], "obstacles": [], "risks": []}
    )
    kb = KB.model_copy(update={"use_cases": {"cas-a": uc}})
    text = report_for(state(), kb=kb).use_cases[0].text
    assert "Première étape" in text
    assert not any(l in text for l in ("Prérequis", "Obstacles", "Risques"))


def test_segment_benchmark_is_shown_with_value_and_source():
    r = report_for(state(sector="construction"), kb=KB_SECTOR_ONLY)
    assert [i.refs[0].id for i in r.benchmarks] == ["repere-construction"]
    item = r.benchmarks[0]
    assert "25 %" in item.text and item.sources and item.sources[0].url
    assert item.sources[0].source_id in [s.source_id for s in r.sources]
    assert report_for(state()).benchmarks[0].refs[0].id == "repere-a"


def test_stale_benchmark_is_flagged():
    r = report_for(state(), today=date(2027, 12, 3))
    assert r.benchmarks and all(i.note == STALE_NOTE for i in r.benchmarks)
    assert all(s.stale for i in r.benchmarks for s in i.sources)




# --- F5 : repères affichés avec leur périmètre, sans doublon

def test_finding_evidence_sentence_with_scope():
    item = report_for(S_FULL).by_dimension[Dimension.SECURITE][0]
    assert item.text == (
        "Des comptes personnels sont utilisés pour des outils d'IA. "
        "Repère : adoption — 40 % (Entreprises de 1 à 249 salariés, T1 2026)."
    )


def test_unpublished_scope_is_stated():
    b = KB.benchmarks["repere-a"].model_copy(update={"scope_published": False})
    kb = KB.model_copy(update={"benchmarks": {**KB.benchmarks, "repere-a": b}})
    item = report_for(S_FULL, kb=kb).by_dimension[Dimension.SECURITE][0]
    assert item.text.endswith("(Entreprises de 1 à 249 salariés, T1 2026). Taille des entreprises interrogées non publiée.")
    other = report_for(state(), kb=kb).benchmarks[0]
    assert other.text.endswith("Taille des entreprises interrogées non publiée.")


def test_benchmark_shown_with_finding_is_not_repeated():
    assert report_for(S_FULL).benchmarks == []
    assert [i.refs[0].id for i in report_for(state()).benchmarks] == ["repere-a"]


# --- F6 : aucun identifiant technique pour le lecteur

def test_profile_labels():
    r = report_for(state(stage="usage_individuel", sector="peche"))
    assert (r.stage_label, r.sector_label) == ("usage individuel", "pêche")
    assert report_for(state(stage="non_utilisatrice")).stage_label == "non utilisatrice"


def test_verification_names_rules_and_aids_it_conditions():
    from audit_ia.kb.models import Test

    rule = KB.rules["regle-a"].model_copy(update={"applies_when": Test(fact="f1", op="eq", value=True)})
    aid = KB.aids["aide-a"].model_copy(update={"eligibility": Test(fact="f1", op="eq", value=True)})
    kb = KB.model_copy(update={"rules": {**KB.rules, "regle-a": rule}, "aids": {"aide-a": aid}})
    s = state()
    r = report_for(s, kb=kb)
    item = next(i for i in r.verifications if i.refs[0].id == "f1")
    assert item.text == (
        "L'entreprise a-t-elle une stratégie IA formalisée ? "
        "Cela conditionne : Règle A de test ; Aide A."
    )
    assert {(x.kind, x.id) for x in item.refs} >= {("rule", "regle-a"), ("aid", "aide-a")}
    assert item.sources and check_report(r, s, kb) == []


def test_verification_blocking_only_problems_names_nothing():
    item = next(i for i in report_for(state()).verifications if i.refs[0].id == "comptes_perso")
    assert item.text == "Des comptes personnels sont-ils utilisés pour les outils d'IA ?"
    assert ("problem", "HUM-S1") in {(x.kind, x.id) for x in item.refs}


# --- F3 : une dimension vide dit pourquoi

NON_COVERED = (
    "Cette dimension n'est pas encore couverte par la base de connaissances : "
    "aucun constat ne peut être établi."
)


def test_dimension_status_and_placeholders():
    r = report_for(state(comptes_perso=False))
    assert r.dimension_status[Dimension.SECURITE] == "aucun_constat"
    assert r.by_dimension[Dimension.SECURITE][0].text == "Aucun constat sur cette dimension d'après vos réponses."
    assert r.dimension_status[Dimension.GOUVERNANCE] == "a_verifier"
    assert r.by_dimension[Dimension.GOUVERNANCE][0].text == (
        "Rien n'a pu être établi sur cette dimension : 1 point reste à vérifier."
    )
    assert r.dimension_status[Dimension.STRATEGIE] == "non_couverte"
    assert r.by_dimension[Dimension.STRATEGIE][0].text == NON_COVERED
    assert report_for(S_FULL).dimension_status[Dimension.SECURITE] == "constats"


def test_points_to_verify_plural():
    from audit_ia.kb.models import All, Test

    problem = KB.problems["HUM-G1"].model_copy(
        update={"triggers": All(all=[Test(fact="charte_ia", op="eq", value=False),
                                     Test(fact="f1", op="eq", value=False)])}  # fmt: skip
    )
    kb = KB.model_copy(update={"problems": {**KB.problems, "HUM-G1": problem}})
    text = report_for(state(), kb=kb).by_dimension[Dimension.GOUVERNANCE][0].text
    assert text == "Rien n'a pu être établi sur cette dimension : 2 points restent à vérifier."


# --- F7 : synthèse lisible

def test_summary_texts():
    texts = [i.text for i in report_for(S_FULL).summary]
    assert texts == [
        "1 constat établi : sécurité 1. 1 dimension reste à vérifier. "
        "5 dimensions non couvertes par la base de connaissances.",
        "Premier cas d'usage à étudier : Rédaction assistée de courriers.",
        "1 obligation applicable et 1 échéance à venir.",
        "1 vérification à mener.",
    ]


def test_summary_without_finding_and_with_estimate_and_stale():
    texts = [i.text for i in report_for(state()).summary]
    assert texts[0] == (
        "Aucun constat établi à ce stade. 2 dimensions restent à vérifier. "
        "5 dimensions non couvertes par la base de connaissances."
    )
    assert texts[3] == "2 vérifications à mener."
    s = state(comptes_perso=("estime", True), charte_ia=False)
    texts = [i.text for i in report_for(s, today=date(2027, 12, 3)).summary]
    assert texts[0].startswith("2 constats établis : gouvernance 1, sécurité 1.")
    assert texts[3] == (
        "Aucune vérification à mener. 1 constat repose sur une estimation. "
        "4 informations à revérifier."
    )


def test_summary_without_use_case_or_rules():
    kb = KB.model_copy(update={"use_cases": {}, "rules": {}})
    texts = [i.text for i in report_for(state(), kb=kb).summary]
    assert texts[1] == "Aucun cas d'usage prioritaire ne ressort de vos réponses."
    assert texts[2] == "Aucune obligation applicable ni échéance à venir identifiée."
    assert not any("(s)" in t or " 0 " in f" {t}" for t in texts)
