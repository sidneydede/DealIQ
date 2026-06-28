# Cahier des charges — Plateforme privée de qualification, préparation et matching PME ↔ investisseurs (UEMOA / CEMAC)

**Objet :** Spécifications fonctionnelles, UX/UI et techniques de la plateforme\
**Nom de code projet :** DealIQ *(nom de marque à confirmer)*\
**Version :** 1.1 — Intégration des spécifications UX/UI\
**Date :** Juin 2026\
**Statut :** Pour validation\
**Maître d'ouvrage (MOA) :** Cabinet de conseil financier *(le « Cabinet »)*\
**Zone cible :** UEMOA (prioritaire : 2 pays) + CEMAC (1 pays)\
**Confidentialité :** Strictement confidentiel\
**Fondé sur :** Cadrage AMOA + Revue critique du projet (juin 2026)

> **Note de lecture.** Document à **audience mixte** : le corps (parties 1 à 5, 9 à 13) est accessible aux décideurs, sponsors et financeurs ; les spécifications fonctionnelles détaillées (partie 6), **UX/UI & design** (partie 7) et techniques (partie 8) ainsi que les annexes s'adressent à l'équipe de réalisation (interne ou prestataire). Chaque fonctionnalité est **taguée par phase** : **[MVP]** (pilote 90 jours), **[V1]** (12 mois), **[V2]** (18-24 mois). Les éléments réglementaires sont **indicatifs** et doivent être validés par des avocats spécialisés UEMOA/CEMAC/OHADA.

---

# 1. Synthèse exécutive

## 1.1 Objet

Ce cahier des charges définit le périmètre fonctionnel et technique d'une **plateforme privée, curée et B2B** permettant au Cabinet de (1) capter et qualifier des entrepreneurs en recherche de financement, (2) mesurer leur niveau de préparation (*readiness*) et les transformer en dossiers réellement investissables via des services payants, puis (3) apporter aux financeurs (PE, VC, fonds de dette, impact funds, family offices, banques, DFI, corporates) un *dealflow* filtré, documenté et exécutable jusqu'au closing.

## 1.2 Le produit en une phrase

> Une infrastructure privée qui rend les PME d'Afrique francophone **bancables** avant de les exposer aux financeurs, et qui donne aux financeurs un **dealflow préparé et pré-qualifié**, orchestré jusqu'au closing — opérée par une équipe d'experts, outillée par une plateforme.

## 1.3 Principes directeurs (issus de la revue critique)

1. **Services-first, pas plateforme-first.** La valeur naît du conseil et de la curation humaine ; le logiciel outille, il ne remplace pas. Le moat est la **donnée propriétaire + la réputation**, jamais l'algorithme.
2. **Manual-first, automate-what-scales.** Toute fonction est d'abord opérée manuellement, puis outillée quand le volume et la preuve de valeur le justifient.
3. **Buy / Partner pour la commodité, Build pour l'avantage.** On achète VDR, e-signature, KYC/AML, paiement ; on construit le funnel, le scoring, le modèle de données, la lecture OHADA/SYSCOHADA.
4. **Qui paie d'abord : l'institution.** Le programme sponsorisé (DFI/banque) est l'ancre de revenu MVP/V1 ; l'entrepreneur (cash-pauvre) ne verse qu'un ticket d'engagement ; le success fee est un *upside*.
5. **Curation impitoyable + sourcing actif.** On ne présente jamais un dossier non « investor-ready » ; on *source activement* la qualité plutôt que de seulement filtrer l'inbound (anti-sélection adverse).
6. **Confidentialité graduée (privacy-by-design).** Anonymisation par défaut, accès par niveaux, NDA + non-circonvention, traçabilité complète.
7. **Conformité by-design.** Positionnement « préparation et conseil » + placement privé à investisseurs qualifiés ; jamais d'appel public à l'épargne ni de promesse de financement.
8. **Mobile-first, low-bandwidth, collecte progressive.** Adapté aux usages réels de la zone.

## 1.4 Phasage en un coup d'œil

| Phase | Horizon | Cœur | Objectif de preuve |
|---|---|---|---|
| **MVP (couche 1)** | 0-4 mois | Funnel entrepreneur : onboarding → readiness → mini-rapport → packs ; CRM/reporting | Les entrepreneurs viennent **et paient** la préparation |
| **V1 (couche 2 + 3)** | 4-16 mois | Référentiel & matching investisseurs, teaser, NDA, **VDR achetée**, KYC, pipeline, mandats/fees | Les investisseurs **s'engagent** ; 1ers closings ; 1 programme sponsorisé |
| **V2 (scale)** | 16-24 mois | DD OHADA/SYSCOHADA, ESG, deal execution avancé, market intelligence, multi-pays | Industrialisation, récurrence, défendabilité |

## 1.5 Conditions de succès

Geler le périmètre MVP sur la couche 1 ; sécuriser l'avis juridique sur l'intermédiation ; ancrer un sponsor institutionnel ; élargir la cible financeur aux instruments de dette ; mettre en place une stratégie de sourcing actif. **Plus gros piège à éviter :** construire la plateforme biface complète avant d'avoir prouvé manuellement l'économie du deal et l'adoption des deux faces.

---

# 2. Contexte, enjeux et objectifs

## 2.1 Contexte marché

Les MSME représentent > 90 % des entreprises, ~70 % de l'emploi et ~50 % du PIB ; le déficit de financement MSME atteint 5,7 Tn$ (8 Tn$ avec l'informel — IFC). En Afrique de l'Ouest, les PME sont perçues comme risquées faute de taille, d'historique et de **documentation** (Banque mondiale). Le private capital africain est en phase sélective : ~73 deals / ~0,3 Md$ en Afrique de l'Ouest en 2025 (AVCA) — **le marché valorise peu de dossiers, mais de meilleurs dossiers, plus vite**. Les usages sont mobile-first : bancarisation UEMOA stricte 25,2 % / élargie 47,4 % (2024) ; mobile money > 2 Md comptes (GSMA).

**Implication produit :** un *moteur* automatisé de matching est prématuré à ce volume ; la valeur est la **préparation** et la **curation**.

## 2.2 Contexte réglementaire

OHADA (17 États, SYSCOHADA révisé) pour le droit des sociétés, les sûretés et la comptabilité ; **AMF-UMOA / CREPMF** pour le marché financier UEMOA ; **COSUMAF** pour la CEMAC. Toute offre publique exige une note d'information visée ; le placement privé relève d'un autre régime (information moindre, investisseur procédant à sa propre évaluation). **Conséquence structurante :** plateforme **privée**, curée, à **investisseurs qualifiés**, accès gradués — **jamais** une marketplace ouverte au public. Point de vigilance non tranché : l'acte d'**intermédiation rémunérée / démarchage** peut nécessiter un statut, *indépendamment* du caractère privé (à valider).

## 2.3 Problème à résoudre

Côté entrepreneurs : « Suis-je finançable, par quel instrument, qu'est-ce qui manque à mon dossier ? » et l'incapacité à produire un dossier bancable. Côté financeurs : sourcing fiable rare, dossiers peu documentés et coûteux à instruire (DD difficile sur comptes SYSCOHADA faibles). Côté Cabinet : coût d'acquisition élevé, conversion incertaine, difficulté à industrialiser le conseil.

## 2.4 Objectifs du projet

**Objectifs business :** réduire le CAC du Cabinet (inbound qualifié) ; augmenter la conversion vers missions payantes ; constituer un actif propriétaire (base de dossiers qualifiés + critères investisseurs) ; ouvrir des revenus institutionnels (programmes sponsorisés).

**Objectifs produit (SMART, indicatifs à confirmer en Phase 0) :**

| # | Objectif | Cible | Échéance |
|---|---|---|---|
| O1 | Taux de complétion du diagnostic | ≥ 40 % | Fin MVP |
| O2 | Conversion diagnostic → pack payant | ≥ 15 % | Fin MVP |
| O3 | Packs de préparation vendus | ≥ 3 | Fin MVP |
| O4 | Taux teaser → intérêt investisseur | ≥ 30 % | Fin pilote |
| O5 | Dossiers entrés en DD / term sheet | ≥ 1 | Fin pilote |
| O6 | Programme sponsorisé signé | 1 | Fin V1 |

## 2.5 Facteurs clés de succès & hypothèses à valider

H1 — des entrepreneurs *cibles* viennent et complètent ; H2 — un sous-ensemble paie la préparation ; H3 — les investisseurs s'engagent sur un dealflow curé ; H4 — le TAM de PME bancables est suffisant ; H5 — l'activité reste juridiquement défendable. **Aucune n'est prouvée à ce jour** : le MVP existe pour les tester (voir §13).

---

# 3. Vision produit & principes directeurs

## 3.1 Positionnement

**Boutique de conseil tech-enabled** (marges projet, scalabilité humaine outillée) — *ni* SaaS pur, *ni* marketplace à effets de réseau. Le volet « plateforme investisseur » et la logique d'abonnement sont une **option de croissance** (V1+), pas le cœur initial.

**Énoncé de positionnement :** *« Nous rendons les PME d'Afrique francophone bancables, puis nous apportons aux financeurs un dealflow préparé et pré-qualifié — par une équipe d'experts, outillée par une plateforme. »*

## 3.2 Proposition de valeur par persona

| Persona | Promesse | Preuve / livrable |
|---|---|---|
| Entrepreneur | « Sachez pourquoi on vous dit non, et devenez finançable » | Mini-rapport readiness + dossier bancable |
| Investisseur (PE/VC/dette/DFI) | « Un dealflow pré-qualifié, propre, filtré sur *vos* critères » | Teasers curés + data room structurée |
| Cabinet | Canal d'acquisition + industrialisation du conseil | Pipeline qualifié, productivité |
| Sponsor institutionnel (DFI/banque) | Préparer et déployer du capital vers le *missing middle* | Cohorte PME préparées + reporting/impact |

## 3.3 Principes directeurs détaillés

Reprend §1.3 et les décline en règles de conception : (a) tout module a un **mode manuel** documenté avant tout build ; (b) toute donnée sensible est **anonymisée par défaut** ; (c) toute mise en relation passe par une **validation humaine** et un contrôle conformité ; (d) toute donnée IA porte un **label de fiabilité** et une **validation humaine** ; (e) aucune fonction n'entre en MVP si elle n'est pas indispensable à la couche 1.

## 3.4 Hors périmètre (anti-scope)

