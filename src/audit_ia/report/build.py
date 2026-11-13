"""Construction du rapport structuré à partir d'un diagnostic.

Chaque ligne renvoie à des faits ou à des entrées de la base ; aucune
information n'est extrapolée ; une entrée périmée est signalée, jamais masquée.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel

from audit_ia.audit.models import AuditState, Certainty, CompanyProfile, Dimension, Stage
from audit_ia.diagnostic.engine import Diagnosis
from audit_ia.kb.freshness import is_stale
from audit_ia.kb.models import Benchmark, Confidence, Horizon, KnowledgeBase, Provenance

STALE_NOTE = "À revérifier : cette information n'a pas été recontrôlée récemment."
ESTIMATED_NOTE = "Fondé sur une estimation du décideur, à confirmer."
NO_FINDING_TEXT = "Aucun constat établi sur cette dimension."
UNPUBLISHED_SCOPE = "Taille des entreprises interrogées non publiée."

_MONTHS = [
    "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
    "août", "septembre", "octobre", "novembre", "décembre",
]  # fmt: skip

DIMENSION_LABELS = {
    Dimension.STRATEGIE: "stratégie",
    Dimension.GOUVERNANCE: "gouvernance",
    Dimension.DONNEES: "données",
    Dimension.SI: "systèmes d'information",
    Dimension.SECURITE: "sécurité",
    Dimension.COMPETENCES: "compétences",
    Dimension.VALEUR: "valeur",
}


STAGE_LABELS = {
    Stage.NON_UTILISATRICE: "non utilisatrice",
    Stage.USAGE_INDIVIDUEL: "usage individuel",
    Stage.USAGE_OUTILLE: "usage outillé",
    Stage.PROCESSUS_TRANSFORME: "processus transformé",
}


class Ref(BaseModel):
    kind: Literal["fact", "rule", "benchmark", "problem", "use_case", "action", "aid"]
    id: str


class SourceLine(BaseModel):
    source_id: str
    title: str
    publisher: str
    url: str
    verified_on: date | None
    confidence: Confidence
    stale: bool


class ReportItem(BaseModel):
    text: str
    refs: list[Ref]
    sources: list[SourceLine] = []
    note: str | None = None


class Report(BaseModel):
    kb_version: str
    generated_on: date
    profile: CompanyProfile
    stage_label: str
    sector_label: str
    summary: list[ReportItem]
    by_dimension: dict[Dimension, list[ReportItem]]
    benchmarks: list[ReportItem]
    use_cases: list[ReportItem]
    obligations: list[ReportItem]
    upcoming: list[ReportItem]
    watch: list[ReportItem]
    plan: dict[Horizon, list[ReportItem]]
    verifications: list[ReportItem]
    aids: list[ReportItem]
    not_measured: list[str]
    sources: list[SourceLine]


def format_date_fr(d: date) -> str:
    """« 2 décembre 2027 », sans dépendre de la locale du système."""
    day = "1er" if d.day == 1 else str(d.day)
    return f"{day} {_MONTHS[d.month - 1]} {d.year}"


def _source_line(kb: KnowledgeBase, provenance: Provenance, stale: bool) -> SourceLine:
    source = kb.sources[provenance.source_id]
    return SourceLine(
        source_id=source.id,
        title=source.title,
        publisher=source.publisher,
        url=source.url,
        verified_on=provenance.verified_on,
        confidence=provenance.confidence,
        stale=stale,
    )


def benchmark_sentence(b: Benchmark) -> str:
    """Indicateur, valeur, population et terrain, en une phrase."""
    text = f"{b.indicator} — {b.value} ({b.population}, {b.fieldwork})."
    if not b.scope_published:
        text += f" {UNPUBLISHED_SCOPE}"
    return text


def _notes(*notes: str | None) -> str | None:
    kept = [n for n in notes if n]
    return " ".join(kept) if kept else None


def build_report(
    state: AuditState, diagnosis: Diagnosis, kb: KnowledgeBase, today: date
) -> Report:
    # --- constats par dimension
    by_dimension: dict[Dimension, list[ReportItem]] = {d: [] for d in Dimension}
    benchmark_hits = {h.benchmark_id: h for h in diagnosis.benchmarks}
    shown_with_finding: set[str] = set()
    for finding in diagnosis.findings:
        problem = kb.problems[finding.problem_id]
        refs = [Ref(kind="problem", id=problem.id)]
        refs += [Ref(kind="fact", id=f) for f in finding.fact_ids]
        sources: list[SourceLine] = []
        stale = False
        text = problem.symptom
        for bid in problem.evidence_benchmark_ids:
            hit = benchmark_hits.get(bid)
            if hit is None:
                continue
            refs.append(Ref(kind="benchmark", id=bid))
            text += f" Repère : {benchmark_sentence(kb.benchmarks[bid])}"
            shown_with_finding.add(bid)
            sources.append(_source_line(kb, kb.benchmarks[bid].provenance, hit.stale))
            stale = stale or hit.stale
        by_dimension[problem.dimension].append(
            ReportItem(
                text=text,
                refs=refs,
                sources=sources,
                note=_notes(
                    ESTIMATED_NOTE if finding.certainty is Certainty.ESTIME else None,
                    STALE_NOTE if stale else None,
                ),
            )
        )
    for dimension, items in by_dimension.items():
        if not items:
            items.append(ReportItem(text=NO_FINDING_TEXT, refs=[]))

    # --- règles
    sections: dict[str, list[ReportItem]] = {
        "applicable": [], "a_venir": [], "en_projet": [], "reference": [],
    }  # fmt: skip
    for hit in diagnosis.rules:
        rule = kb.rules[hit.rule_id]
        text = rule.statement
        if hit.timing == "a_venir" and rule.effective_on is not None:
            text += f" Applicable à partir du {format_date_fr(rule.effective_on)}."
        if rule.bounds:
            text += f" Limites : {rule.bounds}"
        sections[hit.timing].append(
            ReportItem(
                text=text,
                refs=[Ref(kind="rule", id=rule.id)],
                sources=[_source_line(kb, rule.provenance, hit.stale)],
                note=STALE_NOTE if hit.stale else None,
            )
        )

    # --- autres repères du segment (ceux déjà cités près d'un constat exclus)
    benchmarks = []
    for hit in diagnosis.benchmarks:
        if hit.benchmark_id in shown_with_finding:
            continue
        b = kb.benchmarks[hit.benchmark_id]
        benchmarks.append(
            ReportItem(
                text=benchmark_sentence(b),
                refs=[Ref(kind="benchmark", id=b.id)],
                sources=[_source_line(kb, b.provenance, hit.stale)],
                note=STALE_NOTE if hit.stale else None,
            )
        )

    # --- cas d'usage
    use_cases = []
    for uc_id in diagnosis.use_case_ids:
        uc = kb.use_cases[uc_id]
        parts = [f"{uc.title}."]
        for label, values in (
            ("Prérequis", uc.prerequisites),
            ("Obstacles fréquents", uc.obstacles),
            ("Risques", uc.risks),
        ):
            if values:
                parts.append(f"{label} : {' ; '.join(values)}.")
        parts.append(f"Première étape : {uc.first_step}")
        use_cases.append(
            ReportItem(
                text=" ".join(parts),
                refs=[Ref(kind="use_case", id=uc.id)],
            )
        )

    # --- plan d'action
    plan: dict[Horizon, list[ReportItem]] = {h: [] for h in Horizon}
    for action_id in diagnosis.action_ids:
        action = kb.actions[action_id]
        causes = [
            Ref(kind="problem", id=f.problem_id)
            for f in diagnosis.findings
            if action_id in kb.problems[f.problem_id].action_ids
        ]
        plan[action.horizon].append(
            ReportItem(
                text=f"{action.title}. Critère de réussite : {action.success_check}",
                refs=[Ref(kind="action", id=action.id), *causes],
            )
        )

    # --- vérifications : la question, et ce qu'elle conditionne parmi les
    # règles et les aides (nommées par leur libellé, sourcées) ; les problèmes
    # et cas d'usage bloqués restent dans les références.
    verifications = []
    for v in diagnosis.verifications:
        text = kb.facts[v.fact_id].prompt_hint if v.fact_id in kb.facts else v.fact_id
        refs = [Ref(kind="fact", id=v.fact_id)]
        labels: list[str] = []
        v_sources: list[SourceLine] = []
        for blocked in v.blocks:
            if blocked in kb.problems:
                refs.append(Ref(kind="problem", id=blocked))
            elif blocked in kb.use_cases:
                refs.append(Ref(kind="use_case", id=blocked))
        # règles d'abord, puis aides
        for kind, table in (("rule", kb.rules), ("aid", kb.aids)):
            for blocked in v.blocks:
                if blocked not in table:
                    continue
                entry = table[blocked]
                refs.append(Ref(kind=kind, id=blocked))
                labels.append(entry.label)
                v_sources.append(_source_line(kb, entry.provenance, is_stale(entry, today)))
        if labels:
            text += f" Cela conditionne : {' ; '.join(labels)}."
        verifications.append(ReportItem(text=text, refs=refs, sources=v_sources))

    # --- aides
    aids = []
    for hit in diagnosis.aids:
        aid = kb.aids[hit.aid_id]
        aids.append(
            ReportItem(
                text=f"{aid.name} : {aid.amount}",
                refs=[Ref(kind="aid", id=aid.id)],
                sources=[_source_line(kb, aid.provenance, hit.stale)],
                note=STALE_NOTE if hit.stale else None,
            )
        )

    # --- non mesuré
    not_measured = [
        f"Aucun repère publié pour votre taille et votre secteur sur : {indicator}."
        for indicator in diagnosis.indicators_without_benchmark
    ]

    # --- synthèse
    per_dim = ", ".join(
        f"{DIMENSION_LABELS[d]} {sum(1 for f in diagnosis.findings if kb.problems[f.problem_id].dimension is d)}"
        for d in Dimension
    )
    summary = [
        ReportItem(
            text=f"Constats par dimension : {per_dim}.",
            refs=[Ref(kind="problem", id=f.problem_id) for f in diagnosis.findings],
        ),
        ReportItem(
            text=(
                f"Premier cas d'usage à étudier : {use_cases[0].text}"
                if use_cases
                else "Aucun cas d'usage n'a pu être retenu sur la base des informations recueillies."
            ),
            refs=list(use_cases[0].refs) if use_cases else [],
        ),
        ReportItem(
            text=(
                f"{len(sections['applicable'])} obligation(s) applicable(s) et "
                f"{len(sections['a_venir'])} échéance(s) à venir."
            ),
            refs=[
                Ref(kind="rule", id=h.rule_id)
                for h in diagnosis.rules
                if h.timing in ("applicable", "a_venir")
            ],
        ),
        ReportItem(
            text=f"{len(verifications)} vérification(s) à mener.",
            refs=[Ref(kind="fact", id=v.fact_id) for v in diagnosis.verifications],
        ),
    ]

    # --- annexe des sources
    seen: dict[tuple, SourceLine] = {}
    all_items = (
        [i for items in by_dimension.values() for i in items]
        + sections["applicable"] + sections["a_venir"]
        + sections["en_projet"] + sections["reference"] + aids + benchmarks
    )  # fmt: skip
    for item in all_items:
        for line in item.sources:
            seen.setdefault(tuple(line.model_dump().values()), line)
    annex = sorted(
        seen.values(),
        key=lambda s: (s.source_id, s.verified_on or date.min, s.confidence.value),
    )

    return Report(
        kb_version=kb.version,
        generated_on=today,
        profile=state.profile,
        stage_label=STAGE_LABELS[state.profile.stage],
        sector_label=(
            kb.sectors[state.profile.sector].label
            if state.profile.sector in kb.sectors
            else state.profile.sector
        ),
        summary=summary,
        by_dimension=by_dimension,
        benchmarks=benchmarks,
        use_cases=use_cases,
        obligations=sections["applicable"],
        upcoming=sections["a_venir"],
        watch=sections["en_projet"] + sections["reference"],
        plan=plan,
        verifications=verifications,
        aids=aids,
        not_measured=not_measured,
        sources=annex,
    )
