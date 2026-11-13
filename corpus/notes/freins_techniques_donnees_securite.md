# Freins techniques, données, infrastructure, cybersécurité et coûts à l'intégration de l'IA dans les entreprises françaises (état au 12 novembre 2026)

> **Avertissement méthodologique (à lire avant toute réutilisation).**
> - **Aucune page n'a pu être ouverte.** Dans cette session, l'outil de lecture de pages a échoué sur tous les hôtes testés (`www.lemondeinformatique.fr`, `www.solutions-numeriques.com`, `www.journaldunet.com`, `www.actuia.com`, `www.ademe.fr`, `www.leto.legal` : hôtes hors de la liste réseau autorisée). Tous les faits ci-dessous proviennent donc **d'extraits et de résumés de résultats de recherche**, et non de la lecture intégrale des documents. La colonne « ouvert ? » de la bibliographie vaut **« non »** pour toutes les lignes.
> - **Le quota de recherche de la session a été atteint** avant la fin (dernières requêtes non exécutées : avis ADEME juillet 2026, Snowflake/Omdia France, baromètre DaVinciDoc, dépendance aux hyperscalers, coûts de tokens AFP, CSRD et IA, Proofpoint). Ces points sont signalés dans les sections « Gaps ».
> - Chaque chiffre doit être **revérifié dans la source primaire** avant d'entrer dans le corpus de l'application. Les mentions « non vérifié », « source secondaire » et « discours éditeur » sont posées fait par fait.
> - Les dates « non vérifiée » signifient que l'extrait ne donnait pas la date exacte de publication.
> - Format des constats auditables : **Symptôme / Cause technique / Profil touché / Preuve chiffrée / Parade citée / Source**.

---

## 1. Données : qualité, silos, gouvernance, documents non structurés, maturité des PME pour l'IA et le RAG