**Explicitement exclus** (au moins jusqu'à V2, voire définitivement) : marketplace ouverte au public ; appel public à l'épargne ; gestion de fonds pour compte de tiers ; conseil en investissement *aux investisseurs* ; scoring exposé aux investisseurs comme label de qualité ; moteur de matching automatique en MVP ; VDR propriétaire ; application mobile native en MVP (web responsive d'abord) ; comptabilité/ERP ; signature électronique maison ; scraping/veille proactive de masse.

---

# 4. Parties prenantes & personas

## 4.1 Personas

- **Entrepreneur cible** — PME « solide mais mal préparée » : activité réelle, comptes SYSCOHADA faibles, pas de BP crédible, accès limité aux financeurs. Mobile, asynchrone, méfiant (peur fiscale). *Besoin :* comprendre sa bancabilité, obtenir un dossier, accéder aux bons financeurs.
- **Investisseur** — distinguer : (a) **equity** PE/VC/impact ; (b) **dette/mezzanine/garanties** (le plus pertinent pour le missing middle) ; (c) **DFI** (additionnalité, impact, gouvernance). *Besoin :* sourcing fiable, dossiers DD-ables, fit avec la thèse.
- **Consultant Cabinet** — analyste (qualification/enrichissement), consultant senior (préparation, relation investisseur), responsable conformité, responsable plateforme/ops.
- **Sponsor institutionnel** — DFI/banque/agence finançant des cohortes de préparation PME.
- **Administrateur** — gestion des rôles, sécurité, paramétrage, audit.

## 4.2 Matrice RACI macro

| Activité | Entrepreneur | Analyste | Consultant senior | Conformité | Admin |
|---|---|---|---|---|---|
| Saisie du dossier | R | C | I | I | I |
| Qualification / readiness | C | R | A | I | I |
| Préparation du dossier | C | R | A | I | I |
| Curation / matching | I | C | R/A | C | I |
| KYC / NDA / conflits | I | I | C | R/A | I |
| Mise en relation | I | I | R | A | I |
| Paramétrage / sécurité | — | I | I | C | R/A |

*(R=Réalise, A=Approuve, C=Consulté, I=Informé)*

---

# 5. Périmètre fonctionnel & phasage

## 5.1 Cartographie des modules

M1 Comptes/rôles/accès · M2 Référentiel entreprises · M3 Onboarding & qualification entrepreneur · M4 Collecte documentaire · M5 Financing Readiness Score · M6 Mini-rapport & recommandation d'instrument · M7 Catalogue de services & conversion · M8 Espace mission / préparation · M9 Référentiel investisseurs & critères · M10 Matching · M11 Teaser & anonymisation · M12 Mise en relation, NDA & non-circonvention · M13 Data room · M14 Q&A & messagerie · M15 KYC/KYB/AML · M16 Pipeline deal execution · M17 Mandats & honoraires · M18 DD OHADA/SYSCOHADA · M19 ESG/impact · M20 CRM cabinet · M21 Reporting & dashboards · M22 Administration & audit · M23 Programmes sponsorisés.

## 5.2 Matrice de phasage

| Module | MVP | V1 | V2 | Build/Buy |
|---|:--:|:--:|:--:|---|
| M1 Comptes / rôles / accès | ● | + | | Build (RBAC simple) |
| M2 Référentiel entreprises | ● | + | | Build léger |
| M3 Onboarding & qualification | ● | + | | Build |
| M4 Collecte documentaire | ● | + | | Build + stockage acheté |
| M5 Readiness Score | ● (interne) | + | | Build |
| M6 Mini-rapport & reco instrument | ● | + | | Build |
| M7 Catalogue services & conversion | ● | + | | Build léger |
| M8 Espace mission / préparation | ◐ (léger) | ● | + | Build |
| M9 Référentiel investisseurs | ◐ (tableur) | ● | | Build léger |
| M10 Matching | ○ (manuel) | ● | + | Manuel→Build |
| M11 Teaser & anonymisation | ◐ (gabarit) | ● | | Manuel→Build |
| M12 Mise en relation / NDA | ○ (manuel/e-sign) | ● | | Buy e-sign + Build workflow |
| M13 Data room | ○ (acheté) | ● | + | **Buy** |
| M14 Q&A & messagerie | ○ (email) | ● | | Email→Build léger |
| M15 KYC/KYB/AML | ○ (manuel) | ● | + | **Buy/API** |
| M16 Pipeline deal execution | ◐ (statuts) | ◐ | ● | Build (tard) |
| M17 Mandats & honoraires | ◐ (léger) | ● | | Build |
| M18 DD OHADA/SYSCOHADA | | ◐ | ● | Build (différenciateur) |
| M19 ESG/impact | | ● (si DFI) | + | Build checklist |
| M20 CRM cabinet | ● | + | | **Buy** (HubSpot/Airtable) |
| M21 Reporting & dashboards | ◐ (léger) | ● | + | Buy BI (Metabase) |
| M22 Administration & audit | ● | + | | Build minimal |
| M23 Programmes sponsorisés | ◐ (process) | ● | + | Build léger |

*Légende : ● cœur de phase · ◐ version allégée · ○ opéré manuellement / via outil acheté · + enrichissement · (vide) hors phase.*

## 5.3 Critères de passage de phase

| Passage | Condition (go) |
|---|---|
| MVP → V1 | O1 (complétion ≥ 40 %) **et** O2/O3 (conversion payante prouvée) **et** ≥ 1 deal en DD manuelle |
| V1 → V2 | Unit economics positives par dossier ; ≥ N closings ; 1 programme sponsorisé signé ; rétention investisseur |
| V2 → Scale | Rentabilité par marché ; pipeline DFI multi-pays ; processus DD industrialisé |

---

# 6. Spécifications fonctionnelles détaillées

> Convention : chaque user story (US) et règle de gestion (RG) est taguée par phase. Les critères d'acceptation listés sont les **clés** (non exhaustifs) ; ils seront complétés en backlog. Format US : *« En tant que [rôle], je veux [action] afin de [bénéfice]. »*

## 6.1 M1 — Comptes, rôles & accès **[MVP]**

**Objectif.** Authentifier les utilisateurs, gérer les rôles et garantir le moindre privilège.

**User stories.**
- US-M1-01 [MVP] En tant qu'utilisateur, je veux créer un compte (email + mot de passe + OTP) afin d'accéder à mon espace.
- US-M1-02 [MVP] En tant qu'entrepreneur, je veux valider mon email/téléphone (OTP) afin de sécuriser mon compte.
- US-M1-03 [MVP] En tant qu'admin, je veux attribuer des rôles (entrepreneur, investisseur, analyste, senior, conformité, admin) afin de contrôler les accès.
- US-M1-04 [V1] En tant qu'utilisateur, je veux activer le MFA afin de renforcer la sécurité.
- US-M1-05 [V1] En tant qu'investisseur, je veux être invité (par lien) afin d'accéder à un espace fermé.

**Règles de gestion.**
- RG-M1-01 Modèle RBAC : un rôle ↔ un ensemble de permissions (cf. Annexe B).
- RG-M1-02 Mot de passe : politique de complexité + hachage fort (bcrypt/argon2) ; jamais en clair.
- RG-M1-03 Session expirante + révocation possible ; jetons signés (JWT court + refresh).
- RG-M1-04 Tout accès et changement de droit est journalisé (audit trail, M22).

**Critères d'acceptation.** Un utilisateur sans rôle ne voit aucune donnée métier ; un changement de rôle est tracé ; l'OTP expire ; le verrouillage après N tentatives fonctionne.

**Dépendances.** M22 (audit), M15 (qualification investisseur).

## 6.2 M2 — Référentiel entreprises **[MVP]**

**Objectif.** Base maître des PME (actif propriétaire du Cabinet).

**User stories.**
- US-M2-01 [MVP] En tant qu'analyste, je veux une fiche entreprise unique (identité, secteur, pays, taille, besoin) afin de centraliser le dossier.
- US-M2-02 [MVP] En tant qu'analyste, je veux détecter/fusionner les doublons afin de garder une base propre.
- US-M2-03 [V1] En tant qu'analyste, je veux un historique des versions de la fiche afin de tracer l'évolution.

**Règles de gestion.**
- RG-M2-01 Clé d'unicité : RCCM + pays (à défaut, nom normalisé + pays).
- RG-M2-02 Champs obligatoires minimaux à la création : nom, pays, secteur.
- RG-M2-03 Statut du dossier : *brouillon / qualifié / en préparation / investor-ready / en deal / clos / archivé*.
- RG-M2-04 Données financières marquées « déclaré / non audité » tant que non vérifiées par pièces.

**Critères d'acceptation.** Pas de doublon non signalé ; toute fiche a un statut ; le passage de statut est tracé.

## 6.3 M3 — Onboarding & qualification entrepreneur **[MVP]**

**Objectif.** Capter la demande et le niveau de préparation via un questionnaire progressif, mobile-first.

**User stories.**
- US-M3-01 [MVP] En tant qu'entrepreneur, je veux répondre à 6-8 questions clés (secteur, pays, CA en fourchette, besoin, usage des fonds, stade) afin d'obtenir un premier verdict en < 10 minutes.
- US-M3-02 [MVP] En tant qu'entrepreneur, je veux pouvoir interrompre et reprendre afin de m'adapter à une connexion mobile instable.
- US-M3-03 [MVP] En tant qu'entrepreneur, je veux un questionnaire à logique conditionnelle afin de ne voir que les questions pertinentes.
- US-M3-04 [V1] En tant qu'analyste, je veux des seuils d'éligibilité (gating) afin d'écarter les dossiers hors cible.

**Règles de gestion.**
- RG-M3-01 La première session ne demande que le strict minimum ; les documents sensibles sont demandés **plus tard** (après l'effet « wow »).
- RG-M3-02 Sauvegarde automatique à chaque étape ; reprise via lien/relogin.
- RG-M3-03 Gating : pays/secteur hors cible, besoin sous un seuil, incohérence majeure → orientation/nurturing, pas pipeline investisseur.
- RG-M3-04 Consentement explicite (traitement des données) requis avant enregistrement.

**Critères d'acceptation.** Complétion possible sur smartphone ; reprise sans perte ; un dossier hors cible n'entre pas dans le pipeline ; consentement horodaté.

**Dépendances.** M5, M22, conformité (§11).

## 6.4 M4 — Collecte documentaire & checklist **[MVP]**

**Objectif.** Mesurer la maturité documentaire réelle et préparer la vérification.

**User stories.**
- US-M4-01 [MVP] En tant qu'entrepreneur, je veux téléverser mes pièces (RCCM, statuts, états financiers, pitch, BP) afin de compléter mon dossier.
- US-M4-02 [MVP] En tant qu'entrepreneur, je veux voir une checklist (pièces reçues / manquantes) afin de savoir quoi fournir.
- US-M4-03 [V1] En tant qu'analyste, je veux un statut de vérification par pièce (reçu / vérifié / rejeté) afin de fiabiliser le scoring.

**Règles de gestion.**
- RG-M4-01 Types de fichiers contrôlés (PDF, images, xlsx) + taille max + anti-malware.
- RG-M4-02 Chaque pièce porte un statut et un horodatage ; intégrité par hash.
- RG-M4-03 Confidentialité fiscale : message rassurant + accès strictement limité (cf. §12) afin de lever la réticence au partage.

**Critères d'acceptation.** Upload mobile fonctionnel ; checklist à jour en temps réel ; pièce vérifiée non modifiable sans trace.

## 6.5 M5 — Financing Readiness Score **[MVP — usage interne]**

**Objectif.** Trier et orienter (outil interne + hook entrepreneur), sans fausse précision.

**User stories.**
- US-M5-01 [MVP] En tant qu'analyste, je veux un score multi-dimensions (cf. Annexe C) afin de prioriser l'effort.
- US-M5-02 [MVP] En tant qu'entrepreneur, je veux connaître ma **catégorie** (investor-ready / à préparer / plutôt dette-banque / trop précoce) et mes gaps afin d'agir.
- US-M5-03 [V1] En tant qu'analyste, je veux recalculer le score après vérification des pièces afin d'obtenir un score fiable.

**Règles de gestion.**
- RG-M5-01 **Gating documentaire** : pas de score « élevé » sans pièces vérifiées.
- RG-M5-02 Pondérations explicites (Annexe C) ; dimensions subjectives (scalabilité, ESG) plafonnées et traitées en commentaire qualitatif.
- RG-M5-03 Affichage d'un **indice de confiance** ; mention « provisoire, sous réserve de vérification ».
- RG-M5-04 **Visibilité** : entrepreneur = catégorie + gaps ; Cabinet = score complet ; **investisseur = jamais** le score auto-attribué (au plus, label « revu et validé par le Cabinet »).

**Critères d'acceptation.** Un score élevé sans pièces vérifiées est impossible ; l'entrepreneur ne voit pas le détail brut ; chaque calcul est tracé avec sa version de grille.

**Dépendances.** M4, M6, Annexe C.

## 6.6 M6 — Mini-rapport & recommandation d'instrument **[MVP]**

**Objectif.** Livrer un verdict utile et actionnable (effet « wow »).

**User stories.**
- US-M6-01 [MVP] En tant qu'entrepreneur, je veux un mini-rapport (catégorie + 3-5 blocages + instrument adapté + ce qui me sépare d'un dossier bancable) afin de comprendre ma situation.
- US-M6-02 [MVP] En tant qu'entrepreneur, je veux recevoir ce rapport en PDF/web afin de le conserver/partager.
- US-M6-03 [MVP] En tant qu'analyste, je veux que le rapport propose les services adaptés afin d'amorcer la conversion.

**Règles de gestion.**
- RG-M6-01 Orientation instrument : equity / dette / quasi-equity / subvention selon profil de cash-flow, besoin, garanties.
- RG-M6-02 Aucune promesse de financement ; formulation conforme (§11).
- RG-M6-03 Chaque gap → un service recommandé (lien vers M7).

**Critères d'acceptation.** Rapport généré automatiquement ; contenu personnalisé ; disclaimers présents.

## 6.7 M7 — Catalogue de services & conversion **[MVP]**

**Objectif.** Transformer le diagnostic en mission payante (tunnel commercial).

**User stories.**
- US-M7-01 [MVP] En tant qu'entrepreneur, je veux voir un catalogue d'offres (diagnostic+, packs préparation, mandat) avec prix/contenu afin de choisir.
- US-M7-02 [MVP] En tant qu'entrepreneur, je veux prendre rendez-vous avec un consultant afin de discuter mon dossier.
- US-M7-03 [MVP] En tant qu'analyste, je veux un devis contextualisé (selon les gaps) afin d'accélérer la vente.
- US-M7-04 [V1] En tant qu'entrepreneur, je veux payer en ligne (carte / mobile money) afin de souscrire un pack.

**Règles de gestion.**
- RG-M7-01 Architecture tarifaire : Gratuit / Diagnostic+ / Préparation (paliers) / Mandat (retainer + success fee) (cf. §9).
- RG-M7-02 Anti « pay-to-play » : payer n'augmente pas la probabilité d'être **sélectionné** pour présentation investisseur ; seule la qualité du dossier le fait — affiché explicitement.
- RG-M7-03 En MVP, paiement = devis/facturation manuelle ; paiement en ligne en V1.

**Critères d'acceptation.** Le catalogue est visible ; un RDV se prend ; le message anti-pay-to-play est présent.

## 6.8 M8 — Espace mission / préparation de dossier **[MVP léger → V1]**

**Objectif.** Produire les livrables (BP, modèle financier, valorisation, teaser, data room initiale) en collaboration cabinet ↔ entrepreneur.

**User stories.**
- US-M8-01 [MVP] En tant que consultant, je veux un espace mission par dossier (tâches, pièces, statut) afin de piloter la production.
- US-M8-02 [V1] En tant que consultant, je veux le versionnage des livrables et une validation cabinet afin de garantir la qualité.
- US-M8-03 [V1] En tant qu'entrepreneur, je veux suivre l'avancement de ma mission afin de rester informé.

**Règles de gestion.**
- RG-M8-01 Checklist « investor-ready » obligatoire avant tout passage en curation (M10).
- RG-M8-02 Double validation (analyste + senior) avant présentation investisseur.
- RG-M8-03 Modèles standardisés (BP, teaser, modèle financier) versionnés.

**Critères d'acceptation.** Un dossier ne devient « investor-ready » qu'après checklist + double validation tracées.

## 6.9 M9 — Référentiel investisseurs & critères **[MVP tableur → V1]**

**Objectif.** Base maître des financeurs et de leurs thèses (condition du matching).

**User stories.**
- US-M9-01 [MVP] En tant qu'analyste, je veux une fiche investisseur (type, juridiction, équipe, contacts) afin de gérer la relation.
- US-M9-02 [MVP] En tant qu'analyste, je veux paramétrer les critères d'investissement (pays, secteur, **instrument**, ticket, stade, exclusions, ESG) afin de filtrer le dealflow.
- US-M9-03 [V1] En tant qu'investisseur, je veux gérer moi-même mes critères afin de recevoir un flux pertinent.

**Règles de gestion.**
- RG-M9-01 Typologie financeur : equity (PE/VC/impact), dette/mezzanine/garanties, DFI, family office, corporate, banque.
- RG-M9-02 Critères structurés (filtres durs) + champs « appétence » (historique de deals) pour la pondération.
- RG-M9-03 Liste d'exclusions par investisseur (secteurs, pays, pratiques).

**Critères d'acceptation.** Tout investisseur a au moins les filtres durs renseignés ; l'instrument est un champ structuré obligatoire.

## 6.10 M10 — Matching **[MVP manuel → V1 outillé]**

**Objectif.** Rapprocher entreprises et investisseurs ; jugement humain au cœur.

**User stories.**
- US-M10-01 [MVP] En tant que consultant, je veux filtrer les investisseurs compatibles (filtres durs) afin de bâtir une shortlist.
- US-M10-02 [V1] En tant que consultant, je veux un **score de fit** (somme pondérée de critères vérifiables) afin de prioriser.
- US-M10-03 [V1] En tant que consultant, je veux valider/écarter chaque suggestion afin d'éviter les faux positifs.
- US-M10-04 [V1] En tant que consultant, je veux capter le feedback investisseur (motif de refus, next step) afin d'améliorer le matching.

**Règles de gestion.**
- RG-M10-01 **Filtres durs (bloquants) :** pays, secteur, instrument, fourchette de ticket, stade, exclusions.
- RG-M10-02 **Critères pondérés :** qualité financière, complétude documentaire, profil cash-flow vs instrument, ESG, gouvernance, appétence historique.
- RG-M10-03 **Validation humaine obligatoire** avant toute mise en relation ; un dossier non « investor-ready » n'est jamais proposé.
- RG-M10-04 Le moteur **propose**, le consultant **dispose** ; pas de mise en relation automatique.

**Critères d'acceptation.** Aucun match présenté ne viole un filtre dur ; toute mise en relation est validée par un humain ; les feedbacks sont stockés et exploitables.

## 6.11 M11 — Teaser & anonymisation **[MVP gabarit → V1]**

**Objectif.** Présenter une opportunité sans sur-exposer l'entreprise.

**User stories.**
- US-M11-01 [MVP] En tant que consultant, je veux générer un teaser **anonymisé** (secteur, géo approximative, taille, besoin, points forts) afin de susciter l'intérêt sans révéler l'identité.
- US-M11-02 [V1] En tant que consultant, je veux un générateur semi-automatique (gabarit + données du dossier) afin de gagner du temps.
- US-M11-03 [V1] En tant qu'investisseur, je veux filtrer les teasers (instrument, ticket, secteur, géo) afin de trouver des opportunités pertinentes.

**Règles de gestion.**
- RG-M11-01 Anonymisation par défaut : pas de nom, pas d'éléments ré-identifiants (localisation précise, clients nommés, chiffres trop signants).
- RG-M11-02 Levée d'anonymat **uniquement** après consentement entrepreneur + intérêt formalisé + NDA (M12).
- RG-M11-03 Le teaser est validé par le Cabinet avant publication.

**Critères d'acceptation.** Un teaser publié ne contient aucun champ ré-identifiant ; la levée d'anonymat respecte la séquence.

## 6.12 M12 — Mise en relation, NDA & non-circonvention **[MVP manuel/e-sign → V1]**

**Objectif.** Ouvrir les discussions de façon contrôlée et protéger le Cabinet.

**User stories.**
- US-M12-01 [MVP] En tant qu'investisseur, je veux manifester mon intérêt sur un teaser afin de déclencher le process.
- US-M12-02 [MVP] En tant que consultant, je veux faire signer un NDA + clause de **non-circonvention** (e-signature) avant tout accès identifiant afin de prévenir le contournement.
- US-M12-03 [V1] En tant que consultant, je veux un workflow d'introduction tracé (statuts, consentements) afin de piloter la mise en relation.

**Règles de gestion.**
- RG-M12-01 Séquence imposée : intérêt → consentement entrepreneur → NDA + non-circonvention signés → accès gradué.
- RG-M12-02 Versionnage et horodatage des NDA ; valeur juridique via prestataire e-signature.
- RG-M12-03 Toute mise en relation est précédée d'un contrôle conformité (conflits, KYC) et d'une validation senior.

**Critères d'acceptation.** Aucun accès identifiant sans NDA signé ; la clause de non-circonvention est jointe ; chaque étape est tracée.

## 6.13 M13 — Data room **[V1 — solution achetée]**

**Objectif.** Partage documentaire sécurisé pour la diligence (ne pas construire en propre).

**User stories.**
- US-M13-01 [V1] En tant que consultant, je veux ouvrir une data room par deal avec droits par document et par investisseur afin de contrôler l'accès.
- US-M13-02 [V1] En tant qu'investisseur, je veux consulter les documents autorisés (watermark) afin d'instruire le dossier.
- US-M13-03 [V1] En tant que consultant, je veux les logs d'accès/téléchargement afin de tracer l'activité.

**Règles de gestion.**
- RG-M13-01 Solution **achetée** (iDeals / Ansarada / Datasite, option low-bandwidth) intégrée via SSO/API.
- RG-M13-02 Watermark dynamique (identité + horodatage), expiration des accès, interdiction d'export selon sensibilité.
- RG-M13-03 Cloisonnement strict par deal ; logs conservés (M22).

**Critères d'acceptation.** Droits granulaires effectifs ; watermark présent ; logs exhaustifs ; aucun accès inter-deals.

## 6.14 M14 — Q&A & messagerie **[MVP email → V1]**

**Objectif.** Centraliser et tracer les échanges (réduire le hors-plateforme).

**User stories.**
- US-M14-01 [MVP] En tant qu'investisseur, je veux poser des questions (par email cadré en MVP) afin d'obtenir des réponses tracées.
- US-M14-02 [V1] En tant que consultant, je veux une interface Q&A liée aux documents (assignation, statut) afin d'organiser les réponses.

**Règles de gestion.**
- RG-M14-01 Q&A rattachée au deal/document ; pas d'email parallèle pour les sujets sensibles.
- RG-M14-02 Historique horodaté et exportable.

**Critères d'acceptation.** Toute question/réponse est tracée et rattachée au deal.

## 6.15 M15 — KYC / KYB / AML **[V1 — API achetée]**

**Objectif.** Vérifier identités et risques des deux côtés (exigence PE/DFI/banques).

**User stories.**
- US-M15-01 [V1] En tant que conformité, je veux vérifier l'entreprise (KYB : identité légale, actionnariat, bénéficiaires effectifs) afin de fiabiliser le dossier.
- US-M15-02 [V1] En tant que conformité, je veux screener investisseurs et dirigeants (sanctions, PEP, adverse media) afin de réduire le risque.
- US-M15-03 [MVP] En tant que conformité, je veux une checklist KYC manuelle afin de couvrir le besoin avant l'intégration API.

**Règles de gestion.**
- RG-M15-01 Intégration **API achetée** (Smile ID / Youverify / Dojah pour l'Afrique ; World-Check / Moody's Grid pour PEP/sanctions).
- RG-M15-02 Un deal ne progresse pas en data room sans KYC/KYB validé.
- RG-M15-03 Conservation des preuves de vérification (durée légale à confirmer §11).

**Critères d'acceptation.** Un investisseur non vérifié n'accède pas à la data room ; les hits sanctions/PEP bloquent et alertent la conformité.

## 6.16 M16 — Pipeline deal execution **[MVP statuts → V2 outillé]**

**Objectif.** Suivre la transaction jusqu'au closing.

**User stories.**
- US-M16-01 [MVP] En tant que consultant, je veux des statuts de deal (intérêt, NDA, data room, DD, term sheet, closing) afin de suivre l'avancement.
- US-M16-02 [V2] En tant que consultant, je veux jalons, tâches, relances et documents de closing (term sheet, CPs, SPA/SHA) afin d'orchestrer le closing.

**Règles de gestion.**
- RG-M16-01 Pipeline simple (statuts) en MVP ; workflow outillé en V2.
- RG-M16-02 Chaque changement de statut est tracé et déclenche les notifications utiles.

**Critères d'acceptation.** Le statut d'un deal est toujours visible et tracé.

## 6.17 M17 — Mandats & honoraires (fees) **[MVP léger → V1]**

**Objectif.** Sécuriser la monétisation et la gouvernance des conflits.

**User stories.**
- US-M17-01 [MVP] En tant que consultant, je veux enregistrer un mandat (type, exclusivité, durée, périmètre, partie représentée) afin de cadrer la mission.
- US-M17-02 [V1] En tant que consultant, je veux suivre les honoraires (retainer, success fee, échéances) afin de piloter le revenu.
- US-M17-03 [V1] En tant que conformité, je veux le journal des rôles (qui paie quoi par deal) afin de gérer les conflits d'intérêts.

**Règles de gestion.**
- RG-M17-01 Pour chaque deal, **définir de qui le Cabinet est mandataire** ; muraille sur les fees ; disclosure systématique.
- RG-M17-02 Success fee rédigé sur **prestation de conseil** (vs placement de titres) — à valider juridiquement (§11).
- RG-M17-03 Facturation manuelle en MVP ; outillée en V1.

**Critères d'acceptation.** Tout mandat précise la partie représentée ; le registre des conflits est tenu ; aucun deal sans mandat signé.

## 6.18 M18 — DD OHADA / SYSCOHADA **[V2 — différenciateur]**

**Objectif.** Lecture financière locale et retraitements (atout concurrentiel régional).

**User stories.**
- US-M18-01 [V2] En tant qu'analyste, je veux importer une balance SYSCOHADA et mapper les comptes afin d'automatiser la lecture.
- US-M18-02 [V2] En tant qu'analyste, je veux des retraitements (EBITDA, dette nette, BFR) et une revue fiscale/sociale afin de produire une synthèse investisseur.

**Règles de gestion.**
- RG-M18-01 Référentiel de comptes SYSCOHADA révisé maintenu et versionné.
- RG-M18-02 Tout retraitement est traçable (règle appliquée, source).

**Critères d'acceptation.** Mapping reproductible ; synthèse investisseur générée ; retraitements auditables.

## 6.19 M19 — ESG / impact **[V1 si cible DFI → V2]**

**Objectif.** Répondre aux exigences des impact funds et DFI.

**User stories.**
- US-M19-01 [V1] En tant qu'analyste, je veux collecter des champs ESG (emplois, genre, climat, gouvernance) afin de qualifier l'impact.
- US-M19-02 [V2] En tant qu'analyste, je veux un pré-screening impact (checklist) afin d'alimenter la DD des DFI.

**Règles de gestion.**
- RG-M19-01 Champs ESG optionnels hors cible DFI, requis si programme sponsorisé/DFI.
- RG-M19-02 Anti impact-washing : données justifiées par pièces quand c'est possible.

**Critères d'acceptation.** Checklist ESG disponible ; export pour la DD DFI.

## 6.20 M20 — CRM cabinet **[MVP — solution achetée]**

**Objectif.** Piloter prospects, dossiers et mandats (industrialiser le conseil).

**User stories.**
- US-M20-01 [MVP] En tant que consultant, je veux suivre prospects et opportunités (pipeline commercial) afin de piloter la conversion.
- US-M20-02 [MVP] En tant que consultant, je veux des relances et tâches afin de ne rien perdre.

**Règles de gestion.**
- RG-M20-01 CRM **acheté** (HubSpot / Airtable) intégré ; pas de CRM maison.
- RG-M20-02 Synchronisation des statuts dossier ↔ CRM.

**Critères d'acceptation.** Un prospect est suivi de bout en bout ; les relances se déclenchent.

## 6.21 M21 — Reporting & dashboards **[MVP léger → V1]**

**Objectif.** Décision et apprentissage ; preuve aux sponsors.

**User stories.**
- US-M21-01 [MVP] En tant que direction, je veux un tableau de bord (inscriptions, complétion, conversion, packs vendus) afin de piloter le MVP.
- US-M21-02 [V1] En tant que direction, je veux des KPI deal (teaser→intérêt, NDA, DD, closing, délais) afin de piloter la performance.
- US-M21-03 [V1] En tant que sponsor, je veux un reporting cohorte/impact afin de suivre le programme.

**Règles de gestion.**
- RG-M21-01 BI **achetée** (Metabase) branchée sur la base ; pas de dashboards maison.
- RG-M21-02 Données sponsor anonymisées/agrégées (pas de ré-identification).

**Critères d'acceptation.** KPI MVP visibles ; export reporting sponsor disponible.

## 6.22 M22 — Administration, rôles, permissions & audit **[MVP]**

**Objectif.** Sécurité, traçabilité, preuve (condition de confiance).

**User stories.**
- US-M22-01 [MVP] En tant qu'admin, je veux gérer rôles et permissions (RBAC) afin d'appliquer le moindre privilège.
- US-M22-02 [MVP] En tant qu'admin, je veux un audit trail inaltérable (auth, accès documents, NDA, mises en relation, changements de droits, exports) afin de prouver la conformité.

**Règles de gestion.**
- RG-M22-01 Logs horodatés, non modifiables, conservés selon la politique de rétention (§11).
- RG-M22-02 Toute action sensible est journalisée avec acteur, objet, date.

**Critères d'acceptation.** Chaque action sensible laisse une trace ; les logs ne sont pas modifiables.

## 6.23 M23 — Programmes sponsorisés (DFI / banque) **[MVP process → V1]**

**Objectif.** Ancrer le payeur institutionnel (revenu MVP/V1).

**User stories.**
- US-M23-01 [MVP] En tant que direction, je veux modéliser un programme (sponsor, cohorte, périmètre, livrables, reporting) afin de contractualiser.
- US-M23-02 [V1] En tant que sponsor, je veux suivre l'avancement de la cohorte et son impact afin de justifier le financement.

**Règles de gestion.**
- RG-M23-01 Un programme regroupe une cohorte d'entreprises avec readiness + préparation financées par le sponsor.
- RG-M23-02 Reporting d'impact agrégé/anonymisé (M21, M19).

**Critères d'acceptation.** Une cohorte est rattachée à un sponsor ; le reporting programme est généré.

---

# 7. Expérience utilisateur : parcours, UI/UX & design system

> Cette partie spécifie l'expérience cible (parcours, écrans, design system, microcopy, mobile, KPI UX). Tous les écrans et composants sont tagués **[MVP] / [V1] / [V2]** selon le phasage (§5). Règles transverses rappelées : readiness en **4 catégories non exposées à l'investisseur** (M5), **accès gradué** à la confidentialité (Annexe B), **vocabulaire réglementaire conforme** (§11). Au MVP, le périmètre UI = **funnel entrepreneur + cockpit cabinet minimal + reporting sponsor simple** ; le portail investisseur, le matching outillé, la data room in-app, le NDA et la Q&A sont **V1** (manuels au MVP).

## 7.1 Entrepreneur

`Landing` → `Inscription (OTP)` → `Questionnaire 6-8 questions (< 10 min)` → `Mini-rapport readiness (catégorie + gaps + instrument)` → **effet wow** → `Proposition de pack + prise de RDV` → *(après vente)* `Espace mission` → `Upload pièces + checklist` → `Livraison du dossier bancable`.
*Points de friction à surveiller :* upload documentaire (peur fiscale) et passage payant → demander les pièces **après** la valeur, rassurer sur la confidentialité.

## 7.2 Investisseur

`Invitation` → `Qualification express (validée à la main)` → `Catalogue de 3-5 teasers anonymisés filtrables` → `Bouton « intérêt »` → `NDA + non-circonvention (e-signature)` → `Accès data room (achetée)` → `Q&A` → `DD` → `Term sheet`.
*Principe :* friction minimale avant le teaser ; NDA uniquement au moment de l'accès identifiant ; la récurrence se gagne par la **qualité** du flux et la réactivité humaine.

## 7.3 Consultant Cabinet

`Réception dossier qualifié` → `Revue readiness` → `Devis / mission` → `Production (espace mission)` → `Checklist investor-ready + double validation` → `Curation/matching` → `Contrôle conformité (KYC, conflits)` → `Mise en relation` → `Suivi deal`.

---

## 7.4 Vision & principes UX

**Phrase directrice :** *« Une expérience sobre, confidentielle et guidée qui transforme un dossier brut en opportunité investissable. »*

**Émotions cibles par persona :** entrepreneur = *compris, guidé, en contrôle* (jamais examiné/puni) ; investisseur = *dealflow rare, sélectionné, propre* (gain de temps) ; consultant = *maîtrise et priorisation* ; sponsor/DFI = *redevabilité et impact*.

**5 principes fondateurs :** (1) **clarté avant complexité** ; (2) **information progressive** (révélée au bon moment) ; (3) **action guidée** (toujours une prochaine étape claire) ; (4) **confidentialité visible mais non anxiogène** ; (5) **conformité par le langage** (vocabulaire §11). Corollaire : *humain augmenté* — l'accompagnement du Cabinet est rendu visible (concierge/analyst support), jamais masqué par l'automatisation.

## 7.5 Architecture d'information & sitemap UI

| Espace | Navigation principale (modules) | Phase d'ouverture |
|---|---|---|
| **Entrepreneur** | Tableau de bord · Mon diagnostic (M3) · Mon entreprise (M2) · Données financières (M4) · Documents/checklist (M4) · Ma readiness — catégorie (M5/M6) · Recommandations (M6) · Accompagnement/offres (M7) · Rendez-vous (M7) · Notifications · Confidentialité (M22) | **MVP** ; *Data room, suivi investisseur, consentement* = V1 |
| **Investisseur** | Tableau de bord · Critères (dont instrument, M9) · Opportunités/teasers (M11) · Shortlist · Deals suivis (M16) · Data rooms (M13) · Q&A (M14) · Feedback · Paramètres | **V1** (manuel au MVP) |
| **Cabinet** | Cockpit · Pipeline entrepreneur (M3/M5) · Document checklist (M4) · Task center · Mandats (M17) · Reporting (M21) · *(V1)* Pipeline deals (M16), Investisseurs (M9), Matching (M10), Teaser builder (M11), Fees (M17) | **MVP** (cœur) → V1 |
| **Sponsor / DFI** | Vue cohorte (M23) · Avancement readiness · Pipeline qualifié · Reporting d'impact (M19/M21) | MVP simple → V1 |
| **Admin** | Utilisateurs · Rôles/permissions (M1) · Logs/audit (M22) · Config scoring/matching · Templates · Paramètres pays/devise · Sécurité | **MVP** (minimal) → V1 |

Navigation : barre latérale gauche persistante (desktop) / barre inférieure + menu (mobile entrepreneur). Profondeur max 2 niveaux. Statut transactionnel toujours visible en en-tête de fiche.

## 7.6 Inventaire priorisé des écrans

| Écran | Utilisateur | Module | Phase | CTA principal | Donnée critique | Risque UX |
|---|---|---|---|---|---|---|
| Landing privée | Public | — | MVP | « Évaluer ma readiness » | Promesse claire, conforme | Ton « marketplace » |
| Signup + OTP | Entrepreneur | M1 | MVP | « Créer mon compte » | Consentement | Friction OTP mobile |
| Questionnaire progressif | Entrepreneur | M3 | MVP | « Continuer » | Complétion < 10 min | Longueur perçue |
| Upload + checklist | Entrepreneur | M4 | MVP | « Ajouter une pièce » | Statut pièces | Peur fiscale |
| Readiness (catégorie + gaps) | Entrepreneur | M5/M6 | MVP | « Voir mes recommandations » | Catégorie + confiance | Effet « note punitive » |
| Mini-rapport | Entrepreneur | M6 | MVP | « Choisir un accompagnement » | Instrument + blocages | Promesse de financement |
| Catalogue de packs | Entrepreneur | M7 | MVP | « Prendre rendez-vous » | Prix/contenu | Perception pay-to-play |
| Cockpit cabinet | Consultant | M20/M21 | MVP | « Traiter le dossier » | Priorisation/SLA | Surcharge d'info |
| Fiche entreprise | Consultant | M2/M5 | MVP | « Qualifier / scorer » | Score + gaps | Doublons |
| Dashboard investisseur | Investisseur | M21 | V1 | « Voir les opportunités » | Opportunités du jour | Catalogue bruyant |
| Carte opportunité (anonymisée) | Investisseur | M11 | V1 | « Manifester mon intérêt » | Fit + instrument (sans score readiness) | Sur-exposition |
| Détail teaser | Investisseur | M11 | V1 | « Demander l'accès » | Données clés anonymisées | Identité fuitée |
| NDA + non-circonvention | Investisseur | M12 | V1 | « Signer » | Statut signature | Étape bloquante |
| Data room (intégrée) | Investisseur | M13 | V1 | « Consulter » | Droits/watermark/logs | Accès non maîtrisé |
| Matching screen | Consultant | M10 | V1 | « Valider la shortlist » | Fit + filtres durs | Faux positifs |
| Vue cohorte sponsor | Sponsor | M23 | MVP simple→V1 | « Exporter le reporting » | Avancement + impact | Ré-identification |

## 7.7 Wireframes textuels (écrans MVP prioritaires)

Structure : `[Header] · [Hero/résumé] · [Statut/KPI] · [Contenu principal] · [Actions] · [Sidebar] · [Réassurance] · [Aide/footer]`.

**a) Readiness — catégorie & gaps [MVP, M5/M6]**
`[Header: logo, étape 4/5, indicateur confidentialité]` · `[Hero: « Votre dossier est : À PRÉPARER » — badge catégorie, indice de confiance « Évaluation provisoire, sous réserve de vérification »]` · `[Statut: readiness ladder — 4 paliers, position actuelle surlignée]` · `[Contenu: 3-5 blocages prioritaires (cartes), instrument recommandé (badge), « ce qui vous sépare d'un dossier bancable »]` · `[Actions: « Voir mes recommandations » (primaire), « Télécharger le mini-rapport »]` · `[Sidebar: progression du parcours]` · `[Réassurance: « Vos données restent confidentielles. Payer ne change pas votre sélection — seule la qualité de votre dossier compte. »]`. **Jamais de score chiffré ici.**

**b) Dashboard entrepreneur [MVP]**
`[Header]` · `[Hero: salutation + catégorie readiness + prochaine action unique mise en avant]` · `[Statut: progression vers « présentation investisseur », pièces manquantes (n)]` · `[Contenu: cartes « À faire » triées, recommandations, prochain RDV]` · `[Actions: « Compléter mon dossier »]` · `[Réassurance: niveau de confidentialité + accompagnement Cabinet visible]`.

