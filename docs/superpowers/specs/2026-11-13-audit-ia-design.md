# audit-ia — spécification

Version 0.3 du 13 novembre 2026. **Statut : proposition à valider.** Les six décisions de cadrage ont été prises par le porteur du projet (section 9) ; leurs conséquences sont intégrées ci-dessous.

Ce document est rédigé sous l'angle d'un dossier présentable à un financeur public : un outil gratuit et neutre, inséré dans les dispositifs existants, dont la première version est un démonstrateur. Les éléments marqués *(choix proposé)* sont des propositions de rédaction, pas des décisions prises par le porteur du projet.

Les chiffres cités viennent de `corpus/rapport-freins-ia-2026.md` et portent sa convention : **[V]** lu sur la source primaire le 13/11/2026, **[V2]** confirmé par une source secondaire lue en entier.

## 1. Pourquoi cet outil

En 2026, les entreprises françaises n'ont plus un problème d'accès à l'IA mais de conversion : l'usage individuel est massif, l'usage organisé minoritaire.

- 40 % des TPE-PME utilisent l'IA, 19 % paient un outil, 9 à 11 % automatisent une tâche **[V]** (France Num).
- 31 % seulement des entreprises utilisatrices d'IA générative constatent un gain de productivité **[V]** (Banque de France).
- Le premier frein des non-utilisatrices est l'absence de cas d'usage identifié (49 %), loin devant le coût (9 %) **[V]** (Banque de France). À l'Insee, le coût n'est que la sixième raison de non-usage **[V]**.
- Le plan Osez l'IA a sensibilisé plus de 35 000 entreprises, mais 70 Diagnostics Data IA seulement ont été engagés pour un objectif de 1 000 **[V]** (DGE).

L'offre actuelle laisse un vide entre la sensibilisation et le diagnostic payant : l'autodiagnostic en ligne rend un score sans feuille de route, le diagnostic accompagné coûte 10 000 € HT (dont 40 % pris en charge) et exclut les entreprises de moins de 10 salariés.

**audit-ia occupe ce vide** : un entretien gratuit, mené à la voix, qui part de l'activité réelle de l'entreprise et rend un rapport de mise en œuvre.

## 2. Ce que fait l'outil

Un décideur (dirigeant, directeur général, directeur de fonction, entrepreneur) dialogue à la voix avec l'application. Celle-ci pose des questions concrètes sur l'entreprise, enchaîne avec des questions de suivi selon les réponses, établit un bilan, propose des solutions, permet de les affiner dans un second échange, puis remet un rapport écrit.

### Parcours

| Étape | Ce que vit le décideur | Ce que produit l'outil |
|---|---|---|
| 1. Cadrage | Deux minutes : qui il est, taille, secteur, ce qu'il attend. Consentement explicite à l'enregistrement et au traitement. | Profil (taille, secteur, stade) qui conditionne questions, benchmarks et aides. |
| 2. Entretien | 20 à 30 minutes de dialogue, en une ou plusieurs sessions reprenables. | Faits structurés, chacun rattaché à ce qui a été dit. |
| 3. Bilan | À l'écran : « voici ce que j'ai compris ». Il confirme ou corrige, à la voix ou au clavier. | Bilan validé : constats, points forts, points à vérifier. |
| 4. Solutions | Propositions classées, expliquées à la voix et affichées. | Actions candidates, chacune reliée à un constat. |
| 5. Affinage | Dialogue libre : écarter, préciser, repondérer. | Plan retenu. |
| 6. Rapport | Document écrit, téléchargeable. | Rapport de mise en œuvre. |
| 7. Suite, à sa demande | Il peut chercher un accompagnement. | Orientation vers les annuaires publics d'accompagnateurs ; aucune transmission à un prestataire. |

### Principes de l'entretien

