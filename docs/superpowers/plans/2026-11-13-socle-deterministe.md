# Socle déterministe d'audit-ia — plan de réalisation (plan 1 sur 6)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**But :** à partir d'un fichier de faits d'audit, produire un rapport HTML traçable, sans aucun modèle de langage ni service externe.

**Architecture :** une base de connaissances en fichiers YAML versionnés, validée au chargement ; un état d'audit fait de faits typés à trois niveaux de certitude ; un moteur de diagnostic en logique à trois valeurs qui en déduit constats, obligations, repères, aides, actions et vérifications ; un rapport structuré dont chaque ligne renvoie à un fait ou à une entrée de la base.

**Pile :** Python 3.12, pydantic 2, PyYAML, Jinja2, pytest. Aucune dépendance réseau.

**Spécification :** `docs/superpowers/specs/2026-11-13-audit-ia-design.md`

## Découpage en six plans

La spécification couvre plusieurs sous-systèmes indépendants. Chacun fait l'objet d'un plan qui livre un logiciel testable seul.

| Plan | Livre | Dépend de |
|---|---|---|
| **1. Socle déterministe** (ce document) | Base de connaissances, diagnostic, rapport HTML, en ligne de commande | — |
| 2. Entretien en mode texte | Conducteur et extracteur sur Mistral Large 4, dialogue au clavier | Plan 1 ; vérification de Mistral Large 4 |
| 3. Couche vocale | Voxtral et orchestrateur, audio en flux jamais écrit sur disque | Plan 2 ; vérification de Voxtral |
| 4. Interface web | Parcours complet dans le navigateur (Next.js), bilan corrigeable, PDF | Plans 2 et 3 |
| 5. Hébergement et confidentialité | Déploiement Scaleway, consentements, suppression, analyse d'impact | Plan 4 |
| 6. Campagne de démonstration | Entretiens avec les décideurs, retours des builders, dossier Bpifrance | Plan 5 |

Le plan 1 ne dépend d'aucune des vérifications techniques encore ouvertes (Voxtral, Mistral Large 4, Scaleway). Les plans 2 à 6 seront rédigés un par un, chacun après la livraison du précédent.

## Contraintes globales

- Aucune règle, échéance, aide ou repère chiffré n'est affiché sans sa source, sa date et son niveau de confiance.
- Les modèles de langage ne décident ni du droit applicable, ni des chiffres, ni des aides : dans ce plan, il n'y en a aucun.
- Base de connaissances du démonstrateur limitée aux entrées de confiance `V` et `V2`.
- Entreprises de 1 à 249 salariés.
- Sept dimensions, quatre stades, trois niveaux de certitude (`constate`, `estime`, `inconnu`).
- Le rapport ne nomme aucun prestataire ni éditeur ; TCKC n'y apparaît pas.
- Une entrée périmée ou non revérifiée est signalée dans le rapport, jamais masquée.
- Aucune extrapolation : ce que le corpus ne mesure pas n'est pas chiffré.
- Identifiants de code en anglais, valeurs métier et textes affichés en français.
- Code sous EUPL 1.2, base de connaissances sous Licence Ouverte 2.0.

## Points de vigilance

Cinq situations que la spécification implique sans les décrire, de la plus probable à la moins probable. Chacune a son test dans la tâche indiquée.

1. **Audit presque vide** (le décideur ne sait presque rien) : le rapport est produit, sans constat inventé, avec la liste des vérifications à mener. Tâche 4.
2. **Entrée de la base périmée** (règle revérifiée il y a plus de 180 jours, repère au-delà de sa date de péremption) : elle reste affichée avec la mention « à revérifier ». Tâches 2 et 6.
3. **Aucun repère pour le segment** (secteur absent des enquêtes) : le rapport le dit, et n'affiche jamais un repère d'un autre périmètre à la place. Tâche 4.
4. **Profil hors périmètre** (0 salarié, 250 et plus) : refus explicite avec le périmètre du démonstrateur, pas de rapport dégradé. Tâche 1.
5. **Base incohérente** (identifiant en double, condition citant un fait inexistant, source manquante) : le chargement échoue en nommant le fichier et l'entrée. Tâche 2.

---

## Arborescence

```
pyproject.toml
kb/
  sources.yaml  facts.yaml  rules.yaml  benchmarks.yaml  problems.yaml
  use_cases.yaml  actions.yaml  aids.yaml  neutrality.yaml  VERSION
src/audit_ia/
  audit/models.py        profil, faits, état d'audit
  audit/planner.py       prochain fait à recueillir
  kb/models.py           objets de la base
  kb/loader.py           chargement et validation croisée
  kb/freshness.py        péremption
  diagnostic/conditions.py   logique à trois valeurs
  diagnostic/engine.py       diagnostic
  report/build.py        rapport structuré
  report/check.py        traçabilité et neutralité
  report/render.py       HTML
  report/templates/report.html.j2
  cli.py
tests/
  (un fichier de test par module)
  fixtures/kb_min/       petite base de test
  fixtures/audits/       trois audits de référence
```

---

### Task 1: projet et modèle d'audit

**Fichiers**
- Créer : `pyproject.toml`, `src/audit_ia/__init__.py`, `src/audit_ia/audit/__init__.py`, `src/audit_ia/audit/models.py`
- Test : `tests/audit/test_models.py`

**Interfaces — produit**