**c) Questionnaire progressif [MVP, M3]**
`[Header: barre de progression, « reprise possible à tout moment »]` · `[Contenu: 1 question par écran, logique conditionnelle, réponses en fourchettes]` · `[Actions: « Continuer » / « Reprendre plus tard »]` · `[Réassurance: « ~8 questions, moins de 10 minutes. Aucune pièce demandée à ce stade. »]`. Sauvegarde auto à chaque étape.

**d) Cockpit cabinet [MVP]**
`[Header: filtres rapides (à traiter / SLA dépassé / investor-ready)]` · `[Statut/KPI: leads, taux de qualification, conversion diagnostic→pack, dossiers investor-ready, revenus attendus]` · `[Contenu: file de dossiers triée par priorité/SLA, colonne score + gaps + statut]` · `[Actions: « Qualifier », « Proposer un pack », « Relancer »]` · `[Sidebar: alertes (dossier bloqué, investisseur intéressé, mandat à proposer, dossier éligible programme sponsorisé)]`.

**e) Landing privée [MVP]**
`[Header: logo sobre, « Accès investisseur » discret]` · `[Hero: promesse conforme « Évaluez votre préparation au financement », CTA]` · `[Contenu: 3 étapes « Comment ça marche », réassurance confidentialité/sélection]` · `[Footer: mentions, pas de jargon « financement garanti »]`. Aucune tonalité marketplace.

