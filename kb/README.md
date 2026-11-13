# Base de connaissances

Données consommées par le moteur de diagnostic d'`audit-ia`. Version : voir `VERSION` (`2026.11.0`).

## Règle unique : rien sans source, date et niveau de confiance

Chaque règle, repère et aide porte une `provenance` : identifiant de source (`sources.yaml`), date de vérification (`verified_on`), niveau de confiance (`confidence`) et relecture humaine (`human_reviewed`).

- Une valeur n'entre dans `rules.yaml`, `benchmarks.yaml` ou `aids.yaml` que si `corpus/rapport-freins-ia-2026.md` la marque **[V]** (lue sur la source primaire) ou **[V2]** (confirmée par une page secondaire lue en entier). Le niveau est reporté dans `confidence`, avec `verified_on: 2026-11-13`.
- Les valeurs, dates et URL sont copiées depuis la ligne du rapport, sans arrondi ni reformulation d'un chiffre. Un commentaire `# corpus l. N` au-dessus de chaque entrée renvoie à la ligne d'origine.
- `human_reviewed` vaut `false` partout : la relecture humaine reste à faire. `audit-ia validate-kb --require-review` échoue tant qu'elle ne l'est pas.
- Aucune entrée ne repose sur une source non lue (Journal officiel, Légifrance, jurisprudence du CSE lue à la source, ANSSI).

Valider la base : `audit-ia validate-kb --verified-only` (code 0 attendu). Toute clé inconnue est refusée, avec le nom du fichier et l'identifiant de l'entrée.

## Fichiers

Tous les fichiers sauf `VERSION` et `neutrality.yaml` sont des listes d'entrées YAML ayant chacune un `id` unique. Le schéma exact est dans `src/audit_ia/kb/models.py`.

| Fichier | Contenu | Champs |
|---|---|---|
| `VERSION` | Version de la base | une ligne |
| `sources.yaml` | Sources citées | `id`, `title`, `publisher`, `url`, `published_on` (facultatif, seulement si le rapport donne le jour) |
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
- Clés de secteur (ventilation Insee du rapport) : `information_communication`, `activites_specialisees`, `activites_immobilieres`, `energie_eau_dechets`, `services_administratifs`, `industrie_manufacturiere`, `commerce`, `hebergement_restauration`, `construction`, `transports`, et `autre`.

### Neutralité

`neutrality.yaml` liste TCKC et les éditeurs, hébergeurs, cabinets et prestataires cités par le corpus. Les organismes et dispositifs publics (Bpifrance, France Num, CNIL, Insee, DGE, « Diagnostic Data IA », « Osez l'IA »...) n'y figurent pas : les aides les nomment. Les titres et éditeurs des sources n'apparaissent que dans les lignes de source. La comparaison se fait par sous-chaîne, sans casse : un nom qui est aussi une partie d'un mot courant (« Sage » dans « usage ») est saisi sous une forme plus longue.

## Licence

Base de connaissances sous Licence Ouverte 2.0 (Etalab). Le fichier de licence reste à ajouter au dépôt.