```python
class Stage(StrEnum):       # non_utilisatrice, usage_individuel, usage_outille, processus_transforme
class Dimension(StrEnum):   # strategie, gouvernance, donnees, si, securite, competences, valeur
class Certainty(StrEnum):   # constate, estime, inconnu

class CompanyProfile(BaseModel):
    headcount: int          # 1..249
    sector: str             # clé de secteur, ex. "construction"
    stage: Stage
    respondent_role: str

class Fact(BaseModel):
    fact_id: str
    value: bool | int | float | str | None
    certainty: Certainty
    quote: str | None = None    # extrait de l'entretien

class AuditState(BaseModel):
    profile: CompanyProfile
    facts: dict[str, Fact] = {}
    def record(self, fact: Fact) -> None    # remplace le fait de même fact_id

class OutOfScopeError(ValueError)
```

- [ ] **Étape 1 : écrire les tests qui échouent**

```python
def test_headcount_bounds():
    for n in (0, 250):
        with pytest.raises(OutOfScopeError) as e:
            CompanyProfile(headcount=n, sector="construction",
                           stage="usage_individuel", respondent_role="dirigeant")
        assert "1 à 249 salariés" in str(e.value)

def test_unknown_fact_has_no_value():
    with pytest.raises(ValidationError):
        Fact(fact_id="x", value=True, certainty="inconnu")
    with pytest.raises(ValidationError):
        Fact(fact_id="x", value=None, certainty="constate")

def test_record_replaces():
    s = AuditState(profile=PROFILE)
    s.record(Fact(fact_id="a", value=1, certainty="estime"))
    s.record(Fact(fact_id="a", value=2, certainty="constate"))
    assert s.facts["a"].value == 2

def test_state_roundtrips_json():
    assert AuditState.model_validate_json(STATE.model_dump_json()) == STATE
```

- [ ] **Étape 2 : lancer** `pytest tests/audit -v` — attendu : échec à l'import.
- [ ] **Étape 3 : écrire `pyproject.toml`** (paquet `audit_ia` sous `src/`, `requires-python = ">=3.12"`, dépendances `pydantic>=2`, `pyyaml`, `jinja2`, extra `dev` avec `pytest`, script `audit-ia = "audit_ia.cli:main"`) **et les modèles ci-dessus.** `value is None` si et seulement si `certainty == inconnu`. `OutOfScopeError` est levée par un validateur de `headcount`.
- [ ] **Étape 4 : lancer** `pip install -e ".[dev]" && pytest tests/audit -v` — attendu : 4 réussites.
- [ ] **Étape 5 : commit** `feat: modèle d'audit (profil, faits, certitude)`

---

### Task 2: base de connaissances, chargement et péremption

**Fichiers**
- Créer : `src/audit_ia/kb/models.py`, `src/audit_ia/kb/loader.py`, `src/audit_ia/kb/freshness.py`, `tests/fixtures/kb_min/*.yaml`
- Test : `tests/kb/test_loader.py`, `tests/kb/test_freshness.py`

**Interfaces — consomme** `Stage`, `Dimension` (tâche 1).

**Interfaces — produit**

```python
class Confidence(StrEnum):   # V, V2, A, B, C
class RuleStatus(StrEnum):   # applicable, adopte_non_applicable, projet, proposition, recommandation, jurisprudence
class Horizon(StrEnum):      # j30, j90, m12

class Source(BaseModel):      id; title; publisher; url; published_on: date | None
class Provenance(BaseModel):  source_id: str; verified_on: date | None; confidence: Confidence; human_reviewed: bool = False

# Condition : arbre récursif
class Test(BaseModel):  fact: str; op: Literal["eq","ne","lt","lte","gt","gte","in"]; value: Any
class All(BaseModel):   all: list[Condition]
class AnyOf(BaseModel): any: list[Condition]
class Not(BaseModel):   not_: Condition          # alias YAML "not"
Condition = Test | All | AnyOf | Not

class FactDef(BaseModel):   id; dimension: Dimension; kind: Literal["bool","int","float","enum","text"]
                            choices: list[str] | None; prompt_hint: str
                            stages: list[Stage] = []    # vide = tous les stades
                            priority: int = 0
class Rule(BaseModel):      id; statement; status: RuleStatus; effective_on: date | None
                            bounds: str | None; applies_when: Condition | None; provenance: Provenance
class Benchmark(BaseModel): id; indicator; value: str; headcount_min: int | None; headcount_max: int | None
                            sectors: list[str] = []     # vide = tous secteurs
                            population: str; fieldwork: str; expires_on: date; provenance: Provenance
class Problem(BaseModel):   id; symptom; dimension: Dimension; triggers: Condition
                            evidence_benchmark_ids: list[str] = []; action_ids: list[str] = []
class UseCase(BaseModel):   id; function; title; prerequisites: list[str]; obstacles: list[str]
                            risks: list[str]; first_step: str; applies_when: Condition | None; priority: int = 0
class Action(BaseModel):    id; title; horizon: Horizon; effort: Literal["faible","moyen","fort"]
                            prerequisites: list[str] = []; success_check: str
class Aid(BaseModel):       id; name; eligibility: Condition | None; headcount_min: int | None
                            headcount_max: int | None; amount: str; provenance: Provenance

class KnowledgeBase(BaseModel):
    version: str
    sources: dict[str, Source]; facts: dict[str, FactDef]; rules: dict[str, Rule]
    benchmarks: dict[str, Benchmark]; problems: dict[str, Problem]; use_cases: dict[str, UseCase]
    actions: dict[str, Action]; aids: dict[str, Aid]; forbidden_terms: list[str]

class KBError(Exception):    file: str; entry_id: str | None; message: str

def load_kb(root: Path, *, verified_only: bool = False, require_review: bool = False) -> KnowledgeBase
def referenced_facts(cond: Condition) -> set[str]        # dans kb/models.py

RULE_MAX_AGE_DAYS = 180
def is_stale(entry: Rule | Benchmark | Aid, today: date) -> bool
```