## 7.8 Design system

**Palette** (premium institutionnel, Afrique francophone sans folklore) :

| Rôle | Couleur (indicative) | Usage |
|---|---|---|
| Principale (encre/confiance) | Bleu nuit `#102A43` | En-têtes, navigation, fonds sombres, titres |
| Secondaire (ardoise) | `#334E68` / `#486581` | Textes secondaires, bordures, états neutres |
| Accent premium (parcimonieux) | Doré sobre `#B08D4C` | CTA clés, surlignage de valeur, badges « validé » |
| Fond | Blanc cassé `#F7F9FC` | Arrière-plan, respiration |
| Succès | Vert `#1E7F4F` | Validation, investor-ready |
| Attention | Ambre `#B7791F` | À préparer, en attente |
| Risque (sobre) | Rouge brique `#B42318` | Red flags, blocages — jamais pour « mauvais score » |
| Info | Bleu `#2B6CB0` | Aides, statuts neutres |

Règle : l'accent doré est **rare** ; le risque ne doit **pas** dramatiser la catégorie readiness (progression, pas sanction).

**Typographie :** UI sans-serif lisible (ex. Inter / IBM Plex Sans), base ≥ 16 px (mobile) ; **chiffres financiers en tabular figures** (alignement des montants) ; titres pouvant utiliser un serif éditorial sobre (optionnel) ; mentions/disclaimers en petit corps lisible (≥ 12 px, contraste AA).

