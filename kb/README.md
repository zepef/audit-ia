# Base de connaissances

Données consommées par le moteur de diagnostic d'`audit-ia`. Version : voir `VERSION` (`2026.11.0`).

## Règle unique : rien sans source, date et niveau de confiance

Chaque règle, repère et aide porte une `provenance` : identifiant de source (`sources.yaml`), date de vérification (`verified_on`), niveau de confiance (`confidence`) et relecture humaine (`human_reviewed`).

- Une valeur n'entre dans `rules.yaml`, `benchmarks.yaml` ou `aids.yaml` que si `corpus/rapport-freins-ia-2026.md` la marque **[V]** (lue sur la source primaire) ou **[V2]** (confirmée par une page secondaire lue en entier). Le niveau est reporté dans `confidence`, avec `verified_on: 2026-11-13`.
- Les valeurs, dates et URL sont copiées depuis la ligne du rapport, sans arrondi ni reformulation d'un chiffre. Un commentaire `# corpus l. N` au-dessus de chaque entrée renvoie à la ligne d'origine.
- `human_reviewed` vaut `false` partout : la relecture humaine reste à faire. `audit-ia validate-kb --require-review` échoue tant qu'elle ne l'est pas.
- Les entrées fondées sur des sources non lues (Journal officiel, Légifrance, jurisprudence sur le CSE, ANSSI) n'entrent dans la base qu'après relecture humaine. La base initiale n'en contient aucune.

Valider la base : `audit-ia validate-kb --verified-only` (code 0 attendu). Toute clé inconnue est refusée, avec le nom du fichier et l'identifiant de l'entrée.

## Fichiers

Tous les fichiers sauf `VERSION` et `neutrality.yaml` sont des listes d'entrées YAML ayant chacune un `id` unique. Le schéma exact est dans `src/audit_ia/kb/models.py`.

| Fichier | Contenu | Champs |
|---|---|---|
| `VERSION` | Version de la base | une ligne |
| `sources.yaml` | Sources citées | `id`, `title`, `publisher`, `url`, `published_on` (facultatif, seulement si le rapport donne le jour) |
| `sectors.yaml` | Secteurs reconnus | `id`, `label` (libellé affiché dans le rapport) |
| `facts.yaml` | Faits recueillis auprès du décideur | `id`, `dimension` (une des sept), `kind` (`bool`, `int`, `float`, `enum`, `text`), `choices` (pour `enum`), `prompt_hint`, `stages` (vide = tous les stades), `priority` |
| `rules.yaml` | Règles et échéances datées | `id`, `statement`, `status` (`applicable`, `adopte_non_applicable`, `projet`, `proposition`, `recommandation`, `jurisprudence`), `effective_on`, `bounds`, `applies_when`, `provenance` |
| `benchmarks.yaml` | Repères chiffrés | `id`, `indicator`, `value`, `headcount_min`, `headcount_max`, `sectors` (vide = tous), `population`, `fieldwork`, `expires_on`, `provenance` |
| `problems.yaml` | Problèmes auditables | `id` (préfixe `HUM`, `DAT`, `SI`, `GEN`, `CYB`, `COU`, `ENV` ou `FON`), `symptom`, `dimension`, `triggers`, `evidence_benchmark_ids`, `action_ids` |
| `use_cases.yaml` | Cas d'usage | `id`, `function`, `title`, `prerequisites`, `obstacles`, `risks`, `first_step`, `applies_when`, `priority` |
| `actions.yaml` | Actions du plan | `id`, `title`, `horizon` (`j30`, `j90`, `m12`), `effort` (`faible`, `moyen`, `fort`), `prerequisites`, `success_check` |
| `aids.yaml` | Aides publiques | `id`, `name`, `eligibility`, `headcount_min`, `headcount_max`, `amount`, `provenance` |
| `neutrality.yaml` | Neutralité commerciale | `forbidden_terms` : termes qui ne doivent apparaître dans aucun texte de rapport |

### Conditions

`applies_when`, `triggers` et `eligibility` sont des arbres de tests sur les faits : `{fact, op, value}` avec `op` parmi `eq`, `ne`, `lt`, `lte`, `gt`, `gte`, `in`, combinés par `all`, `any` et `not`. L'évaluation est à trois valeurs : un fait absent ou `inconnu` rend le test indécidable, et le moteur en tire une vérification à mener, jamais un constat. Les conditions sont écrites pour n'être vraies que sur ce que le décideur a effectivement déclaré. Une règle qui s'impose à toute entreprise (par exemple l'article 4 du règlement IA) n'a pas d'`applies_when`.

### Repères

- `expires_on` : un an après la fin du terrain d'enquête ; à défaut, un an après la publication.
- Pour un même `indicator`, un repère sectoriel remplace le repère tous secteurs.
- Clés de secteur : celles de `sectors.yaml` (ventilations Insee et Banque de France du rapport, plus `autre`). Un repère qui cite un secteur absent de `sectors.yaml` est refusé au chargement, et un audit dont le secteur n'y figure pas est refusé par `audit-ia report`.

### Neutralité

`neutrality.yaml` liste TCKC et les éditeurs, hébergeurs, cabinets et prestataires cités par le corpus. La liste s'applique au texte du rapport : constats, repères (indicateur, valeur, population), actions, cas d'usage, notes. Elle ne s'applique pas aux citations de source (`sources.yaml` : titre, éditeur, URL), qui restent exactes : nommer qui a publié un chiffre relève de la traçabilité, pas de la recommandation d'un prestataire. Les organismes et dispositifs publics (Bpifrance, France Num, CNIL, Insee, DGE, « Diagnostic Data IA », « Osez l'IA »...) n'y figurent pas : les aides les nomment. Les titres et éditeurs des sources n'apparaissent que dans les lignes de source. La comparaison se fait par sous-chaîne, sans casse : un nom qui est aussi une partie d'un mot courant (« Sage » dans « usage ») est saisi sous une forme plus longue.

## Lacunes connues

- **Aucun problème vérifié pour les dimensions stratégie et système d'information.** Le catalogue du rapport (l. 252-287) n'a, pour ces deux dimensions, aucune ligne dont la preuve soit marquée [V] ou [V2] : SI-S4, SI-S7, GEN-G3 et GEN-EVAL ne sont pas vérifiés. Les problèmes gardent la dimension que leur donne le rapport. Le planificateur pose quand même des questions sur ces dimensions, mais aucun constat ne peut y être établi tant que le corpus n'a pas été complété.
- **Deux aides seulement** (Diagnostic Data IA, Accélérateurs IA). IA Booster est écarté, car son statut 2026 est inconnu. Autodiag IA est écarté aussi : la ligne vérifiée (l. 182) ne donne aucun prix.
- **Consultation du CSE** : aucune règle, puisque la jurisprudence n'a pas été lue à la source. Elle entrera après relecture humaine.

## Licence

Base de connaissances sous Licence Ouverte 2.0 (Etalab). Le fichier de licence reste à ajouter au dépôt.