- **Partir de l'activité, pas de l'IA.** Les premières questions portent sur le métier, les tâches qui prennent du temps, les irritants. Les cas d'usage se déduisent de là.
- **Adapter au stade.** Quatre stades : non-utilisatrice, usage individuel, usage outillé, processus transformé. Le premier frein change avec le stade, donc les questions aussi.
- **Distinguer ce que le décideur sait de ce qu'il suppose.** 42 % des utilisateurs passent surtout par un compte personnel et 14 % des salariés déclarent connaître une règle interne **[V]** (Ipsos bva/Google) : la parole du dirigeant ne décrit pas tout. Chaque fait porte un niveau de certitude — *constaté*, *estimé*, *inconnu* — et les *inconnus* deviennent des vérifications à mener dans le rapport.
- **Mesurer séparément l'usage individuel et le processus transformé.** Qui utilise quoi avec quel compte, d'un côté ; quelle tâche est réellement automatisée et validée par qui, de l'autre.
- **La voix recueille, l'écran restitue.** Bilan, solutions et rapport sont toujours lisibles et corrigeables.

### Les sept dimensions du bilan

1. Stratégie et portefeuille de cas d'usage
2. Gouvernance, risque et conformité
3. Données et référentiels
4. Système d'information et intégration
5. Sécurité et souveraineté
6. Compétences, formation, conduite du changement et dialogue social
7. Valeur, coûts et frugalité

Le catalogue de problèmes auditables du corpus (33 entrées, identifiants `HUM-`, `DAT-`, `SI-`, `GEN-`, `CYB-`, `COU-`, `ENV-`, `FON-`) fournit les constats possibles : symptôme, preuve de référence, dimension.

### Le rapport