**Composants UI à produire :** cards · KPI cards · **deal cards anonymisées** · badges · **badge catégorie readiness (4 niveaux)** · score ring **(vue Cabinet uniquement)** · radar sous-scores (Cabinet) · progress stepper · readiness ladder · tables financières · filtres (dont **instrument**) · side panels · modals · **panneau de confirmation avant partage** · uploader de documents · **connecteur/vue data room (VDR achetée)** · timeline · activity feed / logs · fils Q&A · permission chips · risk badges · **investor fit score** (≠ readiness) · CTA premium.

**Iconographie :** trait fin/duotone, sobre. Représenter confidentialité (cadenas/œil barré), instrument de financement, document/checklist, risque, progression. **Éviter** les codes e-commerce (panier, étoiles de notation publique).

**Motion :** sobre et rassurant — transitions douces, états de chargement explicites, *reveal* digne de la catégorie readiness (non gamifié), confirmation d'upload, accès data room, NDA signé. Le motion fluidifie, ne distrait pas.

## 7.9 Microcopy & ton

Ton : clair, institutionnel, sobre ; sans jargon, sans promesse excessive, sans légèreté startup ni froideur bancaire. **Vocabulaire imposé (§11) :** interdits — « plateforme de financement », « marketplace », « financement garanti », « rendement », « collecte » ; préférés — « préparation au financement », « readiness », « dealflow qualifié pour investisseurs qualifiés », « mise en relation privée », « conseil ».

