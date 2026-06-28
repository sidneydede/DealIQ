# Prompt UX/UI — DealIQ (révisé et aligné sur le cahier des charges)

> **À l'usage.** Ceci est le brief à coller à un LLM ou à remettre à un Lead UX/UI. Il a été **réaligné sur le cahier des charges DealIQ v1.0** : phasage strict MVP→V1→V2, périmètre MVP réduit à la *couche 1* (funnel entrepreneur), logique *manual-first / buy-don't-build*, ajout du persona **sponsor institutionnel / DFI**, règles de **visibilité du score**, **vocabulaire réglementaire** contraint, **accès gradué** à la confidentialité, **instrument de financement** comme filtre de premier rang. Les ajouts/contraintes issus du CDC sont marqués _[CDC]_. Un récapitulatif des changements figure en fin de document.

---

## Rôle

Agis comme un **Lead UX/UI Designer senior** spécialisé dans les plateformes B2B premium pour Private Equity, banques d'affaires, cabinets de conseil financier, plateformes de dealflow, data rooms, fintech B2B et financement des PME. Tu as conçu des produits utilisés par des dirigeants de PME en recherche de financement, des fonds PE/VC/impact, des **financeurs de dette/mezzanine/garanties**, des banques, des family offices, des **DFI**, des cabinets de conseil, et des deal teams (analystes, partners, investment managers). _[CDC : la cible financeur n'est pas seulement l'equity PE/VC ; le « missing middle » relève surtout de dette/DFI/blended.]_

## Contexte produit

Je conçois **DealIQ** *(nom de marque à confirmer)*, une plateforme digitale **privée, curée et B2B** pour un cabinet de conseil financier (« le Cabinet ») opérant en **UEMOA et CEMAC**. 

**Positionnement assumé _[CDC]_ : une boutique de conseil *tech-enabled***, et non une marketplace ouverte ni un SaaS scalable comme cœur de modèle. La valeur naît de la curation humaine et de la préparation des dossiers ; la plateforme **outille** le Cabinet, elle ne le remplace pas. La promesse produit : *« Une infrastructure privée qui rend les PME d'Afrique francophone bancables avant de les exposer aux financeurs, et qui donne aux financeurs un dealflow préparé et pré-qualifié, orchestré jusqu'au closing. »*