- Synthèse d'une page pour le dirigeant.
- Bilan par dimension, avec situation de l'entreprise par rapport aux repères de sa taille et de son secteur.
- Trois à cinq cas d'usage prioritaires, avec prérequis, risques et première étape.
- Obligations applicables et échéances à venir, datées et sourcées.
- Plan d'action en trois horizons (30 jours, 90 jours, 12 mois).
- Vérifications à mener en interne (les *inconnus* de l'entretien).
- Aides et dispositifs correspondant au profil.
- Annexe : sources, dates de vérification, niveaux de confiance.

## 3. Engagements

Ces engagements conditionnent la crédibilité d'un outil gratuit financé sur fonds publics.

- **Neutralité totale** *(décision du porteur)*. Le rapport se suffit à lui-même et ne recommande aucun prestataire ni éditeur nommé. L'outil ne donne à aucun accompagnateur, TCKC compris, une position privilégiée : pas de transmission automatique, pas de mise en avant. Conséquences proposées : l'orientation renvoie vers les annuaires publics existants ; tout le code, la base de connaissances et les règles de diagnostic sont publiés sous licence libre et leurs modifications tracées ; toute future mise en relation obéit à des règles d'admission publiques, identiques pour tous.
- **Complémentarité.** Le rapport oriente vers les dispositifs existants quand le profil y correspond (Diagnostic Data IA, catalogue de prestataires et ambassadeurs du plan Osez l'IA, France Num) au lieu de les doubler.
- **Traçabilité.** Aucune règle, échéance, aide ou repère chiffré n'est affiché sans sa source, sa date et son niveau de confiance.
- **Exemplarité.** L'outil est lui-même un système d'IA qui écoute des informations confidentielles. La crainte sur les données est le frein le plus spécifiquement français : hébergement, choix des modèles et transparence doivent pouvoir être montrés.
- **Bien commun.** Avec consentement distinct, les bilans anonymisés alimentent un observatoire des freins réels par taille et secteur, que personne ne produit aujourd'hui.

## 4. Approches envisagées

**A. Questionnaire à branches, habillé de voix.** Un arbre de questions écrit à l'avance ; la voix ne fait que lire et transcrire. Résultat reproductible et simple à valider, mais c'est l'autodiagnostic existant avec un micro : pas de questions de suivi réelles, donc pas de cas d'usage qui émergent.

**B. Agent conversationnel libre.** Un modèle de langage mène l'entretien et rédige le rapport de bout en bout. Dialogue naturel, mais couverture des dimensions non garantie, deux entretiens non comparables, et surtout risque de règles ou d'aides inventées : inacceptable pour un outil qui cite le droit applicable.

**C. Hybride : dialogue libre, bilan déterministe.** *(choix proposé)* Le modèle de langage conduit la conversation et en extrait des faits ; un état d'audit structuré décide de ce qui reste à explorer ; le diagnostic et le choix des règles, repères et aides sont calculés par des règles explicites sur ces faits ; le modèle ne rédige qu'à partir de constats déjà établis.

C est retenue parce qu'elle est la seule à tenir ensemble les deux exigences : des questions de suivi réelles et un bilan dont chaque ligne est traçable.

## 5. Architecture

### Séparation des rôles

| Composant | Nature | Rôle |
|---|---|---|
| Interface vocale | Reconnaissance et synthèse vocales en flux | Écouter, parler, gérer les interruptions et les reprises. |
| Conducteur d'entretien | Modèle de langage | Formuler la question suivante dans le registre du décideur. |
| Extracteur | Modèle de langage, sortie structurée | Transformer chaque réponse en faits typés, avec citation et niveau de certitude. |
| Planificateur | Déterministe | Choisir le prochain objectif selon le stade, les dimensions non couvertes et le temps restant. |
| Moteur de diagnostic | Déterministe | Appliquer les règles : constats, obligations applicables, repères du segment, aides éligibles. |
| Rédacteur | Modèle de langage | Mettre en phrases le bilan et le rapport, sans ajouter de fait. |
| Contrôleur | Déterministe, puis modèle de langage | Vérifier que chaque affirmation du rapport renvoie à un fait ou à une entrée de la base. |

Règle de conception : **les modèles de langage parlent et rédigent ; ils ne décident ni du droit applicable, ni des chiffres, ni des aides.**

### Base de connaissances

Versionnée dans le dépôt, extraite du corpus, relue par un humain avant publication.

| Objet | Attributs obligatoires |
|---|---|
| Règle | Énoncé, date d'effet, statut (applicable, adopté non applicable, projet, proposition, recommandation, jurisprudence), bornes, source primaire, date et mode de vérification. |
| Repère chiffré | Indicateur, valeur, périmètre (taille, secteur, population interrogée), date de terrain, source, niveau de confiance, date de péremption. |
| Problème auditable | Identifiant, symptôme, faits déclencheurs, dimension, preuve de référence. |
| Cas d'usage | Fonction, prérequis, obstacles typiques, risques, première étape. |
| Action | Constat traité, horizon, effort, prérequis, vérification de réussite. |
| Aide | Dispositif, conditions d'éligibilité, montant, source, date de vérification. |

Un repère périmé ou une règle non revérifiée depuis un délai fixé est signalé comme tel dans le rapport, pas masqué.

### Données d'un audit

Profil de l'entreprise ; transcription ; faits (énoncé, valeur, certitude, extrait d'origine) ; constats ; plan retenu ; rapport ; consentements. Le rapport est régénérable à tout moment à partir des faits et de la version de la base.

### Confidentialité et conformité de l'outil

- Annonce claire, dès l'ouverture, que l'interlocuteur est une IA (article 50 du règlement IA, applicable depuis le 2 août 2026 **[V]**).
- Consentement distinct pour le traitement de l'entretien et pour l'observatoire.
- **Aucune conservation de l'audio** *(décision du porteur)* : le son est traité en flux et n'est jamais écrit sur disque ; seule la transcription est gardée. Transcription et rapport sont supprimables par le décideur.
- **Hébergement et traitement souverains** *(décision du porteur)* : voir la pile technique ci-dessous.
- Aucune donnée d'entretien réutilisée pour entraîner un modèle.
- Analyse d'impact relative à la protection des données menée avant l'ouverture à de vrais utilisateurs.

### Pile technique

Les décisions « hébergement souverain », « fournisseurs choisis sur la qualité et la souveraineté » et « aucune conservation de l'audio » écartent les plateformes vocales intégrées et les modèles voix-à-voix des fournisseurs américains. Reste la chaîne composée et auto-orchestrée.

Définition retenue de « souverain » *(à confirmer)* : opérateur soumis au seul droit européen, données et calculs en France, sans appel à un service relevant d'une loi extraterritoriale. La souveraineté est un critère éliminatoire ; la qualité départage ensuite les candidats, mesurée sur un jeu d'entretiens de test en français.

| Couche | Choix | Candidats à évaluer |
|---|---|---|
| Orchestration vocale | Orchestrateur ouvert, auto-hébergé | LiveKit Agents, Pipecat |
| Transcription | **Voxtral (Mistral)** *(décision du porteur)*, exécuté sur notre infrastructure si les conditions d'hébergement de Mistral ne répondent pas à la définition de « souverain » | Repli : Whisper auto-hébergé, modèles Kyutai |
| Modèle de langage | **Mistral Large 4** *(décision du porteur)*, derrière une interface commune qui permet d'en changer ; identifiant exact, disponibilité et lieu d'exécution à vérifier | Repli : modèle à poids ouverts auto-hébergé |
| Synthèse vocale | Famille Voxtral si elle couvre la synthèse en français avec une qualité suffisante *(à vérifier)* ; sinon modèle ouvert auto-hébergé | Modèles Kyutai, autres modèles ouverts en français |
| Service d'entretien et de diagnostic | Python | — |
| Interface | Next.js (TypeScript), comme le site tckc.ai | — |
| Base de connaissances et règles | Fichiers structurés versionnés dans le dépôt, validés par schéma ; règles en code typé | — |
| Stockage | PostgreSQL | — |
| Hébergement | **Scaleway** *(décision du porteur)* ; qualification SecNumCloud visée pour l'ouverture au public, état de celle de Scaleway à vérifier | Repli : OVHcloud, Outscale |
| Rapport | HTML converti en PDF | — |

À vérifier en premier : si les modèles Mistral, Voxtral compris, peuvent être exécutés sur l'infrastructure Scaleway (service géré ou auto-hébergement), ce qui garderait toute la chaîne chez un seul hébergeur français. Les candidats n'ont pas été évalués : disponibilité, qualité en français, latence et conditions d'hébergement sont à vérifier avant tout engagement. Risque assumé : la qualité vocale des briques souveraines peut être inférieure à celle des plateformes américaines ; le bilan confirmé à l'écran et la saisie au clavier en limitent l'effet.

## 6. Première version : le démonstrateur

But : montrer que le parcours complet fonctionne et produit un rapport utile, devant trois publics *(décision du porteur)* :

- **Bpifrance**, comme financeur potentiel : il doit voir le besoin, le parcours et les engagements tenus.
- **Les « builders »**, ceux qui construisent et mettent en œuvre l'IA en entreprise : ils doivent pouvoir lire l'architecture, la base de connaissances et les règles, et juger s'ils s'appuieraient dessus.
- **Quelques décideurs** : ils passent réellement l'entretien et jugent le rapport.

**Inclus**

- Parcours complet, de l'entretien vocal au rapport.
- Français uniquement, dans un navigateur, sur ordinateur et mobile.
- Entreprises de 1 à 249 salariés *(choix proposé : c'est la cible que les dispositifs actuels atteignent le moins)*.
- Sept dimensions, quatre stades.
- Fonctions de gestion et d'administration couvertes en profondeur : finance-comptabilité et ressources humaines-paie, les deux seules documentées de bout en bout dans le corpus. Les autres fonctions sont traitées plus légèrement.
- Base de connaissances initiale limitée aux entrées **[V]** et **[V2]** du corpus.
- Orientation vers les annuaires publics d'accompagnateurs, sans transmission à un prestataire.
- Dépôt lisible par les builders : architecture, base de connaissances et règles documentées.

**Exclus de cette version**

- Annuaire d'accompagnateurs et mise en relation.
- Observatoire public.
- Suivi de la mise en œuvre après le rapport.
- Collecte auprès des salariés pour confronter la parole du dirigeant.
- Connexion aux logiciels de l'entreprise.
- Autres langues, application mobile native.

**Critères de réussite** *(choix proposés)*

- Entretiens menés à terme avec les décideurs volontaires (objectif proposé : dix).
- Un rapport jugé « utilisable tel quel » par au moins sept décideurs sur dix.
- Retour écrit d'au moins trois builders sur l'architecture et la base de connaissances.
- Aucune règle, échéance ou aide erronée relevée à la relecture humaine des dix rapports.
- Entretien bouclé en 30 minutes ou moins.

## 7. Suite envisagée

1. Ouverture à de vrais utilisateurs : exigences d'hébergement et de sécurité relevées, analyse d'impact, couverture élargie des fonctions et des secteurs.
2. Annuaire d'accompagnateurs (indépendants, entreprises spécialisées) et mise en relation, avec règles d'admission publiées.
3. Second entretien à trois ou six mois pour mesurer ce qui a été mis en œuvre.
4. Questionnaire court aux salariés, pour confronter usage déclaré et usage réel.
5. Observatoire public des freins, alimenté par les bilans anonymisés.

## 8. Risques

| Risque | Parade |
|---|---|
| Base de connaissances qui se périme (le cadre juridique a changé en juillet 2026, les taux d'adoption doublent chaque année) | Date de vérification et péremption sur chaque entrée ; revue périodique ; signalement dans le rapport. |
| Sources primaires non lues à ce jour (Journal officiel, Légifrance, jurisprudence sur le CSE, ANSSI) | Relecture humaine avant d'entrer dans la base ; à défaut, entrée exclue du démonstrateur. |
| Bilan fondé sur la seule perception du dirigeant | Niveaux de certitude ; vérifications internes listées dans le rapport ; questionnaire salariés en version ultérieure. |
| Transcription vocale défaillante (accents, bruit, vocabulaire métier) | Bilan toujours confirmé à l'écran ; saisie au clavier possible à tout moment. |
| Rapport perçu comme un argumentaire commercial | Engagement de neutralité ; mise en relation séparée et à la demande. |
| Défiance sur la confidentialité | Engagements de la section 5 affichés avant l'entretien. |
| Lacunes du corpus (pas de taux d'échec français, peu de gains mesurés indépendants) | Aucune extrapolation : le rapport dit ce qui n'est pas mesuré. |

## 9. Décisions du porteur du projet

Prises le 13 novembre 2026.

| Sujet | Décision | Conséquence dans ce document |
|---|---|---|
| Cible du démonstrateur | Bpifrance, les builders, quelques décideurs | Trois publics et leurs critères de réussite (section 6). |
| Hébergement | Souverain ; Scaleway ; SecNumCloud à l'ouverture au public | Pile technique (section 5). |
| Fournisseurs de modèles et de voix | Qualité et souveraineté ; Mistral Large 4 pour le modèle de langage, Voxtral pour la voix | Souveraineté éliminatoire, qualité pour départager ; Voxtral retenu d'emblée (section 5). |
| Conservation de l'audio | Aucune | Traitement en flux, seule la transcription est gardée (section 5). |
| Gouvernance de la neutralité | Totale ; TCKC en dehors de l'outil ; code sous EUPL 1.2, base sous Licence Ouverte 2.0 | Aucune position privilégiée, code, base et règles publiés (section 3). |
| Financeur et calendrier | À déterminer | La date du démonstrateur reste ouverte. |

### Précisions et points restants

1. **Neutralité totale et rôle de TCKC.** *Confirmé par le porteur le 13 novembre 2026* : TCKC reste en dehors de l'outil, qui ne lui transmet aucune demande. Son accompagnement existe à côté, au même titre que celui de tout autre accompagnateur.
2. **« Builders ».** *Confirmé par le porteur le 13 novembre 2026* : ce sont les indépendants et les entreprises qui mettent l'IA en œuvre chez les clients.
3. **Ouverture du code.** *Décidé par le porteur le 13 novembre 2026* : tout le code est publié sous **EUPL 1.2**, la base de connaissances sous **Licence Ouverte 2.0** (Etalab). Reste ouvert : le moment où le dépôt devient public (proposé : quand le démonstrateur tourne).
4. **« Souverain ».** *Confirmé par le porteur le 13 novembre 2026* : opérateur soumis au seul droit européen, données et calculs en France ; la qualification SecNumCloud est visée à l'ouverture au public, pas pour le démonstrateur.
5. **Périmètre de Voxtral.** La décision « Voxtral » tranche la question de la brique vocale. Restent à vérifier, avant de s'engager, que Voxtral couvre la transcription en flux et la synthèse en français, et où Mistral l'exécute ; à défaut, auto-hébergement des poids ouverts pour la transcription et modèle ouvert pour la synthèse.
6. **Latence du dialogue** *(proposition)* : Mistral Large 4 pour l'extraction des faits et la rédaction ; un modèle Mistral plus léger à tester pour la conduite de l'entretien si le temps de réponse gêne la conversation.

## 10. Laissé à la réalisation

Choix final de chaque brique vocale et du modèle de langage après évaluation, schéma de stockage, format exact de la base de connaissances, conception des écrans, rédaction des consignes des modèles, jeu d'entretiens de test.