Exemples :

| Contexte | Microcopy recommandée (FR) |
|---|---|
| Accueil entrepreneur | « Évaluez votre préparation au financement en moins de 10 minutes. » |
| Catégorie readiness | « Votre dossier est *À préparer*. Voici ce qui vous sépare d'un dossier bancable. » |
| Anti pay-to-play | « Nos services préparent votre dossier. Ils n'achètent pas un financement ni une présentation : seule la qualité de votre dossier décide. » |
| Consentement (avant partage) | « Vous gardez le contrôle. Aucune information identifiante n'est partagée sans votre accord et un engagement de confidentialité signé. » |
| Dossier non prêt | « Votre projet a du potentiel. Quelques éléments manquent encore pour convaincre un financeur — voici le plan. » |
| Invitation investisseur | « Une opportunité qualifiée correspond à votre thèse. Consultez le teaser anonymisé. » |
| NDA requis (investisseur) | « L'accès au dossier complet requiert la signature d'un accord de confidentialité et de non-circonvention. » |
| Disclaimer pied de page | « DealIQ prépare et met en relation de façon privée des sociétés et des investisseurs qualifiés. Aucune garantie de financement. Pas d'offre au public. » |

## 7.10 UX de la confidentialité, du consentement & de l'accès gradué

Matérialiser la **séquence d'accès** (Annexe B) : `teaser anonymisé → intérêt → consentement entrepreneur → NDA + non-circonvention → data room (droits/watermark/logs) → Q&A`. Composants UX dédiés : **privacy banner** (niveau de confidentialité courant) · **panneau de consentement** (granulaire, révocable, tracé) · **« qui peut voir ceci ? »** · **statut NDA + non-circonvention** · **journal de consultation** (logs lisibles) · **demander / révoquer un accès**. Principe : rendre la sécurité **visible sans anxiété** ; anonymisation **par défaut** ; aucune donnée identifiante avant NDA.

## 7.11 Visualisation du Readiness Score (règles UI)

Conforme à M5 et à l'Annexe C. **Sortie = 4 catégories** (*Investor-ready / À préparer / Plutôt dette-banque / Trop précoce*) + **indice de confiance** + **gating documentaire**. **Visibilité :**

| Acteur | Ce qui s'affiche | Visualisation recommandée |
|---|---|---|
| Entrepreneur | Catégorie + gaps + marges de progression | **Readiness ladder** + checklist (non punitif) |
| Cabinet | Score complet, sous-scores, confiance, historique | Score ring + radar des dimensions |
| Investisseur | **Aucun score** ; au plus label « revu et validé par le Cabinet » | Badge de curation |

Le rendu entrepreneur est un **outil de progression**, jamais une note scolaire. Mise à jour du score **après vérification des pièces** (recalcul tracé).

## 7.12 Mobile-first, i18n & accessibilité

**Mobile-first** (UEMOA/CEMAC) : tout le parcours entrepreneur jusqu'au RDV doit être réalisable sur smartphone ; uploads par photo (compression) ; **sauvegarde automatique + reprise** après coupure ; **canal WhatsApp** (relances, reprise, notifications) ; saisie réduite (fourchettes, choix guidés). Le cockpit cabinet et l'instruction investisseur en data room restent **desktop-first**.

**i18n / localisation :** **FR par défaut, EN pour l'investisseur** ; multi-devise **FCFA / EUR / USD** ; formats de date ; pays UEMOA/CEMAC ; libellés et postes **OHADA / SYSCOHADA**.

**Accessibilité :** **WCAG AA** (contraste, navigation clavier, tailles de cible), formulaires simples, langage accessible (anti-jargon) pour des utilisateurs peu familiers des plateformes financières.

## 7.13 KPI UX (alignés sur les objectifs §2 / O1-O6)

| KPI | Cible | Événement à tracker | Action si sous le seuil |
|---|---|---|---|
| Taux de complétion du diagnostic | ≥ 40 % | `questionnaire_completed` | Raccourcir, clarifier les étapes d'abandon |
| Temps moyen de complétion | < 10 min | durée session diagnostic | Réduire la saisie, fourchettes |
| Taux d'upload de pièces | suivi | `document_uploaded` | Différer/rassurer (peur fiscale) |
| Conversion diagnostic → pack | ≥ 15 % | `pack_purchased` | Revoir offre/prix/mini-rapport |
| Prise de RDV | suivi | `meeting_booked` | CTA, créneaux, relance WhatsApp |
| Teaser → intérêt investisseur (V1) | ≥ 30 % | `interest_expressed` | Améliorer curation/teaser |
| Taux NDA signé (V1) | suivi | `nda_signed` | Simplifier l'étape e-sign |
| Dossiers actifs / consultant | ≤ 5-10 | charge cockpit | Renforcer gating/automatisation |

---

# 8. Spécifications techniques

> La stack ci-dessous est **recommandée** (greenfield) et ajustable selon les compétences de l'équipe retenue. Le principe directeur : **acheter/intégrer la commodité, construire l'avantage** ; rester simple tant que le volume ne justifie pas la complexité.

## 8.1 Architecture cible

Architecture **modulaire** (monolithe modulaire au départ, découplage progressif), orientée API, **mobile-first** (web responsive PWA avant toute app native).

**Vue logique (couches) :**
1. **Présentation** — application web responsive (entrepreneur, investisseur, cabinet/admin), PWA pour usage mobile/offline partiel.
2. **API / services** — API REST sécurisée (authz, métier : onboarding, scoring, matching, deals, mandats).
3. **Données** — base relationnelle (cœur), stockage objet (documents), cache, file de tâches.
4. **Intégrations** — VDR, e-signature, KYC/AML, paiement, emailing/SMS-OTP, BI, services IA.
5. **Transverse** — IAM/RBAC, audit/logs, observabilité, secrets.

**Vue déploiement :** conteneurs (Docker) orchestrés ; environnements *dev / staging / prod* ; hébergement cloud avec **résidence des données** à arbitrer (UE vs régional) selon §11 ; CDN pour les assets ; sauvegardes chiffrées.

## 8.2 Stack technologique recommandée

| Couche | Recommandation | Justification |
|---|---|---|
| Frontend | React (Vite) + TypeScript, PWA, i18n (FR par défaut) | Écosystème large, mobile-first, offline partiel |
| Backend | Python (FastAPI) **ou** Node (NestJS) | Productivité, typage, async, large vivier |
| Base de données | PostgreSQL | Relationnel robuste, JSONB pour la flexibilité |
| Stockage documents | Stockage objet S3-compatible (chiffré) | Sécurité, scalabilité, coût |
| Cache / file | Redis + worker (Celery/RQ ou BullMQ) | Tâches asynchrones (IA, emails, exports) |
| Recherche/filtre | Postgres (index) → moteur dédié si besoin (V2) | Éviter la sur-ingénierie au MVP |
| Auth | JWT (access court + refresh) + MFA (V1) | Standard, simple |
| Infra | Docker + orchestrateur managé ; IaC | Reproductibilité, portabilité |
| Observabilité | Logs centralisés + métriques + traces + Sentry | Exploitabilité dès le MVP |

## 8.3 Modèle de données (entités principales)

| Entité | Attributs clés | Relations | Sensibilité |
|---|---|---|---|
| `User` | id, email, hash_mdp, rôle, MFA, statut | ↔ Company / Investor (selon rôle) | Élevée (perso) |
| `Company` | id, nom, pays, secteur, RCCM, CA (fourchette), stade, statut | 1-n Contact, 1-n Document, 1-1 Score, 1-n Deal | Élevée |
| `Contact` | id, nom, rôle, email, tél, KYC_statut | n-1 Company | Élevée (perso) |
| `Investor` | id, type, juridiction, équipe, statut_qualif | 1-n Fund, 1-1 Criteria, 1-n Interaction | Moyenne |
| `Fund` | id, thèse, AUM, instruments | n-1 Investor | Moyenne |
| `InvestmentCriteria` | pays[], secteurs[], instrument[], ticket_min/max, stade[], exclusions[], ESG | n-1 Investor/Fund | Moyenne |
| `FinancingNeed` | montant, usage, horizon, instrument souhaité | n-1 Company, 1-1 Deal | Moyenne |
| `Score` | sous-scores, catégorie, indice_confiance, version_grille | 1-1 Company | Élevée |
| `Document` | id, type, version, hash, statut_vérif, droits | n-1 Company/Deal, n-1 DataRoom | **Critique** |
| `Teaser` | contenu_anonymisé, version, statut | n-1 Deal/Company | Moyenne |
| `Deal` | id, statut, instrument, montant, parties | n-1 Company, n-1 Investor, 1-1 Mandate | **Critique** |
| `NDA` | parties, modèle, date, signature_ref, non_circonvention | n-1 Deal/Investor | Élevée |
| `DataRoom` | id (réf. prestataire), arborescence, droits, logs | 1-1 Deal | **Critique** |
| `QAItem` | question, réponse, statut, auteur | n-1 Deal/Document | Moyenne |
| `Interaction` | type, date, canal, notes | n-1 (toute entité) | Moyenne |
| `Mandate` | type, exclusivité, durée, périmètre, partie_représentée | n-1 Company/Investor, 1-n Fee | Élevée |
| `Fee` | type (retainer/success), montant, échéance, statut | n-1 Mandate/Deal | Élevée |
| `Feedback` | motif, next_step, score_révisé | n-1 Deal/Investor | Faible |
| `Program` | sponsor, cohorte[], périmètre, livrables | 1-n Company | Moyenne |
| `AuditLog` | acteur, action, objet, date, méta | n-1 (toute entité) | Élevée |

**Principes :** propriété des données = l'entreprise possède ses données ; le Cabinet possède scores, curation et agrégats anonymisés. Intégrité documentaire par hash + horodatage. **Cloisonnement strict par deal**. Multi-pays/multi-devise prévu dès la conception (champ devise, pays sur les entités financières).

## 8.4 Principes d'API

API **REST** versionnée (`/api/v1`), JSON, authentification Bearer (JWT), autorisation RBAC par ressource. Conventions : pagination, filtrage, tri standardisés ; codes d'erreur normalisés ; idempotence sur les écritures sensibles ; rate-limiting.

**Exemples d'endpoints clés (non exhaustif) :**

