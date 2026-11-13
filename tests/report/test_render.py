from datetime import date
from markupsafe import escape

from kb_helpers import KB_SECTOR_ONLY, S_FULL, report_for, state

from audit_ia.audit.models import Fact
from audit_ia.kb.models import Confidence
from audit_ia.report.build import STALE_NOTE
from audit_ia.report.render import render_html


def test_html_sections_in_order():
    html = render_html(report_for(S_FULL))
    titles = ["Synthèse", "Bilan par dimension", "Cas d'usage prioritaires", "Obligations et échéances",
              "Plan d'action", "Vérifications à mener", "Aides et dispositifs", "Sources"]  # fmt: skip
    assert [html.index(t) for t in titles] == sorted(html.index(t) for t in titles)


def test_html_escapes_quotes_from_interview():
    s = state()
    s.record(Fact(fact_id="f1", value="<script>x</script>", certainty="constate"))
    assert "<script>x" not in render_html(report_for(s))


def test_html_escapes_report_text():
    r = report_for(S_FULL)
    r.summary[0].text = "<script>x</script>"
    html = render_html(r)
    assert "<script>x" not in html and "&lt;script&gt;" in html


def test_html_has_no_external_resource():
    html = render_html(report_for(S_FULL))
    assert "<link" not in html and "src=" not in html


def test_html_shows_source_metadata():
    r = report_for(S_FULL)
    # la base de test ne contient aucune entrée V2 : on en force une pour contrôler l'affichage
    r.obligations[0].sources[0].confidence = Confidence.V2
    html = render_html(r)
    assert "Vérifié le" in html and "Niveau de confiance : V2" in html and "Éditeur A" in html
    assert "V2" in html and "Base de connaissances test" in html


def test_html_is_standalone_french_document():
    html = render_html(report_for(S_FULL))
    assert html.startswith("<!doctype html>") and '<html lang="fr">' in html
    assert "13 novembre 2026" in html


BENCH_TITLE = "Autres repères"


def test_html_renders_segment_benchmarks_in_place():
    r = report_for(state())
    assert r.benchmarks
    html = render_html(r)
    pos = [html.index("Bilan par dimension"), html.index(BENCH_TITLE), html.index("40 %", html.index(BENCH_TITLE)),
           html.index("Cas d'usage prioritaires")]  # fmt: skip
    assert pos == sorted(pos)
    assert "Vérifié le" in html[html.index(BENCH_TITLE) : html.index("Cas d'usage prioritaires")]


def test_html_stale_benchmark_shows_note():
    r = report_for(state(), today=date(2027, 12, 3))
    assert r.benchmarks and r.benchmarks[0].note == STALE_NOTE
    page = render_html(r)
    section = page[page.index(BENCH_TITLE) : page.index("Cas d'usage prioritaires")]
    assert str(escape(STALE_NOTE)) in section


def test_html_without_benchmark_omits_subsection():
    r = report_for(state(sector="peche"), kb=KB_SECTOR_ONLY)
    assert not r.benchmarks
    assert BENCH_TITLE not in render_html(r)


def test_html_shows_french_labels_not_identifiers():
    html = render_html(report_for(state(stage="usage_individuel", sector="peche")))
    assert "stade : usage individuel" in html and "secteur pêche" in html
    assert "usage_individuel" not in html


def test_html_refs_are_attributes_not_text():
    html = render_html(report_for(S_FULL))
    assert "Réf. :" not in html
    assert 'data-refs="problem:HUM-S1 fact:comptes_perso benchmark:repere-a"' in html
