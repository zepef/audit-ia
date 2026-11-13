# audit-ia

Application d'audit et d'implémentation de l'IA pour les entreprises françaises.

Ce README est tenu à jour au fil du projet : la section « État » et le « Journal » en bas de page sont modifiés à chaque étape.

## Objet

Aider une entreprise française (TPE, PME, ETI) à :

1. **auditer** sa situation face à l'IA — usages réels, données, système d'information, compétences, gouvernance, conformité, coûts ;
2. **implémenter** — relier chaque écart constaté à une action, une échéance et, quand elle existe, une aide mobilisable.

Le constat de départ, tiré du corpus : en 2026, le problème n'est plus l'accès à l'IA mais sa conversion en processus transformés, gouvernés et mesurés. L'usage individuel est massif, l'usage organisé minoritaire, et le coût n'est presque jamais le premier frein.

## État

| Élément | État | Dernière mise à jour |
|---|---|---|
| Corpus documentaire (rapport + notes) | Rédigé ; 210 affirmations contrôlées sur sources primaires (128 confirmées, 32 corrigées, 4 infirmées, 23 non retrouvées, 23 inaccessibles) | 13/11/2026 |
| Spécification de l'application | Version 0.1 rédigée, à valider (`docs/superpowers/specs/2026-11-13-audit-ia-design.md`) | 13/11/2026 |
| Modèle de données (règles datées, benchmarks, problèmes auditables) | À faire | — |
| Code | Non commencé | — |

## Contenu du dépôt

```
corpus/
  rapport-freins-ia-2026.md     synthèse : freins à l'intégration de l'IA en France (2026)
  notes/                        six notes de recherche, une par axe
  verification/                 trois notes de vérification sur sources primaires
docs/superpowers/specs/         spécification de l'application
```

Les six axes des notes : baromètres d'adoption, cadre juridique et conformité, freins humains et organisationnels, freins techniques (données, SI, cybersécurité, souveraineté, coûts), fonctions de gestion et d'administration, méthodes d'audit et dispositifs d'aide.

Ce que le rapport fournit directement pour l'application :

- des dimensions d'audit et un axe de stade d'avancement ;
- un catalogue de problèmes auditables (symptôme, cause, population touchée, preuve) ;
- un tableau de règles et d'échéances datées, avec leur statut ;
- des benchmarks avec périmètre, date et niveau de confiance ;
- une bibliographie, majoritairement datée de 2026.

## Conventions de preuve

Tout fait du corpus porte un marqueur. Le code doit le conserver : aucune règle ni aucun benchmark ne doit être présenté à l'utilisateur sans sa source, sa date et son niveau de confiance.

| Marqueur | Sens |
|---|---|
| **[V]** | Lu sur la source primaire le 13/11/2026 |
| **[V2]** | Confirmé seulement par une page secondaire lue en entier |
| **[A]** | Non vérifié ; attribué à la source primaire et recoupé par au moins deux extraits de recherche |
| **[B]** | Non vérifié ; un seul extrait ou relais de presse |
| **[C]** | Non vérifié ; site tiers ou blog |
| **[éditeur]**, **[cabinet]**, **[commercial]** | Source intéressée, à ne pas utiliser comme mesure indépendante |

Deux conséquences pour la conception :

- **Les règles juridiques sont datées et à statut** (applicable, adopté non applicable, projet, jurisprudence). Le cadre a bougé en 2026 et bougera encore ; une règle sans date de vérification est une règle fausse en attente.
- **Les benchmarks d'adoption se périment en moins d'un an** : les taux doublent d'une année sur l'autre dans deux séries indépendantes.

## Limites connues du corpus

- **Sources restées inaccessibles** à la vérification automatisée : EUR-Lex, Légifrance, ANSSI (cyber.gouv.fr), vie-publique.fr. Les textes officiels, les décisions de justice sur la consultation du CSE et les recommandations de l'ANSSI ne sont donc pas lus à la source.
- **Sources hors périmètre de vérification** : tous les hôtes en dehors des 20 autorisés, dont la plupart des éditeurs et cabinets.
- **Lacunes de fond** : aucun taux français mesuré d'échec ou d'abandon de projets IA, très peu de cas privés nommés d'échec, aucun gain chiffré indépendant en comptabilité ou en paie.
- **Bibliographie** fusionnée par script à partir des notes ; le classement 2026 / antérieur et l'étiquette « source commerciale » y sont approximatifs.

## Prochaines étapes

- [ ] Relire le rapport et arbitrer les contradictions restées ouvertes
- [ ] Vérifier à la main les sources restées inaccessibles (textes officiels, jurisprudence, ANSSI)
- [x] Rédiger la spécification (version 0.1)
- [ ] Valider la spécification et trancher ses six décisions ouvertes
- [ ] Définir le modèle de données : règle datée, benchmark, problème auditable, action, aide
- [ ] Extraire du rapport les jeux de données initiaux dans un format exploitable par le code
- [ ] Choisir l'architecture et la pile technique

## Journal

| Date | Changement |
|---|---|
| 12/11/2026 | Recherche documentaire sur six axes et première version du rapport, à partir d'extraits de moteur de recherche (aucune page source ouverte) |
| 13/11/2026 | Passe de vérification sur sources primaires (20 hôtes autorisés) ; rapport corrigé et annoté ; création du dépôt et de ce README |
| 13/11/2026 | Spécification 0.1 : entretien vocal avec un décideur, bilan déterministe, rapport de mise en œuvre ; première version en démonstrateur |