| Domaine | Endpoint (exemple) | Méthode |
|---|---|---|
| Auth | `/auth/login`, `/auth/refresh`, `/auth/me` | POST/GET |
| Entreprise | `/companies`, `/companies/{id}` | GET/POST/PATCH |
| Onboarding | `/companies/{id}/questionnaire` | POST |
| Documents | `/companies/{id}/documents` | POST/GET |
| Scoring | `/companies/{id}/score` | POST/GET |
| Rapport | `/companies/{id}/report` | GET |
| Investisseurs | `/investors`, `/investors/{id}/criteria` | GET/POST/PATCH |
| Matching | `/deals/{id}/matches` | GET |
| Teaser | `/deals/{id}/teaser` | POST/GET |
| Intérêt / NDA | `/deals/{id}/interest`, `/deals/{id}/nda` | POST |
| Data room | `/deals/{id}/dataroom` (proxy prestataire) | GET/POST |
| Mandats/Fees | `/mandates`, `/mandates/{id}/fees` | GET/POST/PATCH |
| Audit | `/audit` (lecture admin) | GET |

## 8.5 Intégrations & matrice Build / Buy / Partner

| Brique | Décision | Solution(s) cible | Mode d'intégration | Phase |
|---|---|---|---|---|
| CRM | Buy | HubSpot / Airtable | API/webhooks | MVP |
| Stockage documents | Buy | S3-compatible chiffré | SDK | MVP |
| Emailing / SMS-OTP | Buy | Brevo / Mailchimp ; passerelle SMS locale | API | MVP |
| Paiement | Buy/Partner | PSP local + mobile money | API (V1 ; manuel MVP) | MVP→V1 |
| Data room (VDR) | Buy | iDeals / Ansarada / Datasite | SSO + API/proxy | V1 |
| E-signature | Buy | DocuSign / équivalent | API | V1 |
| KYC/KYB/AML | Buy/API | Smile ID, Youverify, Dojah ; World-Check / Moody's Grid | API | V1 |
| BI / dashboards | Buy | Metabase | Connexion DB read-only | MVP léger→V1 |
| Services IA | Partner | LLM (extraction/structuration) | API + garde-fous (§8.8) | MVP léger→V1 |
| Funnel, scoring, matching, modèle de données, OHADA | **Build** | — | — | MVP→V2 |

## 8.6 Sécurité