La plateforme sert **trois** publics (et non deux) _[CDC]_ :
1. **Entrepreneurs / PME** — cible précise : *« solides mais mal préparés »* (activité réelle, comptes SYSCOHADA faibles, pas de dossier bancable, accès limité aux financeurs). Ils viennent évaluer leur capacité à lever, comprendre leur readiness, identifier les pièces manquantes, recevoir une **catégorie** de readiness + une orientation d'instrument, être accompagnés (packs payants), puis être mis en relation avec les bons financeurs.
2. **Investisseurs / financeurs** — PE, VC, impact, **fonds de dette/mezzanine/garanties**, banques, family offices, **DFI**. Ils accèdent à un dealflow qualifié, filtré sur **leurs critères (dont l'instrument)**, consultent des teasers anonymisés, manifestent leur intérêt, signent un NDA + clause de non-circonvention, accèdent à une data room, posent des questions, suivent leurs deals, donnent du feedback, jusqu'à la DD et au closing.
3. **Sponsor institutionnel / DFI / banque _[CDC — persona manquant dans le brief initial]_** — finance des **cohortes** de préparation PME (programme sponsorisé) ; c'est le **payeur ancre** du modèle au démarrage. Il suit l'avancement de la cohorte et son impact.

## Impression à produire

Sérieux, confidentialité, sophistication, confiance, **sélection**, accompagnement humain, excellence transactionnelle, premium finance, fluidité. UX *investment-oriented* : décisions financières sérieuses, deals privés, informations sensibles, investisseurs exigeants, entrepreneurs à guider. **Jamais** l'effet « marketplace grand public ».

## Niveau de qualité attendu

Pas d'UX SaaS générique. Simple mais pas simpliste ; premium mais pas froid ; fluide mais sécurisé ; rassurant mais orienté action ; confiance dès les premières secondes.

---

## ⚠️ Contraintes issues du cahier des charges (NON négociables) _[CDC]_

Toute proposition UX doit respecter les décisions suivantes du CDC. Elles priment sur toute interprétation contraire des sections ci-dessous.

### C1 — Phasage strict (périmètre par phase)

| Domaine | MVP (couche 1, 0-4 mois) | V1 (4-16 mois) | V2 (16-24 mois) |
|---|---|---|---|
| Entrepreneur | Funnel complet : onboarding → questionnaire → upload → **readiness (catégories)** → mini-rapport → catalogue de packs → RDV | Espace mission outillé, paiement en ligne, suivi investisseur | Personnalisation, IA avancée |
| Investisseur | **Pas de portail in-app** : teasers envoyés **à la main** par le Cabinet ; qualification manuelle | **Portail investisseur** : critères, teasers filtrables, intérêt, NDA, data room, Q&A, pipeline | Comparaison avancée, market intelligence, alertes IA |
| Cabinet | **Cockpit minimal** : pipeline entrepreneur, scoring, statuts, reporting, mandats léger | Matching outillé, teaser semi-auto, fees, dashboards, KYC | DD OHADA/SYSCOHADA, deal execution avancé |
| Sponsor/DFI | Process + reporting cohorte basique | Espace sponsor, reporting d'impact | Programmes multiples, market insights |

**Conséquence directe :** le MVP UX = **le funnel entrepreneur + le cockpit cabinet minimal + un reporting sponsor simple**. Le **portail investisseur, le matching outillé, la data room in-app, le workflow NDA, le pipeline de deal et la Q&A sont V1** — au MVP ils sont **opérés manuellement** par le Cabinet (voir C2). Ne conçois pas d'écrans MVP pour ces fonctions ; conçois-les comme livrables V1.

### C2 — Manual-first au MVP

Au MVP, les fonctions suivantes sont **manuelles / hors-app** : matching (tableur + jugement), teaser (gabarit Word/PDF), NDA (signature via prestataire e-sign), data room (solution achetée), facturation (devis classique), Q&A (email cadré), qualification investisseur (validation humaine). L'UX MVP doit en tenir compte : pas de sur-conception d'écrans pour ce qui est encore manuel.

### C3 — Buy-don't-build (ne pas reconcevoir l'existant du marché)

Sont **achetés/intégrés**, pas construits : **CRM** (HubSpot/Airtable), **BI/dashboards** (Metabase), **e-signature** (DocuSign), **KYC/KYB/AML** (Smile ID / Youverify / Dojah ; World-Check / Moody's Grid), **data room / VDR** (iDeals / Ansarada / Datasite), stockage, emailing/SMS-OTP, paiement (PSP local + mobile money). Le travail UX consiste à **encapsuler/intégrer** ces briques (SSO, accès, cohérence visuelle, couche de permissions), **pas** à recréer une VDR ou un CRM maison. Sont **construits** (et donc à designer finement) : funnel entrepreneur, scoring, recommandation, matching (couche de décision), modèle de données, lecture OHADA/SYSCOHADA, cockpit cabinet.

### C4 — Readiness score : 4 catégories + règles de visibilité

Sortie = **4 catégories actionnables** : *Investor-ready / À préparer / Plutôt dette-banque / Trop précoce*. **Gating documentaire** : pas de score « élevé » sans pièces vérifiées. Afficher un **indice de confiance**. **Visibilité (strict)** : l'entrepreneur voit la **catégorie + les gaps**, *jamais* le score brut détaillé ; le Cabinet voit le score complet + sous-scores ; **l'investisseur ne voit JAMAIS le score** auto-attribué comme signal de qualité — au plus un label « revu et validé par le Cabinet ». Le score se présente comme un **outil de progression**, pas une note punitive.

### C5 — Anti « pay-to-play »

Payer achète de la **préparation**, jamais un accès privilégié au financement. Afficher explicitement que **payer n'augmente pas la probabilité d'être sélectionné** pour présentation aux investisseurs — seule la **qualité du dossier** le détermine.

### C6 — Accès gradué à la confidentialité (séquence imposée)

`Teaser anonymisé` → `Manifestation d'intérêt` → `Consentement entrepreneur` → `NDA + clause de non-circonvention (e-sign)` → `Accès data room (droits par doc + watermark + logs)` → `Q&A`. **Anonymisation par défaut** (pas de nom, pas d'éléments ré-identifiants). Aucun accès identifiant sans NDA signé.

### C7 — Vocabulaire réglementaire (conformité by-design)

**Interdit** dans toute l'UX/microcopy : « plateforme de financement », « marketplace d'investissement », « financement garanti », « rendement », « collecte », « accès aux investisseurs » (au sens vente d'accès). **À utiliser** : « préparation au financement », « readiness », « dealflow qualifié pour investisseurs qualifiés », « mise en relation privée », « conseil ». **Disclaimers** présents là où c'est utile : non-garantie de financement ; pas de conseil en investissement aux investisseurs ; investisseurs réputés qualifiés procédant à leur propre évaluation ; pas d'offre au public.

### C8 — Instrument de financement = filtre de premier rang

Côté investisseur et matching, l'**instrument** (equity / dette / quasi-equity / subvention) est un **filtre dur** au même titre que pays, secteur, ticket, stade, exclusions. Côté entrepreneur, la recommandation oriente vers l'instrument adapté au profil de cash-flow.

### C9 — Mobile-first / réalité régionale

Première session entrepreneur **< 10 minutes** ; demander les **pièces sensibles plus tard** (après l'effet « wow ») ; **rassurer sur la confidentialité fiscale** (frein majeur) ; OTP + canal WhatsApp ; reprise après coupure + sauvegarde automatique ; **multi-devise FCFA / EUR / USD** ; **FR par défaut, EN pour l'investisseur** ; documents et formats **OHADA / SYSCOHADA**.

### C10 — Réalité opérationnelle du Cabinet (le goulot)

Le cockpit doit gérer le **goulot consultant** : gating des dossiers faibles, **priorisation** impitoyable, SLA (mini-rapport < 48 h, réponse investisseur < 24 h, data room < 5 j après NDA), plafond ~5-10 dossiers actifs par senior. L'UX doit **réduire la revue manuelle**, pas la multiplier.

### C11 — KPI cibles du CDC (à instrumenter)

Complétion du diagnostic ≥ 40 % ; conversion diagnostic → pack payant ≥ 15 % ; ≥ 3 packs vendus (fin MVP) ; teaser → intérêt investisseur ≥ 30 % ; ≥ 1 entrée en DD/term sheet ; 1 programme sponsorisé signé.

### C12 — Modules de référence

Mappe chaque écran proposé aux modules du CDC (M1 à M23) et indique sa phase. *(M1 accès · M2 référentiel entreprises · M3 onboarding · M4 documents · M5 scoring · M6 mini-rapport · M7 catalogue/conversion · M8 espace mission · M9 référentiel investisseurs · M10 matching · M11 teaser/anonymisation · M12 NDA/non-circonvention · M13 data room · M14 Q&A · M15 KYC · M16 pipeline · M17 mandats/fees · M18 DD OHADA · M19 ESG · M20 CRM · M21 reporting · M22 admin/audit · M23 programmes sponsorisés.)*

---

# 1. Vision UX générale

Définis la vision UX en intégrant les contraintes C1-C12.

- Émotion visée chez l'**entrepreneur** : se sentir **compris, guidé et en contrôle** (« je comprends enfin pourquoi on me dit non, et j'ai un plan »), sans noyade dans le jargon ni sentiment d'examen punitif.
- Émotion visée chez l'**investisseur** : sentir un dealflow **rare, sélectionné et propre** ; gagner du temps analyste ; confiance par la traçabilité et l'anonymisation maîtrisée.
- Émotion visée chez le **consultant Cabinet** : **maîtrise et priorisation** ; voir d'un coup d'œil quoi traiter, quoi monétiser, quoi débloquer (cf. C10).
- Émotion visée chez le **sponsor/DFI _[CDC]_** : **redevabilité et impact** ; voir une cohorte progresser et un pipeline qualifié se constituer.
- Traduire confiance/confidentialité/sérieux : accès gradué visible (C6), anonymisation par défaut, statut transactionnel transparent, traçabilité (logs), langage institutionnel et conforme (C7).
- Éviter l'effet marketplace : pas de catalogue bruyant, pas de « offres » publiques, accès sur invitation/qualification, peu d'opportunités mais curées.

**Phrase directrice** (proposée, à challenger) : *« Une expérience sobre, confidentielle et guidée qui transforme un dossier brut en opportunité investissable. »*

**Propose 5 principes UX fondateurs** parmi/au-delà de : clarté avant complexité · confidentialité visible mais non anxiogène · action guidée · information progressive · premium sans surcharge · humain augmenté par la plateforme · contrôle et consentement · transparence du statut · confiance par la traçabilité · **conformité par le langage _[CDC : C7]_**.

---

# 2. Personas UX

Décris chaque persona avec : profil · maturité digitale · objectifs · peurs · irritants · informations voulues vite · actions principales · niveau de détail attendu · ton à adopter. **Respecte la cible entrepreneur « solide mais mal préparé » et ajoute le persona sponsor** _[CDC]_.

Personas à couvrir :

1. **Entrepreneur / dirigeant PME** *(cible : solide mais mal préparé)* — veut savoir s'il est finançable, sans jargon, ce qui manque, se sentir accompagné, garder le contrôle de ses données (peur fiscale forte → C9).
2. **CFO / responsable financier PME** — upload des pièces, données financières, comprendre les retraitements (SYSCOHADA), suivre les demandes Cabinet/investisseurs.
3. **Investisseur equity (PE / VC / impact)** — voir vite si le deal est dans sa thèse ; filtrer (pays, secteur, **instrument**, ticket, EBITDA/CA, impact) ; teasers propres ; éviter les dossiers faibles.
4. **Financeur de dette / mezzanine / DFI _[CDC]_** — logique d'instrument différente (cash-flow, garanties, covenants, additionnalité/impact, ESG) ; filtres et signaux adaptés.
5. **Investment analyst** — comparer, consulter/instruire les documents, poser des questions, suivre la DD, documenter le feedback.
6. **Partner / membre de comité d'investissement** — vue synthétique *executive-ready*, red flags, qualité de l'opportunité en quelques secondes.
7. **Consultant Cabinet** — décliner en **analyste** (qualification, enrichissement), **consultant senior** (préparation, relation investisseur), **conformité** (KYC/NDA/conflits), **ops-plateforme** (admin, données, reporting) _[CDC : rôles distincts]_.
8. **Sponsor institutionnel / DFI / banque _[CDC]_** — financer une cohorte, suivre avancement et impact (emplois, genre, climat, gouvernance), justifier le financement.
9. **Administrateur plateforme** — accès, permissions, logs, incidents, qualité des données.

---

# 3. Architecture UX globale

Propose l'architecture (espaces, menus, hiérarchie, navigation, dashboards, modules, niveaux d'accès) **sous forme de sitemap/tableau, chaque module mappé à M1-M23 et tagué MVP/V1/V2** _[CDC : C1, C12]_.

## Espace entrepreneur _(cœur du MVP)_
Accueil/dashboard · Mon diagnostic · Mon entreprise · Mes données financières · Mes documents (checklist) · Ma readiness (catégorie + gaps) · Mes recommandations · Mon accompagnement (packs) · Mes rendez-vous · Mes notifications · Paramètres & confidentialité. *(Mes financeurs potentiels, Ma data room, Mon suivi investisseur = **V1**.)*

## Espace investisseur _(V1 ; manuel au MVP)_
Dashboard · Critères d'investissement (dont **instrument**) · Opportunités/teasers anonymisés filtrables · Shortlist · Deals suivis · Data rooms (intégrées) · Q&A · Feedback · Alertes · Équipe · Paramètres.

## Espace cabinet _(cockpit minimal au MVP)_
Cockpit · Pipeline entrepreneur · Scoring · Mandats (léger) · Reporting *(MVP)* — puis Pipeline deals · Matching · Investisseurs · Teaser builder · Document checklist · Q&A · Fees *(V1)* — puis DD OHADA *(V2)*.

## Espace sponsor / DFI _[CDC]_ _(simple au MVP → V1)_
Vue cohorte · Avancement readiness · Pipeline qualifié · Reporting d'impact (agrégé/anonymisé).

## Back-office admin
Utilisateurs · Rôles & permissions · Logs/audit · Sécurité · Config scoring · Config matching · Templates · Workflows · Paramètres pays/devise · Paramètres documents · Paramètres réglementaires.

Indique pour chaque espace : niveaux d'accès et **règles de visibilité** (notamment C4 score, C6 accès gradué).

---

# 4. Parcours UX entrepreneur complet

Conçois un parcours **très guidé, fluide et rassurant** — jamais un formulaire administratif interminable, mais un *parcours de préparation au financement*. Pour chaque étape : objectif UX · écran · contenu · actions · microcopy (conforme C7) · frictions à éviter · éléments premium · éléments de réassurance · données collectées · sortie attendue. **Tague chaque étape MVP/V1/V2** et respecte C9 (1ère session < 10 min, pièces sensibles plus tard, peur fiscale).

Étapes (avec phase recommandée) :
1. Landing privée _(MVP)_ · 2. Création de compte + OTP _(MVP)_ · 3. Qualification rapide _(MVP)_ · 4. Promesse/valeur _(MVP)_ · 5. Questionnaire de financement progressif _(MVP)_ · 6. Profil entreprise _(MVP)_ · 7. Données financières _(MVP, en fourchettes d'abord)_ · 8. Upload documentaire **après l'effet wow** _(MVP)_ · 9. Analyse en cours _(MVP)_ · 10. **Readiness : catégorie + gaps** _(MVP — pas de score brut, C4)_ · 11. Recommandations + **instrument** _(MVP)_ · 12. Proposition de diagnostic/pack _(MVP, anti pay-to-play C5)_ · 13. Prise de RDV Cabinet _(MVP)_ · 14. Passage offre payante _(MVP devis ; paiement en ligne V1)_ · 15. Préparation du dossier (espace mission) _(V1 ; léger MVP)_ · 16. Validation du teaser _(V1)_ · 17. **Consentement de partage** _(V1, C6)_ · 18. Matching financeurs _(V1)_ · 19. Mise en relation _(V1)_ · 20. Suivi des statuts _(V1)_ · 21. Data room _(V1, intégrée/achetée C3)_ · 22. Questions investisseurs _(V1)_ · 23. Feedback _(V1)_ · 24. Term sheet/closing _(V2)_ · 25. Post-closing/réorientation _(V2)_.

Important — l'entrepreneur doit se sentir **accompagné et en contrôle**. L'effet « wow » = un **mini-rapport personnalisé** (catégorie + 3-5 blocages + instrument adapté + « ce qui vous sépare d'un dossier bancable »), pas un chiffre.

Fournis aussi : **(a)** une version courte du parcours **en 5 étapes** (Découvrir → Diagnostiquer → Comprendre sa readiness → Choisir un accompagnement → Avancer) ; **(b)** la version détaillée ; **(c)** les **écrans MVP prioritaires** (étapes 1-14) ; **(d)** les écrans repoussés en V1/V2 (15-25).

---

# 5. Parcours UX investisseur / PE complet _(V1 ; manuel au MVP — C1/C2)_

> **Cadrage CDC :** au **MVP, il n'y a pas de portail investisseur** ; le Cabinet envoie les teasers à la main et qualifie manuellement. Conçois ce parcours comme le **livrable V1**, en précisant ce qui reste manuel au MVP.

Pour chaque étape : objectif UX · écran · contenu · actions · informations visibles · **niveau d'anonymisation** · microcopy (C7) · éléments de confiance · éléments de productivité · données · sortie.

Étapes : 1. Invitation / demande d'accès · 2. Création profil investisseur · 3. **Validation par le Cabinet** (manuelle) · 4. Critères d'investissement (**dont instrument**, C8) · 5. Dashboard · 6. Opportunités recommandées · 7. Teasers **anonymisés** · 8. Filtres avancés · 9. Shortlist · 10. Comparaison · 11. Manifestation d'intérêt · 12. Attente du **consentement entrepreneur** (C6) · 13. **NDA + non-circonvention** (e-sign, C3/C6) · 14. Accès data room (achetée, droits/watermark/logs) · 15. Q&A · 16. Feedback · 17. DD · 18. Management meeting · 19. Term sheet · 20. Closing · 21. Historique.

Le dealflow doit paraître **sélectionné, filtré, rare et sérieux** — pas un catalogue bruyant. Chaque deal = une opportunité **qualifiée**, données clés lisibles en quelques secondes.

Fournis aussi :
- structure d'une **carte « opportunité investisseur »** (anonymisée) : secteur, géo approximative, taille, instrument, ticket, 2-3 signaux forts, label « revu par le Cabinet » — **sans** score readiness (C4) ;
- structure d'une **page détail teaser** (avant NDA) ;
- structure d'une **shortlist** ;
- les **filtres indispensables** : pays, secteur, **instrument** (C8), fourchette de ticket, stade, exclusions, ESG/impact ;
- les **signaux de qualité** à afficher (sans exposer le score) et les **signaux de risque / red flags** ;
- les **informations à masquer avant NDA** (identité, éléments ré-identifiants, documents détaillés) et **à révéler après NDA**.

---

# 6. Parcours UX consultant cabinet _(cockpit minimal MVP → V1)_

Conçois le cockpit pour piloter toute l'activité, **en gérant le goulot consultant** (C10 : gating, priorisation, SLA, plafond dossiers/senior). Écrans : cockpit global · pipeline entrepreneur · pipeline deal _(V1)_ · fiche entreprise · fiche investisseur _(V1)_ · fiche deal _(V1)_ · matching screen _(V1)_ · task center · document checklist · fee tracker _(V1)_ · reporting · admin permissions.

Pour chaque écran : objectif · données affichées · actions principales · indicateurs · alertes · éléments de priorisation · complexité · **priorité MVP/V1/V2** et **module M\***.

Le consultant doit répondre vite à : quels dossiers traiter aujourd'hui ? · qui est qualifié ? · quels dossiers sont monétisables ? · quels deals sont *investor-ready* ? · quels investisseurs relancer ? · quels dossiers bloquent (pièces manquantes) ? · quels deals ont une forte probabilité de closing ? · quels revenus sont attendus ? · **quels dossiers relèvent d'un programme sponsorisé ?** _[CDC]_

---

# 7. Design des dashboards

Pour chaque dashboard : hiérarchie visuelle · KPI cards · graphiques · alertes · CTA · zones de réassurance · erreurs à éviter. **Aligne les KPI sur C11.**

## Dashboard entrepreneur _(MVP)_
Statut du parcours · **catégorie de readiness** (pas le score brut, C4) · pièces manquantes · prochaines actions · recommandations + instrument · rendez-vous · niveau de confidentialité · progression vers présentation investisseur.

## Dashboard investisseur _(V1)_
Opportunités recommandées · shortlist · NDA en attente · data rooms ouvertes · Q&A en cours · nouveaux deals · filtres de thèse (dont instrument) · alertes.

## Dashboard cabinet _(MVP léger → V1)_
Leads · **taux de qualification, complétion, conversion diagnostic→pack** (C11) · dossiers *investor-ready* · diagnostics/packs vendus · mandats actifs · investisseurs engagés · deals en NDA · deals en data room · term sheets · closings · revenus attendus · **cohortes sponsorisées**.

## Dashboard sponsor / DFI _[CDC]_ _(MVP simple → V1)_
Taille et avancement de la **cohorte** · part *investor-ready* · pipeline qualifié · **indicateurs d'impact** (emplois, genre, climat, gouvernance) — agrégés/anonymisés.

## Dashboard admin
Utilisateurs actifs · accès sensibles · logs · erreurs · documents partagés · KYC en attente · sécurité · qualité des données.

---

# 8. Écrans clés à designer

Liste **tous** les écrans avec : objectif · utilisateur · **priorité MVP/V1/V2** · **module M\*** · composants · CTA principal · CTA secondaire · donnée critique · risque UX. **Respecte C1** (le portail investisseur, le matching, la data room, le NDA, la Q&A, le pipeline deal sont **V1**).

- **Publics/acquisition** _(MVP)_ : landing · « Évaluer ma capacité à lever des fonds » · « Accès investisseur » (sur invitation) · « Comment ça marche » · confidentialité · offres/packs (anti pay-to-play) · demande de RDV.
- **Entrepreneur** _(MVP sauf indication)_ : signup · login · dashboard · questionnaire · profil entreprise · données financières · upload · checklist documents · **readiness (catégorie)** · rapport synthétique · recommandations · offres d'accompagnement · prise de RDV · consentement de partage _(V1)_ · data room _(V1)_ · suivi investisseur _(V1)_ · notifications.
- **Investisseur** _(V1)_ : demande d'accès · profil · critères (instrument) · dashboard · opportunités · carte deal · détail teaser · shortlist · comparaison · NDA · data room · Q&A · feedback · pipeline.
- **Cabinet** : cockpit _(MVP)_ · liste/fiche entreprise _(MVP)_ · scoring _(MVP)_ · liste/fiche investisseur _(V1)_ · liste/fiche deal _(V1)_ · matching _(V1)_ · teaser builder _(V1)_ · document checklist _(MVP)_ · task center _(MVP)_ · pipeline _(V1)_ · mandats _(MVP léger)_ · fees _(V1)_ · reporting _(MVP léger → V1)_.
- **Sponsor/DFI** _[CDC]_ : espace cohorte · reporting d'impact _(MVP simple → V1)_.
- **Admin** : utilisateurs · rôles · permissions · logs · paramètres scoring · paramètres matching · templates · workflows · config pays/devise · sécurité.

---

# 9. Wireframes textuels

Produis des wireframes textuels exploitables pour Figma. **Priorise les écrans MVP** (1-5, 10, 15) ; marque clairement ceux qui sont V1 (6-9, 11-14). Structure imposée : `[Header] [Hero/résumé] [KPI ou statut] [Contenu principal] [Actions] [Sidebar] [Messages de réassurance] [Footer/aide]`.

À produire :
1. Landing premium _(MVP)_ · 2. Dashboard entrepreneur _(MVP)_ · 3. Questionnaire de diagnostic _(MVP)_ · 4. Écran **readiness (catégorie + gaps, indice de confiance)** _(MVP, C4)_ · 5. Écran recommandations + instrument _(MVP)_ · 6. Dashboard investisseur _(V1)_ · 7. Carte opportunité investisseur (anonymisée, sans score) _(V1)_ · 8. Page détail teaser _(V1)_ · 9. Shortlist investisseur _(V1)_ · 10. Cockpit cabinet _(MVP)_ · 11. Fiche deal cabinet _(V1)_ · 12. Écran matching _(V1)_ · 13. Data room (intégrée/achetée) _(V1)_ · 14. Q&A _(V1)_ · 15. Consentement entrepreneur _(V1, C6)_.

Pour chaque wireframe, intègre les **messages de réassurance** conformes (C7) et les **statuts de confidentialité** (C6).

---

# 10. Ton UX et microcopy

Stratégie de microcopy **premium et conforme** : clarté, autorité, sobriété, sans jargon inutile, sans promesse excessive, sans ton startup léger ni froideur bancaire. **Respecte impérativement le vocabulaire réglementaire C7** (interdits/préférés) et insère les disclaimers utiles.

Propose des exemples (FR par défaut, EN pour l'investisseur) pour :
- **Entrepreneurs** : accueil · invitation à démarrer le diagnostic · explication de la **catégorie de readiness** (pas « note ») · pièces manquantes · recommandation de service (anti pay-to-play C5) · consentement avant partage (C6) · dossier non prêt (bienveillant, orienté progression) · dossier *investor-ready* · demande de RDV.
- **Investisseurs** : invitation à consulter une opportunité **qualifiée** · explication d'un teaser **anonymisé** · manifestation d'intérêt · **NDA + non-circonvention requis** · accès data room · feedback demandé · deal hors critères (motivé) · nouvelle opportunité compatible.
- **Cabinet** : alerte dossier incomplet · investisseur intéressé · deal bloqué · relance à effectuer · score à revoir · mandat à proposer · **dossier éligible à un programme sponsorisé** _[CDC]_.

Donne, pour chaque cas, une version **conforme** et signale tout terme à bannir (C7).

---

# 11. Design system premium

Direction artistique : premium, institutionnelle, moderne, sobre, rassurante, orientée finance, **adaptée à l'Afrique francophone sans folklore**, internationale mais localement crédible.

## Palette
Couleur principale (confiance/institutionnel) · secondaire · accent (action, parcimonieux) · couleurs d'état · **couleurs de risque** (red flags) · succès · neutres. **Explique l'usage**, pas seulement les noms. Prévois un usage sobre des couleurs « risque » (ne pas dramatiser la catégorie readiness, C4).

## Typographie
Style · hiérarchie · titres · **chiffres financiers** (tabular figures, alignement) · petits textes (mentions/disclaimers C7) · lisibilité mobile (C9).

## Composants
Cards · KPI cards · **deal cards (anonymisées)** · badges · **readiness category badge** (4 niveaux, pas un score-ring punitif — C4) · score ring **réservé à la vue Cabinet** · progress stepper · tables · filters (dont **instrument**) · side panels · modals · confirmation panels (avant partage, C6) · document uploaders · **connecteur data room (vue intégrée d'une VDR achetée)** _[CDC : C3]_ · timeline · activity feed/logs · Q&A threads · permission chips · risk badges · **investor fit score (vue Cabinet/investisseur, ≠ readiness score)** · CTA premium.

## Iconographie
Style sobre, fil de fer fin/duotone. Représenter : confidentialité, deal, instrument de financement, documents, risque, progression. Éviter les icônes « marketplace/e-commerce » (paniers, étoiles de notation publique).

## Motion design
Sobre et rassurant : transitions, chargements, progression, confirmation, **score/catégorie reveal** (digne, pas gamifié), upload, accès data room, NDA signé. Le motion **rassure et fluidifie**, ne distrait pas.

---

# 12. Expérience premium

Décris concrètement le premium : onboarding très guidé · progression visible · espace privé · langage institutionnel (C7) · cartes deal élégantes (anonymisées) · data-viz propre · **catégorie de readiness présentée intelligemment** (progression, pas punition — C4) · documents organisés · sentiment de contrôle · **confirmation avant partage** (C6) · réactivité · **accompagnement humain visible** (concierge/analyst support, RDV expert — cœur du positionnement boutique) · rapports PDF élégants · teasers générés professionnellement · synthèses *executive-ready*.

Fournis : **10 détails UX qui font premium** · **10 erreurs qui font amateur** (inclure : exposer le score à l'investisseur, vocabulaire « financement garanti », catalogue bruyant, sur-collecte de pièces en première session) · **10 éléments de réassurance** (inclure : statut d'anonymisation, « qui peut voir ceci ? », logs de consultation, mention confidentialité fiscale — C9).

---

# 13. Fluidité et réduction de friction

Pour chaque friction : problème · solution UX · **règle produit** · phase (MVP/V1/V2). Intègre les frictions spécifiques du CDC.

- **Entrepreneurs** : formulaire trop long → collecte progressive < 10 min (C9) · pièces indisponibles → demande différée + checklist · **peur de partager (fisc)** → réassurance confidentialité + accès limité (C9) · jargon → catégorie + langage clair (C4/C7) · frustration si non qualifié → orientation/nurturing bienveillant, pas de mur · **paiement avant valeur perçue → packs après l'effet wow** (C5) · faible maturité digitale → mobile-first, WhatsApp.
- **Investisseurs** : trop peu d'info avant NDA → teaser riche mais anonymisé (C6) · deals non pertinents → filtres durs dont instrument + curation (C8) · **scoring non crédible → ne pas exposer le score, montrer le label de curation** (C4) · friction de connexion → SSO/invitation · mauvaise data room → VDR achetée de qualité (C3) · Q&A lente → SLA (C10) · manque de feedback loop → formulaire de refus structuré.
- **Cabinet** : trop de leads faibles → **gating** (C10) · surcharge de revue → priorisation + automatisation de la qualification · doublons → dédup (M2) · documents mal nommés → checklist normalisée · absence de priorisation → cockpit trié par SLA/probabilité · relances manuelles → rappels/notifications.

---

# 14. Confidentialité, consentement et confiance

Conçois l'UX de confidentialité **autour de la séquence d'accès gradué C6** et de la matrice de permissions du CDC (Annexe B). Rends la sécurité **visible sans devenir anxiogène**.

Propose : affichage du **niveau de confidentialité** · explication de l'**anonymisation** (avant NDA) · **demande de consentement entrepreneur** (granulaire, révocable, tracé) · « **qui a accès à quoi** » · gestion de l'accès **après NDA + non-circonvention** · prévention des partages non autorisés (watermark, interdiction d'export selon sensibilité) · **logs de consultation** · réassurance sur la sécurité documentaire (VDR achetée).

Composants/écrans : privacy banner · consentement de partage · access control panel · document visibility status · **NDA + non-circonvention status** · audit activity · « who can see this? » · « request access » · « revoke access ».

---

# 15. Scoring et visualisation financière

Conçois l'affichage du **Financing Readiness Score en respectant strictement C4** : sortie en **4 catégories** (*Investor-ready / À préparer / Plutôt dette-banque / Trop précoce*), **gating documentaire**, **indice de confiance**, et **règles de visibilité** (entrepreneur = catégorie + gaps ; Cabinet = score complet + sous-scores ; **investisseur = jamais le score**).

Précise : catégorie globale · sous-scores (**vue Cabinet uniquement**) · niveau de fiabilité/confiance · explication de la catégorie · actions recommandées (→ packs, instrument) · documents impactant le score · comparaison au seuil *investor-ready* · marges d'amélioration · mise à jour après vérification des pièces.

Visualisations (en distinguant la **vue entrepreneur** de la **vue Cabinet**) : readiness **ladder** (progression, recommandé côté entrepreneur) · checklist · barres de progression · score ring **(Cabinet)** · radar des sous-dimensions **(Cabinet)** · heatmap des gaps · benchmark sectoriel · timeline de progression. **Le rendu entrepreneur doit être un outil de préparation et de progression, jamais une note scolaire punitive.**

---

# 16. UX du matching investisseur _(manuel au MVP → outillé V1 — C1/C2)_

Conçois l'UX du matching **avec validation humaine obligatoire** (le moteur propose, le consultant dispose) et l'**instrument comme filtre dur** (C8).

**Pour le Cabinet** _(V1)_ : écran de matching · **filtres durs** (pays, secteur, **instrument**, ticket, stade, exclusions) · **score de fit** (somme pondérée de critères vérifiables) · justification du match · investisseurs recommandés · exclusions · **override humain** · shortlist · teaser à envoyer.

**Pour l'investisseur** _(V1)_ : « pourquoi ce deal m'est recommandé » · fit avec ma thèse (dont instrument) · points forts · points de vigilance/red flags · données clés · demander plus d'information · refuser avec motif (feedback loop) · sauvegarder. **Ne jamais afficher le readiness score** ici (C4).

Fournis : structure du **score de fit** (≠ readiness score) · badges de compatibilité · explication du matching · feedback loop investisseur · design des filtres · design de la comparaison de deals. Précise ce qui reste **manuel au MVP** (shortlist sur tableur, envoi manuel du teaser).

---

# 17. UX data room et Q&A _(V1 ; solution achetée — C3)_

> **Cadrage CDC :** la data room n'est **pas construite** ; c'est une **VDR achetée** (iDeals / Ansarada / Datasite). Le travail UX porte sur **l'intégration (SSO/embed), la couche de permissions/anonymisation et la cohérence visuelle**, pas sur la reconstruction d'une VDR.

Couvre (via la solution intégrée) : structure de dossiers · documents requis/fournis/manquants · versioning · statut de validation · **permissions par document et par investisseur** · watermark dynamique · logs d'accès · recherche · prévisualisation · **téléchargement contrôlé** · expiration d'accès. Respecte l'accès gradué (C6) : aucun document identifiant avant NDA.

Module **Q&A** _(email cadré au MVP → in-app V1)_ : poser · catégoriser · assigner · répondre · valider la réponse · lier à un document · suivre le statut · gérer les relances (SLA C10) · exporter l'historique. UX simple, sobre, très lisible.

---

# 18. Responsive et mobile-first

Stratégie **mobile-first** pour l'UEMOA/CEMAC (C9). Précise : ce qui doit être faisable sur mobile (tout le parcours entrepreneur jusqu'au RDV) vs ce qui reste desktop (cockpit cabinet, instruction investisseur en data room) · uploads depuis téléphone (photo de pièces, compression) · **intégration WhatsApp** (relances, reprise de parcours, notifications) · gestion des connexions instables (sauvegarde auto, reprise, files d'attente d'upload) · réduction de la saisie (fourchettes, choix guidés) · conception pour utilisateurs **peu habitués aux plateformes financières**.

Détaille : parcours **mobile entrepreneur** (prioritaire) · parcours **mobile investisseur** (consultation teaser/Q&A — V1) · parcours **desktop cabinet** · cas d'usage **WhatsApp** · cas d'usage **email**.

---

# 19. Accessibilité, langues et localisation

Recommandations : **FR par défaut**, **EN pour l'investisseur** (C9) ; portugais/espagnol en option future · **devises FCFA / EUR / USD** (formats, conversion d'affichage) · formats de date · pays **UEMOA / CEMAC** · secteurs · documents et postes **OHADA / SYSCOHADA** (libellés, retraitements) · niveau de langage accessible (anti-jargon) · **WCAG AA** (contraste, lisibilité, navigation clavier) · formulaires simples. Précise l'architecture i18n et la gestion multi-devise dès la conception.

---

# 20. Parcours MVP recommandé _(= couche 1 du CDC — C1)_

Objectif : lancer vite sans perdre le premium, en **prouvant l'adoption et la conversion** (C11) avant de construire le biface.

## MVP entrepreneur _(cœur)_
Écrans indispensables : landing · signup/OTP · questionnaire progressif · profil + données (fourchettes) · upload + checklist · **readiness (catégorie + gaps)** · mini-rapport · catalogue de packs · prise de RDV. Livrable immédiat : le **mini-rapport personnalisé**. Premium minimal : guidage, progression, réassurance, langage institutionnel. Automatisé : qualification, scoring interne, mini-rapport. Manuel accepté : préparation, facturation (devis).

## MVP investisseur _(manuel — pas de portail)_
Pas d'écrans in-app au MVP : **teasers anonymisés envoyés à la main** par le Cabinet, qualification et NDA **manuels** (e-sign), data room **achetée**. Le seul « écran » éventuel : une page d'**accès investisseur** sur invitation. Conçois la **trame du teaser** et de l'email d'introduction (conformes C7). Tout le portail = V1.

## MVP cabinet _(cockpit minimal)_
Cockpit : pipeline entrepreneur · scoring · statuts dossiers · document checklist · task center · mandats (léger) · reporting MVP (KPI C11) · **suivi cohorte sponsorisée (simple)**. Matching = **tableur + jugement**, teaser = **gabarit**.

## MVP sponsor _[CDC]_
Une vue cohorte + reporting simple (peut être un export/PDF au départ).

Pour chaque MVP : objectifs · écrans · composants · **critères de succès (C11)** · métriques UX · limites assumées.

---

# 21. Roadmap UX V1 / V2 _(miroir du phasage CDC)_

| Phase | Focus UX | Écrans/composants à ajouter | Critère de passage (CDC) | Risques |
|---|---|---|---|---|
| **MVP** | Acquisition, diagnostic, **catégorie de readiness**, conversion vers packs ; cockpit minimal ; reporting sponsor | Funnel entrepreneur complet, cockpit, dashboards MVP | Complétion ≥ 40 % · diagnostic→pack ≥ 15 % · ≥ 3 packs · ≥ 1 deal en DD (manuelle) | Construire au lieu de vendre |
| **V1** | **Portail investisseur**, matching outillé, **data room (achetée) + NDA + Q&A**, pipeline deal, fees, reporting cabinet ; espace sponsor | Espace investisseur, fiche/fiche deal, matching screen, teaser builder, fee tracker, intégration VDR/e-sign/KYC | Teaser→intérêt ≥ 30 % · 1 closing · 1 programme sponsorisé signé · unit economics positives | Sélection adverse ; flux tari ; sur-build |
| **V2** | Intelligence, automatisation, **DD OHADA/SYSCOHADA**, ESG, market insights, personnalisation, expérience institutionnelle | DD OHADA, ESG screening, market intelligence, comparaison avancée, alertes IA | Rentabilité par marché ; pipeline DFI multi-pays | Dispersion |

Pour chaque phase : objectifs UX · écrans à ajouter · composants à enrichir · risques · critère de passage.

---

# 22. KPI UX et product analytics

KPI à suivre, **alignés sur les cibles C11**. Pour chaque KPI : définition · événement analytics à tracker · **seuil de succès** · action d'amélioration si mauvais.

- **Entrepreneur** : taux de démarrage diagnostic · **taux de complétion (cible ≥ 40 %)** · temps moyen de complétion (cible < 10 min) · abandon par étape · taux d'upload · taux de prise de RDV · **conversion vers pack payant (cible ≥ 15 %)**.
- **Investisseur** _(V1)_ : taux d'activation · deals consultés · deals shortlistés · **taux de manifestation d'intérêt / teaser (cible ≥ 30 %)** · taux NDA signé · taux de feedback · temps avant première action · récurrence de connexion.
- **Cabinet** : temps de revue dossier · **nombre de dossiers traités/consultant (vs plafond ~5-10, C10)** · taux de matching validé · taux d'introduction · taux de relance · taux de conversion en mandat.
- **Sponsor _[CDC]_** : avancement de cohorte · part *investor-ready* · indicateurs d'impact.

---

# 23. Livrables attendus

À la fin de ta réponse, fournis : **(1)** synthèse de la vision UX (10 lignes) · **(2)** sitemap global (mappé M1-M23, tagué MVP/V1/V2) · **(3)** parcours entrepreneur, investisseur (V1) et cabinet, + flux sponsor · **(4)** liste priorisée des écrans · **(5)** wireframes textuels des écrans critiques (priorité MVP) · **(6)** principes de design system · **(7)** microcopies clés (conformes C7) · **(8)** recommandations mobile-first (C9) · **(9)** règles UX de confidentialité (C6) · **(10)** MVP UX recommandé (= couche 1) · **(11)** erreurs à éviter · **(12)** prochaines étapes pour produire une maquette Figma.

---

# 24. Contraintes de style de réponse

Réponds en **français**. Style professionnel, précis, premium, orienté décision. Tableaux quand utile. Concret, pas théorique. Parcours et écrans **directement exploitables**. Évite le jargon UX inutile. Explique les choix. **Priorise fortement MVP/V1/V2 selon le phasage CDC (C1).** Pense comme un designer produit senior. La réponse doit permettre à un PO, un UI designer et un dev front-end de démarrer. **En cas de doute, les contraintes C1-C12 priment.**

---

## Récapitulatif des révisions (alignement CDC)

1. **Périmètre MVP recentré sur la couche 1** : le portail investisseur, le matching outillé, la data room in-app, le NDA workflow, la Q&A et le pipeline deal passent en **V1** ; au MVP ils sont **manuels** (C1/C2).
2. **Ajout du persona + espace + dashboard « sponsor institutionnel / DFI »** (payeur ancre) et des **programmes sponsorisés** (C1, M23).
3. **Buy-don't-build explicité** : data room, e-sign, KYC, CRM, BI sont **achetés/intégrés**, pas reconçus ; l'UX en fait une couche d'intégration (C3).
4. **Règles de visibilité du readiness score** : 4 catégories, gating documentaire, indice de confiance, **score jamais exposé à l'investisseur** ; rendu entrepreneur non punitif (C4).
5. **Anti pay-to-play** intégré au parcours et à la microcopy (C5).
6. **Vocabulaire réglementaire contraint** (termes interdits/préférés + disclaimers) injecté dans la microcopy et le design system (C7).
7. **Instrument de financement** promu **filtre dur de premier rang** ; cible financeur élargie à la **dette/mezzanine/DFI** (C8) + persona dédié.
8. **Mobile-first régional précisé** : 1ère session < 10 min, pièces sensibles différées, peur fiscale, WhatsApp, multi-devise FCFA/EUR/USD, OHADA/SYSCOHADA (C9).
9. **Réalité opérationnelle du Cabinet** (gating, SLA, plafond dossiers/senior) intégrée au cockpit (C10).
10. **KPI alignés sur les cibles du CDC** (complétion ≥ 40 %, conversion ≥ 15 %, teaser→intérêt ≥ 30 %, etc.) (C11).
11. **Mapping systématique des écrans aux modules M1-M23** et au phasage (C12).
12. **Roadmap UX calquée sur le phasage CDC** (MVP/V1/V2) avec critères de passage.

> Le reste de la structure d'origine (24 sections) est conservé pour rester familier et complet ; seules les orientations contraires au CDC ont été corrigées.



