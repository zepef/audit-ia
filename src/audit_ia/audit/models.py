"""Modèle de domaine de l'audit : profil, faits, certitude."""

from enum import StrEnum

from pydantic import BaseModel, ValidationError, field_validator, model_validator

HEADCOUNT_MIN = 1
HEADCOUNT_MAX = 249


class Stage(StrEnum):
    NON_UTILISATRICE = "non_utilisatrice"
    USAGE_INDIVIDUEL = "usage_individuel"
    USAGE_OUTILLE = "usage_outille"
    PROCESSUS_TRANSFORME = "processus_transforme"


class Dimension(StrEnum):
    STRATEGIE = "strategie"
    GOUVERNANCE = "gouvernance"
    DONNEES = "donnees"
    SI = "si"
    SECURITE = "securite"
    COMPETENCES = "competences"
    VALEUR = "valeur"


class Certainty(StrEnum):
    CONSTATE = "constate"
    ESTIME = "estime"
    INCONNU = "inconnu"


class OutOfScopeError(ValueError):
    """Entreprise hors du périmètre de l'audit."""


class CompanyProfile(BaseModel):
    """Profil de l'entreprise auditée (1 à 249 salariés).

    Le constructeur lève OutOfScopeError pour un effectif entier hors
    périmètre. Via model_validate / model_validate_json, ou avec une entrée
    non entière ("0", 250.0), pydantic lève une ValidationError : pour un
    refus cohérent quel que soit le mode de chargement, passer par
    load_audit_state.
    """

    headcount: int
    sector: str
    stage: Stage
    respondent_role: str

    def __init__(self, **data):
        # Pydantic encapsule les ValueError levées par un validateur dans une
        # ValidationError ; on contrôle donc l'effectif avant pour lever
        # OutOfScopeError telle quelle. Le validateur ci-dessous couvre
        # model_validate / model_validate_json.
        headcount = data.get("headcount")
        if isinstance(headcount, int) and not isinstance(headcount, bool):
            _check_headcount(headcount)
        super().__init__(**data)

    @field_validator("headcount")
    @classmethod
    def _headcount_in_scope(cls, value: int) -> int:
        return _check_headcount(value)


def _check_headcount(value: int) -> int:
    if not HEADCOUNT_MIN <= value <= HEADCOUNT_MAX:
        raise OutOfScopeError(
            f"Hors périmètre : l'audit couvre les entreprises de "
            f"1 à 249 salariés (effectif reçu : {value})."
        )
    return value


class Fact(BaseModel):
    fact_id: str
    value: bool | int | float | str | None
    certainty: Certainty
    quote: str | None = None

    @model_validator(mode="after")
    def _value_matches_certainty(self) -> "Fact":
        unknown = self.certainty == Certainty.INCONNU
        if unknown and self.value is not None:
            raise ValueError("un fait inconnu ne peut pas avoir de valeur")
        if not unknown and self.value is None:
            raise ValueError("un fait constaté ou estimé doit avoir une valeur")
        return self


class AuditState(BaseModel):
    profile: CompanyProfile
    facts: dict[str, Fact] = {}

    @model_validator(mode="after")
    def _keys_match_fact_ids(self) -> "AuditState":
        for key, fact in self.facts.items():
            if key != fact.fact_id:
                raise ValueError(
                    f"clé « {key} » différente de l'identifiant du fait « {fact.fact_id} »"
                )
        return self

    def record(self, fact: Fact) -> None:
        """Enregistre le fait, en remplaçant celui de même fact_id."""
        self.facts[fact.fact_id] = fact


def load_audit_state(data: str | bytes | dict) -> AuditState:
    """Charge un état d'audit depuis du JSON (texte ou octets) ou un dict.

    Point d'entrée unique pour relire un audit. Lève OutOfScopeError (message
    contenant « 1 à 249 salariés ») dès que l'effectif est hors périmètre,
    y compris pour des entrées coercées comme "0" ou 250.0. Toute autre
    erreur de validation (stade inconnu, JSON invalide...) lève la
    ValidationError de pydantic.
    """
    try:
        if isinstance(data, dict):
            return AuditState.model_validate(data)
        return AuditState.model_validate_json(data)
    except ValidationError as exc:
        for err in exc.errors():
            cause = (err.get("ctx") or {}).get("error")
            if isinstance(cause, OutOfScopeError):
                raise cause from None
        raise