- **Authentification/Autorisation :** JWT (access court + refresh) ; MFA (V1) ; RBAC par ressource (moindre privilège) ; séparation stricte des espaces entrepreneur/investisseur/cabinet.
- **Chiffrement :** TLS en transit ; chiffrement au repos (DB + stockage objet) ; secrets dans un coffre (vault), jamais dans le code.
- **Confidentialité graduée :** anonymisation par défaut (M11) ; accès par niveaux ; cloisonnement par deal ; watermark + logs en data room (M13).
- **Audit & preuve :** journalisation inaltérable (M22) ; horodatage ; intégrité par hash.
- **Durcissement :** validation des entrées, anti-malware sur uploads, rate-limiting, protection CSRF/XSS/SQLi, gestion des sessions, revue d'accès périodique.
- **Paliers :** MVP (RBAC, chiffrement, MFA optionnel, logs, NDA+non-circonvention) → V1 (VDR, e-sign, KYC, rétention, revue d'accès) → V2 (cloisonnement renforcé, DLP, pentests, ISO 27001 si cible DFI).

## 8.7 Conformité & protection des données

- **Cadre :** Convention de Malabo + lois nationales (CDP Sénégal, ARTCI Côte d'Ivoire, etc.) — **responsable de traitement à désigner**, base légale = consentement + intérêt légitime.
- **Consentement :** granulaire (quelles données, à qui, pour quoi, durée), révocable, tracé.
- **Droits des personnes :** accès, rectification, suppression, portabilité (procédures à définir).
- **Rétention :** politique par type de donnée (dossiers, KYC, logs) — durées à confirmer juridiquement.
- **Résidence des données :** arbitrage hébergement (UE vs régional) selon exigences sponsors/DFI.
- **Conformité marché :** voir §11 (positionnement privé, investisseurs qualifiés, formulations, disclaimers).

## 8.8 IA & enrichissement (accélérateur, pas produit)

L'IA est un **accélérateur de préparation de dossier**, jamais un décideur. Cas d'usage : extraction/structuration de documents (deck, états financiers), pré-remplissage de fiches, mapping SYSCOHADA (V2), génération de brouillons de mini-rapport/teaser, questions guidées de complétion.

**Garde-fous (obligatoires) :**
- RG-IA-01 Toute donnée produite par IA porte un **label de fiabilité** (« IA — à vérifier », « inférence », « déclaré / non audité »).
- RG-IA-02 **Validation humaine champ par champ** ; jamais d'écrasement automatique d'une donnée saisie.
- RG-IA-03 Aucune décision d'éligibilité/score « finale » prise par l'IA seule.
- RG-IA-04 Données sensibles : usage maîtrisé (anonymisation, pas d'entraînement sur données clients sans consentement).

## 8.9 Exigences non-fonctionnelles (NFR)

| Domaine | Exigence (cible indicative) |
|---|---|
| Performance | Pages clés < 2,5 s sur 3G/4G ; questionnaire utilisable hors pic réseau |
| Mobile / offline | Responsive + PWA ; reprise après coupure ; uploads résilients |
| Disponibilité | ≥ 99,5 % (hors maintenance planifiée) |
| Scalabilité | Horizontale (stateless API) ; volumétrie modérée au MVP, montée progressive |
| Sécurité | Cf. §8.6 ; tests de sécurité avant V1 |
| Confidentialité | Anonymisation, cloisonnement, traçabilité (cf. §12) |
| i18n / l10n | FR par défaut ; multi-devise ; multi-pays (formats, RCCM) |
| Accessibilité | Bonnes pratiques WCAG AA visées |
| Observabilité | Logs, métriques, alerting, traçage des erreurs |
| Maintenabilité | Code typé, tests automatisés, doc API, CI |
| Portabilité | Conteneurisé ; pas de lock-in fort hors briques achetées |

## 8.10 Environnements, CI/CD, sauvegarde & PRA

Environnements *dev / staging / prod* isolés ; **CI/CD** (build, tests, lint, déploiement automatisé) ; migrations de schéma versionnées ; **sauvegardes** chiffrées régulières + test de restauration ; **PRA** (RPO/RTO à définir) ; gestion des secrets ; revue de sécurité avant chaque passage de phase.

---

# 9. Modèle économique & tarification

**Principe :** modèle **hybride**, ancré sur le payeur le plus solvable au démarrage (**l'institution**), wedge sur les **packs de préparation**, success fee en *upside* — jamais en rente unique.

## 9.1 Architecture tarifaire (6 offres)

| Offre | Cible | Logique de prix | Contenu | Phase |
|---|---|---|---|---|
| **Gratuit** | Entrepreneur | 0 | Diagnostic readiness + mini-rapport + orientation instrument | MVP |
| **Diagnostic+** | Entrepreneur | Ticket d'engagement bas | Rapport approfondi + plan d'action + RDV | MVP |
| **Préparation** (paliers) | Entrepreneur | Forfait par livrable | BP / modèle financier / valorisation / teaser / data room | MVP/V1 |
| **Mandat** | Entrepreneur ou fonds | Retainer + success fee | Levée/sourcing, mise en relation, suivi closing | V1 |
| **Investisseur** | PE/VC/dette/DFI/FO | Abonnement annuel (après preuve) | Dealflow filtré + teasers + Q&A ; sourcing dédié en option | V1 |
| **Programme** | DFI/banque/agence | Contrat de programme | Cohorte PME préparées + pipeline qualifié + reporting/impact | MVP/V1 |

## 9.2 Séquencement & priorités

- **Wedge MVP :** packs de préparation + ancrage d'un programme sponsorisé.
- **Plus rentable moyen terme :** retainers + success fees + abonnement investisseur (après preuve de flux).
- **Plus risqué :** dépendre du success fee seul → le traiter en upside sur une base récurrente.
- **Anti pay-to-play :** payer = préparation, jamais un accès privilégié au financement ; la sélection pour présentation dépend de la **qualité du dossier** uniquement.

---

# 10. Modèle opérationnel cabinet

**Risque central :** chaque « revue cabinet » est un goulot de consultant senior. Sans modèle opérationnel, la plateforme génère plus de travail manuel qu'elle n'en économise.

| Élément | Définition |
|---|---|
| **Rôles** | Analyste (qualification, enrichissement) · Consultant senior (préparation, relation investisseur) · Conformité (KYC/NDA/conflits) · Ops-plateforme (admin, données, reporting) |
| **Charge indicative/dossier** | Qualification 1-2 h · Préparation *investor-ready* 20-40 h · Curation/matching 2-4 h · Suivi deal : dizaines d'heures |
| **Plafond de débit** | ~5-10 dossiers actifs par consultant senior |
| **SLA** | Mini-rapport < 48 h · Devis < 72 h · Réponse investisseur < 24 h · Mise en data room < 5 j après NDA |
| **À standardiser** | Grille readiness, modèles (BP, teaser, NDA), checklist DD, scripts de qualification |
| **Automatisable** | Qualification initiale, enrichissement IA, relances, mini-rapport, reporting |
| **À garder humain** | Revue readiness finale, curation, mise en relation, négociation, jugement de fit |
| **Contrôle qualité** | Checklist « investor-ready » + double validation + revue conformité avant toute mise en relation |
| **Indicateurs** | Dossiers/consultant, h/dossier, taux qualif→pack, taux teaser→intérêt, délai onboarding→term sheet |

---

# 11. Gouvernance, conformité & gestion des risques

## 11.1 Cartographie réglementaire (indicative — à valider par avocats UEMOA/CEMAC/OHADA)

| Zone | Sujets | Conduite |
|---|---|---|
| **🔴 Rouge** | Appel public à l'épargne / offre publique sans note visée ; sollicitation du public ; promesse de financement/rendement « garanti » ; gestion de fonds pour compte de tiers | Proscrire absolument |
| **🟠 Grise** | **Intermédiation/démarchage rémunéré** (même en privé) ; conseil en investissement ; success fee sur placement de titres ; ciblage actif d'investisseurs ; transfrontalier ; usage KYC | **Sécuriser par avis juridique ciblé** (angle mort principal) |
| **🟢 Verte** | Conseil et préparation (readiness, BP, modèle, valorisation, data room) ; mise en relation **privée** entre société et **investisseurs qualifiés** sous NDA ; success fee sur **conseil** bien rédigé ; market intelligence anonymisée | Cœur d'activité, sous réserve de rédaction |

**Formulations à éviter :** « plateforme de financement », « marketplace d'investissement », « financement garanti », « rendement », « collecte ». **Préférer :** « préparation au financement », « readiness », « dealflow qualifié pour investisseurs qualifiés », « mise en relation privée », « conseil ».

**Disclaimers requis :** non-garantie de financement ; pas de conseil en investissement aux investisseurs ; investisseurs réputés qualifiés procédant à leur propre évaluation ; pas d'offre au public ; exactitude des données à la charge de l'entreprise.

**Validations juridiques avant V1 :** (1) intermédiation/démarchage (CREPMF-AMF-UMOA / COSUMAF) ; (2) structure du success fee ; (3) données personnelles (Malabo + lois nationales) ; (4) définition d'investisseur qualifié par pays ; (5) transfrontalier.

## 11.2 Gouvernance

Registre des conflits d'intérêts ; muraille sur les fees (qui paie quoi par deal) ; journal des rôles/mandats ; politique de consentement ; **comité de conformité** validant chaque mise en relation.

## 11.3 Registre des risques (synthèse — détail en Annexe D)

| Risque | Gravité | Mitigation |
|---|---|---|
| Sélection adverse (dossiers faibles) | Critique | Sourcing actif + curation impitoyable |
| Personne ne paie (WTP entrepreneur) | Critique | Ancre sponsor institutionnel + packs |
| Surcharge opérationnelle | Élevée | Gating + SLA + plafond dossiers/consultant |
| Requalification réglementaire | Élevée | Avis juridique + positionnement conseil/privé |
| Fuite / contournement | Élevée | Anonymisation + NDA/non-circonvention + logs |
| Périmètre qui dérive (sur-build) | Élevée | Gel du MVP couche 1 + go/no-go |
| TAM trop mince | Moyenne | Étude TAM en Phase 0 |

---

# 12. Planning, lotissement & jalons

| Phase | Durée | Objectifs | Livrables clés | KPI / Go | Risques |
|---|---|---|---|---|---|
| **0 — Cadrage** | 0-1 mois | Geler MVP, TAM, juridique, 2 pays, design-partners | Note de périmètre, étude TAM, mémo juridique, cohorte investisseurs | Décisions structurantes prises | Lancer les 4 lots au lieu de la couche 1 |
| **1 — MVP (couche 1)** | 1-4 mois | Funnel entrepreneur + conversion + 1 sponsor | Onboarding, readiness, mini-rapport, catalogue, CRM/reporting | Complétion ≥ 40 % ; ≥ 3 packs ; ≥ 1 deal en DD | Construire au lieu de vendre |
| **2 — Pilote (couche 2)** | 4-10 mois | Dealflow curé + engagement investisseur + 1er closing | Référentiel investisseurs, matching manuel→léger, teasers, VDR achetée, NDA, KYC | Teaser→intérêt ≥ 30 % ; 1 closing ; 1 programme signé | Sélection adverse ; flux tari |
| **3 — V1** | 10-16 mois | Industrialiser ; abonnement investisseur | Matching outillé, teaser semi-auto, Q&A, KYC/AML, mandats/fees, dashboards | Récurrence ; ≥ N closings ; rétention | Sur-build ; surcharge ops |
| **4 — Scale** | 16-24 mois | Multi-pays ; DD OHADA ; market intel | DD OHADA/SYSCOHADA, ESG, market intel, programmes DFI | Couverture multi-pays ; marges | Dispersion géographique |

**Détail MVP 90 jours :** objectif = prouver venue + paiement + engagement investisseur, sans plateforme biface. Inclus : M1-M7, M20-M22 (couche 1) ; manuel : matching, teaser, NDA, data room, facturation, Q&A. Go = conversion payante prouvée **et** ≥ 1 deal en DD ; sinon pivot/refonte (cf. §13).

---

# 13. Recette & critères d'acceptation

## 13.1 Stratégie de test

Tests unitaires et d'intégration (backend), tests E2E des parcours clés (entrepreneur, investisseur, cabinet), tests de sécurité avant V1 (authz, cloisonnement, uploads), tests de charge ciblés, recette fonctionnelle par module (critères d'acceptation §6), UAT avec utilisateurs réels (cohorte pilote).

## 13.2 Critères d'acceptation produit (MVP)

| Domaine | Critère de recette |
|---|---|
| Onboarding | Diagnostic complétable sur mobile en < 10 min, reprise sans perte |
| Readiness | Catégorie + gaps rendus ; score élevé impossible sans pièces vérifiées |
| Rapport | Mini-rapport personnalisé généré + disclaimers |
| Conversion | Catalogue + RDV + message anti pay-to-play |
| Sécurité | RBAC effectif ; cloisonnement ; audit trail inaltérable |
| Conformité | Consentement tracé ; formulations conformes |

## 13.3 KPI de validation & go/no-go

KPI : complétion ≥ 40 % ; diagnostic→pack ≥ 15 % ; ≥ 3 packs vendus ; teaser→intérêt ≥ 30 % ; ≥ 1 entrée en DD ; 1 programme sponsorisé. **Go** si conversion payante **et** ≥ 1 deal en DD. **Pivot** si flux sans conversion (WTP) ou conversion sans flux (acquisition). **No-go/refonte** sinon.

---

# 14. Annexes

## Annexe A — Glossaire

AMF-UMOA/CREPMF (régulateur marché UEMOA) · COSUMAF (régulateur marché CEMAC) · OHADA (droit des affaires, 17 États) · SYSCOHADA (référentiel comptable) · DFI (institution de financement du développement) · Missing middle (PME trop grandes pour la microfinance, trop petites/peu préparées pour banque/PE) · Readiness (préparation au financement) · Teaser (présentation anonymisée d'une opportunité) · VDR (data room virtuelle) · NDA (accord de confidentialité) · KYC/KYB/AML (connaissance client/entreprise, anti-blanchiment) · PEP (personne politiquement exposée) · Success fee (commission de succès au closing) · Retainer (honoraire récurrent) · Investor-ready (dossier présentable à un investisseur).

## Annexe B — Matrice de permissions (accès gradué)

| Rôle | Avant intérêt | Après intérêt + NDA | En data room | Deal execution |
|---|---|---|---|---|
| Investisseur | Teaser anonymisé | Identité + dossier résumé | Documents selon droits + watermark + logs | Term sheet, Q&A |
| Entrepreneur | Son dossier + statut | Voit l'intérêt (selon consentement) | Gère les accès accordés | Pipeline, tâches |
| Analyste | Ses dossiers | Idem + préparation | Lecture | Suivi |
| Consultant senior | Tout (ses dossiers) | Tout | Tout + administration | Tout |
| Conformité | KYC, conflits | NDA, contrôles | Politiques d'accès | Audit conformité |
| Admin | Config, rôles, logs | — | Politiques d'accès | Audit |

## Annexe C — Grille de scoring readiness (recommandée)

| Dimension | Pondération | Données | Fiabilité | Biais |
|---|---|---|---|---|
| Traction commerciale | 20 % | États financiers, factures, contrats | Moyenne (si pièces) | Survente |
| Profitabilité / cash-flow | 20 % | Comptes SYSCOHADA, relevés | Moyenne-haute (si vérifié) | Comptes informels |
| Qualité de l'information financière | 15 % | États certifiés, expert-comptable | **Haute (vérifiable)** | Faible |
| Clarté & cohérence du besoin | 10 % | Montant, usage, horizon | Moyenne | Déclaratif |
| Gouvernance / actionnariat | 10 % | RCCM, statuts, cap table, bénéf. effectifs | Haute (vérifiable) | Opacité |
| Qualité documentaire (complétude) | 10 % | Checklist de pièces | **Haute (objective)** | Faible |
| Scalabilité / marché | 5 % | Narratif, marché | Basse (subjectif) | Optimisme |
| ESG / impact | 5 % | Checklist impact | Basse-moyenne | Impact-washing |
| **Facteurs de risque (malus)** | −15 % | Litiges, dettes fiscales, concentration | Moyenne | Dissimulation |

**Sorties (catégories) :** *Investor-ready* → mandat ; *À préparer* → pack préparation ; *Plutôt dette-banque* → orientation crédit ; *Trop précoce* → nurturing gratuit. **Règle :** gating documentaire + indice de confiance + score jamais exposé à l'investisseur.

## Annexe D — Registre des risques (détaillé)

| # | Risque | Prob. | Impact | Gravité | Mitigation | Responsable |
|---|---|---|---|---|---|---|
| R1 | Sélection adverse | Élevée | Élevé | Critique | Sourcing actif (banques, incubateurs, prescripteurs) + curation | Senior |
| R2 | WTP entrepreneur insuffisante | Élevée | Élevé | Critique | Ancre sponsor + packs à valeur tangible | Direction |
| R3 | Surcharge opérationnelle | Moyenne | Élevé | Élevée | Gating + SLA + plafond + automatisation | Ops |
| R4 | Requalification réglementaire | Moyenne | Élevé | Élevée | Avis juridique + positionnement + disclaimers | Conformité |
| R5 | Fuite / contournement | Moyenne | Élevé | Élevée | Anonymisation + NDA/non-circonvention + logs | Conformité |
| R6 | Sur-build / dérive de périmètre | Élevée | Moyen | Élevée | Gel MVP couche 1 + jalons go/no-go | Direction |
| R7 | TAM trop mince | Moyenne | Élevé | Moyenne | Étude TAM Phase 0 ; cible multi-instruments | Direction |
| R8 | Conflit d'intérêts (payé 2 côtés) | Moyenne | Moyen | Moyenne | Mandataire défini par deal + muraille fees + disclosure | Conformité |
| R9 | Qualité documentaire (blocage DD) | Élevée | Moyen | Moyenne | Pack readiness + checklist + vérification | Analyste |
| R10 | Dépendance success fee | Moyenne | Moyen | Moyenne | Base récurrente (packs, retainers, sponsoring) | Direction |

## Annexe E — Hypothèses & questions ouvertes à trancher (avant build)

1. Positionnement assumé : boutique tech-enabled (non-scalable) vs plateforme scalable ?
2. Cible financeur : equity PE/VC seul ou multi-instruments (dette/DFI/blended) ?
3. Pays prioritaires (2 UEMOA + 1 CEMAC) ?
4. Périmètre MVP gelé sur la couche 1 ?
5. Qui paie d'abord : confirmation de l'ancre sponsor institutionnel ?
6. Success fee : sur conseil ou sur placement (implication réglementaire) ?
7. Intermédiation rémunérée : agrément requis ? (avis juridique)
8. Définition d'« investisseur qualifié » par pays ?
9. Résidence des données (UE vs régional) ?
10. Stratégie de sourcing actif des bons dossiers ?

## Annexe F — Références

Cadrage AMOA (juin 2026) ; Revue critique du projet (juin 2026). Sources marché/réglementaire : IFC (MSME Finance), Banque mondiale (PME Afrique de l'Ouest), AVCA (Private Capital 2025), BCEAO (inclusion financière UEMOA 2024), GSMA (Mobile Money 2025), OHADA, AMF-UMOA, COSUMAF, IFC Sustainability Framework. Standards produits : DealCloud, Affinity, Dynamo, Datasite, Intralinks, Ansarada, iDeals, LSEG World-Check, Moody's Grid.

---

*Fin du cahier des charges. Document fondé sur le cadrage AMOA et la revue critique. Les éléments réglementaires sont indicatifs et doivent être validés par des avocats spécialisés UEMOA/CEMAC/OHADA avant tout engagement. Version 1.1 (intégration des spécifications UX/UI) — à enrichir en backlog détaillé lors du lancement de la Phase 0.*




