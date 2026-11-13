"""Contrôle d'un rapport : traçabilité des lignes et neutralité commerciale."""

from audit_ia.audit.models import AuditState, Dimension
from audit_ia.kb.models import Horizon, KnowledgeBase
from audit_ia.report.build import Ref, Report, ReportItem

SOURCED_KINDS = {"rule", "benchmark", "aid"}


def _ref_exists(ref: Ref, state: AuditState, kb: KnowledgeBase) -> bool:
    match ref.kind:
        case "fact":
            return ref.id in state.facts or ref.id in kb.facts
        case "rule":
            return ref.id in kb.rules
        case "benchmark":
            return ref.id in kb.benchmarks
        case "problem":
            return ref.id in kb.problems
        case "use_case":
            return ref.id in kb.use_cases
        case "action":
            return ref.id in kb.actions
        case "aid":
            return ref.id in kb.aids
    return False


def _sections(report: Report) -> list[tuple[str, ReportItem]]:
    named: list[tuple[str, list[ReportItem]]] = [
        ("summary", report.summary),
        ("use_cases", report.use_cases),
        ("obligations", report.obligations),
        ("upcoming", report.upcoming),
        ("watch", report.watch),
        ("verifications", report.verifications),
        ("aids", report.aids),
    ]
    named += [(f"by_dimension[{d.value}]", i) for d, i in report.by_dimension.items()]
    named += [(f"plan[{h.value}]", i) for h, i in report.plan.items()]
    return [(name, item) for name, items in named for item in items]


def check_report(report: Report, state: AuditState, kb: KnowledgeBase) -> list[str]:
    """Violations relevées ; liste vide = rapport conforme.

    La synthèse ne porte que des décomptes de lignes détaillées ailleurs (et
    sourcées là) : elle est exemptée de l'exigence de ligne de source.
    """
    violations: list[str] = []

    for d in Dimension:
        if d not in report.by_dimension:
            violations.append(f"Clé manquante dans by_dimension : {d.value}")
    for h in Horizon:
        if h not in report.plan:
            violations.append(f"Clé manquante dans plan : {h.value}")

    forbidden = [t for t in kb.forbidden_terms if t]
    items = _sections(report)
    for section, item in items:
        for ref in item.refs:
            if not _ref_exists(ref, state, kb):
                violations.append(
                    f"{section} : référence inexistante {ref.kind} « {ref.id} »"
                )
        if (
            section != "summary"
            and not item.sources
            and any(r.kind in SOURCED_KINDS for r in item.refs)
        ):
            violations.append(f"{section} : élément sans ligne de source : {item.text!r}")
        for line in item.sources:
            if not line.url:
                violations.append(f"{section} : source {line.source_id} sans URL")
        for label, value in (("text", item.text), ("note", item.note)):
            low = (value or "").lower()
            for term in forbidden:
                if term.lower() in low:
                    violations.append(f"{section} : terme interdit « {term} » dans {label}")

    for line in report.sources:
        if not line.url:
            violations.append(f"sources : source {line.source_id} sans URL")
    for text in report.not_measured:
        low = text.lower()
        for term in forbidden:
            if term.lower() in low:
                violations.append(f"not_measured : terme interdit « {term} »")
    return violations