### Takeaway
En 2026, la qualité des données et l'intégration aux systèmes existants sont les deux freins techniques les plus cités par les décideurs français (KPMG : 75 % et 63 % pour le passage à l'échelle), mais aucune source consultée ne donne une « part des entreprises citant la donnée comme premier frein » qui fasse consensus : les chiffres vont de 29 % (EY, non-utilisateurs) à 75 % (KPMG, passage à l'échelle) selon la question posée. Côté TPE-PME, l'usage est massif mais superficiel (40 % d'utilisatrices, 11 % pour automatiser), ce qui indique que la donnée d'entreprise est encore peu branchée sur l'IA.

### Cited Findings

**Constats auditables**

- **D1 — Données de qualité insuffisante bloquant le passage à l'échelle.**
  Symptôme : pilotes IA qui fonctionnent sur un périmètre restreint mais ne se généralisent pas. Cause technique : données incomplètes, incohérentes, non réconciliées entre systèmes. Profil : grandes entreprises et ETI françaises (356 décideurs, 8 fonctions). Preuve : freins au passage à l'échelle = qualité des données 75 %, intégration avec des systèmes existants « qui ne communiquent pas ou mal entre eux » 63 % ; freins à l'adoption = intégration avec les systèmes existants 80 %, manque de budget ou de temps 65 %, qualité des données 59 %. Parade citée : investissement dans « la gestion d'une data de qualité ». **Réserve : l'extrait ne permet pas de confirmer que ces cinq pourcentages viennent tous de l'édition 2026 de l'étude ; à vérifier dans le PDF.** — [KPMG, page « Tendances IA – adoption par fonctions »](https://kpmg.com/fr/fr/insights/dirigeants/tendances-ia-adoption-fonctions-entreprise.html) ; [KPMG, communiqué Trends of AI 2026, 23 janvier 2026](https://kpmg.com/fr/fr/media/press-releases/2026/01/adoption-ia-entreprises-francaises.html) ; [PDF de l'étude](https://assets.kpmg.com/content/dam/kpmgsites/fr/pdf/insights/etude-adoption-ia-2026.pdf)

- **D2 — « Dette de données » révélée par l'IA.**
  Symptôme : taux d'échec élevés des projets IA, résultats incohérents. Cause technique : pratiques de gestion de données obsolètes, raccourcis d'infrastructure, sources mal documentées (absence de lignage et de catalogue). Profil : entreprises avec SI ancien. Preuve : citation d'expert « l'IA ne crée pas de problèmes de données ; elle les révèle et les accélère » ; Gartner prévoit que d'ici 2030, 50 % des entreprises subiront des retards de déploiement IA ou des coûts de maintenance plus élevés. Étude mondiale, relayée par la presse française, sans coupe France identifiée. — [Le Monde Informatique, « La stratégie IA entravée par la dette technique sur les données », 2026, date non vérifiée](https://www.lemondeinformatique.fr/actualites/lire-la-strategie-ia-entravee-par-la-dette-technique-sur-les-donnees-100038.html)

- **D3 — Données « non prêtes pour l'IA ».**
  Preuve : seules 7 % des organisations estiment leurs données prêtes pour l'IA (Cloudera / Harvard Business Review Analytic Services, mars 2026). **Étude mondiale, pas de coupe France identifiée ; phrase tronquée dans l'extrait, à vérifier.** — [Solutions Numériques, « L'IA agentique révèle les fragilités des fondations data des entreprises », 2026, date non vérifiée](https://www.solutions-numeriques.com/?p=247498)

- **D4 — Manque de données de qualité cité comme obstacle majeur.**
  Preuve : 68 % de 1 250 décideurs considèrent le manque de données de qualité comme un obstacle majeur (étude BCG relayée par Le Monde Informatique). **Étude mondiale ; attribution à BCG à vérifier dans l'article.** — [Le Monde Informatique, « Les projets IA révèlent les défis de la qualité des données », date non vérifiée](https://www.lemondeinformatique.fr/actualites/lire-les-projets-ia-revelent-les-defis-de-la-qualite-des-donnees-99083.html)

- **D5 — Données fragmentées et gouvernance incohérente (coupe France).**
  Symptôme : aucun frein unique ne domine en France (aucune barrière citée par plus d'un tiers des répondants), le blocage se déplace vers « l'opérationnalisation et l'intégration ». Cause : « les données fragmentées réduisent l'efficacité de l'IA, les systèmes hérités ralentissent l'intégration alors qu'une gouvernance incohérente introduit des risques ». Profil : 250 décideurs français (enquête YouGov, mars-avril 2026, quatre pays). **Source éditeur (Infor vend des ERP) ; pourcentages détaillés non trouvés.** — [Infor, « Le tournant de l'IA pour la France », avril 2026](https://www.infor.com/fr-fr/blog/france-ai-market-slow-adoption-risk)

- **D6 — Sécurité des données et confiance dans les résultats comme freins déclarés.**
  Preuve : 60 % des entreprises françaises n'ont pas de cadre formalisé pour leurs usages de l'IA ; freins cités : sécurité des données et conformité 41 %, manque de maturité interne 31 %, confiance dans les analyses produites par l'IA 30 % (900 décideurs, Coface avec Les Echos Études). — [ActuIA, « Six entreprises sur dix utilisent l'IA sans cadre, selon Coface » (baromètre publié le 5 octobre 2026)](https://www.actuia.com/actualite/six-entreprises-sur-dix-utilisent-lia-sans-cadre-selon-coface/)

- **D7 — Non-utilisateurs français : incompatibilité des outils et difficultés de données.**
  Preuve : parmi les entreprises françaises qui n'utilisent pas l'IA, 71 % n'en voient pas l'utilité, 54 % citent le manque d'expertise interne, **38 % l'incompatibilité avec leurs outils existants, 29 % des difficultés avec les données**. **Attribution incertaine dans l'extrait (EY ou Insee) : à vérifier dans l'article.** — [Le Monde Informatique, « L'IA est partout dans les entreprises, les agents presque nulle part », 2026, date non vérifiée](https://www.lemondeinformatique.fr/actualites/lire-l-ia-est-partout-dans-les-entreprises-les-agents-presque-nulle-part-100750.html)

- **D8 — TPE-PME : usage large mais déconnecté des données et processus de l'entreprise.**
  Preuve : 40 % des TPE-PME utilisent au moins une solution d'IA (13 % en 2024, 26 % en 2025) ; seules 19 % paient pour une solution ; 11 % l'utilisent pour automatiser des tâches contre 34 % pour générer du contenu ; l'IA n'est une priorité numérique 2026-2027 que pour 18 % ; 21 % ont suivi une formation au numérique en 2025. Enquête Crédoc pour la DGE, environ 9 655 entreprises, publiée le 28 septembre 2026. — [DGE, communiqué Baromètre France Num 2026](https://www.entreprises.gouv.fr/espace-presse/barometre-france-num-2026-quatre-tpe-pme-sur-dix-utilisent-desormais-lintelligence) ; [ActuIA, « 40 % des TPE-PME utilisent l'IA, mais 19 % seulement la paient »](https://www.actuia.com/actualite/40-des-tpe-pme-utilisent-lia-mais-19-seulement-la-paient/) ; [BDM, « 10 chiffres sur le numérique dans les TPE et PME en 2026 »](https://www.blogdumoderateur.com/ia-cyber-budgets-10-chiffres-numerique-tpe-pme-2026/)

- **D9 — Diffusion rapide, gains rares.**
  Preuve : début 2026, plus des deux tiers des entreprises d'au moins 20 salariés déclarent utiliser l'IA générative, surtout dans les fonctions support ; environ un tiers des utilisateurs signalent des gains tangibles (enquête auprès d'environ 7 000 entreprises, fin février à début avril 2026). — [Banque de France, Bulletin n° 266, septembre 2026](https://www.banque-france.fr/fr/publications-et-statistiques/publications/lia-sinstalle-dans-les-entreprises-francaises-une-diffusion-rapide-mais-des-gains-de-productivite) ; [PDF](https://www.banque-france.fr/system/files/2026-09/BDF266-1_IA-et-entreprises_web.pdf)

- **D10 — Écart France / zone euro.**
  Preuve : 23 % des entreprises en France font état d'une utilisation modérée ou importante de l'IA contre 39 % dans la zone euro ; les auteurs ne trouvent pas de facteur explicatif clair. — [Banque de France, Eco Notepad n° 451, mai 2026](https://www.banque-france.fr/system/files/2026-05/Billet_451_VF.pdf)

- **D11 — Gestion documentaire et gouvernance des LLM mesurées chez les DSI.**
  Un baromètre national « DaVinciDoc » (746 réponses de DSI, CTO et décideurs IT, 18 secteurs) évalue sept dimensions de maturité, de la gestion documentaire à la gouvernance des LLM. **Résultats chiffrés non obtenus ; date non vérifiée ; émetteur de type consortium d'éditeurs, à qualifier.** — [BDM, guide « Baromètre national DSI Data & IA »](https://www.blogdumoderateur.com/guides/barometre-national-dsi-data-ia-maturite-reelle-organisations-francaises/)

- **D12 — Sources 2025 (faute d'équivalent 2026 trouvé).**
  Salesforce/OpinionWay (14 mars 2025) : 94 % des entreprises françaises ont lancé des projets IA, 51 % en phase d'exploration ; freins : manque de compétences 40 %, coûts 38 %. **Source éditeur, 2025.** — [Salesforce, communiqué du 14 mars 2025](https://www.salesforce.com/fr/news/press-releases/2025/03/14/barometre-ia-salesforce-x-opinionway-les-entreprises-francaises-misent-sur-les-agents-autonomes-pour-accelerer-leur-transformation-grace-a-lia/)
  Precisely / Drexel LeBow : 50 % des répondants déclarent la qualité des données comme principal problème des projets IA. **Source éditeur, mondiale, date non vérifiée.** — [Precisely, communiqué](https://www.precisely.com/fr/press-release/selon-une-nouvelle-etude-internationale-publiee-par-precisely-le-manque-de-qualite-et-de-gouvernance-des-donnees-constitue-un-obstacle-majeur-a-la-preparation-des-entreprises-a-lutilisation)

### Inferences
- Le chiffre le plus défendable pour « la donnée comme frein principal en France en 2026 » est celui de KPMG (75 % pour le passage à l'échelle), sous réserve de vérification ; il mesure un frein au passage à l'échelle chez des organisations déjà engagées, et non un frein à l'entrée.
- L'écart France Num entre génération de contenu (34 %) et automatisation (11 %) suggère que la majorité des TPE-PME utilisent des assistants généralistes sans connexion à leurs données de gestion : le sujet RAG/données maîtres ne se pose pas encore pour elles, il se posera au moment de l'automatisation.
- Pour un audit, les signaux observables sont : absence de référentiel client/article unique, absence de catalogue ou de lignage, documents non structurés non indexés, droits d'accès documentaires non maîtrisés (qui deviennent un risque de fuite dès qu'un RAG ou un copilote les indexe).

### Gaps
- Aucune statistique 2026 spécifiquement française sur la part de données non structurées, l'existence d'un catalogue de données, ou la maturité « master data » des PME n'a été trouvée.
- Aucune source 2026 de Hub France IA, Numeum, PAC/teknowlogy, Markess, IDC France, Wavestone, Capgemini, Dataiku ou Sopra Steria n'a pu être consultée (quota de recherche atteint).
- Les freins détaillés du baromètre France Num 2026 (coût, compétences, sécurité, données) ne figuraient pas dans les extraits ; à lire dans le rapport Crédoc.
- Chiffres Snowflake/Omdia (ROI quantifié à 32 % en France contre 49 % dans le monde) vus seulement via un résumé de l'article du Monde Informatique : non vérifiés.

---

## 2. Systèmes d'information : legacy, dette technique, intégration aux ERP/CRM/SIRH/compta utilisés en France, API, verrouillage et hausses de prix liées à l'IA embarquée

### Takeaway
L'intégration aux systèmes existants est le premier frein déclaré à l'adoption (80 % chez KPMG, à vérifier), et 2026 ajoute deux contraintes nouvelles : la restriction contractuelle de l'accès des agents tiers aux API d'ERP (SAP API Policy v4/2026, portée contestée) et l'inflation des licences justifiée par l'IA embarquée (étude Cigref/Asterès : 8,7 % par an constatés, 12 % par an anticipés, l'IA « by design » citée par 32 % des répondants comme mécanisme de hausse). L'ouverture agentique des logiciels français de gestion est inégale : Pennylane a un serveur MCP en lecture seule depuis août 2026, aucun serveur MCP éditeur n'a été trouvé pour Sage 100 ou Sage X3.

### Cited Findings

**Constats auditables**

- **S1 — Inflation cloud et logicielle, l'IA en bundle comme deuxième cause.**
  Symptôme : hausse des factures à périmètre constant, fonctions IA imposées dans les offres. Cause : verrouillage technologique ou contractuel (cité par 40 % des répondants), fonctions d'IA intégrées par défaut censées justifier les hausses (32 %). Profil : grandes organisations membres ou proches du Cigref. Preuve : surcoûts estimés à 140 Md€ par an pour les organisations européennes ; hausse moyenne déclarée de 8,7 % par an sur trois ans ; 12 % par an anticipés sur cinq ans ; un DSI sur deux ne parvient pas à mesurer ce que l'IA en bundle lui rapporte. **Limite : échantillon de 54 décideurs IT ; le Cigref est une partie prenante acheteuse.** Étude réalisée par Asterès, mai 2026. — [Le Monde Informatique, « L'inflation gonfle la facture cloud et logicielle de 140 Md€ par an », mai 2026, jour non vérifié](https://www.lemondeinformatique.fr/actualites/lire-l-inflation-gonfle-la-facture-cloud-et-logicielle-de-140-mdeteuro-par-an-100293.html) ; [ActuIA, « Cigref : 140 Md€ de surcoûts cloud en Europe, l'IA en bundle en deuxième cause »](https://www.actuia.com/actualite/cigref-140-mdeur-de-surcouts-cloud-en-europe-lia-en-bundle-en-deuxieme-cause/)

- **S2 — Copilot double environ le coût de la licence utilisateur.**
  Preuve : « opter pour Copilot de Microsoft fait environ doubler le coût de la licence utilisateur ». **Affirmation d'un cabinet de conseil en achats (Elée), pas du Cigref.** — [Le Monde Informatique, article 100293 cité ci-dessus](https://www.lemondeinformatique.fr/actualites/lire-l-inflation-gonfle-la-facture-cloud-et-logicielle-de-140-mdeteuro-par-an-100293.html)

- **S3 — Hausse des tarifs Microsoft 365 au 1er juillet 2026, justifiée par l'IA.**
  Symptôme : hausse au renouvellement, Copilot Chat ajouté aux suites de base, Microsoft 365 Copilot complet restant une option payante (environ 30 dollars par utilisateur et par mois). Preuve : hausses variables selon les suites ; les sources secondaires divergent (5 à 43 % pour l'une, 0 à 33 % pour d'autres ; Business Basic de 6 à 7 dollars, Business Standard de 12,50 à 14 dollars, Business Premium et Office 365 E1 inchangés). **Montants en dollars, sources secondaires contradictoires, grille en euros non vérifiée.** — [Solutions Numériques, « Microsoft 365 renchérit ses abonnements : l'IA a désormais un prix », 2026, date non vérifiée](https://www.solutions-numeriques.com/microsoft-365-rencherit-ses-abonnements-lia-a-desormais-un-prix/) ; [Nordflux, « Augmentation prix Microsoft 365 2026 »](https://nordflux.de/fr/ressources/microsoft-365-hausse-de-prix-2026) ; [Beancount, guide du 22 août 2026](https://beancount.io/fr/blog/2026/08/22/microsoft-365-price-increase-july-2026-commercial-rate-hike-budgeting-guide)

- **S4 — SAP restreint l'usage de ses API par des agents IA tiers.**
  Symptôme : un agent externe (non SAP) qui planifie et enchaîne des appels d'API SAP peut se retrouver hors contrat. Cause : section 2.2.2 de la SAP API Policy v4/2026, qui exclut l'usage des API pour l'interaction avec des systèmes d'IA (semi-)autonomes ou génératifs qui planifient, sélectionnent ou exécutent des séquences d'appels. Profil : clients SAP (grands comptes et ETI). Preuve et controverse : Forrester estime que SAP cherche à devenir le « gatekeeper » de l'IA d'entreprise, note l'absence de clause d'antériorité et indique que les agents tiers devraient passer par Joule après le quatrième trimestre 2026 ; Techzine lit la politique comme une interdiction des agents externes ; à l'inverse, un analyste Gartner cité par The Register affirme que la politique ne restreint pas l'accès des agents tiers. Les dates de publication citées divergent (février ou fin avril 2026 ; enregistrement obligatoire des agents externes au 1er octobre 2026 selon une source). Parade citée par Forrester : pas d'engagement de trois ans ou plus sans exceptions écrites. **Sources en anglais, non françaises ; aucune réaction de l'USF trouvée ; texte officiel SAP non consulté.** — [Forrester, blog « SAP Is Attempting To Become The Gatekeeper Of Enterprise AI »](https://www.forrester.com/blogs/sap-is-attempting-to-become-the-gatekeeper-of-enterprise-ai-cios-should-push-back/) ; [The Register, 19 mai 2026](https://www.theregister.com/saas/2026/05/19/saps-ai-strategy-come-for-the-openness-stay-because-you-have-to/5241109) ; [Techzine, « SAP blocks external AI agents, Salesforce and ServiceNow don't »](https://www.techzine.eu/blogs/applications/141323/sap-blocks-external-ai-agents-salesforce-and-servicenow-dont/) ; [Kai Waehner, 2 mai 2026](https://www.kai-waehner.de/blog/2026/05/02/data-ownership-in-the-age-of-agentic-ai-why-saps-api-policy-forces-a-data-integration-reckoning-for-every-enterprise/)

- **S5 — Crédits IA SAP prépayés et peu consommés.**
  Preuve : les clients souhaitant utiliser Joule ou les fonctions d'IA sont incités à acheter des crédits à l'avance ; « jusqu'à 99 % des clients » n'utiliseraient pas ces unités faute de scénarios productifs. **Analyse d'un média spécialisé de la communauté SAP, chiffre non sourcé officiellement, à traiter comme non vérifié.** — [E3 Magazine, « Le coût de l'IA pour un client SAP existant »](https://e3mag.com/fr/le-cout-de-ki-pour-un-client-sap-existant/)

- **S6 — Salesforce multiplie les modèles tarifaires pour l'IA agentique.**
  Preuve : selon LeMagIT, l'IA agentique force Salesforce à multiplier les modèles tarifaires, avec un risque de frictions avec des clients qui ancrent l'IA dans des « écosystèmes hybrides ». **Détail des tarifs non obtenu.** — [LeMagIT, rubrique Applications d'entreprise](https://www.lemagit.fr/actualites/Applications-dentreprise)

- **S7 — Pennylane : serveur MCP disponible, en lecture seule.**
  Fait produit (source éditeur) : MCP Pennylane publié le 4 août 2026, pour les cabinets et les entreprises en abonnement Essentiel ou supérieur ; l'IA accède aux données avec les droits de l'utilisateur, « en lecture seule pour commencer », écriture en développement ; authentification OAuth pour le MCP, tokens pour l'API. Conséquence auditable : pas d'automatisation en écriture (saisie, lettrage, paiement) via MCP à cette date. — [Pennylane, « Le MCP Pennylane est disponible »](https://www.pennylane.com/fr/blog/produit/mcp-pennylane) ; [page MCP](https://www.pennylane.com/fr/mcp)

- **S8 — Sage : plateforme agentique annoncée d'abord sur Sage Intacct ; rien trouvé pour Sage 100 et X3.**
  Fait produit (source éditeur, **novembre 2025**) : « AI Developer Solutions » et Sage AI Gateway (serveurs MCP et API REST), première phase centrée sur Sage Intacct. Un site tiers indique qu'il n'existe pas de serveur MCP, ni éditeur ni communautaire fiable, pour Sage 100 ou Sage X3. **Le second point vient d'un site tiers commercial : non vérifié.** — [Sage, communiqué de novembre 2025](https://www.sage.com/en-gb/company/digital-newsroom/2025/11/sage-launches-ai-developer-solutions-to-accelerate-partner-led-innovation/) ; [anythingmcp, guide Sage](https://anythingmcp.com/es/guides/sage-to-mcp)

- **S9 — Cegid : agents « Pulse » embarqués, API d'agents non documentée publiquement.**
  Fait produit (discours éditeur) : les agents Cegid Pulse « s'intègrent dans vos applications et vos processus métier, sans nécessiter de changer de logiciel » ; Cegid Loop annonce « plus de 20 moteurs d'IA » et une ouverture par API publiques. Aucune documentation d'API publique des agents Pulse ni de parcours de migration on-premise vers SaaS n'a été trouvée. — [Cegid, page « Logiciels IA »](https://www.cegid.com/fr/ia/) ; [Cegid, « IA pour les experts-comptables »](https://www.cegid.com/fr/ia/experts-comptables/)

- **S10 — Coût de mise à niveau du SI non imputé au projet IA.**
  Symptôme : cas d'usage rentable sur le papier, bloqué par un prérequis de montée de version. Preuve : « le coût d'une mise à niveau de SAP, d'un outil finance ou d'un logiciel RH, parfois indispensable pour un cas d'usage, n'est pas toujours imputé au projet IA, bien qu'il conditionne sa faisabilité et sa rentabilité ». — [EY France, communiqué « Agents, trop chers ! », 28 octobre 2026](https://www.ey.com/fr_fr/newsroom/2026/10/agents-ia-trop-chers-maitriser-cout-ia-agentique)

- **S11 — Dette technique et legacy (études mondiales relayées en France, sans coupe France).**
  Cognizant : 85 % des dirigeants doutent que leur SI puisse supporter des projets IA avancés ; causes citées : complexité des architectures existantes 63 %, manque de talents pour moderniser le code 50 %. — [Solutions Numériques, « Dette technologique : les entreprises doutent de leur capacité à supporter l'IA », date non vérifiée](https://www.solutions-numeriques.com/dette-technologique-les-entreprises-doutent-de-leur-capacite-a-supporter-lia/)
  Ensono : près de neuf responsables informatiques sur dix déclarent que la maintenance du legacy a entravé leurs projets de modernisation avec l'IA. — [Le Monde Informatique, « Les DSI règlent leur dette technique avec l'externalisation », date non vérifiée](https://www.lemondeinformatique.fr/actualites/lire-les-dsi-reglent-leur-dette-technique-avec-l-externalisation-98747.html)
  HFS Research (étude financée par l'éditeur Unqork) : 43 à 45 % des dirigeants anticipent que l'IA créera sa propre dette technique. — [Le Monde Informatique, « Les DSI divisés sur l'impact de l'IA sur la dette technologique », date non vérifiée](https://www.lemondeinformatique.fr/actualites/lire-les-dsi-divises-sur-l-impact-de-l-ia-sur-la-dette-technologique-98628.html)

- **S12 — SAP : maintenance on-premise en hausse.**
  Preuve : l'USF indique que SAP relève ses coûts de maintenance on-premise, hausse plafonnée à 5 %. **Interview dont la date n'a pas été vérifiée (identifiant d'article ancien, probablement antérieure à 2026).** — [Le Monde Informatique, interview de Gianmaria Perancin (USF)](https://www.lemondeinformatique.fr/actualites/lire-gianmaria-perancin-president-usf--sap-doit-clarifier-sa-position-vis-a-vis-des-clouds-de-confiance-91471.html)

### Inferences
- Le verrouillage par copilote embarqué prend trois formes observables en audit : (1) IA incluse d'office dans la licence avec hausse de prix, (2) crédits IA prépayés, (3) clauses d'API limitant les agents tiers. Les trois sont vérifiables dans les contrats et bons de commande.
- Pour une PME française sur Sage 100, EBP ou une version on-premise de Cegid, l'intégration d'un agent passe aujourd'hui par des connecteurs ou exports plutôt que par un protocole agentique natif ; c'est une inférence tirée de l'absence d'annonce trouvée, et non un fait établi.
- La controverse Forrester/Gartner sur SAP montre qu'un audit doit lire le texte contractuel en vigueur chez le client, et non s'appuyer sur la presse.

### Gaps
- Aucune information 2026 trouvée sur EBP, Divalto, Odoo, Oracle, Microsoft Dynamics ni sur la disponibilité d'API par version on-premise ou SaaS.
- Pas de chiffrage officiel en euros des hausses Microsoft 365, SAP ou Salesforce en France.
- Aucune étude française 2026 dédiée à la dette technique comme frein à l'IA.
- Mémo Cigref sur le retour sur investissement de l'IA générative et agentique : existence confirmée par un communiqué relayé, date et contenu non obtenus. — [windpress, communiqué Cigref](https://windpress.info/it/press-release/1054525/assessing-the-return-on-investment-of-generative-and-agentic-ai-solutions-cigref)

---

## 3. IA générative et agents en production : fiabilité, évaluation, limites du RAG, MCP, taux d'échec, dépréciation de modèles, performance en français

### Takeaway
Les taux d'échec les plus cités en France en 2026 restent des chiffres mondiaux (Gartner : plus de 40 % des projets agentiques abandonnés d'ici fin 2027, prévision de juin 2025) ; aucune statistique d'abandon propre à la France n'a été trouvée. Les faits français solides sont indirects : un tiers seulement des utilisateurs voit des gains (Banque de France), 30 % citent la confiance dans les résultats comme frein (Coface), et les agents restent rares en production.

### Cited Findings

- **G1 — Abandon des projets agentiques (prévision mondiale, 2025).**
  Gartner (juin 2025) : plus de 40 % des projets d'IA agentique seront abandonnés d'ici fin 2027 pour cause de coûts, de valeur métier limitée et de contrôle des risques insuffisant ; « agent washing » : environ 130 fournisseurs réellement agentiques parmi des milliers. **Source 2025, mondiale ; repose en partie sur un sondage de janvier 2025 auprès de participants à un webinaire.** Chiffre repris en 2026 par la presse française. — [Journal du Net, « Agents IA en entreprise : la facture qui surprend, les modèles qui disparaissent, et ce que les DSI font maintenant », 2026, date non vérifiée](https://www.journaldunet.com/intelligence-artificielle/1551391-agents-ia-en-entreprise-la-facture-qui-surprend-les-modeles-qui-disparaissent-et-ce-que-les-dsi-font-maintenant/) ; [Mobile World Live (français)](https://www.mobileworldlive.com/french/pour-gartner-plus-des-deux-tiers-des-projets-dia-agentique-sont-condamnes/)

- **G2 — Agents désactivés après incident (prévision 2026, source secondaire).**
  Une analyse Gartner de mai 2026 prévoirait que 40 % des entreprises rétrograderont ou désactiveront des agents autonomes d'ici 2027 après des failles de gouvernance révélées par un incident en production ; une étude Forrester/Anaconda indiquerait que 88 % des pilotes d'agents n'atteignent jamais la production. **Vu uniquement via un blog tiers : non vérifié, à ne pas citer sans la source primaire.** — [Blog P. Pillitteri, « Pourquoi les projets d'agents IA échouent en entreprise »](https://pasqualepillitteri.it/fr/news/19690/pourquoi-agents-ia-echouent-entreprise)

- **G3 — Modèles retirés sans préavis et coûts incontrôlés.**
  Symptôme : agent qui change de comportement ou cesse de fonctionner après le retrait d'un modèle par le fournisseur. Preuve : l'article du JDN décrit « coûts incontrôlés, modèles retirés sans préavis, concurrence chinoise 10x moins chère ». **Détail des modèles et des cas non obtenu.** — [Journal du Net, article 1551391](https://www.journaldunet.com/intelligence-artificielle/1551391-agents-ia-en-entreprise-la-facture-qui-surprend-les-modeles-qui-disparaissent-et-ce-que-les-dsi-font-maintenant/)

- **G4 — Agents peu présents en production en France.**
  Preuve : enquête EY publiée le 26 mars 2026 (18 152 personnes, 23 pays) : la France figure dans le groupe en retard avec le Royaume-Uni et le Japon, un peu plus de 70 % d'usage et l'un des plus faibles taux de délégation à l'IA. — [Le Monde Informatique, « L'IA est partout dans les entreprises, les agents presque nulle part »](https://www.lemondeinformatique.fr/actualites/lire-l-ia-est-partout-dans-les-entreprises-les-agents-presque-nulle-part-100750.html)

- **G5 — Stratégie sans mesure.**
  Preuve : 95 % des entreprises ont une stratégie IA, 8 % en mesurent réellement le retour sur investissement (KPMG AI Pulse Survey, mai 2026). **Périmètre géographique de l'enquête non vérifié.** — [KPMG France, communiqué de mai 2026](https://kpmg.com/fr/fr/media/press-releases/2026/05/ai-pulse-survey-2026.html) ; [Siècle Digital, 29 mai 2026](https://siecledigital.fr/2026/05/29/95-des-entreprises-ont-une-strategie-ia-mais-seules-8-savent-vraiment-ce-quelle-rapporte/)

- **G6 — Évaluation des RAG : deux méthodes imparfaites.**
  Preuve : Capgemini Invent France (arXiv, **juillet 2025**) : l'annotation humaine est précise mais coûteuse, l'évaluation par LLM-juge passe à l'échelle mais peut être biaisée ; proposition d'un protocole par domaine métier, à l'échelle de la phrase, pour localiser les hallucinations. **Source 2025.** — [arXiv 2507.21753](https://arxiv.org/pdf/2507.21753v1)

- **G7 — Hallucinations : deux familles, deux remèdes.**
  Preuve : conférence Devoxx France 2026 distinguant deux familles d'hallucinations aux causes et remèdes différents, avec une pile RAG type (LlamaIndex, Qdrant, Cohere). **Compte rendu de blog individuel.** — [Blog A. Lima, compte rendu Devoxx 2026](https://angelo-lima.fr/fr/hallucinations-llm-devoxx-2026/)

- **G8 — Performance en français : benchmarks encore jeunes.**
  Preuve : COLE (**2025**), 23 tâches de compréhension du français, 95 modèles évalués, écart important entre modèles fermés et modèles à poids ouverts ; difficultés : question-réponse extractive sans exemple, désambiguïsation fine, variations régionales. CARTE (2026), connaissances géographiques et régionales de la France, 27 LLM. SyntaxGym pour le français (LREC 2026). Atelier EvalLLM 2026 sur l'évaluation des LLM en français, motivé par des benchmarks « largement anglo-centrés », avec des chercheurs Inria au comité. — [COLE, arXiv 2510.05046](https://arxiv.org/pdf/2510.05046v2) ; [CARTE, arXiv 2606.01995](https://arxiv.org/html/2606.01995) ; [SyntaxGym for French, LREC 2026](https://preview.aclanthology.org/ingest-lrec/2026.lrec-main.178/) ; [EvalLLM 2026](https://evalllm2026.sciencesconf.org/?lang=en)

- **G9 — MCP : surface d'attaque et immaturité (voir aussi section 4).**
  Preuve : une trentaine à une quarantaine de CVE publiées sur des implémentations MCP entre janvier et avril 2026 selon des sources secondaires ; 36 % des serveurs MCP sans authentification selon l'une d'elles. **Chiffres de blogs et d'éditeurs de sécurité, non vérifiés.** — [Noqta, « MCP Security: 30 CVEs in 60 Days »](https://noqta.tn/en/blog/securite-serveurs-mcp-vulnerabilites-protection-guide-2026) ; [Techzine, « Rapid adoption of AI agents exposes structural weakness in MCP »](https://www.techzine.eu/news/privacy-compliance/138283/rapid-adoption-of-ai-agents-exposes-structural-weakness-in-mcp)

### Inferences
- Aucun taux d'échec ou d'annulation propre à la France n'existe dans les sources trouvées ; tout chiffre de ce type présenté comme « français » dans le corpus serait une extrapolation.
- Les trois dépendances à auditer pour un agent en production sont : version de modèle épinglée et date de retrait annoncée, jeu d'évaluation maison rejouable, journalisation des appels d'outils.
- Les benchmarks français existants mesurent la compréhension générale ; aucun ne mesure la performance sur des documents de gestion français (factures, paie, plan comptable).

### Gaps
- Pas de source 2026 de LeMagIT, Silicon.fr, ZDNet France, Next, Alliancy ou IT for Business consultée sur l'observabilité et l'évaluation.
- Pas de donnée sur la dérive de modèles ou les calendriers de dépréciation appliqués à des entreprises françaises.
- Pas de mesure indépendante 2026 comparant Mistral et les modèles américains sur des tâches métier en français.

---

## 4. Cybersécurité : injection de prompt, fuite de données, alertes ANSSI/CERT-FR 2026, attaques assistées par IA, sécurité des agents avec accès aux outils

### Takeaway
Le fait marquant de 2026 est le bulletin CERTFR-2026-ACT-016 du 13 avril 2026, par lequel le CERT-FR déconseille le déploiement d'agents IA autonomes sur les postes de travail (OpenClaw et Claude Cowork cités). Côté entreprises, 27 % des répondants du CESIN n'ont aucune politique d'usage de l'IA générative et plus de la moitié des usages relèveraient encore du shadow AI (Netskope, mondial). Aucun incident nommé touchant une entreprise française via un agent IA n'a été trouvé.

### Cited Findings

- **C1 — CERT-FR : pas d'agents autonomes sur les postes de travail.**
  Symptôme : agents installés par les salariés hors validation IT, avec accès à la messagerie, aux fichiers et aux secrets. Cause technique : droits excessifs, exécution d'actions non maîtrisées, exposition à l'injection de contenus. Preuve : bulletin CERTFR-2026-ACT-016 publié le 13 avril 2026 ; citation rapportée : « les assistants personnels autonomes tels qu'OpenClaw ne doivent pas être déployés sur des postes de travail et leur usage doit être proscrit » ; périmètre élargi aux « produits d'automatisation par IA agentique sur les postes de travail », OpenClaw et Claude Cowork nommés ; cinq risques relevés par les lectures de presse : compromission, fuite de données, droits excessifs, partage de secrets, actions non maîtrisées. Parades citées : recenser et retirer les agents non validés, gestion des comptes de messagerie utilisés, approbations d'exécution, isolement des processus (sandbox) ; postes Windows, Linux et mobiles visés. **Texte officiel non consulté ; détails issus de la presse et d'un cabinet juridique.** — [BDM, « OpenClaw, Claude Cowork : le CERT-FR met en garde contre les agents IA autonomes »](https://www.blogdumoderateur.com/openclaw-claude-cowork-cert-fr-agents-ia-autonomes/) ; [Clubic, « L'ANSSI alerte : OpenClaw est bien trop risqué sur votre poste de travail »](https://www.clubic.com/actualite-608878-l-anssi-alerte-openclaw-est-bien-trop-risque-sur-votre-poste-de-travail.html) ; [Leto, analyse du bulletin](https://www.leto.legal/news/anssi-ia-agentique-postes-travail-risques-2026)

- **C2 — ANSSI, Panorama de la cybermenace 2025 (publié le 11 mars 2026).**
  Preuve : chapitre « Évolution de l'outillage des attaquants » couvrant les capacités issues de l'IA ; l'IA générative peut accroître la sophistication des attaques ; la compromission d'un système d'IA peut entraîner des fuites de données sensibles ; une IA de génération de code compromise peut introduire des failles ; près de 29 % des vulnérabilités exploitées le jour même de leur divulgation ; 1 361 incidents (1 366 selon une autre source), niveau stable. Vincent Strubel présente l'IA comme un facteur qui comprime le calendrier plutôt que comme une menace entièrement nouvelle. — [ANSSI, Panorama de la cybermenace 2025](https://cyber.gouv.fr/nous-connaitre/publications/panoramas-de-la-cybermenace/panorama-de-la-cybermenace-2025/) ; [Vie publique, « Quel niveau de cybermenaces en 2025 ? »](https://www.vie-publique.fr/en-bref/302500-quel-niveau-de-cybermenaces-en-2025) ; [Solutions Numériques, « IA et cybersécurité : l'ANSSI appelle à sortir de l'obsession »](https://www.solutions-numeriques.com/ia-et-cybersecurite-lanssi-appelle-a-sortir-de-lobsession-pour-retrouver-la-vue-densemble/)

- **C3 — Référentiel ANSSI de sécurité de l'IA générative (2024, toujours la référence).**
  Preuve : guide « Recommandations de sécurité pour un système d'IA générative », 29 avril 2024, 35 recommandations sur tout le cycle de vie, scénarios d'attaque par manipulation, infection et exfiltration. **Source 2024 ; aucune mise à jour 2026 trouvée.** — [ANSSI, guide PDF](https://cyber.gouv.fr/sites/default/files/document/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf)

- **C4 — Absence de politique d'usage de l'IA générative.**
  Preuve : Instantanés du CESIN (21 mini-sondages au premier semestre 2026, 84 à 160 répondants selon les questions) : environ 27 % des répondants, surtout des ETI, n'ont défini aucune politique d'usage de l'IA générative ; l'outil est arrivé « par les navigateurs, les suites bureautiques déjà installées, les extensions et les abonnements personnels ». — [Solutions Numériques, « RSSI sommés d'arbitrer sur tous les fronts : les Instantanés du CESIN »](https://www.solutions-numeriques.com/rssi-sommes-darbitrer-sur-tous-les-fronts-les-instantanes-du-cesin/) ; [Leto, « Priorités 2026 : la conformité dans le trio de tête de 61 % des ETI, selon le CESIN »](https://www.leto.legal/news/cesin-instantanes-priorites-rssi-conformite-2026)

- **C5 — Baromètre CESIN (janvier 2026).**
  Preuve : près de 400 responsables cybersécurité interrogés ; 40 % des entreprises ont subi au moins une cyberattaque significative sur l'année ; vol de données en tête des conséquences (52 %) ; la souveraineté devient un enjeu de gestion du risque, plus d'une entreprise sur deux se déclarant concernée. **Chiffres spécifiques à l'IA non présents dans les extraits.** — [Le Journal des Entreprises, « Souveraineté numérique et cloud de confiance »](https://www.lejournaldesentreprises.com/article/souverainete-numerique-et-cloud-de-confiance-plus-dune-entreprise-sur-deux-se-declare-concernee-2140957) ; [Le Monde Informatique, « Baromètre CESIN 2025 : des attaques plus virulentes mais mieux maîtrisées »](https://www.lemondeinformatique.fr/actualites/lire-barometre-cesin-2025-des-attaques-plus-virulentes-mais-mieux-maitrisees-99136.html)

- **C6 — Shadow AI et fuite de données (mondial, source éditeur).**
  Preuve : rapport 2026 de Netskope Threat Labs : plus de la moitié des usages d'IA générative proviennent encore du shadow AI ; navigateurs IA et serveurs MCP attendus comme facteurs aggravants ; le rapport 2025 indiquait 72 % d'accès via des comptes personnels et un volume de données partagées multiplié par 30. **Source éditeur de sécurité, pas de coupe France.** — [Le Monde Informatique, « Le shadow IA, vecteur de fuites de données sensibles »](https://www.lemondeinformatique.fr/actualites/lire-le-shadow-ia-vecteur-de-fuites-de-donnees-sensibles-98993.html) ; [Solutions Numériques, « Les agents d'IA deviennent la nouvelle faille des entreprises »](https://www.solutions-numeriques.com/les-agents-dia-deviennent-la-nouvelle-faille-des-entreprises/)

- **C7 — Shadow IA persistant malgré interdiction (France).**
  Preuve : une entreprise sur huit constate que le shadow IA persiste malgré une interdiction claire (Baromètre IA Entreprise et Durabilité, ESSCA et Forvis Mazars, mars 2026, 826 professionnels). — [BDM, « IA en entreprise : quand la règle et la formation arrivent tard, l'usage s'installe seul »](https://www.blogdumoderateur.com/ia-entreprise-regle-formation-tard-usage-installe-seul/)

- **C8 — RSSI français et IA générative.**
  Preuve : les préoccupations de sécurité liées à l'IA générative gagnent 36 points en France pour atteindre 88 % (Proofpoint, Voice of the CISO 2026). **Source éditeur.** — [Proofpoint, communiqué France](https://www.proofpoint.com/fr/newsroom/press-releases/rapport-2026-voice-ciso-de-proofpoint-la-securisation-de-lia-generative)

- **C9 — Vulnérabilités MCP documentées en 2026.**
  Preuve : CVE-2026-27825 (CVSS 9.1) dans le serveur mcp-atlassian, écriture de fichier arbitraire via les pièces jointes Confluence menant à une exécution de code à distance ; CVE-2026-26118, faille SSRF dans les outils du serveur MCP Azure permettant le vol de jetons, corrigée par Microsoft le 10 mars 2026 ; avis OX Security du 15 avril 2026 décrivant une exécution de commandes liée à un choix de conception des SDK MCP officiels, plus de 200 000 serveurs évoqués, le concepteur ayant répondu « comportement attendu » ; analyse Enkrypt AI : plus de 143 000 vulnérabilités sur 25 000 serveurs, 73 % des serveurs touchés. Mécanisme : empoisonnement d'outils (les définitions d'outils sont examinées une fois à la connexion, les réponses circulent en continu dans le contexte de l'agent). Parades citées : inventaire des outils exposés, serveurs de sources vérifiées, authentification obligatoire, moindre privilège. **Sources secondaires et éditeurs de sécurité ; identifiants CVE à vérifier dans les bases officielles ; aucun cas français.** — [Noqta](https://noqta.tn/en/blog/securite-serveurs-mcp-vulnerabilites-protection-guide-2026) ; [Blog P. Pillitteri, avis OX Security](https://pasqualepillitteri.it/fr/news/1152/vulnerabilite-mcp-anthropic-200000-serveurs-ia-rce) ; [OECD.AI, incident 2026-02-26](https://oecd.ai/en/incidents/2026-02-26-2961)

- **C10 — Cybermalveillance : l'IA n'est pas encore un facteur massif démontré.**
  Preuve : rapport d'activité 2025 publié le 26 mars 2026 : hameçonnage en hausse de 70 % ; pour les entreprises et associations, piratage de compte 21 % des parcours (en hausse de 52 %), hameçonnage 16 %, faux ordres de virement 13,5 % ; le directeur général indique que « sauf cas très particuliers, on n'a pas encore d'utilisation massive démontrée de l'IA ». **Citation à vérifier et à dater.** — [Cybermalveillance.gouv.fr, communiqué](https://www.cybermalveillance.gouv.fr/medias/2026/03/CP-RA2026.pdf) ; [Le Monde Informatique, « Les demandes d'aide face aux cybermenaces explosent en France »](https://www.lemondeinformatique.fr/actualites/lire-les-demandes-d-aide-face-aux-cybermenaces-explosent-en-france-99756.html)

- **C11 — CNIL : sécurité du développement des systèmes d'IA (2025).**
  Preuve : recommandations finalisées le 22 juillet 2025, dont une fiche sur la sécurité du développement combinant analyse de sécurité classique et mesures propres à l'IA ; périmètre limité à la phase de développement, pas au déploiement ; fiche santé du 5 mars 2026. **Source principalement 2025 ; aucune fiche CNIL dédiée au RAG trouvée.** — [CNIL, finalisation des recommandations](https://cnil.fr/fr/ia-finalisation-recommandations-developpement-des-systemes-ia) ; [CNIL, IA et santé](https://www.cnil.fr/fr/ia-et-sante-developper-et-evaluer-des-systemes-dia-en-conformite-avec-la-reglementation)

- **C12 — Guide Campus Cyber.**
  Un « Guide d'implémentation Sécurité IA » est publié sur le wiki du Campus Cyber. **Date et contenu non obtenus.** — [Campus Cyber, PDF](https://wiki.campuscyber.fr/images/6/65/Guide_impl%C3%A9mentation_S%C3%A9curit%C3%A9_IA.pdf)

### Inferences
- Les sources officielles françaises 2026 (ANSSI, Cybermalveillance) minimisent l'idée d'une vague d'attaques « par IA » et insistent sur l'accélération et sur le risque porté par les systèmes d'IA eux-mêmes ; le risque documenté est interne (agents sur-habilités, shadow AI) avant d'être externe.
- Points de contrôle auditables : inventaire des agents et extensions IA sur les postes, comptes personnels utilisés pour l'IA, habilitations des connecteurs (messagerie, drive, ERP), présence d'une validation humaine avant action, journalisation des appels d'outils, origine des serveurs MCP.

### Gaps
- Aucun incident 2026 nommé et documenté d'une entreprise française compromise via injection de prompt ou via un agent n'a été trouvé.
- Texte intégral du bulletin CERTFR-2026-ACT-016 non lu ; l'URL officielle sur cert.ssi.gouv.fr n'est pas confirmée.
- Aucune source Clusif 2026 trouvée ; chiffres IA du baromètre CESIN de janvier 2026 non obtenus.

---

## 5. Souveraineté et infrastructure : dépendance aux hyperscalers, SecNumCloud, Mistral, GPU, capacité des centres de données

### Takeaway
L'offre IA qualifiée SecNumCloud reste étroite en 2026 : S3NS est qualifié depuis le 17 décembre 2025, OVHcloud a livré des GPU Nvidia L4 qualifiés, Bleu et Scaleway sont encore « en cours de qualification » selon une source d'octobre 2026. La capacité électrique n'est pas le facteur limitant en France, mais le raccordement l'est (2 à 7 ans selon RTE). L'infrastructure « souveraine » de Mistral repose sur des GPU Nvidia.

### Cited Findings

- **I1 — État des qualifications SecNumCloud (source secondaire, à vérifier sur le catalogue ANSSI).**
  Preuve : en octobre 2026, 3DS Outscale, OVHcloud, Cloud Temple, Worldline et Cegedim détiennent des qualifications IaaS ; Numspot (IaaS, septembre 2026) et S3NS (décembre 2025) ont annoncé la leur ; Scaleway et Bleu sont « en cours de qualification ». **Comparatif de blog commercial ; le catalogue officiel ANSSI fait foi.** — [Qovery, comparatif SecNumCloud](https://www.qovery.com/blog/numspot-ovhcloud-scaleway-secnumcloud-sovereign-cloud-comparison) ; [Solutions Numériques, « SecNumCloud : avec OVHcloud, Numspot rejoint le cercle restreint des clouds qualifiés »](https://www.solutions-numeriques.com/secnumcloud-avec-ovhcloud-numspot-rejoint-le-cercle-restreint-des-clouds-qualifies/)

- **I2 — S3NS : qualifié, IA en deuxième vague.**
  Preuve : qualification SecNumCloud 3.2 obtenue le 17 décembre 2025 ; deuxième vague de services attendue au premier semestre 2026 ; GPU à la demande avec Nvidia B200 annoncé « bientôt ». — [Le Monde Informatique, « Après le label SecNumCloud, S3NS met le cap sur l'IA et l'Europe », date non vérifiée](https://www.lemondeinformatique.fr/actualites/lire-apres-le-label-secnumcloud-s3ns-met-le-cap-sur-l-ia-et-l-europe-99384.html) ; [Futurum, analyse S3NS](https://futurumgroup.com/insights/s3ns-sovereignty-can-thales-google-venture-make-ai-sovereignty-work-at-scale/)

- **I3 — OVHcloud : premiers GPU qualifiés, de gamme inférence.**
  Preuve : Bare Metal POD annoncé qualifié SecNumCloud début avril ; premiers GPU qualifiés livrés, des Nvidia L4. **Année de l'annonce non vérifiée (article probablement de 2025).** Conséquence auditable : les GPU qualifiés disponibles sont dimensionnés pour l'inférence, pas pour l'entraînement de grands modèles. — [Journal du Net, « Comparatif des clouds souverains dans l'IA : OVHcloud se démarque », date non vérifiée](https://www.journaldunet.com/cloud/1541471-comparatif-des-clouds-souverains-dans-l-ia-ovhcloud-se-demarque/)

- **I4 — Bleu : disponibilité commerciale tardive.**
  Preuve : jalon J0 validé le 17 avril 2025, disponibilité commerciale prévue au second semestre 2026 ; l'ANSSI a indiqué que rien ne s'oppose à la qualification de Bleu et S3NS. **Sources secondaires.** — [Tech Insider, comparatif cloud souverain 2026](https://tech-insider.org/fr/cloud-souverain-vs-cloud-public-2026/) ; [Next, « SecNumCloud : pour l'ANSSI, rien ne s'oppose à la qualification de Bleu et S3NS »](https://next.ink/186562/secnumcloud-pour-lanssi-rien-ne-soppose-a-la-qualification-de-bleu-et-s3ns)

- **I5 — Mistral AI : capacité propre en construction, sur matériel Nvidia.**
  Preuve : environ 830 millions de dollars de dette levés (annonce du 30 mars 2026) pour un centre de données à Bruyères-le-Châtel (Essonne), environ 44 MW et 13 800 puces Nvidia GB300 ; mise en service annoncée pour fin juin 2026 ou le second semestre 2026 selon les sources ; site d'inférence de 10 MW aux Ulis annoncé en mai 2026 ; objectif de 200 MW en Europe fin 2027 ; projet de campus de 1,4 GW avec MGX, Bpifrance et Nvidia. **Capacités divergentes selon les sources (40, 44, jusqu'à 60 MW) ; mise en service effective non confirmée.** — [SiliconANGLE, 30 mars 2026](https://siliconangle.com/?p=736800) ; [Unite.AI](https://www.unite.ai/mistral-ai-secures-830-million-in-debt-to-build-paris-data-center/) ; [DataCenterDynamics, campus 1,4 GW](https://www.datacenterdynamics.com/br/not%C3%ADcias/mgx-bpifrance-nvidia-e-mistral-ai-planejam-campus-de-data-center-de-14-gw-em-paris/)

- **I6 — Raccordement électrique : le vrai goulot.**
  Preuve : en mai 2026, RTE avait réservé près de 18 GW pour environ 80 projets de centres de données, contre 5 GW fin 2024 ; puissance totale demandée d'environ 28,6 GW ; délais de raccordement de 2 à 7 ans, jusqu'à neuf ans en zones tendues d'Île-de-France ; les centres raccordés depuis deux ou trois ans n'utilisent en moyenne qu'environ 20 % de la puissance demandée ; RTE ne s'inquiète pas de la capacité de production. Cinq sites « fast track » priorisés pour plus de 700 MW sous trois à quatre ans, 26 sites sécurisés. **Chiffres RTE repris par la presse, bilan RTE non consulté.** — [Techniques de l'Ingénieur, « Les opérateurs de datacenters font face à des délais de raccordement qui s'allongent »](https://www.techniques-ingenieur.fr/actualite/articles/les-operateurs-de-datacenters-font-face-a-des-delais-de-raccordement-qui-sallongent-156141/) ; [Next, « Datacenters en France : 26 sites sécurisés, dont 5 projets fast track »](https://next.ink/222076/datacenters-en-france-26-sites-securises-dont-5-projets-fast-track-dau-moins-700-mw/) ; [Banque des Territoires, Institut Paris Région](https://www.banquedesterritoires.fr/linstitut-paris-region-alerte-sur-lexplosion-des-besoins-electriques-des-datacenters-franciliens)

- **I7 — Marché public et IA souveraine.**
  Preuve : l'État fait évoluer son marché cloud pour permettre aux administrations de souscrire à des offres d'IA souveraine, « à l'image des modèles de Mistral AI déployés sur infrastructure SecNumCloud ». **Source secondaire, date non vérifiée.** — [Tech Insider](https://tech-insider.org/fr/cloud-souverain-vs-cloud-public-2026/)

- **I8 — Autonomie stratégique vue par le Cigref.**
  Preuve : David Krieff (Cigref) : « L'IA et les plateformes nous obligent à repenser notre autonomie stratégique ». **Titre d'interview seulement, contenu non obtenu.** — [CIO Mag](https://cio-mag.com/?p=60700)

### Inferences
- Pour une entreprise soumise à une exigence SecNumCloud, le choix de modèles et de GPU qualifiés reste limité en 2026 ; les modèles de pointe américains ne sont accessibles en périmètre qualifié que via S3NS (technologie Google) et, à terme, Bleu (technologie Microsoft), ce qui déplace la dépendance au niveau logiciel plutôt qu'elle ne la supprime. C'est une inférence à partir des faits I1 à I4.
- La souveraineté de Mistral est opérationnelle et juridique, pas matérielle (GPU Nvidia).

### Gaps
- Aucune donnée 2026 trouvée sur la part de marché des hyperscalers américains dans les charges IA des entreprises françaises, ni sur les prix et délais d'accès aux GPU en France.
- Aucune information sur les contraintes de latence ou de localisation d'hébergement.
- Offres IA d'Outscale et de Scaleway non documentées ; catalogue ANSSI non consulté.

---

## 6. Coûts et environnement : coût total de possession, prévisibilité, empreinte énergétique, référentiel AFNOR « IA frugale », reporting

### Takeaway
En 2026, le coût devient un frein technique à part entière : les licences augmentent (section 2), la consommation des agents est difficile à prévoir, et EY France publie en octobre 2026 un communiqué intitulé « Agents, trop chers ! ». Côté environnement, l'Arcep constate en mai 2026 que 84 % des modèles d'IA ne publient aucune information environnementale, ce qui rend le reporting de l'empreinte IA impraticable par mesure directe.

### Cited Findings

- **E1 — Coût réel des agents sous-estimé.**
  Symptôme : dossiers d'investissement qui n'intègrent ni le calcul ni les prérequis de SI. Preuve : EY recommande de « piloter le véritable coût IT », les agents consommant de la puissance de calcul fournie par le cloud ou par des GPU internes ; la valeur d'usage des agents est jugée « difficile à dire contrairement aux précédentes innovations technologiques (Cloud, SaaS…) » ; EY juge risquée une course générale aux agents. — [EY France, « Agents, trop chers ! », 28 octobre 2026](https://www.ey.com/fr_fr/newsroom/2026/10/agents-ia-trop-chers-maitriser-cout-ia-agentique)

- **E2 — Budgets et coûts d'infrastructure des agents permanents.**
  Preuve : budget moyen d'IA en entreprise passé de 1,2 million de dollars par an en 2024 à 7 millions en 2026 ; agents « toujours actifs » pouvant dépasser 200 000 dollars de coûts d'infrastructure mensuels pour une seule application. **Chiffres mondiaux en dollars, source d'origine non identifiée dans l'extrait.** — [Journal du Net, article 1551391](https://www.journaldunet.com/intelligence-artificielle/1551391-agents-ia-en-entreprise-la-facture-qui-surprend-les-modeles-qui-disparaissent-et-ce-que-les-dsi-font-maintenant/)

- **E3 — Repli vers des modèles moins coûteux.**
  Preuve : « l'émergence des agents d'IA a fait exploser la facture IA de bon nombre d'entreprises, qui se tournent vers des modèles moins coûteux ». **Dépêche reprise, périmètre mondial, 2 juin 2026 d'après l'URL.** — [FashionUnited, « Les entreprises se tournent vers de l'IA moins gourmande, sur fond de flambée des coûts »](https://fashionunited.fr/actualite/business/les-entreprises-se-tournent-vers-de-lia-moins-gourmande-sur-fond-de-flambee-des-couts/2026060241907)

- **E4 — Coût variable à anticiper (source consulaire).**
  La CCI Lyon Métropole publie une actualité « IA agentique : un coût variable à anticiper ». **Contenu non obtenu.** — [CCI Lyon Métropole](https://www.lyon-metropole.cci.fr/actualite/ia-agentique-un-cout-variable-anticiper)

- **E5 — Retour sur investissement non mesuré.**
  Preuve : un DSI sur deux ne mesure pas ce que l'IA en bundle rapporte (Cigref/Asterès, mai 2026) ; 8 % des entreprises mesurent réellement le ROI de l'IA (KPMG, mai 2026, périmètre non vérifié). — [ActuIA, Cigref](https://www.actuia.com/actualite/cigref-140-mdeur-de-surcouts-cloud-en-europe-lia-en-bundle-en-deuxieme-cause/) ; [KPMG, communiqué](https://kpmg.com/fr/fr/media/press-releases/2026/05/ai-pulse-survey-2026.html)

- **E6 — Arcep : opacité environnementale de l'IA générative.**
  Preuve : rapport « Intelligence artificielle générative : quels défis environnementaux ? », 21 mai 2026 ; les centres de données sont la composante la plus influente ; l'inférence devient le principal enjeu ; 84 % des modèles d'IA ne font l'objet d'aucune information environnementale ; neuf recommandations, dont des méthodologies d'évaluation normalisées et la collecte de données par les pouvoirs publics ; proposition d'un critère d'achat public « IA frugale » fondé sur le RGESN et le référentiel IA frugale. Consommation électrique des centres de données en France : 2,7 TWh en 2024, hausse de 38 % en trois ans ; les centres mis en service en 2024 atteignent 20 MW en moyenne. — [Arcep, rapport du 21 mai 2026](https://www.arcep.fr/uploads/tx_gspublication/rapport-IA-et-environnement_210526.pdf) ; [Siècle Digital, 26 mai 2026](https://siecledigital.fr/2026/05/26/larcep-tire-la-sonnette-dalarme-sur-limpact-ecologique-de-lia-generative/) ; [Banque des Territoires](https://www.banquedesterritoires.fr/datacenters-larcep-salarme-de-lexplosion-de-lempreinte-environnementale) ; [Acteurs publics, clause IA frugale](https://acteurspublics.fr/articles/pour-limiter-limpact-environnemental-larcep-propose-dintegrer-une-clause-ia-frugale-dans-les-marches-publics/)

- **E7 — ADEME : avis IA de juillet 2026.**
  Preuve : l'ADEME renvoie aux bonnes pratiques d'écoconception du référentiel général pour l'IA frugale de l'AFNOR et sa prospective 2026 prévoit une croissance très forte de la consommation d'énergie des centres de données pour les usages français, portée notamment par l'IA. **Chiffres non obtenus (recherche non exécutée, PDF inaccessible).** — [ADEME, communiqué de juillet 2026](https://www.ademe.fr/wp-content/uploads/2026/07/cp-ademe-avis-ia-072026.pdf)

- **E8 — Référentiel AFNOR « IA frugale » (2024).**
  Preuve : AFNOR SPEC 2314, publiée en juin 2024, six mois de travail et 150 contributeurs, méthodologies de calcul et bonnes pratiques, gratuite, d'application volontaire. **Source 2024 ; aucune nouvelle version 2026 trouvée.** — [AFNOR, présentation du référentiel](https://www.afnor.org/en/news/artificial-intelligence/reference-framework-reduce-environmental-impact-ai/) ; [Ministère de la Transition écologique, 28 juin 2024](https://www.ecologie.gouv.fr/presse/publication-du-referentiel-general-lia-frugale-sattaquer-limpact-environnemental-lia)

- **E9 — Empreinte du numérique en France (2025).**
  Preuve : 4,4 % de l'empreinte carbone nationale, soit 29,5 MtCO2e en 2022 (mise à jour 2025 de l'étude ADEME-Arcep). **Source 2025, vue via un résumé.** — [Ministère de l'Économie, « IA en entreprise : quels impacts environnementaux ? »](https://www.entreprises.gouv.fr/decryptages-de-nos-experts/intelligence-artificielle-en-entreprise-quels-impacts-environnementaux)

- **E10 — Standardisation de la mesure en cours.**
  Preuve : présentation Boavizta à l'Assemblée nationale (24 juin 2026) qualifiant 2026 d'année de la standardisation de l'évaluation de l'impact environnemental de l'IA. **Diapositive, sans détail.** — [Assemblée nationale, support Boavizta](https://hackathon2026.assemblee-nationale.fr/supports-conferences/2_AliceDRAHON__2026%2006%2024%20-%20Assembl%C3%A9%20nationale%20IA%20frugale%20-%20Boavizta.pdf)

### Inferences
- Avec 84 % de modèles sans information environnementale, une entreprise ne peut aujourd'hui chiffrer l'empreinte de ses usages IA que par estimation (facteurs d'émission génériques) ; c'est une contrainte technique directe pour tout reporting de durabilité qui inclurait les services numériques achetés.
- Le coût total de possession d'un agent comporte au moins cinq postes auditables : licences par siège, consommation de tokens ou crédits, intégration et montée de version du SI, exploitation et évaluation continue, sécurité. Seuls les deux premiers apparaissent en général dans les devis.

### Gaps
- Aucune source trouvée sur l'articulation entre CSRD et empreinte de l'IA (recherche non exécutée, quota atteint).
- Aucun prix de tokens ou barème de consommation d'agents en euros, aucune étude française de coût total de possession.
- Chiffres de l'avis ADEME de juillet 2026 et contenu du mémo Cigref sur le ROI non obtenus.

---

## Bibliographie

Légende : **Ouvert ?** = la page a-t-elle été ouverte et lue. Réponse « non » partout : seuls des extraits de résultats de recherche ont été vus. Type : O = institution ou autorité publique ; A = analyste, cabinet ou association professionnelle ; E = éditeur ou fournisseur (discours commercial) ; P = presse ; R = recherche académique ; B = blog ou site tiers peu fiable.

### Sources publiées en 2026

| # | Titre | Éditeur | Date | URL | Type | Ouvert ? |
|---|---|---|---|---|---|---|
| 1 | Panorama de la cybermenace 2025 | ANSSI | 11 mars 2026 | https://cyber.gouv.fr/nous-connaitre/publications/panoramas-de-la-cybermenace/panorama-de-la-cybermenace-2025/ | O | non |
| 2 | Quel niveau de cybermenaces en 2025 ? | Vie publique | 2026, jour non vérifié | https://www.vie-publique.fr/en-bref/302500-quel-niveau-de-cybermenaces-en-2025 | O | non |
| 3 | OpenClaw, Claude Cowork : le CERT-FR met en garde contre les agents IA autonomes (bulletin CERTFR-2026-ACT-016 du 13 avril 2026) | BDM | avril 2026, jour non vérifié | https://www.blogdumoderateur.com/openclaw-claude-cowork-cert-fr-agents-ia-autonomes/ | P | non |
| 4 | L'ANSSI alerte : OpenClaw est bien trop risqué sur votre poste de travail | Clubic | 2026, jour non vérifié | https://www.clubic.com/actualite-608878-l-anssi-alerte-openclaw-est-bien-trop-risque-sur-votre-poste-de-travail.html | P | non |
| 5 | IA agentique au bureau : l'ANSSI déconseille formellement tout déploiement en production | Leto | avril 2026, jour non vérifié | https://www.leto.legal/news/anssi-ia-agentique-postes-travail-risques-2026 | B | non |
| 6 | IA et cybersécurité : l'ANSSI appelle à sortir de l'obsession | Solutions Numériques | 2026, jour non vérifié | https://www.solutions-numeriques.com/ia-et-cybersecurite-lanssi-appelle-a-sortir-de-lobsession-pour-retrouver-la-vue-densemble/ | P | non |
| 7 | RSSI sommés d'arbitrer sur tous les fronts : les Instantanés du CESIN | Solutions Numériques | 2026, jour non vérifié | https://www.solutions-numeriques.com/rssi-sommes-darbitrer-sur-tous-les-fronts-les-instantanes-du-cesin/ | P | non |
| 8 | Priorités 2026 : la conformité dans le trio de tête de 61 % des ETI, selon le CESIN | Leto | 2026, jour non vérifié | https://www.leto.legal/news/cesin-instantanes-priorites-rssi-conformite-2026 | B | non |
| 9 | Souveraineté numérique et cloud de confiance : plus d'une entreprise sur deux se déclare concernée (baromètre CESIN, janvier 2026) | Le Journal des Entreprises | 2026, jour non vérifié | https://www.lejournaldesentreprises.com/article/souverainete-numerique-et-cloud-de-confiance-plus-dune-entreprise-sur-deux-se-declare-concernee-2140957 | P | non |
| 10 | Baromètre CESIN 2025 : des attaques plus virulentes mais mieux maîtrisées | Le Monde Informatique | janvier 2026, jour non vérifié | https://www.lemondeinformatique.fr/actualites/lire-barometre-cesin-2025-des-attaques-plus-virulentes-mais-mieux-maitrisees-99136.html | P | non |
| 11 | Communiqué, rapport d'activité 2025 | Cybermalveillance.gouv.fr | 26 mars 2026 | https://www.cybermalveillance.gouv.fr/medias/2026/03/CP-RA2026.pdf | O | non |
| 12 | Les demandes d'aide face aux cybermenaces explosent en France | Le Monde Informatique | mars 2026, jour non vérifié | https://www.lemondeinformatique.fr/actualites/lire-les-demandes-d-aide-face-aux-cybermenaces-explosent-en-france-99756.html | P | non |
| 13 | Le shadow IA, vecteur de fuites de données sensibles (rapport Netskope 2026) | Le Monde Informatique | 2026, jour non vérifié | https://www.lemondeinformatique.fr/actualites/lire-le-shadow-ia-vecteur-de-fuites-de-donnees-sensibles-98993.html | P | non |
| 14 | Les agents d'IA deviennent la nouvelle faille des entreprises | Solutions Numériques | 2026, jour non vérifié | https://www.solutions-numeriques.com/les-agents-dia-deviennent-la-nouvelle-faille-des-entreprises/ | P | non |
| 15 | Rapport 2026 Voice of the CISO : la sécurisation de l'IA générative, nouvelle priorité des RSSI français | Proofpoint | 2026, jour non vérifié | https://www.proofpoint.com/fr/newsroom/press-releases/rapport-2026-voice-ciso-de-proofpoint-la-securisation-de-lia-generative | E | non |
| 16 | IA en entreprise : quand la règle et la formation arrivent tard, l'usage s'installe seul (baromètre ESSCA / Forvis Mazars, mars 2026) | BDM | 2026, jour non vérifié | https://www.blogdumoderateur.com/ia-entreprise-regle-formation-tard-usage-installe-seul/ | P | non |
| 17 | MCP Security: 30 CVEs in 60 Days | Noqta | 2026, jour non vérifié | https://noqta.tn/en/blog/securite-serveurs-mcp-vulnerabilites-protection-guide-2026 | B | non |
| 18 | Vulnérabilité MCP : 200 000 serveurs IA exposés (avis OX Security du 15 avril 2026) | Blog P. Pillitteri | avril 2026, jour non vérifié | https://pasqualepillitteri.it/fr/news/1152/vulnerabilite-mcp-anthropic-200000-serveurs-ia-rce | B | non |
| 19 | Security Risks of Autonomous AI Agents Using MCP in Enterprises | OECD.AI (base d'incidents) | 26 février 2026 | https://oecd.ai/en/incidents/2026-02-26-2961 | O | non |
| 20 | Rapid adoption of AI agents exposes structural weakness in MCP | Techzine | 2026, jour non vérifié | https://www.techzine.eu/news/privacy-compliance/138283/rapid-adoption-of-ai-agents-exposes-structural-weakness-in-mcp | P | non |
| 21 | L'inflation gonfle la facture cloud et logicielle de 140 Md€ par an (étude Cigref / Asterès) | Le Monde Informatique | mai 2026, jour non vérifié | https://www.lemondeinformatique.fr/actualites/lire-l-inflation-gonfle-la-facture-cloud-et-logicielle-de-140-mdeteuro-par-an-100293.html | P | non |
| 22 | Cigref : 140 Md€ de surcoûts cloud en Europe, l'IA en bundle en deuxième cause | ActuIA | mai 2026, jour non vérifié | https://www.actuia.com/actualite/cigref-140-mdeur-de-surcouts-cloud-en-europe-lia-en-bundle-en-deuxieme-cause/ | P | non |
| 23 | Microsoft 365 renchérit ses abonnements : l'IA a désormais un prix | Solutions Numériques | 2026, jour non vérifié | https://www.solutions-numeriques.com/microsoft-365-rencherit-ses-abonnements-lia-a-desormais-un-prix/ | P | non |
| 24 | Guide hausse de prix Microsoft 365 juillet 2026 | Beancount | 22 août 2026 | https://beancount.io/fr/blog/2026/08/22/microsoft-365-price-increase-july-2026-commercial-rate-hike-budgeting-guide | B | non |
| 25 | SAP Is Attempting To Become The Gatekeeper Of Enterprise AI — CIOs Should Push Back | Forrester (blog) | 2026, jour non vérifié | https://www.forrester.com/blogs/sap-is-attempting-to-become-the-gatekeeper-of-enterprise-ai-cios-should-push-back/ | A | non |
| 26 | SAP's AI strategy: come for the openness, stay because you have to | The Register | 19 mai 2026 | https://www.theregister.com/saas/2026/05/19/saps-ai-strategy-come-for-the-openness-stay-because-you-have-to/5241109 | P | non |
| 27 | SAP blocks external AI agents, Salesforce and ServiceNow don't | Techzine | 2026, jour non vérifié | https://www.techzine.eu/blogs/applications/141323/sap-blocks-external-ai-agents-salesforce-and-servicenow-dont/ | P | non |
| 28 | Data Ownership in the Age of Agentic AI: Why SAP's API Policy Forces a Data Integration Reckoning | Kai Waehner (blog) | 2 mai 2026 | https://www.kai-waehner.de/blog/2026/05/02/data-ownership-in-the-age-of-agentic-ai-why-saps-api-policy-forces-a-data-integration-reckoning-for-every-enterprise/ | B | non |
| 29 | Le MCP Pennylane est disponible | Pennylane | 4 août 2026 | https://www.pennylane.com/fr/blog/produit/mcp-pennylane | E | non |
| 30 | Agents, trop chers ! | EY France | 28 octobre 2026 | https://www.ey.com/fr_fr/newsroom/2026/10/agents-ia-trop-chers-maitriser-cout-ia-agentique | A | non |
| 31 | Agents IA en entreprise : la facture qui surprend, les modèles qui disparaissent, et ce que les DSI font maintenant | Journal du Net | 2026, jour non vérifié | https://www.journaldunet.com/intelligence-artificielle/1551391-agents-ia-en-entreprise-la-facture-qui-surprend-les-modeles-qui-disparaissent-et-ce-que-les-dsi-font-maintenant/ | P | non |
| 32 | Les entreprises se tournent vers de l'IA moins gourmande, sur fond de flambée des coûts | FashionUnited (reprise de dépêche) | 2 juin 2026 (d'après l'URL) | https://fashionunited.fr/actualite/business/les-entreprises-se-tournent-vers-de-lia-moins-gourmande-sur-fond-de-flambee-des-couts/2026060241907 | P | non |
| 33 | Étude Trends of AI 2026 : l'IA s'ancre dans le pilotage transverse des organisations | KPMG France | 23 janvier 2026 | https://kpmg.com/fr/fr/media/press-releases/2026/01/adoption-ia-entreprises-francaises.html | A | non |
| 34 | Tendances IA : adoption par les fonctions de l'entreprise | KPMG France | 2026, jour non vérifié | https://kpmg.com/fr/fr/insights/dirigeants/tendances-ia-adoption-fonctions-entreprise.html | A | non |
| 35 | IA : 95 % des entreprises ont une stratégie, mais seulement 8 % en mesurent réellement le ROI | KPMG France | mai 2026, jour non vérifié | https://kpmg.com/fr/fr/media/press-releases/2026/05/ai-pulse-survey-2026.html | A | non |
| 36 | Six entreprises sur dix utilisent l'IA sans cadre, selon Coface (baromètre du 5 octobre 2026) | ActuIA | octobre 2026, jour non vérifié | https://www.actuia.com/actualite/six-entreprises-sur-dix-utilisent-lia-sans-cadre-selon-coface/ | P | non |
| 37 | Baromètre France Num 2026 : quatre TPE-PME sur dix utilisent désormais l'intelligence artificielle | DGE / France Num | 28 septembre 2026 | https://www.entreprises.gouv.fr/espace-presse/barometre-france-num-2026-quatre-tpe-pme-sur-dix-utilisent-desormais-lintelligence | O | non |
| 38 | 40 % des TPE-PME utilisent l'IA, mais 19 % seulement la paient | ActuIA | 2026, jour non vérifié | https://www.actuia.com/actualite/40-des-tpe-pme-utilisent-lia-mais-19-seulement-la-paient/ | P | non |
| 39 | IA, cyber, budgets : 10 chiffres sur le numérique dans les TPE et PME en 2026 | BDM | 2026, jour non vérifié | https://www.blogdumoderateur.com/ia-cyber-budgets-10-chiffres-numerique-tpe-pme-2026/ | P | non |
| 40 | L'IA s'installe dans les entreprises françaises : une diffusion rapide mais des gains de productivité encore limités (Bulletin n° 266) | Banque de France | 3 septembre 2026 (4 septembre selon une autre source) | https://www.banque-france.fr/fr/publications-et-statistiques/publications/lia-sinstalle-dans-les-entreprises-francaises-une-diffusion-rapide-mais-des-gains-de-productivite | O | non |
| 41 | Eco Notepad n° 451 | Banque de France | mai 2026, jour non vérifié | https://www.banque-france.fr/system/files/2026-05/Billet_451_VF.pdf | O | non |
| 42 | Le tournant de l'IA pour la France : un marché équilibré exposé au risque d'une progression trop lente | Infor | avril 2026, jour non vérifié | https://www.infor.com/fr-fr/blog/france-ai-market-slow-adoption-risk | E | non |
| 43 | L'IA est partout dans les entreprises, les agents presque nulle part | Le Monde Informatique | 2026, jour non vérifié | https://www.lemondeinformatique.fr/actualites/lire-l-ia-est-partout-dans-les-entreprises-les-agents-presque-nulle-part-100750.html | P | non |
| 44 | La stratégie IA entravée par la dette technique sur les données | Le Monde Informatique | 2026, jour non vérifié | https://www.lemondeinformatique.fr/actualites/lire-la-strategie-ia-entravee-par-la-dette-technique-sur-les-donnees-100038.html | P | non |
| 45 | L'IA agentique révèle les fragilités des fondations data des entreprises | Solutions Numériques | 2026, jour non vérifié | https://www.solutions-numeriques.com/?p=247498 | P | non |
| 46 | Intelligence artificielle générative : quels défis environnementaux ? | Arcep | 21 mai 2026 | https://www.arcep.fr/uploads/tx_gspublication/rapport-IA-et-environnement_210526.pdf | O | non |
| 47 | L'Arcep tire la sonnette d'alarme sur l'impact écologique de l'IA générative | Siècle Digital | 26 mai 2026 | https://siecledigital.fr/2026/05/26/larcep-tire-la-sonnette-dalarme-sur-limpact-ecologique-de-lia-generative/ | P | non |
| 48 | Pour limiter l'impact environnemental, l'Arcep propose d'intégrer une clause IA frugale dans les marchés publics | Acteurs publics | mai 2026, jour non vérifié | https://acteurspublics.fr/articles/pour-limiter-limpact-environnemental-larcep-propose-dintegrer-une-clause-ia-frugale-dans-les-marches-publics/ | P | non |
| 49 | Communiqué, avis de l'ADEME sur l'IA | ADEME | juillet 2026, jour non vérifié | https://www.ademe.fr/wp-content/uploads/2026/07/cp-ademe-avis-ia-072026.pdf | O | non |
| 50 | Support Boavizta, IA frugale | Assemblée nationale (hackathon 2026) | 24 juin 2026 | https://hackathon2026.assemblee-nationale.fr/supports-conferences/2_AliceDRAHON__2026%2006%2024%20-%20Assembl%C3%A9%20nationale%20IA%20frugale%20-%20Boavizta.pdf | O | non |
| 51 | Les opérateurs de datacenters font face à des délais de raccordement qui s'allongent | Techniques de l'Ingénieur | 2026, jour non vérifié | https://www.techniques-ingenieur.fr/actualite/articles/les-operateurs-de-datacenters-font-face-a-des-delais-de-raccordement-qui-sallongent-156141/ | P | non |
| 52 | Datacenters en France : 26 sites sécurisés, dont 5 projets fast track d'au moins 700 MW | Next | 2026, jour non vérifié | https://next.ink/222076/datacenters-en-france-26-sites-securises-dont-5-projets-fast-track-dau-moins-700-mw/ | P | non |
| 53 | Mistral, financement de 830 M$ pour un centre de données | SiliconANGLE | 30 mars 2026 | https://siliconangle.com/?p=736800 | P | non |
| 54 | Après le label SecNumCloud, S3NS met le cap sur l'IA et l'Europe | Le Monde Informatique | date non vérifiée (fin 2025 ou début 2026) | https://www.lemondeinformatique.fr/actualites/lire-apres-le-label-secnumcloud-s3ns-met-le-cap-sur-l-ia-et-l-europe-99384.html | P | non |
| 55 | SecNumCloud : avec OVHcloud, Numspot rejoint le cercle restreint des clouds qualifiés | Solutions Numériques | 2026, jour non vérifié | https://www.solutions-numeriques.com/secnumcloud-avec-ovhcloud-numspot-rejoint-le-cercle-restreint-des-clouds-qualifies/ | P | non |
| 56 | NumSpot, OVHcloud, Scaleway: SecNumCloud sovereign cloud comparison | Qovery | octobre 2026 (d'après le texte), jour non vérifié | https://www.qovery.com/blog/numspot-ovhcloud-scaleway-secnumcloud-sovereign-cloud-comparison | E | non |
| 57 | CARTE: A Benchmark for Mapping Language Model… | arXiv | 2026 (identifiant de juin 2026) | https://arxiv.org/html/2606.01995 | R | non |
| 58 | SyntaxGym for French | LREC 2026 | mai 2026 | https://preview.aclanthology.org/ingest-lrec/2026.lrec-main.178/ | R | non |
| 59 | Atelier EvalLLM 2026 | Sciencesconf | 2026 | https://evalllm2026.sciencesconf.org/?lang=en | R | non |
| 60 | IA et santé : développer et évaluer des systèmes d'IA en conformité | CNIL | 5 mars 2026 | https://www.cnil.fr/fr/ia-et-sante-developper-et-evaluer-des-systemes-dia-en-conformite-avec-la-reglementation | O | non |

### Sources 2025 ou antérieures, ou de date non établie (utilisées faute d'équivalent 2026)

| # | Titre | Éditeur | Date | URL | Type | Ouvert ? |
|---|---|---|---|---|---|---|
| A1 | Recommandations de sécurité pour un système d'IA générative | ANSSI | 29 avril 2024 | https://cyber.gouv.fr/sites/default/files/document/Recommandations_de_s%C3%A9curit%C3%A9_pour_un_syst%C3%A8me_d_IA_g%C3%A9n%C3%A9rative.pdf | O | non |
| A2 | Référentiel général pour l'IA frugale (AFNOR SPEC 2314) | AFNOR | juin 2024 | https://www.afnor.org/en/news/artificial-intelligence/reference-framework-reduce-environmental-impact-ai/ | O | non |
| A3 | IA : la CNIL finalise ses recommandations sur le développement des systèmes d'IA | CNIL | 22 juillet 2025 | https://cnil.fr/fr/ia-finalisation-recommandations-developpement-des-systemes-ia | O | non |
| A4 | Baromètre IA Salesforce x OpinionWay | Salesforce | 14 mars 2025 | https://www.salesforce.com/fr/news/press-releases/2025/03/14/barometre-ia-salesforce-x-opinionway-les-entreprises-francaises-misent-sur-les-agents-autonomes-pour-accelerer-leur-transformation-grace-a-lia/ | E | non |
| A5 | Sage launches AI developer solutions | Sage | novembre 2025 | https://www.sage.com/en-gb/company/digital-newsroom/2025/11/sage-launches-ai-developer-solutions-to-accelerate-partner-led-innovation/ | E | non |
| A6 | Évaluation de RAG en secteurs à risque | arXiv (Capgemini Invent France) | juillet 2025 | https://arxiv.org/pdf/2507.21753v1 | R | non |
| A7 | COLE: a Comprehensive Benchmark for French Language Understanding Evaluation | arXiv | octobre 2025 | https://arxiv.org/pdf/2510.05046v2 | R | non |
| A8 | Prévision Gartner sur l'abandon des projets agentiques (juin 2025), relais francophone | Mobile World Live | 2025, jour non vérifié | https://www.mobileworldlive.com/french/pour-gartner-plus-des-deux-tiers-des-projets-dia-agentique-sont-condamnes/ | P | non |
| A9 | Comparatif des clouds souverains dans l'IA : OVHcloud se démarque | Journal du Net | date non vérifiée (probablement 2025) | https://www.journaldunet.com/cloud/1541471-comparatif-des-clouds-souverains-dans-l-ia-ovhcloud-se-demarque/ | P | non |
| A10 | Interview de G. Perancin (USF) sur SAP | Le Monde Informatique | date non vérifiée (probablement antérieure à 2026) | https://www.lemondeinformatique.fr/actualites/lire-gianmaria-perancin-president-usf--sap-doit-clarifier-sa-position-vis-a-vis-des-clouds-de-confiance-91471.html | P | non |
| A11 | Dette technologique : les entreprises doutent de leur capacité à supporter l'IA (Cognizant) | Solutions Numériques | date non vérifiée | https://www.solutions-numeriques.com/dette-technologique-les-entreprises-doutent-de-leur-capacite-a-supporter-lia/ | P | non |
| A12 | Les DSI règlent leur dette technique avec l'externalisation (Ensono) | Le Monde Informatique | date non vérifiée | https://www.lemondeinformatique.fr/actualites/lire-les-dsi-reglent-leur-dette-technique-avec-l-externalisation-98747.html | P | non |
| A13 | Les projets IA révèlent les défis de la qualité des données | Le Monde Informatique | date non vérifiée | https://www.lemondeinformatique.fr/actualites/lire-les-projets-ia-revelent-les-defis-de-la-qualite-des-donnees-99083.html | P | non |
| A14 | Le coût de l'IA pour un client SAP existant | E3 Magazine | date non vérifiée | https://e3mag.com/fr/le-cout-de-ki-pour-un-client-sap-existant/ | P | non |
| A15 | Logiciels IA Cegid / IA pour les experts-comptables | Cegid | pages non datées | https://www.cegid.com/fr/ia/ | E | non |
| A16 | Baromètre national DSI Data & IA (DaVinciDoc) | BDM (guide) | date non vérifiée | https://www.blogdumoderateur.com/guides/barometre-national-dsi-data-ia-maturite-reelle-organisations-francaises/ | E | non |
| A17 | Intelligence artificielle en entreprise : quels impacts environnementaux ? | Ministère de l'Économie | date non vérifiée | https://www.entreprises.gouv.fr/decryptages-de-nos-experts/intelligence-artificielle-en-entreprise-quels-impacts-environnementaux | O | non |
| A18 | Guide d'implémentation Sécurité IA | Campus Cyber | date non vérifiée | https://wiki.campuscyber.fr/images/6/65/Guide_impl%C3%A9mentation_S%C3%A9curit%C3%A9_IA.pdf | A | non |
