"""Ligne de commande : validation de la base et génération du rapport."""

import argparse
import sys
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from audit_ia.audit.models import OutOfScopeError, load_audit_state
from audit_ia.audit.validation import FactValidationError, validate_state
from audit_ia.diagnostic.engine import diagnose
from audit_ia.kb.loader import KBError, load_kb
from audit_ia.report.build import build_report
from audit_ia.report.check import check_report
from audit_ia.report.render import render_html


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="audit-ia")
    sub = parser.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate-kb", help="valide la base de connaissances")
    v.add_argument("--kb", default="kb")
    v.add_argument("--verified-only", action="store_true")
    v.add_argument("--require-review", action="store_true")

    r = sub.add_parser("report", help="génère le rapport HTML")
    r.add_argument("--facts", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--kb", default="kb")
    r.add_argument("--today", type=date.fromisoformat, default=None)
    r.add_argument("--all-confidence", action="store_true")
    return parser


def _fail(message: str, code: int = 1) -> int:
    print(message, file=sys.stderr)
    return code


def _kb_error(exc: KBError) -> int:
    return _fail(f"{exc.file}: {exc.entry_id + ': ' if exc.entry_id else ''}{exc.message}")


def _validate_kb(args) -> int:
    try:
        load_kb(
            Path(args.kb),
            verified_only=args.verified_only,
            require_review=args.require_review,
        )
    except KBError as exc:
        return _kb_error(exc)
    print("Base de connaissances valide.")
    return 0


def _report(args) -> int:
    kb_dir, facts, out = Path(args.kb), Path(args.facts), Path(args.out)
    if not kb_dir.is_dir():
        return _fail(f"Base de connaissances introuvable : {kb_dir}")
    try:
        data = facts.read_bytes()
    except OSError as exc:
        return _fail(f"Fichier d'audit illisible : {facts} ({exc.strerror})")
    try:
        state = load_audit_state(data)
    except OutOfScopeError as exc:
        return _fail(str(exc), 2)
    except ValidationError:
        return _fail(f"Fichier d'audit invalide : {facts}")
    try:
        kb = load_kb(kb_dir, verified_only=not args.all_confidence)
    except KBError as exc:
        return _kb_error(exc)
    try:
        validate_state(state, kb)
    except FactValidationError as exc:
        return _fail(f"Fichier d'audit incohérent avec la base de connaissances : {exc}")

    today = args.today or date.today()
    report = build_report(state, diagnose(state, kb, today), kb, today)
    violations = check_report(report, state, kb)
    if violations:
        for violation in violations:
            print(violation, file=sys.stderr)
        return 3
    try:
        out.write_text(render_html(report), encoding="utf-8")
    except OSError as exc:
        return _fail(f"Écriture impossible : {out} ({exc.strerror})")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    return _validate_kb(args) if args.command == "validate-kb" else _report(args)


if __name__ == "__main__":
    sys.exit(main())
