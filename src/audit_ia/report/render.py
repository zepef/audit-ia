"""Rendu HTML autonome du rapport structuré (Jinja2, échappement automatique)."""

from jinja2 import Environment, PackageLoader, select_autoescape

from audit_ia.audit.models import Dimension
from audit_ia.kb.models import Horizon
from audit_ia.report.build import DIMENSION_LABELS, Report, format_date_fr

HORIZON_LABELS = {
    Horizon.J30: "Dans les 30 jours",
    Horizon.J90: "Dans les 90 jours",
    Horizon.M12: "Dans les 12 mois",
}

_env = Environment(
    loader=PackageLoader("audit_ia.report", "templates"),
    autoescape=select_autoescape(["html", "j2"], default=True),
    trim_blocks=True,
    lstrip_blocks=True,
)
_env.filters["date_fr"] = format_date_fr


def render_html(report: Report) -> str:
    """Document HTML autonome : feuille de style incluse, aucune ressource externe."""
    template = _env.get_template("report.html.j2")
    return template.render(
        report=report,
        dimensions=list(Dimension),
        dimension_labels=DIMENSION_LABELS,
        horizons=list(Horizon),
        horizon_labels=HORIZON_LABELS,
    )