Un fichier YAML par type, chacun une liste d'entrées ; `VERSION` contient la version de la base ; `neutrality.yaml` contient `forbidden_terms`. Les identifiants de `Problem` respectent `^(HUM|DAT|SI|GEN|CYB|COU|ENV|FON)-[A-Z0-9]+$`.

- [ ] **Étape 1 : écrire `tests/fixtures/kb_min/`** : une base valide minimale (2 sources, 4 faits, 2 règles, 2 repères, 2 problèmes, 1 cas d'usage, 2 actions, 1 aide), dont une règle de confiance `B`.
- [ ] **Étape 2 : écrire les tests qui échouent**

```python
def test_loads_minimal_kb():
    kb = load_kb(KB_MIN)
    assert set(kb.rules) == {"regle-a", "regle-b"} and kb.version == "test"

def test_verified_only_drops_unverified():
    assert set(load_kb(KB_MIN, verified_only=True).rules) == {"regle-a"}

def test_require_review_fails_on_unreviewed():
    with pytest.raises(KBError) as e:
        load_kb(KB_MIN, require_review=True)
    assert e.value.file == "rules.yaml" and e.value.entry_id == "regle-a"

@pytest.mark.parametrize("mutation, file, entry_id", [
    ("duplicate_rule_id",        "rules.yaml",      "regle-a"),
    ("condition_unknown_fact",   "problems.yaml",   "HUM-S1"),
    ("unknown_source",           "benchmarks.yaml", "repere-a"),
    ("problem_unknown_action",   "problems.yaml",   "HUM-S1"),
    ("problem_unknown_benchmark","problems.yaml",   "HUM-S1"),
    ("bad_problem_id",           "problems.yaml",   "hum_s1"),
    ("verified_without_date",    "rules.yaml",      "regle-a"),   # confiance V ou V2 sans verified_on
])
def test_incoherent_kb_names_file_and_entry(tmp_path, mutation, file, entry_id):
    root = mutated_copy(KB_MIN, tmp_path, mutation)
    with pytest.raises(KBError) as e:
        load_kb(root)
    assert (e.value.file, e.value.entry_id) == (file, entry_id)

def test_verified_only_fails_if_dependency_dropped(tmp_path):
    # un problème dont le repère de preuve est de confiance B
    with pytest.raises(KBError):
        load_kb(mutated_copy(KB_MIN, tmp_path, "evidence_is_unverified"), verified_only=True)

def test_staleness():
    today = date(2026, 11, 13)
    assert is_stale(rule(verified_on=date(2026, 5, 16)), today)       # 181 jours
    assert not is_stale(rule(verified_on=date(2026, 5, 17)), today)   # 180 jours
    assert is_stale(rule(verified_on=None), today)
    assert is_stale(benchmark(expires_on=date(2026, 11, 12)), today)
    assert not is_stale(benchmark(expires_on=date(2026, 11, 13)), today)
```

- [ ] **Étape 3 : lancer** `pytest tests/kb -v` — attendu : échec à l'import.
- [ ] **Étape 4 : écrire modèles, `load_kb`, `referenced_facts`, `is_stale`.** `load_kb` lit chaque fichier, valide chaque entrée, puis fait les contrôles croisés dans l'ordre du tableau paramétré. Un repère est périmé après `expires_on` ou si sa vérification dépasse `RULE_MAX_AGE_DAYS` ; une règle ou une aide, sur la seule ancienneté de `verified_on`.
- [ ] **Étape 5 : lancer** `pytest tests/kb -v` — attendu : tout passe.
- [ ] **Étape 6 : commit** `feat: base de connaissances, validation croisée, péremption`

---

### Task 3: conditions à trois valeurs

**Fichiers**
- Créer : `src/audit_ia/diagnostic/__init__.py`, `src/audit_ia/diagnostic/conditions.py`
- Test : `tests/diagnostic/test_conditions.py`

**Interfaces — consomme** `Condition`, `Test`, `All`, `AnyOf`, `Not` (tâche 2) ; `Fact`, `Certainty` (tâche 1).

**Interfaces — produit**

```python
class Tri(Enum):   TRUE, FALSE, UNKNOWN
def evaluate(cond: Condition, facts: Mapping[str, Fact]) -> Tri
def undecided_facts(cond: Condition, facts: Mapping[str, Fact]) -> set[str]
    # faits absents ou « inconnu » qui empêchent de trancher ; vide si le résultat n'est pas UNKNOWN
```

Un fait absent ou de certitude `inconnu` rend son `Test` `UNKNOWN`. `All`, `AnyOf` et `Not` suivent la logique de Kleene : `All` est `FALSE` dès qu'une branche est `FALSE`, même si une autre est `UNKNOWN`.

- [ ] **Étape 1 : écrire les tests qui échouent**

```python
T, F, U = Tri.TRUE, Tri.FALSE, Tri.UNKNOWN

def test_ops():
    f = facts(n=("constate", 12), s=("estime", "sage"))
    assert evaluate(Test(fact="n", op="gte", value=10), f) is T
    assert evaluate(Test(fact="n", op="lt", value=10), f) is F
    assert evaluate(Test(fact="s", op="in", value=["sage", "ebp"]), f) is T

def test_missing_and_unknown_are_unknown():
    f = facts(a=("inconnu", None))
    assert evaluate(Test(fact="a", op="eq", value=True), f) is U
    assert evaluate(Test(fact="absent", op="eq", value=True), f) is U

@pytest.mark.parametrize("left, right, all_, any_", [
    (T, U, U, T), (F, U, F, U), (U, U, U, U), (T, F, F, T),
])
def test_kleene(left, right, all_, any_):
    f, a, b = facts_for(left, right)          # deux tests dont les résultats valent left et right
    assert evaluate(All(all=[a, b]), f) is all_ and evaluate(All(all=[b, a]), f) is all_
    assert evaluate(AnyOf(any=[a, b]), f) is any_ and evaluate(AnyOf(any=[b, a]), f) is any_

def test_not():
    f, a, b = facts_for(T, U)
    assert evaluate(Not(not_=a), f) is F and evaluate(Not(not_=b), f) is U

def test_undecided_facts():
    c = All(all=[Test(fact="a", op="eq", value=True), Test(fact="b", op="eq", value=True)])
    assert undecided_facts(c, facts(a=("constate", True))) == {"b"}
    assert undecided_facts(c, facts(a=("constate", False))) == set()   # déjà FALSE

def test_type_mismatch_is_unknown():
    assert evaluate(Test(fact="s", op="gt", value=3), facts(s=("constate", "texte"))) is U
```

- [ ] **Étape 2 : lancer** `pytest tests/diagnostic/test_conditions.py -v` — attendu : échec.
- [ ] **Étape 3 : écrire `evaluate` et `undecided_facts`.**
- [ ] **Étape 4 : relancer** — attendu : tout passe.
- [ ] **Étape 5 : commit** `feat: évaluation des conditions en logique à trois valeurs`

---

### Task 4: moteur de diagnostic

**Fichiers**
- Créer : `src/audit_ia/diagnostic/engine.py`
- Test : `tests/diagnostic/test_engine.py`

**Interfaces — consomme** `AuditState` (tâche 1) ; `KnowledgeBase`, `is_stale` (tâche 2) ; `evaluate`, `undecided_facts`, `Tri` (tâche 3).

**Interfaces — produit**

```python
class Finding(BaseModel):       problem_id: str; fact_ids: list[str]; certainty: Certainty
class RuleHit(BaseModel):       rule_id: str; timing: Literal["applicable","a_venir","en_projet","reference"]; stale: bool
class BenchmarkHit(BaseModel):  benchmark_id: str; stale: bool
class AidHit(BaseModel):        aid_id: str; stale: bool
class Verification(BaseModel):  fact_id: str; blocks: list[str]     # identifiants des problèmes, règles, aides non tranchés
class Diagnosis(BaseModel):
    findings: list[Finding]; rules: list[RuleHit]; benchmarks: list[BenchmarkHit]
    aids: list[AidHit]; action_ids: list[str]; use_case_ids: list[str]
    verifications: list[Verification]; indicators_without_benchmark: list[str]

MAX_USE_CASES = 5
def diagnose(state: AuditState, kb: KnowledgeBase, today: date) -> Diagnosis
```

Règles de décision :

- **Constat** : `triggers` vaut `TRUE`. `fact_ids` = faits cités par la condition et présents. `certainty` = `estime` si l'un d'eux est estimé, sinon `constate`.
- **Règle** : retenue si `applies_when` est absent ou `TRUE`. `timing` : `en_projet` pour les statuts `projet` et `proposition` ; `reference` pour `recommandation` et `jurisprudence` ; pour `applicable` et `adopte_non_applicable`, `a_venir` si `effective_on` est futur, `applicable` sinon (une règle adoptée dont la date d'effet est passée devient applicable sans attendre la mise à jour de la base).
- **Repère** : effectif dans `[headcount_min, headcount_max]` (borne nulle = ouverte) et secteur compatible. Pour un même `indicator`, le repère sectoriel remplace le repère tous secteurs. Un `indicator` présent dans la base mais sans repère compatible va dans `indicators_without_benchmark`.
- **Aide** : effectif dans les bornes et `eligibility` absente ou `TRUE`.
- **Actions** : union des `action_ids` des constats, sans doublon, dans l'ordre des constats.
- **Cas d'usage** : `applies_when` absent ou `TRUE`, triés par `priority` décroissante puis `id`, au plus `MAX_USE_CASES`.
- **Vérification** : pour chaque condition évaluée à `UNKNOWN`, chaque fait de `undecided_facts` ; une ligne par fait, `blocks` regroupant ce qu'il bloque.
- Toutes les listes sont triées par identifiant, sauf actions et cas d'usage.

- [ ] **Étape 1 : écrire les tests qui échouent**, sur `kb_min`

```python
def test_finding_with_estimated_fact():
    d = diagnose(state(comptes_perso=("estime", True)), KB, TODAY)
    assert d.findings == [Finding(problem_id="HUM-S1", fact_ids=["comptes_perso"], certainty="estime")]
    assert d.action_ids == ["action-outil-officiel"]

def test_empty_audit_invents_nothing():
    d = diagnose(state(), KB, TODAY)
    assert d.findings == [] and d.action_ids == []
    assert {v.fact_id for v in d.verifications} >= {"comptes_perso"}
    assert "HUM-S1" in next(v for v in d.verifications if v.fact_id == "comptes_perso").blocks

def test_rule_timing():
    d = diagnose(state(), KB, date(2026, 11, 13))
    assert timing(d, "regle-a") == "applicable"     # effective_on 2025-02-02
    assert timing(d, "regle-b") == "a_venir"        # adopte_non_applicable, 2027-12-02
    assert timing(diagnose(state(), KB, date(2027, 12, 2)), "regle-b") == "applicable"

def test_stale_entries_are_kept_and_flagged():
    d = diagnose(state(), KB, date(2027, 12, 1))
    assert all(h.stale for h in d.rules) and len(d.rules) == 2

def test_sector_benchmark_replaces_generic():
    d = diagnose(state(sector="construction"), KB, TODAY)
    assert [h.benchmark_id for h in d.benchmarks] == ["repere-construction"]

def test_no_benchmark_for_segment_is_reported():
    d = diagnose(state(headcount=5, sector="peche"), KB_SECTOR_ONLY, TODAY)
    assert d.benchmarks == [] and d.indicators_without_benchmark == ["adoption"]

def test_use_cases_capped_and_ordered():
    d = diagnose(state(), KB_MANY_USE_CASES, TODAY)
    assert len(d.use_case_ids) == 5 and d.use_case_ids[0] == "cas-priorite-9"

def test_aid_headcount_bounds():
    assert aids(diagnose(state(headcount=9), KB, TODAY)) == []          # aide 10..249
    assert aids(diagnose(state(headcount=10), KB, TODAY)) == ["aide-a"]

def test_diagnosis_is_deterministic():
    assert diagnose(S, KB, TODAY) == diagnose(S, KB, TODAY)
```

- [ ] **Étape 2 : lancer** `pytest tests/diagnostic/test_engine.py -v` — attendu : échec.
- [ ] **Étape 3 : écrire `diagnose`** selon les règles de décision ci-dessus.
- [ ] **Étape 4 : relancer** — attendu : tout passe.
- [ ] **Étape 5 : commit** `feat: moteur de diagnostic`

---

### Task 5: planificateur d'entretien

**Fichiers**
- Créer : `src/audit_ia/audit/planner.py`
- Test : `tests/audit/test_planner.py`

**Interfaces — consomme** `AuditState`, `Dimension` (tâche 1) ; `KnowledgeBase`, `FactDef` (tâche 2).

**Interfaces — produit**

```python
MIN_FACTS_PER_DIMENSION = 3
class Objective(BaseModel):   fact_id: str; dimension: Dimension
def next_objective(state: AuditState, kb: KnowledgeBase, *, asked: frozenset[str] = frozenset()) -> Objective | None
def coverage(state: AuditState, kb: KnowledgeBase) -> dict[Dimension, int]   # faits recueillis, « inconnu » compris
```

Candidats : faits de la base ni recueillis ni dans `asked`, dont `stages` est vide ou contient le stade du profil. Choix : dimension la moins couverte (ordre de l'énumération en cas d'égalité), puis `priority` décroissante, puis `id`. Retourne `None` quand il n'y a plus de candidat ou quand toutes les dimensions qui ont encore des candidats atteignent `MIN_FACTS_PER_DIMENSION`.

- [ ] **Étape 1 : écrire les tests qui échouent**

```python
def test_starts_with_least_covered_dimension_in_enum_order():
    assert next_objective(state(), KB).dimension == Dimension.STRATEGIE

def test_skips_facts_of_other_stages():
    # "automatisation.validation_humaine" est réservé au stade processus_transforme
    ids = all_objectives(state(stage="non_utilisatrice"), KB)
    assert "automatisation.validation_humaine" not in ids

def test_unknown_answer_counts_as_covered():
    s = state(); s.record(Fact(fact_id="f1", value=None, certainty="inconnu"))
    assert coverage(s, KB)[Dimension.STRATEGIE] == 1

def test_asked_but_unanswered_is_not_asked_again():
    first = next_objective(state(), KB)
    assert next_objective(state(), KB, asked=frozenset({first.fact_id})).fact_id != first.fact_id

def test_stops_when_every_dimension_is_covered():
    assert next_objective(fully_covered_state(KB), KB) is None

def test_terminates():
    assert len(all_objectives(state(), KB)) <= len(KB.facts)
```

- [ ] **Étape 2 : lancer** `pytest tests/audit/test_planner.py -v` — attendu : échec.
- [ ] **Étape 3 : écrire `coverage` et `next_objective`.**
- [ ] **Étape 4 : relancer** — attendu : tout passe.
- [ ] **Étape 5 : commit** `feat: planificateur d'entretien`

---

### Task 6: rapport structuré, traçabilité et neutralité

**Fichiers**
- Créer : `src/audit_ia/report/__init__.py`, `src/audit_ia/report/build.py`, `src/audit_ia/report/check.py`
- Test : `tests/report/test_build.py`, `tests/report/test_check.py`

**Interfaces — consomme** `AuditState` (tâche 1) ; `KnowledgeBase`, `Horizon` (tâche 2) ; `Diagnosis` (tâche 4).

**Interfaces — produit**

```python
class Ref(BaseModel):         kind: Literal["fact","rule","benchmark","problem","use_case","action","aid"]; id: str
class SourceLine(BaseModel):  source_id: str; title: str; publisher: str; url: str
                              verified_on: date | None; confidence: Confidence; stale: bool
class ReportItem(BaseModel):  text: str; refs: list[Ref]; sources: list[SourceLine] = []; note: str | None = None
class Report(BaseModel):
    kb_version: str; generated_on: date; profile: CompanyProfile
    summary: list[ReportItem]
    by_dimension: dict[Dimension, list[ReportItem]]      # les sept clés toujours présentes
    use_cases: list[ReportItem]
    obligations: list[ReportItem]; upcoming: list[ReportItem]; watch: list[ReportItem]
    plan: dict[Horizon, list[ReportItem]]                # les trois clés toujours présentes
    verifications: list[ReportItem]
    aids: list[ReportItem]
    not_measured: list[str]
    sources: list[SourceLine]                            # annexe, dédoublonnée, triée par source_id

STALE_NOTE = "À revérifier : cette information n'a pas été recontrôlée récemment."
ESTIMATED_NOTE = "Fondé sur une estimation du décideur, à confirmer."

def build_report(state: AuditState, diagnosis: Diagnosis, kb: KnowledgeBase, today: date) -> Report
def check_report(report: Report, state: AuditState, kb: KnowledgeBase) -> list[str]   # violations ; vide = conforme
```

Construction :

- `by_dimension` : un élément par constat (texte = `symptom`), `note = ESTIMATED_NOTE` si le constat est estimé ; ses repères de preuve retenus par le diagnostic figurent dans `sources`. Une dimension sans constat reçoit un seul élément « Aucun constat établi sur cette dimension. », sans référence.
- `obligations`, `upcoming`, `watch` : règles de `timing` `applicable`, `a_venir`, puis `en_projet` et `reference`. Le texte d'une règle à venir contient sa date d'effet au format `2 décembre 2027`.
- `plan` : actions réparties par `horizon`.
- `verifications` : texte = `prompt_hint` du fait.
- `not_measured` : un texte par `indicators_without_benchmark`, « Aucun repère publié pour votre taille et votre secteur sur : … ».
- `summary` : quatre éléments, dans l'ordre : nombre de constats par dimension ; premier cas d'usage ; nombre d'obligations applicables et d'échéances à venir ; nombre de vérifications à mener.
- Toute entrée périmée porte `note = STALE_NOTE` et `stale = True` sur sa ligne de source.

`check_report` signale : une référence inexistante dans l'état ou la base ; un élément issu d'une règle, d'un repère ou d'une aide sans ligne de source ; une ligne de source sans URL ; un `text` ou `note` contenant un terme de `kb.forbidden_terms` (insensible à la casse) ; une clé manquante dans `by_dimension` ou `plan`.

- [ ] **Étape 1 : écrire les tests qui échouent**

```python
def test_sections_always_present():
    r = build_report(state(), diagnose(state(), KB, TODAY), KB, TODAY)
    assert set(r.by_dimension) == set(Dimension) and set(r.plan) == set(Horizon)

def test_empty_audit_report():
    r = report_for(state())
    assert all(len(v) == 1 and v[0].refs == [] for v in r.by_dimension.values())
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
    for item in r.obligations + r.upcoming + r.aids:
        assert item.sources and all(s.url and s.confidence for s in item.sources)

def test_no_benchmark_statement():
    assert report_for(state(sector="peche"), kb=KB_SECTOR_ONLY).not_measured

def test_check_catches_dangling_ref():
    r = report_for(S_FULL); r.obligations[0].refs.append(Ref(kind="rule", id="absente"))
    assert any("absente" in v for v in check_report(r, S_FULL, KB))

def test_check_catches_forbidden_term():
    r = report_for(S_FULL); r.summary[0].text += " Contactez tckc."
    assert any("tckc" in v.lower() for v in check_report(r, S_FULL, KB))    # terme interdit : "TCKC"

def test_built_report_is_always_clean():
    for s in (state(), S_FULL):
        assert check_report(report_for(s), s, KB) == []
```

- [ ] **Étape 2 : lancer** `pytest tests/report -v` — attendu : échec.
- [ ] **Étape 3 : écrire `build_report` et `check_report`.** Les dates sont formatées en français sans dépendre de la locale du système.
- [ ] **Étape 4 : relancer** — attendu : tout passe.
- [ ] **Étape 5 : commit** `feat: rapport structuré, contrôle de traçabilité et de neutralité`

---

### Task 7: rendu HTML et ligne de commande

**Fichiers**
- Créer : `src/audit_ia/report/render.py`, `src/audit_ia/report/templates/report.html.j2`, `src/audit_ia/cli.py`
- Test : `tests/report/test_render.py`, `tests/test_cli.py`

**Interfaces — consomme** `Report`, `build_report`, `check_report` (tâche 6) ; `load_kb` (tâche 2) ; `diagnose` (tâche 4) ; `AuditState` (tâche 1).

**Interfaces — produit**

```python
def render_html(report: Report) -> str        # document HTML autonome, lang="fr", sans ressource externe
def main(argv: list[str] | None = None) -> int
```

```
audit-ia validate-kb [--kb kb] [--verified-only] [--require-review]
audit-ia report --facts audit.json --out rapport.html [--kb kb] [--today AAAA-MM-JJ] [--all-confidence]
```

`report` charge la base avec `verified_only=True` sauf si `--all-confidence`. Codes de sortie : 0 succès ; 1 base invalide (message `fichier: entrée: raison` sur stderr) ; 2 profil hors périmètre ; 3 `check_report` non vide (les violations sur stderr, aucun fichier écrit).

Ordre des sections du document : synthèse ; bilan par dimension ; cas d'usage prioritaires ; obligations et échéances ; plan d'action (30 jours, 90 jours, 12 mois) ; vérifications à mener ; aides et dispositifs ; ce qui n'est pas mesuré ; sources. Chaque ligne de source affiche éditeur, titre en lien, date de vérification et niveau de confiance. Le pied de page affiche la version de la base et la date de génération.

- [ ] **Étape 1 : écrire les tests qui échouent**

```python
def test_html_sections_in_order():
    html = render_html(report_for(S_FULL))
    titles = ["Synthèse", "Bilan par dimension", "Cas d'usage prioritaires", "Obligations et échéances",
              "Plan d'action", "Vérifications à mener", "Aides et dispositifs", "Sources"]
    assert [html.index(t) for t in titles] == sorted(html.index(t) for t in titles)

def test_html_escapes_quotes_from_interview():
    s = state(); s.record(Fact(fact_id="f1", value="<script>x</script>", certainty="constate"))
    assert "<script>x" not in render_html(report_for(s))

def test_html_has_no_external_resource():
    html = render_html(report_for(S_FULL))
    assert "<link" not in html and "src=" not in html

def test_html_shows_source_metadata():
    html = render_html(report_for(S_FULL))
    assert "Vérifié le" in html and "V2" in html and "Base de connaissances test" in html

def test_cli_report_writes_file(tmp_path):
    out = tmp_path / "r.html"
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(AUDIT_JSON), "--out", str(out),
                 "--today", "2026-11-13", "--all-confidence"]) == 0
    assert out.read_text(encoding="utf-8").startswith("<!doctype html>")

def test_cli_exit_codes(tmp_path, capsys):
    assert main(["validate-kb", "--kb", str(BROKEN_KB)]) == 1
    assert "rules.yaml: regle-a:" in capsys.readouterr().err
    assert main(["report", "--kb", str(KB_MIN), "--facts", str(AUDIT_250), "--out", str(tmp_path / "x")]) == 2
    assert not (tmp_path / "x").exists()
```

- [ ] **Étape 2 : lancer** `pytest tests/report/test_render.py tests/test_cli.py -v` — attendu : échec.
- [ ] **Étape 3 : écrire le gabarit, `render_html` et `main`.** Jinja2 avec échappement automatique ; feuille de style incluse dans le document.
- [ ] **Étape 4 : relancer** — attendu : tout passe.
- [ ] **Étape 5 : commit** `feat: rendu HTML et ligne de commande`

---

### Task 8: base de connaissances initiale et audits de référence

**Fichiers**
- Créer : `kb/VERSION`, `kb/sources.yaml`, `kb/facts.yaml`, `kb/rules.yaml`, `kb/benchmarks.yaml`, `kb/problems.yaml`, `kb/use_cases.yaml`, `kb/actions.yaml`, `kb/aids.yaml`, `kb/neutrality.yaml`, `kb/README.md`
- Créer : `tests/fixtures/audits/tpe_non_utilisatrice.json`, `pme_usage_individuel.json`, `pme_usage_outille.json`
- Test : `tests/test_kb_initiale.py`, `tests/test_bout_en_bout.py`
- Modifier : `README.md` (état, arborescence, journal)

**Interfaces — consomme** tout ce qui précède. **Ne produit** que des données.

**Origine de chaque fichier** — tout vient de `corpus/rapport-freins-ia-2026.md` ; une valeur n'entre que si le rapport la marque **[V]** ou **[V2]**, avec ce niveau reporté dans `confidence` et `verified_on: 2026-11-13`. `human_reviewed` vaut `false` partout : la relecture humaine est une étape distincte, hors de ce plan.

| Fichier | Section du rapport | Minimum |
|---|---|---|
| `rules.yaml` | Tableau des règles et échéances, section « Un cadre juridique en mouvement » | 10 règles |
| `benchmarks.yaml` | Tableau « Benchmarks réutilisables » | 15 repères |
| `problems.yaml` | Tableau « Catalogue de problèmes auditables », lignes dont la preuve est **[V]** ou **[V2]** | 15 problèmes |
| `aids.yaml` | Section « 35 000 entreprises sensibilisées, 70 diagnostics engagés » | 3 aides |
| `use_cases.yaml` | Section « Fonction par fonction », finance-comptabilité et ressources humaines-paie | 8 cas d'usage |
| `facts.yaml` | Faits nécessaires aux conditions ci-dessus | 40 faits, au moins 4 par dimension |
| `actions.yaml` | Une action au moins par problème | 20 actions, les trois horizons représentés |
| `neutrality.yaml` | — | `TCKC` et les noms d'éditeurs et de prestataires cités dans le corpus |

`expires_on` d'un repère : un an après la fin de son terrain d'enquête ; à défaut, un an après sa publication. `kb/VERSION` : `2026.11.0`. `kb/README.md` décrit le format de chaque fichier, la Licence Ouverte 2.0 et la règle « rien sans source, date et niveau de confiance ».

Secteurs : les clés de la ventilation Insee du rapport (`information_communication`, `activites_specialisees`, `industrie_manufacturiere`, `commerce`, `construction`, `transports`, et les autres secteurs qu'elle liste), plus `autre`.

- [ ] **Étape 1 : écrire les tests qui échouent**

```python
KB = load_kb(Path("kb"), verified_only=True)

def test_minimum_sizes():
    assert len(KB.rules) >= 10 and len(KB.benchmarks) >= 15 and len(KB.problems) >= 15
    assert len(KB.facts) >= 40 and len(KB.actions) >= 20 and len(KB.aids) >= 3 and len(KB.use_cases) >= 8

def test_every_dimension_has_facts_and_a_problem():
    for d in Dimension:
        assert sum(f.dimension == d for f in KB.facts.values()) >= 4
        assert any(p.dimension == d for p in KB.problems.values())

def test_only_verified_entries():
    for e in [*KB.rules.values(), *KB.benchmarks.values(), *KB.aids.values()]:
        assert e.provenance.confidence in ("V", "V2") and e.provenance.verified_on == date(2026, 11, 13)

def test_pinned_values_from_corpus():
    r = KB.rules["ai-act-annexe-iii"]
    assert (r.status, r.effective_on) == ("adopte_non_applicable", date(2027, 12, 2))
    assert KB.rules["ai-act-annexe-i"].effective_on == date(2028, 8, 2)
    assert KB.rules["ai-act-art-50-transparence"].effective_on == date(2026, 8, 2)
    assert KB.rules["facturation-electronique-reception"].effective_on == date(2026, 9, 1)
    assert KB.rules["facturation-electronique-emission-pme"].effective_on == date(2027, 9, 1)
    b = KB.benchmarks["insee-2025-adoption"]
    assert b.value.startswith("18 %") and b.headcount_min == 10
    assert KB.benchmarks["francenum-2026-adoption"].value.startswith("40 %")
    assert KB.benchmarks["bdf-2026-gain-productivite"].value.startswith("31 %")
    assert {"HUM-S1", "HUM-G2", "CYB-C4", "FON-RH"} <= set(KB.problems)

def test_diagnostic_data_ia_excludes_under_ten():
    a = KB.aids["diagnostic-data-ia"]
    assert a.headcount_min == 10 and "40 %" in a.amount

def test_every_problem_has_an_action():
    assert all(p.action_ids for p in KB.problems.values())

def test_no_forbidden_term_in_kb_texts():
    texts = [a.title for a in KB.actions.values()] + [u.title + u.first_step for u in KB.use_cases.values()]
    assert not [t for t in texts for w in KB.forbidden_terms if w.lower() in t.lower()]
```

```python
# tests/test_bout_en_bout.py
TODAY = date(2026, 11, 13)

@pytest.mark.parametrize("name", ["tpe_non_utilisatrice", "pme_usage_individuel", "pme_usage_outille"])
def test_reference_audit_produces_clean_report(name):
    state = AuditState.model_validate_json((AUDITS / f"{name}.json").read_text(encoding="utf-8"))
    report = build_report(state, diagnose(state, KB, TODAY), KB, TODAY)
    assert check_report(report, state, KB) == []
    assert render_html(report).startswith("<!doctype html>")

def test_pme_usage_individuel_expected_findings():
    d = diagnose(load("pme_usage_individuel"), KB, TODAY)
    assert {"HUM-S1", "CYB-C4"} <= {f.problem_id for f in d.findings}
    assert 3 <= len(d.use_case_ids) <= 5
    assert "diagnostic-data-ia" in {a.aid_id for a in d.aids}

def test_tpe_gets_no_diagnostic_data_ia():
    d = diagnose(load("tpe_non_utilisatrice"), KB, TODAY)      # 6 salariés
    assert "diagnostic-data-ia" not in {a.aid_id for a in d.aids}

def test_recruitment_screening_triggers_high_risk_deadline():
    d = diagnose(load("pme_usage_outille"), KB, TODAY)         # tri de candidatures par IA
    assert "FON-RH" in {f.problem_id for f in d.findings}
    assert ("ai-act-annexe-iii", "a_venir") in {(r.rule_id, r.timing) for r in d.rules}

def test_planner_covers_every_dimension_on_real_kb():
    assert {o.dimension for o in all_objectives(load("tpe_non_utilisatrice").model_copy(update={"facts": {}}), KB)} == set(Dimension)
```

Les trois audits de référence : une TPE de 6 salariés, secteur `construction`, non utilisatrice, dont la moitié des faits sont `inconnu` ; une PME de 45 salariés, `commerce`, usage individuel, comptes personnels estimés, aucune charte ; une PME de 120 salariés, `activites_specialisees`, usage outillé, tri de candidatures par IA sans analyse d'impact.

- [ ] **Étape 2 : lancer** `pytest tests/test_kb_initiale.py tests/test_bout_en_bout.py -v` — attendu : échec, la base n'existe pas.
- [ ] **Étape 3 : écrire les fichiers de la base** en suivant le tableau d'origine. Pour chaque entrée, copier la valeur et l'URL depuis la ligne du rapport, sans reformuler un chiffre. Si une valeur épinglée par un test n'est pas marquée **[V]** ou **[V2]** dans le rapport, s'arrêter et le signaler : ne modifier ni le test ni la donnée pour le faire passer.
- [ ] **Étape 4 : lancer** `audit-ia validate-kb --verified-only` — attendu : code 0.
- [ ] **Étape 5 : écrire les trois audits de référence, puis lancer** `pytest -v` — attendu : toute la suite passe.
- [ ] **Étape 6 : produire un rapport d'exemple** : `audit-ia report --facts tests/fixtures/audits/pme_usage_individuel.json --out /tmp/rapport.html --today 2026-11-13` — attendu : code 0 ; ouvrir le fichier et vérifier à l'œil que chaque obligation affiche sa source et sa date.
- [ ] **Étape 7 : mettre à jour `README.md`** (état du code, arborescence, commande d'exemple, ligne de journal) **et commit** `feat: base de connaissances initiale et audits de référence`

---

## Ce que ce plan ne fait pas

- Aucun texte rédigé par un modèle de langage : la synthèse est factuelle et sèche. La rédaction vient au plan 2.
- Pas de PDF : il vient avec l'interface, au plan 4.
- Pas de relecture humaine de la base : `--require-review` existe et échouera tant qu'elle n'est pas faite. Elle est obligatoire avant le plan 6.
- Pas de fichiers de licence : le texte officiel de l'EUPL 1.2 reste à copier depuis sa source.
- Pas d'entrée fondée sur les sources non lues (Journal officiel, Légifrance, jurisprudence sur le CSE, ANSSI) : elles n'entrent dans la base qu'après relecture humaine.
