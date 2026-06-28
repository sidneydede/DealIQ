# Revue critique — Cadrage AMOA « Plateforme privée de qualification, matching et deal execution PME ↔ investisseurs » (UEMOA / CEMAC)

> **Base de la revue.** Cette analyse porte exclusivement sur le document *« Cadrage AMOA pour une plateforme privée de qualification, matching et deal execution entre PME et investisseurs en Afrique de l'Ouest et Afrique Centrale »* (≈ 23 000 caractères, 6 tableaux, sourcé : IFC, Banque mondiale, AVCA, BCEAO, GSMA, OHADA, AMF-UMOA, COSUMAF, Datasite, Affinity, DealCloud, LSEG, Moody's). Le cadrage est **de bonne facture** : la critique vise donc les angles morts qui subsistent *malgré* sa qualité, pas des fautes de débutant.

---

# 1. Executive review

La vision est **claire, bien argumentée et juridiquement lucide** : refuser la marketplace ouverte au profit d'une plateforme privée, curée, B2B, à investisseurs qualifiés et accès gradués, est le bon choix en UEMOA/CEMAC (offre publique = visa obligatoire ; placement privé = autre régime). Le problème est **réel et chiffré** (déficit MSME 5,7–8 Tn$, PME ouest-africaines jugées risquées faute de documentation), et le choix « vendre la *readiness*, pas le financement » est juste. La proposition de valeur est **forte côté entrepreneur** (« suis-je finançable, par qui, qu'est-ce qui manque ? ») mais **encore non prouvée là où le métier se gagne** : la **sélection adverse** (les bons dossiers vont en direct ; rien dans le cadrage ne *source activement* la qualité — il ne fait que *filtrer* l'inbound) et le **« qui paie en premier »** (le cadrage met l'entrepreneur cash-pauvre en payeur MVP et relègue la DFI/le sponsor — payeur le plus naturel — en V2). Le cadrage ne doit **pas être construit tel quel** : son MVP « 4 lots » est en réalité une mini-plateforme biface, et il **se contredit lui-même** (les briques matching/teaser/recommandations sont cochées « MVP », alors que la reco finale prône 3 couches *séquentielles*). Pire, sa propre donnée AVCA (Afrique de l'Ouest : **73 deals / ~0,3 Md$ en 2025**) invalide l'idée d'un *moteur* de matching dès le MVP : à ce volume, le matching est un tableur + du jugement humain. **Risque principal :** construire la plateforme biface (les 4 lots) avant d'avoir prouvé manuellement l'économie du deal et l'adoption des deux faces. **Levier principal :** la curation humaine et le réseau du cabinet transformés en confiance investisseur — l'actif défendable est la donnée propriétaire + la réputation, jamais l'algorithme.

### Note globale : **66 / 100**

| Critère | Note | Justification |
|---|---|---|
| Vision stratégique | **16 / 20** | Positionnement privé/curé/gradué excellent et juridiquement cohérent. Mais identité non tranchée : *boutique de conseil tech-enabled* vs *plateforme scalable*. |
| Pertinence marché | **15 / 20** | Bien sourcé, problème réel. Mais la demande est cadrée « PE/VC » alors que le missing middle relève surtout de **dette/mezzanine/garanties/DFI** ; et la donnée AVCA n'est pas utilisée pour discipliner le périmètre. |
| Cohérence fonctionnelle | **12 / 20** | **Incohérence interne** MVP-4-lots vs reco-3-couches ; moteur de matching en MVP contredit le volume de marché ; trop de briques *front-loaded*. |
| Faisabilité MVP | **8 / 15** | Le MVP reste une plateforme biface. Le vrai MVP doit être à ~80 % manuel et mono-hypothèse. |
| Monétisation | **9 / 15** | Modèle hybride intelligent, mais 12 sources dispersent le focus ; **payeur le plus dur (entrepreneur) mis en premier**, payeur le plus naturel (DFI/banque) en V2. |
| Gestion des risques | **6 / 10** | Réglementaire, confidentialité, conflits, pay-to-play bien traités. Sous-traités : **sélection adverse, capacité opérationnelle du cabinet, agrément d'intermédiation, peur fiscale de l'entrepreneur**. |

**Lecture :** *cadrage solide, à recentrer avant industrialisation.* Mérite d'être piloté et financé **en pilote manuel**, pas en build complet.

---

# 2. Ce qui est solide dans les specs

**1. Le refus argumenté de la marketplace ouverte.** Adossé au droit réel (visa d'offre publique UMOA, distinction placement privé COSUMAF), ce choix protège juridiquement *et* commercialement (qualité du flux). C'est la décision de positionnement la plus importante et elle est bien prise. *Valeur :* défendabilité par la confiance, pas par le volume.

**2. « Vendre la readiness, pas le financement ».** Mettre la *transformation du dossier* au cœur (livrable maîtrisable et facturable) plutôt que le closing (non maîtrisable) est stratégiquement juste et réputationnellement protecteur. *Valeur :* on facture ce qu'on contrôle, on aligne le discours sur le non-« pay-to-play ».

**3. La catégorisation readiness en 4 sorties actionnables** (*investor-ready / à préparer / plutôt dette-banque / trop précoce*). Bien plus saine qu'un score nu : elle oriente vers le bon instrument et évite de sur-promettre un accès investisseur. *Valeur :* outil de tri *et* de conversion commerciale.

**4. L'accès gradué côté investisseur** (teaser anonymisé → intérêt → NDA → data room → Q&A → DD). C'est l'architecture de confiance correcte, alignée sur les standards Datasite/DealCloud. *Valeur :* concilie confidentialité entrepreneur et fluidité investisseur.

**5. L'ancrage régional réel** (OHADA 17 États, SYSCOHADA révisé, mobile-first justifié par la bancarisation UEMOA à 25,2 % stricte / 47,4 % élargie, mobile money > 2 Md comptes). La brique **DD OHADA/SYSCOHADA** (retraitements EBITDA, dette nette, BFR, revue fiscale/sociale) est un vrai différenciateur que les outils importés n'ont pas. *Valeur :* avantage local défendable.

**6. La logique build-vs-buy déjà posée** (construire : readiness, matching, OHADA, données, monétisation ; acheter : VDR, e-signature, KYC/AML). C'est la bonne intuition et elle évite de réinventer des briques commod-itisées. *Valeur :* concentre l'effort sur l'avantage propriétaire.

**7. Le sponsoring DFI/banque comme débouché.** Avoir identifié que la plateforme peut devenir une *infrastructure de programme* pour une DFI/banque (AfDB SME Program, IFC via intermédiaires) est l'angle de monétisation le plus prometteur — même si le cadrage le sous-exploite (voir §10).

**8. Un registre de risques explicite avec mitigations.** Le cadrage formalise déjà ses principaux risques (pay-to-play, réglementaire, confidentialité, faible adoption PE, qualité documentaire) et leur réponse. Cette discipline « risque » est un signe de maturité rare à ce stade. *Valeur :* base saine pour une gouvernance projet.

---

# 3. Ce qui est fragile, ambigu ou insuffisant

| # | Élément | Problème identifié | Impact | Gravité | Recommandation |
|---|---|---|---|---|---|
| 1 | Sélection adverse | Le cadrage *filtre* l'inbound mais ne *source* pas activement les bons dossiers. Les meilleurs vont en direct. | Base de dossiers moyens → investisseurs partent. | **Critique** | Stratégie de sourcing actif : référencements banques (refus « bons mais pas prêts »), incubateurs, Big4, réseaux cabinet. |
| 2 | Qui paie en premier | Entrepreneur cash-pauvre placé en payeur MVP ; DFI/sponsor en V2. | 12-18 mois de revenus faibles ; trésorerie sous tension. | **Critique** | Remonter le **programme sponsorisé DFI/banque** en MVP/V1 comme ancre de revenu ; entrepreneur = ticket d'engagement, pas la rente. |
| 3 | MVP « 4 lots » | C'est une mini-plateforme biface (matching + teaser + NDA + VDR + pipeline). Contredit la reco « 3 couches séquentielles ». | 9-15 mois avant preuve ; dispersion. | **Critique** | MVP = **couche 1 seule** (qualification entrepreneur), reste manuel (voir §7). |
| 4 | Moteur de matching en MVP | Le volume (73 deals/an en Afrique de l'Ouest, donnée du doc lui-même) ne justifie pas un *moteur*. | Build inutile ; faux positifs qui érodent la confiance. | **Élevée** | Filtres durs + curation humaine sur tableur ; pas de moteur avant V1/V2 (voir §9). |
| 5 | Cible financeur trop « PE/VC » | Le missing middle relève surtout de dette/mezzanine/garanties/DFI, pas d'equity PE. | Promesse de dealflow inadaptée à la demande réelle. | **Élevée** | Re-pondérer la demande vers dette/DFI/blended ; segmenter par **instrument**. |
| 6 | Capacité opérationnelle du cabinet | « Revue cabinet » partout = goulot humain non modélisé (heures-consultant/dossier, plafond de débit). | La plateforme crée *plus* de travail manuel qu'elle n'en économise. | **Élevée** | Modèle opérationnel + SLA + plafond de dossiers/consultant (voir §16). |
| 7 | Fiabilité du scoring | Inputs auto-déclarés/non audités, dans un environnement à faible documentation — le problème même qu'on prétend résoudre. | Score trompeur ; décrédibilisation. | **Élevée** | Score conditionné à des **pièces vérifiées** ; pondérations explicites ; labels « déclaré / non audité ». |
| 8 | Peur fiscale de l'entrepreneur | Onboarding demande RCCM, états financiers réels, bénéficiaires effectifs — exactement ce que cache l'entrepreneur à comptabilité informelle. | Les bons dossiers à livres informels fuient. | **Élevée** | Collecte progressive à faible menace + angle « on vous aide à formaliser » ; engagement de confidentialité fiscale. |
| 9 | Conflit d'intérêts structurel | Cabinet payé des deux côtés : de qui est-il l'agent dans la négociation ? | Défiance investisseur (curation suspecte) et entrepreneur (orienté vers qui paie). | **Élevée** | Disclosure ne suffit pas : définir **par deal** de qui on est mandataire ; muraille sur les fees (voir §10/§11). |
| 10 | Agrément d'intermédiation | Le doc traite l'offre publique vs privée, mais pas si l'*acte d'intermédiation rémunérée* (démarchage, conseil en investissement) requiert un agrément. | Requalification possible **même** en placement privé. | **Élevée** | Avis avocat ciblé sur démarchage/intermédiation CREPMF-AMF-UMOA & COSUMAF (voir §11). |
| 11 | Cold-start biface | « Commencer par un noyau d'investisseurs » est dit mais non opérationnalisé (combien, quel engagement, quelle preuve 90 j). | Plateforme vide d'un côté. | **Moyenne** | Séquencer : 10-20 investisseurs design-partners + offre curée à la main d'abord (voir §15/§18). |
| 12 | TAM réel non quantifié | Aucun chiffrage du nombre de PME bancables/an adressables par pays/secteur. | Marché peut-être trop mince pour le modèle. | **Moyenne** | Étude TAM en Phase 0 (PME 0,5-10 M$ CA, par pays). |
| 13 | 12 sources de revenus | Même priorisées, 4 streams en MVP = dispersion. | Focus dilué, exécution commerciale floue. | **Moyenne** | Un seul wedge monétisé d'abord : **le pack préparation** (voir §10). |

---

# 4. Challenge de la proposition de valeur

## 4.1 Entrepreneurs / PME

**Pourquoi vous plutôt que le direct ?** Un bon entrepreneur connecté ira en direct — il n'est pas votre cible. Votre cible est **l'entrepreneur solide mais mal préparé / mal connecté** : vraie activité, mais comptes SYSCOHADA faibles, pas de BP crédible, pas d'accès aux fonds. Le cadrage le sous-entend mais ne le nomme pas comme segment cible explicite — il faut le faire, sinon la promesse vise tout le monde et personne.

**Diagnostic gratuit assez attractif ?** Oui, *si* le livrable est un mini-rapport **actionnable** (« vos 5 angles morts + l'instrument adapté + ce qui manque »), pas un score nu. Le cadrage prévoit bien un « mini diagnostic » — bon — mais l'effet *wow* doit être l'orientation actionnable, pas le chiffre.

**Paiera-t-il un diagnostic approfondi ?** Rarement en cash significatif. Le consentement à payer se loge sur des **livrables tangibles** (BP, modèle financier, valorisation, teaser, data room), pas sur un « diagnostic approfondi » abstrait. Le cadrage a raison de prévoir des *packs* ; il devrait en faire le wedge n°1 plutôt que le « diagnostic expert ».

**Quand perçoit-il une valeur tangible ?** (1) mini-rapport gratuit (« je comprends enfin pourquoi on me dit non ») ; (2) livraison d'un dossier dont il est fier ; (3) **première vraie conversation avec un financeur sérieux**.

**Risque de frustration sans financement ?** Élevé et structurel. Le cadrage le mitige correctement (vendre la readiness, 4 catégories, pas de promesse). À renforcer : transparence sur les taux de succès réels.

**Éviter le « pay-to-play » ?** Le cadrage pose la bonne règle (« on paie la préparation, pas un financement garanti »). À durcir : afficher que **payer n'augmente pas la probabilité d'être *sélectionné* pour présentation** — seule la qualité du dossier le fait. Sinon la curation paraît achetable.

## 4.2 PE / VC / investisseurs

**Pourquoi paierait-il ?** Seulement pour du **temps gagné** (sourcing propriétaire qualifié) et de l'**accès** à des deals invisibles autrement. Jamais pour une base tout-venant. Sa douleur réelle ici = sourcing fiable + dossiers DD-ables (comptes SYSCOHADA propres). Le cadrage vise juste avec « peu d'opportunités mais mieux structurées ».

**Qualité minimale ?** Règle dure : **aucun dossier présenté qui ne passerait pas un premier comité**. Métrique reine = *taux teaser → intérêt*, pas le nombre d'inscrits.

**Ce qui rend un deal intéressant ?** Fit ticket × instrument × secteur × géo × stade × thèse + équipe + cash-flows réels + **dossier propre** (le différenciateur local). Pour DFI/impact : additionnalité, impact mesurable, gouvernance, pré-screening ESG (bien identifié par le cadrage via IFC).

**Éviter la base de dossiers faibles ?** Curation impitoyable + **sourcing actif** + ne pas confondre « inscrits » et « présentables ». Le cadrage n'a pas de réponse au sourcing *actif* de la qualité — c'est son angle mort (cf. §3, ligne 1).

**Preuve de valeur en 3 mois ?** Présenter à 10-20 investisseurs design-partners **1 à 3 deals excellents** et obtenir ≥ 1 entrée en DD. Pas une démo produit.

**Fonctions MVP investisseur réellement nécessaires ?** Très peu : teaser anonymisé clair, filtre par critères, accès data room sous NDA, canal Q&A. Dashboards/market intelligence = V2.

## 4.3 Cabinet de conseil

**Améliore-t-il le business model ?** Oui *si* la plateforme reste **canal d'acquisition + outil de productivité**, pas un produit-à-maintenir qui détourne le cabinet de son métier (faire des deals).

**Réduit-il le CAC ?** Potentiellement (inbound diagnostic + contenu + partenariats DFI/incubateurs/banques). Mais le diagnostic seul ne distribue pas : il faut un moteur d'acquisition (contenu, prescripteurs). Le cadrage n'a pas de plan de distribution — à ajouter.

**Améliore-t-il la conversion vers missions payantes ?** Oui si le parcours diagnostic → livrable → mandat est conçu comme un **tunnel commercial** instrumenté (le scoring sert à prioriser l'effort commercial).

**Actif propriétaire défendable ?** Oui — mais **la donnée + la réputation + les relations DFI**, pas le code. Le cadrage le dit ; à protéger juridiquement (propriété/consentement des données, §17).

**Services à vendre en priorité ?** Dans l'ordre : (1) **BP + modèle financier**, (2) valorisation + readiness report, (3) structuration/data room, (4) mandat (retainer + success fee). Diagnostic = gratuit (aimant). Abonnement investisseur & sourcing dédié = après preuve de flux.

---

# 5. Challenge du positionnement produit

Le cadrage formule **un bon positionnement** (« infrastructure privée de transformation de dossiers en opportunités investissables, puis orchestration jusqu'au closing ») — clair, défendable, juridiquement cohérent. Le problème n'est pas le *flou* (le cadrage est net), c'est l'**ampleur** : il revendique simultanément diagnostic + CRM dealflow + data room + conseil + sourcing PE + transaction support. En MVP, c'est trop : aucune de ces faces ne sera excellente.

**Identité économique à trancher :** le dossier penche clairement vers une **boutique de conseil tech-enabled** (marges projet, scalabilité humaine), pas une fintech/SaaS scalable ni une marketplace à effets de réseau. L'assumer change la valorisation, le discours aux financeurs du projet, et la séquence de build. La couche « plateforme investisseur » et « SaaS » est une **option future**, pas le cœur.

**Positionnement recommandé (1 phrase) :**
> « Nous rendons les PME d'Afrique francophone *bancables*, puis nous apportons aux financeurs un *dealflow préparé et pré-qualifié* — par une équipe d'experts, outillée par une plateforme. »

**Trois variantes :**
1. **Entrepreneur** : « En 10 minutes, sachez pourquoi les financeurs vous disent non — et obtenez le plan (et l'équipe) pour devenir finançable. »
2. **Investisseur** : « Des PME africaines pré-qualifiées, aux dossiers propres et structurés, filtrées sur *vos* critères — instrument, ticket, secteur, géographie. »
3. **Institutionnel / DFI / banque** : « Un dispositif clé en main pour préparer, qualifier et déployer du capital vers le *missing middle*, avec traçabilité, mesure d'impact et coût de sourcing/DD réduit. »

---

# 6. Challenge du périmètre fonctionnel

Le cadrage classe presque tout en MVP. Confronté au volume de marché et à la discipline d'exécution, voici le re-classement recommandé. Légende — Nécessité : **Indisp.** / Utile / Secondaire. Priorité : **MVP** / V1 / V2 / Reporter.

| Brique | Nécessité | Priorité **cadrage** | Priorité **recommandée** | Complexité | Risque sur-spéc. | Reco build/buy |
|---|---|---|---|---|---|---|
| Référentiel entreprises | Indisp. | MVP | **MVP** | Faible | Faible | Construire léger |
| Référentiel investisseurs + critères | Indisp. | MVP | **MVP** (tableur) | Faible | Moyen | Construire léger |
| Onboarding entrepreneur | Indisp. | MVP | **MVP** | Faible | Moyen (trop de champs) | Construire (form progressif) |
| Readiness score | Utile | MVP | **MVP — interne** | Moyenne | **Élevé** (fausse précision) | Construire, inputs vérifiés (§8) |
| Générateur de teaser | Utile | MVP | **MVP — manuel (gabarit)** | Faible | Faible | Manuel → semi-auto V1 |
| Module de recommandations | Secondaire | MVP | **V1** | Élevée | Élevé | Reporter |
| Moteur de matching | Utile | MVP | **V1 (manuel en MVP)** | Élevée | **Élevé** | Manuel ; pas de moteur (§9) |
| CRM cabinet | Indisp. | MVP | **MVP** | Faible | Faible | Acheter (HubSpot/Airtable) |
| Reporting & dashboards | Utile | MVP | **MVP léger → V1** | Moyenne | Moyen | Acheter BI (Metabase) après données |
| Rôles/permissions/audit trail | Indisp. | MVP/V1 | **MVP** | Moyenne | Faible | Construire minimal (RBAC + logs) |
| Data room progressive | Indisp. (en deal) | V1 | **V1 — acheté** | Élevée si construit | Élevé | Acheter (iDeals/Ansarada/Datasite) |
| NDA workflow | Indisp. | V1 | **V1 — acheté** | Moyenne | Moyen | Acheter (e-sign) + non-circonvention |
| KYC/KYB/AML | Indisp. (avant deal) | V1 | **V1 — acheté/API** | Élevée | Moyen | Smile ID/Youverify/Dojah ; World-Check/Grid pour PEP |
| Messagerie & Q&A | Utile | V1 | **V1 (email en MVP)** | Moyenne | Moyen | Manuel/email d'abord |
| Gestion des mandats | Indisp. | V1 | **MVP léger** | Faible | Faible | Construire (statuts + docs) |
| Gestion des fees | Indisp. | V1 | **V1 (facturation manuelle MVP)** | Moyenne | Moyen | Manuel → outillé |
| Workflow deal execution | Secondaire | V1 | **V2** | Élevée | **Élevé** | Reporter ; pipeline simple |
| DD OHADA/SYSCOHADA | Utile (différenciant) | V2 | **V2** | Élevée | Moyen | Construire (l'atout local) |
| ESG/impact (screening) | Utile (si DFI) | V1/V2 | **V1 si cible DFI** | Moyenne | Moyen | Construire checklist + pré-screen |

**Verdict :** le cadrage met en MVP au moins **4 briques prématurées** (matching, teaser auto, recommandations, et implicitement la VDR via le Lot 3). Les sortir du MVP est la correction n°1 : le MVP doit se limiter au **funnel entrepreneur + données + scoring + CRM**, tout le reste manuel ou acheté.

---

# 7. Challenge du MVP

**Le MVP « 4 lots » est trop large.** Les Lots 2 (base investisseurs + matching), 3 (teaser + NDA + data room) et 4 (pipeline transactionnel) supposent déjà les deux faces actives, une VDR, de la signature électronique et un pipeline — c'est une V1 complète déguisée en MVP. Le cadrage le reconnaît implicitement puisque sa reco finale parle de **3 couches *successives*** : il faut suivre cette logique, pas le tableau 4-lots.

**Doivent absolument rester dans le MVP :** onboarding entrepreneur, questionnaire progressif, upload + checklist documentaire, readiness (catégories actionnables), mini-rapport, proposition de services, CRM/reporting cabinet. C'est la **couche 1** : la machine de qualification + conversion. Tout le reste se fait à la main.

**Doivent sortir du MVP :** moteur de matching, teaser automatisé, NDA workflow, data room propriétaire, pipeline transactionnel outillé, recommandations automatiques, DD.

- **MVP le plus simple pour tester la *demande* :** une landing + un diagnostic readiness (même sur Typeform/Tally + grille interne) qui rend un mini-rapport. Mesure : combien d'entrepreneurs le complètent, et la qualité du flux.
- **MVP pour *vendre vite* :** ajouter au-dessus un catalogue de packs (BP, modèle financier, valorisation, data room) et un rendez-vous de closing commercial. Mesure : taux de conversion diagnostic → pack payant.
- **MVP pour *convaincre les investisseurs* :** présenter à la main 1-3 deals curés à 10-20 design-partners. Mesure : taux d'intérêt, entrée en DD. **Pas de plateforme requise.**

### MVP resserré — 90 jours

| Dimension | Contenu |
|---|---|
| **Objectif** | Prouver, sans construire de plateforme biface, que (a) des entrepreneurs *cibles* viennent et complètent, (b) un sous-ensemble **paie un pack de préparation**, (c) un noyau d'investisseurs s'engage sur ≥ 1 deal curé. |
| **Fonctions incluses** | Onboarding + questionnaire progressif ; upload + checklist ; readiness (4 catégories, inputs vérifiés) ; mini-rapport auto ; catalogue de services + prise de RDV ; CRM + reporting cabinet. |
| **Fonctions exclues** | Moteur de matching, teaser auto, NDA workflow, VDR propriétaire, pipeline outillé, DD, paiement en ligne, app mobile native, market intelligence. |
| **Process manuel accepté** | Matching (tableur + jugement) ; teaser (gabarit Word/PDF) ; NDA (DocuSign) ; data room (Drive durci/iDeals essai) ; facturation (devis classique) ; Q&A (email) ; curation des deals (revue consultant). |
| **Livrables** | 1 funnel entrepreneur en ligne ; 1 grille readiness documentée ; 30-50 dossiers qualifiés ; 1 catalogue de packs prix ; 3-5 dossiers « investor-ready » ; 1 dataroom-pilote ; 1 cohorte de 10-20 investisseurs design-partners. |
| **KPI de validation** | ≥ X inscriptions cibles/mois ; ≥ 40 % complétion ; ≥ 15 % diagnostic → pack payant ; ≥ 3 packs vendus ; ≥ 30 % teaser → intérêt investisseur ; ≥ 1 entrée en DD/term sheet. |
| **Go / No-go** | **Go** si conversion payante prouvée *et* ≥ 1 deal en DD. **Pivot** si flux abondant mais zéro conversion (problème de willingness-to-pay) ou conversion mais flux tari (problème d'acquisition). **No-go/refonte** si ni l'un ni l'autre. |

---

# 8. Challenge du scoring entrepreneur

**Crédible ?** Le concept est bon, la formule additive du cadrage est lisible — mais **la fiabilité dépend entièrement des inputs**. Dans un environnement à comptabilité informelle, un score nourri de données *auto-déclarées non auditées* mesure surtout la capacité de l'entrepreneur à bien se présenter, pas sa bancabilité.

**Dimensions à inclure / à manier avec prudence :**

| Dimension | Pondération indicative | Données nécessaires | Fiabilité | Risque de biais |
|---|---|---|---|---|
| Traction commerciale (CA, croissance, clients) | 20 % | États financiers, factures, contrats | Moyenne (si pièces) | Survente ; saisonnalité |
| Profitabilité / cash-flow | 20 % | Comptes SYSCOHADA, relevés | Moyenne-haute (si vérifié) | Comptes informels / double comptabilité |
| Qualité de l'information financière | 15 % | États certifiés, régularité, expert-comptable | **Haute (vérifiable)** | Faible — bon proxy objectif |
| Clarté & cohérence du besoin | 10 % | Montant, usage des fonds, horizon | Moyenne | Déclaratif |
| Gouvernance / actionnariat | 10 % | RCCM, statuts, cap table, bénéf. effectifs | Haute (vérifiable) | Opacité volontaire |
| Qualité documentaire (complétude) | 10 % | Checklist de pièces | **Haute (objective)** | Faible |
| Scalabilité / marché | 5 % | Narratif, marché, modèle | **Basse (subjectif)** | Biais d'optimisme |
| ESG / impact | 5 % | Checklist impact, emplois, genre | Basse-moyenne | Impact-washing |
| **Facteurs de risque (malus)** | −15 % | Litiges, dettes fiscales, secteur sensible, concentration | Moyenne | Dissimulation |

**Trop subjectif (à plafonner ou sortir du score chiffré) :** scalabilité, ESG, « qualité de l'équipe ». À traiter en **commentaire qualitatif**, pas en points, pour éviter la fausse précision.

**Éviter un score trompeur :** (1) **gating documentaire** — pas de score « élevé » sans pièces vérifiées ; (2) pondérer haut les dimensions *objectives et vérifiables* (qualité de l'info, complétude, gouvernance) ; (3) afficher un **intervalle de confiance** (« score provisoire, sous réserve de vérification ») ; (4) recalcul après revue consultant ; (5) labelliser chaque donnée « déclaré / non audité » tant qu'elle n'est pas vérifiée.

**Qui voit quoi ?**

| Acteur | Visibilité recommandée |
|---|---|
| Entrepreneur | **Catégorie** (4 niveaux) + gaps actionnables. *Pas* le score brut détaillé (gaming). |
| Cabinet | Score complet + sous-scores + confiance + historique. |
| Investisseur | **Jamais** le score auto-attribué comme signal de qualité. Il fait confiance à la *curation* du cabinet, pas à un chiffre que le vendeur contrôle. Au mieux : un label de curation (« revu et validé par le cabinet »). |

**Granularité :** 4 catégories en façade ; sous-scores 0-100 en interne. Pas plus — un score à la décimale est un faux signal.

**Transformer le score en offres :** chaque gap → un service. *Investor-ready* → mandat de levée/sourcing. *À préparer* → pack BP + modèle + data room. *Plutôt dette* → orientation banque + dossier de crédit. *Trop précoce* → programme d'incubation/contenu (nurturing gratuit, pas de mandat).

---

# 9. Challenge du moteur de matching

**Au départ : manuel.** Le cadrage le sait à moitié (filtres durs + score souple) mais le met en « MVP construire ». À 73 deals/an pour toute l'Afrique de l'Ouest, **un *moteur* est une sur-ingénierie** : le matching MVP est un tableur filtrable + le jugement du consultant. Le « moteur » vient en V1/V2 quand le volume et les feedbacks le justifient.

| Type de critère | Critères | Rôle |
|---|---|---|
| **Filtres durs (bloquants)** | Pays, secteur, **instrument** (equity/dette/quasi/subvention), fourchette de ticket, stade, listes d'exclusion de l'investisseur | Éliminent d'emblée les incompatibilités absolues |
| **Critères pondérés (score de fit)** | Qualité financière, complétude documentaire, profil de cash-flow vs instrument, ESG/impact, gouvernance, **appétence historique** de l'investisseur (deals passés) | Classent les compatibles |
| **Difficiles à fiabiliser** | Thèse « molle » de l'investisseur, alignement valeurs, timing de levée, chimie fondateur-investisseur | À garder hors algo — jugement humain |

**Intégrer le jugement du cabinet :** validation humaine **obligatoire** avant toute mise en relation (le score propose, le consultant dispose). **Éviter les faux positifs :** seuil de fit minimal + revue consultant + ne jamais présenter un dossier non « investor-ready ». **Exploiter les feedbacks :** formulaire structuré de refus (motif, *next step*) → ré-pondération des critères et apprentissage de l'appétence réelle.

**MVP du matching :**
1. **Filtres durs** sur tableur/Airtable (pays, secteur, ticket, instrument, exclusions).
2. **Score de fit simple** (somme pondérée de 4-5 critères vérifiables).
3. **Validation humaine** systématique.
4. **Feedback loop** par email/formulaire.
5. **Données minimales :** côté entreprise (secteur, géo, besoin, instrument, qualité doc, readiness) ; côté investisseur (critères, exclusions, historique). Rien de plus.

---

# 10. Challenge du modèle économique

| Source | Attractivité | Faisabilité commerciale | Maturité | Risque | Priorité reco |
|---|---|---|---|---|---|
| Freemium (diagnostic) | Élevée (acquisition) | Élevée | Jour 1 | Volume non qualifié | **MVP** |
| Diagnostic expert payant | Moyenne | Moyenne (faible WTP) | MVP | Prix mal calibré ; confusion avec packs | **V1** (pas le wedge) |
| **Pack Investor Readiness** | Élevée | Moyenne-élevée | MVP | Confusion avec promesse de financement | **MVP — wedge n°1** |
| **Pack préparation levée** (BP, modèle, teaser, data room) | Élevée | Élevée | MVP/V1 | Charge de production cabinet | **MVP — wedge n°1** |
| Retainer de mandat | Élevée (récurrent) | Moyenne | V1 | Résistance à payer sans résultat | **V1** |
| Success fee | Très élevée (upside) | Faible court terme | V1 | Revenus irréguliers ; risque réglementaire | **V1 (jamais seul)** |
| Abonnement investisseur | Élevée | Faible avant preuve | V1 | Exige un pipeline crédible | **V1 après preuve** |
| Sourcing dédié (fonds/DFI) | Élevée | Moyenne | V1 | Coût humain fort | **V1** |
| Due diligence premium | Moyenne | Moyenne | V1/V2 | Responsabilité accrue | **V2** |
| Data room fee | Faible | Moyenne | V1 | Mieux acheté que monétisé | **V1 (refacturation)** |
| **Programme sponsorisé DFI/banque** | **Très élevée** | **Moyenne-élevée** | **MVP/V1** | Cycle de vente long | **À REMONTER en MVP/V1 — ancre** |
| Rapports anonymisés / market intel | Moyenne | Faible au début | V2 | Gouvernance des données | **V2** |

**Qui doit payer en premier ?** Le cadrage répond « entrepreneur » — **c'est le payeur le plus dur** (cash-pauvre par définition). Le payeur le plus naturel et le plus solvable au démarrage est l'**institution** (DFI, banque, agence) qui finance déjà la préparation des PME via des programmes d'assistance technique. **Recommandation : ancrer dès le MVP/V1 un programme sponsorisé** (une DFI/banque paie la readiness d'une cohorte), l'entrepreneur ne versant qu'un **ticket d'engagement symbolique**, le success fee venant en sortie.

- **Modèle le plus réaliste au démarrage :** programme sponsorisé + packs de préparation.
- **Le plus rentable à moyen terme :** retainers + success fees sur mandats, + abonnement investisseur une fois le flux prouvé.
- **Le plus risqué :** dépendre du success fee seul (variance, cycle long, exposition réglementaire).
- **Éviter la dépendance au success fee :** le traiter comme *upside* sur une base de revenus récurrents (packs, retainers, sponsoring), pas comme la rente centrale.

**Architecture tarifaire recommandée (packages simples) :**

| Offre | Cible | Prix (logique) | Contenu |
|---|---|---|---|
| **Gratuit** | Entrepreneur | 0 | Diagnostic readiness + mini-rapport + orientation instrument |
| **Diagnostic+** | Entrepreneur | Ticket d'engagement bas | Rapport approfondi + plan d'action + RDV |
| **Préparation** (3 paliers) | Entrepreneur | Forfait par livrable | BP / modèle financier / valorisation / teaser / data room |
| **Mandat** | Entrepreneur ou fonds | Retainer + success fee | Levée/sourcing, mise en relation, suivi closing |
| **Investisseur** | PE/VC/banque/FO | Abonnement annuel (après preuve) | Dealflow filtré + teasers + Q&A ; sourcing dédié en option |
| **Institutionnel / Programme** | DFI/banque/agence | Contrat de programme | Cohorte PME préparées + pipeline qualifié + reporting/impact |

---

# 11. Challenge réglementaire et conformité

Le cadrage est **bon** sur l'axe offre publique vs placement privé. Voici la cartographie consolidée. *(Avis indicatif AMOA — à valider par des avocats UEMOA/CEMAC/OHADA, comme le demande à juste titre le cadrage.)*

| Zone | Sujets | Lecture |
|---|---|---|
| **🔴 Rouge** | Appel public à l'épargne / offre publique sans note d'information visée ; sollicitation *du public* ; promesse de rendement ou de financement « garanti » ; gestion de fonds pour compte de tiers. | Interdits / requalification quasi certaine. À proscrire absolument. |
| **🟠 Grise (à sécuriser)** | **Intermédiation/démarchage financier rémunéré** (même en placement privé) ; **conseil en investissement** ; rémunération au succès sur opération de titres ; ciblage actif d'investisseurs ; transfrontalier (investisseur étranger/DFI sollicitant des entités locales) ; usage de données KYC. | Possiblement soumis à **agrément/statut** indépendamment du caractère privé. **C'est l'angle mort du cadrage.** À cadrer par avis juridique ciblé. |
| **🟢 Acceptable** | Conseil et préparation de dossiers (readiness, BP, modèle, valorisation, data room) ; mise en relation **privée** entre une société et des **investisseurs qualifiés** sous NDA ; success fee sur **prestation de conseil** (vs sur placement de titres) bien rédigé ; market intelligence anonymisée. | Cœur d'activité défendable, sous réserve de rédaction. |

**Formulations commerciales à éviter :** « plateforme de financement », « marketplace d'investissement », « financement garanti », « accès aux investisseurs » (sous-entendu vente d'accès), « rendement », « collecte ». **Préférer :** « préparation au financement », « readiness », « dealflow qualifié pour investisseurs qualifiés », « mise en relation privée », « conseil ».

**Disclaimers nécessaires :** non-garantie de financement ; la plateforme ne fournit pas de conseil en investissement aux investisseurs ; investisseurs réputés qualifiés procédant à leur propre évaluation (cohérent avec la logique COSUMAF du placement privé) ; pas d'offre au public ; responsabilité de l'exactitude des données à la charge de l'entreprise émettrice.

**Validations juridiques à obtenir (avant V1) :** (1) qualification de l'activité d'intermédiation/démarchage en UEMOA (CREPMF-AMF-UMOA) et CEMAC (COSUMAF) ; (2) licéité de la structure de success fee ; (3) régime des données personnelles (Convention de Malabo + lois nationales : CDP Sénégal, ARTCI Côte d'Ivoire, etc.) ; (4) conditions du placement privé / définition d'investisseur qualifié par pays ; (5) transfrontalier.

**Gouvernance à mettre en place :** registre des conflits d'intérêts ; muraille sur les fees (qui paie quoi par deal) ; journal des rôles/mandats ; politique de consentement entrepreneur ; comité de conformité (même léger) validant chaque mise en relation.

---

# 12. Challenge confidentialité, confiance et sécurité

Le risque n°1 du modèle est la **confiance** : fuite de données entrepreneur, partage non autorisé, **contournement du cabinet** (entrepreneur et investisseur se court-circuitent après mise en relation), investisseurs non sérieux qui aspirent le flux, documents financiers trop sensibles exposés trop tôt.

**Matrice de permissions (cible) :**

| Rôle | Avant intérêt | Après intérêt + NDA | En data room | Deal execution |
|---|---|---|---|---|
| Investisseur | Teaser **anonymisé** uniquement | Identité + dossier résumé | Documents selon droits + watermark + logs | Term sheet, Q&A |
| Entrepreneur | Son dossier + statut | Voit l'intérêt (anonymisé ou non selon consentement) | Gère les accès accordés | Pipeline, tâches |
| Consultant cabinet | Tout (sur ses dossiers) | Tout | Tout + administration | Tout |
| Admin | Config, rôles, logs | — | Politiques d'accès | Audit |

**Logique d'anonymisation :** par défaut, teaser sans nom ni éléments ré-identifiants (localisation précise, clients nommés, chiffres trop signants). Levée d'anonymat **uniquement** après consentement entrepreneur + intérêt formalisé + NDA + clause de **non-circonvention** (anti-contournement).

**Règles d'accès data room :** droits par document et par investisseur ; watermark dynamique (identité + horodatage) ; logs d'ouverture/téléchargement ; expiration des accès ; interdiction d'export selon sensibilité ; Q&A liée aux documents (pas d'email parallèle).

**Consentement entrepreneur :** granulaire (quelles données, à qui, pour quoi, durée) ; révocable ; tracé. Propriété des données = entreprise ; licence d'usage au cabinet explicitée.

**Logs à conserver :** authentification, accès documents, signatures NDA, mises en relation, modifications de droits, exports. Horodatés et inaltérables.

**Sécurité par palier :**

| Palier | Mesures |
|---|---|
| **MVP** | RBAC simple, chiffrement au repos/en transit, MFA, logs d'accès, hébergement maîtrisé, NDA + non-circonvention signés, sauvegardes. |
| **V1** | VDR achetée (permissions granulaires, watermark, audit), e-signature, KYC/AML API, politique de rétention, revue d'accès périodique. |
| **V2** | Cloisonnement par deal, DLP, tests d'intrusion réguliers, certification (ISO 27001 si cible DFI), SOC interne léger, anonymisation avancée pour market intelligence. |

---

# 13. Challenge Build vs Buy

Le cadrage a la bonne intuition (construire l'avantage, acheter la commodité). Précision et timing :

| Brique | Reco | Justification | Coût/Complexité | Risque | Timing |
|---|---|---|---|---|---|
| CRM | **Buy** (HubSpot/Airtable) | Commodité ; pas d'avantage à construire | Faible | Lock-in léger | MVP |
| Onboarding entrepreneur | **Build** | Cœur du funnel + données propriétaires | Faible | Sur-collecte | MVP |
| Scoring readiness | **Build** | Avantage propriétaire | Moyen | Fiabilité inputs | MVP (interne) |
| Matching | **Manual → Build** | Volume faible ; jugement humain d'abord | Moyen | Sur-ingénierie | Manuel MVP → Build V1 |
| Data room | **Buy** (iDeals/Ansarada/Datasite) | Sécurité/audit industrialisés | Élevé si construit | Sécurité | V1 |
| Signature électronique | **Buy** (DocuSign/équiv.) | Standard, valeur juridique | Faible | — | V1 |
| KYC/KYB/AML | **Buy/API** (Smile ID, Youverify, Dojah ; World-Check/Grid pour PEP) | Spécialistes Afrique + bases sanctions | Moyen | Couverture locale | V1 |
| Emailing | **Buy** (Brevo/Mailchimp) | Commodité | Faible | — | MVP |
| Messagerie | **Manual (email) → Integrate** | Inutile de construire tôt | Faible | Hors-plateforme | MVP→V1 |
| Q&A | **Build léger** (lié docs) | Traçabilité = valeur | Moyen | — | V1 |
| Paiement | **Buy** (PSP local + mobile money) | Commodité ; manuel possible en MVP | Moyen | Couverture régionale | MVP manuel → V1 |
| BI / dashboards | **Buy** (Metabase) | Rapide sur la donnée existante | Faible | — | MVP léger→V1 |
| Stockage documentaire | **Buy** (cloud durci) → VDR | Commodité | Faible | Sécurité | MVP→V1 |
| Workflow deal execution | **Build (tard)** | Spécifique mais prématuré | Élevé | Sur-spéc. | V2 |
| DD OHADA/SYSCOHADA | **Build** | Différenciateur local fort | Élevé | Complexité | V2 |
| Générateur de teaser | **Manual → Build** | Gabarit d'abord | Faible | — | Manuel MVP→V1 |
| Reporting investisseur | **Build léger** | Lié à la donnée propriétaire | Moyen | — | V1 |
| Market intelligence | **Build (tard)** | Monétise la donnée agrégée | Élevé | Gouvernance données | V2 |

**Règle d'or :** en MVP, **acheter ou faire à la main tout ce qui n'est pas le funnel entrepreneur + la donnée + le scoring**. C'est là, et seulement là, que se construit l'avantage propriétaire.

---

# 14. Benchmark et bonnes pratiques

Le cadrage cite déjà DealCloud, Affinity, Dynamo, Datasite, World-Check. Lecture critique par famille :

| Famille | Acteurs | S'inspirer de | Ne **pas** copier | Trop complexe pour le MVP | Adapter au contexte / différenciant local |
|---|---|---|---|---|---|
| Relationship intelligence / deal CRM | DealCloud, Affinity, 4Degrees, Dynamo | Graphe de relations, pipeline, *deal workflow* continu, capture automatique | Lourdeur entreprise, hypothèses de données US/EU, prix | Auto-capture e-mail à grande échelle, RM avancé | CRM léger mono-cabinet ; la *relation* se construit à la main ici (réseau personnel) |
| VDR / data room | Datasite, Intralinks, Ansarada, iDeals | Permissions granulaires, audit trail, watermark, Q&A liée aux docs | Construire sa propre VDR | Sécurité de niveau M&A dès le départ | **Acheter** ; choisir une option *low-bandwidth/mobile* |
| Fund admin / portfolio | eFront, Allvue | (rien au MVP) | Comptabilité de fonds, reporting LP | Tout | Hors périmètre avant longtemps |
| Data & sourcing intelligence | PitchBook, Preqin, Grata, Sourcescrub, AlphaSense | Recherche par critères, signaux, *AI search* sur documents (AlphaSense) | Prétendre à une couverture exhaustive | Indices de marché, scraping massif | **LE différenciateur :** ces acteurs **ne couvrent quasiment pas les PME d'Afrique francophone** → votre base propriétaire qualifiée est l'actif que personne n'a |

**Trois enseignements structurants :**
1. **La chaîne deal CRM → matching → VDR → closing est un standard** : pensez-les séparés mais connectés (le cadrage l'a compris). Mais ne la construisez pas d'un bloc — achetez la VDR, faites le reste à la main d'abord.
2. **Le moat n'est pas le logiciel** (tous reproductibles) mais **la donnée propriétaire + la curation** sur un marché que les data players ignorent. Investissez là.
3. **L'IA de structuration documentaire** (façon AlphaSense) est pertinente — mais comme **accélérateur de préparation de dossier** (extraction, mapping SYSCOHADA, retraitements), pas comme produit central.

---

# 15. Challenge des parcours utilisateurs

**Parcours entrepreneur — le cadrage prévoit 11 étapes.** C'est **trop long en une session** pour un usage mobile dans la zone. Bon principe (collecte progressive) mais à durcir : la première session ne doit demander que le minimum pour rendre un *premier verdict utile*.

- **Acceptable / à raccourcir :** les 5 premières étapes (inscription → readiness → mini-rapport) doivent tenir en **moins de 10 minutes**. Le reste (upload exhaustif, préparation) vient *après* l'effet wow.
- **Risque d'abandon :** à l'upload documentaire (friction + peur fiscale) et au passage payant. Mitigation : demander les documents **plus tard**, après avoir montré la valeur ; rassurer sur la confidentialité fiscale.
- **Demander au départ :** secteur, pays, CA approximatif (fourchette), besoin de financement (montant + usage), stade. **Rien de plus.**
- **Demander plus tard :** états financiers, RCCM, statuts, cap table, bénéficiaires effectifs.
- **Effet « wow » :** un mini-rapport personnalisé — *« Vous êtes en catégorie ‘À préparer'. Vos 3 blocages : … L'instrument adapté à votre profil : … Voici ce qui vous sépare d'un dossier bancable. »*

**Parcours investisseur — le cadrage prévoit 11 étapes graduées.** L'architecture (accès par niveaux) est juste. Risque : **trop d'étapes avant de voir un deal** décourage un PE sollicité de toutes parts.

- **Minimum pour susciter l'intérêt :** accès quasi-immédiat à 3-5 **teasers anonymisés** de qualité, filtrables (instrument, ticket, secteur, géo). La qualification investisseur peut être **manuelle et rapide** (validation cabinet), pas un formulaire long.
- **Friction acceptable avant NDA :** très faible. Teaser visible sans friction ; NDA **uniquement** au moment d'accéder à l'identité/aux documents.
- **Pour qu'un PE revienne :** régularité d'un flux *rare mais bon* + réactivité humaine du cabinet + feedback pris en compte. La récurrence se gagne par la qualité, pas par les fonctionnalités.

**Parcours MVP simplifiés :**
- **Entrepreneur :** Landing → inscription OTP → 6-8 questions → mini-rapport readiness (catégorie + gaps + instrument) → proposition de pack + RDV. *(Upload et préparation en aval.)*
- **Investisseur :** Invitation → qualification express (validée à la main) → catalogue de 3-5 teasers anonymisés filtrables → bouton « intérêt » → NDA (DocuSign) → data room (achetée) → Q&A par email. *(Pas de moteur, pas de dashboard.)*

---

# 16. Challenge opérationnel cabinet

**C'est le risque le plus sous-estimé du cadrage.** Chaque « revue cabinet » est une heure de consultant senior. Sans modèle opérationnel, la plateforme **génère plus de travail manuel qu'elle n'en économise** : chaque dossier déclenche revue readiness, préparation, curation, matching, suivi.

- **Rôles nécessaires :** un *analyste* (qualification, enrichissement), un *consultant senior* (revue, préparation, relation investisseur), un *responsable conformité* (KYC, conflits, NDA), un *responsable plateforme/ops* (admin, données, reporting). En phase pilote, 2-3 personnes peuvent cumuler.
- **Temps consultant par dossier (estimation) :** qualification 1-2 h ; préparation d'un dossier *investor-ready* 20-40 h ; curation/matching 2-4 h ; suivi deal dizaines d'heures. → **un senior ne peut porter que ~5-10 dossiers actifs.** C'est le plafond de débit réel.
- **À standardiser :** grille readiness, modèles (BP, teaser, NDA), checklist DD, process d'onboarding, scripts de qualification.
- **Automatisable :** qualification initiale, enrichissement assisté par IA, relances, génération de mini-rapport, reporting.
- **À garder humain :** revue de readiness finale, curation, mise en relation, négociation, jugement de fit.
- **Risque de surcharge :** afflux d'inbound non qualifié (le freemium trop généreux). Mitigation : **gating** (seuils d'éligibilité) + auto-tri + nurturing automatisé des « trop précoces ».

**Modèle opérationnel cible :**

| Élément | Définition |
|---|---|
| Rôles | Analyste / Consultant senior / Conformité / Ops-plateforme |
| Responsabilités | Analyste : qualif + enrichissement. Senior : préparation + relation investisseur. Conformité : KYC/NDA/conflits. Ops : données + reporting. |
| SLA | Mini-rapport readiness < 48 h ; devis pack < 72 h ; réponse investisseur < 24 h ; mise en data room < 5 j après NDA. |
| Process clés | Qualification → préparation → curation → matching → mise en relation → exécution. |
| Contrôle qualité | Double validation avant présentation investisseur ; checklist « investor-ready » ; revue conformité avant toute mise en relation. |
| Indicateurs de productivité | Dossiers/consultant, h/dossier, taux qualif→pack, taux teaser→intérêt, délai onboarding→term sheet. |

---

# 17. Challenge data model

Objets principaux et points de vigilance :

| Objet | Champs clés | Relations | Sensibilité | Propriétaire | Risques qualité/sécurité |
|---|---|---|---|---|---|
| Entreprise | Raison sociale, pays, secteur, CA, stade, RCCM | Contacts, Deal, Documents, Score | Élevée | Entreprise | Données auto-déclarées ; doublons |
| Contact / Entrepreneur | Nom, rôle, email, tél, KYC | Entreprise | Élevée (perso) | Personne | RGPD/Malabo ; consentement |
| Investisseur | Type, juridiction, équipe | Fonds, Critères, Interactions | Moyenne | Investisseur/Cabinet | Qualification non vérifiée |
| Fonds | Thèse, AUM, instruments | Investisseur, Critères | Moyenne | Investisseur | Données obsolètes |
| Critères d'investissement | Pays, secteur, ticket, instrument, exclusions | Fonds, Matching | Moyenne | Investisseur | Critères « mous » non exploitables |
| Besoin de financement | Montant, usage, horizon, instrument | Entreprise, Deal | Moyenne | Entreprise | Incohérence besoin/profil |
| Deal | Statut, instrument, montant, parties | Entreprise, Investisseur, Documents, Mandat | **Critique** | Cabinet | Fuite ; contournement |
| Document | Type, version, hash, droits | Entreprise, Deal, Data room | **Critique** | Entreprise | Accès non autorisé ; intégrité |
| Score / Readiness | Sous-scores, catégorie, confiance | Entreprise | Élevée | Cabinet | Inputs non audités ; biais |
| Recommandation | Instrument, services suggérés | Entreprise, Score | Faible | Cabinet | Sur-promesse |
| Teaser | Contenu anonymisé, version | Deal, Entreprise | Moyenne | Cabinet | Ré-identification |
| NDA | Parties, modèle, date, signature | Deal, Investisseur | Élevée | Cabinet | Valeur juridique ; versioning |
| Data room | Arborescence, droits, logs | Deal, Documents | **Critique** | Cabinet | Permissions ; audit |
| Q&A | Question, réponse, statut, auteur | Deal, Document | Moyenne | Cabinet | Hors-plateforme |
| Interaction | Type, date, canal, notes | Tous | Moyenne | Cabinet | Traçabilité incomplète |
| Mandat | Type, exclusivité, durée, périmètre | Entreprise/Fonds, Fees | Élevée | Cabinet | Ambiguïté → litige |
| Fee | Type (retainer/success), montant, échéance | Mandat, Deal | Élevée | Cabinet | Conflit d'intérêts ; recouvrement |
| Feedback | Motif, next step, score révisé | Deal, Investisseur | Faible | Cabinet | Sous-utilisé |
| Statut transactionnel | Étape, jalons, dates | Deal | Moyenne | Cabinet | Pipeline non tenu |

**Principes transverses :** propriété claire (l'entreprise possède ses données ; le cabinet possède scores/curation/agrégats anonymisés) ; consentement granulaire tracé ; horodatage + hash pour l'intégrité documentaire ; séparation stricte des données par deal (cloisonnement) ; agrégats anonymisés pour la market intelligence (jamais de ré-identification).

---

# 18. Challenge roadmap

Roadmap réaliste sur 24 mois — alignée sur « prouver avant de construire ».

| Phase | Durée | Objectifs | Fonctions / livrables | Process manuels acceptés | Ressources | KPI | Critère de passage | Risques |
|---|---|---|---|---|---|---|---|---|
| **0 — Cadrage & validation marché** | 0-1 mois | Geler le périmètre MVP (couche 1) ; quantifier le TAM ; sécuriser le juridique ; choisir 2 pays | Note de périmètre ; étude TAM ; avis juridique ciblé ; cohorte design-partners | Tout | Fondateur + avocat + analyste | TAM chiffré ; 10-20 investisseurs engagés | Décisions structurantes prises (§20) | Lancer les 4 lots au lieu de la couche 1 |
| **1 — MVP 90 j (couche 1)** | 1-4 mois | Funnel entrepreneur + conversion ; ancrer 1 sponsor DFI/banque | Onboarding, readiness, mini-rapport, catalogue packs, CRM/reporting | Matching, teaser, NDA, data room, facturation | Petite équipe (2-3) | Complétion ≥ 40 % ; ≥ 3 packs vendus ; ≥ 1 deal en DD | Conversion payante prouvée | Construire au lieu de vendre |
| **2 — Pilote 6 mois (couche 2)** | 4-10 mois | Dealflow curé + engagement investisseur ; 1er closing | Base investisseurs, matching **manuel→outillé léger**, teasers, feedback, VDR **achetée**, NDA | DD, market intel | + consultant senior + conformité | Taux teaser→intérêt ≥ 30 % ; 1 closing ; 1 programme sponsorisé signé | Économie du deal prouvée | Sélection adverse ; flux tari |
| **3 — V1 (12 mois)** | 10-16 mois | Industrialiser la chaîne ; abonnement investisseur | Matching outillé, teaser semi-auto, Q&A, KYC/AML, gestion mandats/fees, dashboards | DD avancée | Équipe étoffée | Récurrence revenus ; ≥ N closings ; rétention investisseur | Unit economics positives | Sur-build ; surcharge ops |
| **4 — Scale (18-24 mois)** | 16-24 mois | Multi-pays ; DD OHADA ; market intelligence | DD OHADA/SYSCOHADA, ESG, market intel, programmes DFI multiples | — | Équipe + partenaires | Couverture multi-pays ; marges ; pipeline DFI | Rentabilité par marché | Dispersion géographique |

---

# 19. Questions critiques à résoudre avant lancement

**Stratégie**
1. Joue-t-on une *boutique de conseil tech-enabled* ou une *plateforme scalable* ? (la valorisation et le build en dépendent)
2. Cible-t-on l'equity PE/VC ou l'ensemble dette/mezzanine/garanties/DFI ?
3. Quels 2-3 pays prioritaires (où le cabinet a déjà un réseau biface) ?
4. Assume-t-on le caractère non-scalable (services) auprès des financeurs du projet ?

**Produit**
5. La couche 1 (funnel entrepreneur) est-elle bien le périmètre prioritaire vs les 4 lots ?
6. Construit-on le matching, ou reste-t-il manuel jusqu'à quel volume ?
7. Le score est-il interne-only ou exposé, et sous quelle forme ?
8. Quel est le périmètre *gelé* du MVP 90 jours ?

**Monétisation**
9. Qui paie en premier : entrepreneur, investisseur ou institution ?
10. Le pack de préparation est-il le wedge n°1 ?
11. Peut-on signer un programme sponsorisé DFI/banque dès la phase pilote ?
12. Structure du success fee : sur conseil ou sur placement (implication réglementaire) ?

**Réglementaire**
13. L'intermédiation rémunérée exige-t-elle un agrément en UEMOA/CEMAC ?
14. Définition d'« investisseur qualifié » retenue par pays ?
15. Conformité données personnelles (Malabo + lois nationales) : qui est responsable de traitement ?
16. Quelles formulations commerciales sont juridiquement sûres ?

**Investisseurs**
17. Combien de design-partners au démarrage, avec quel engagement ?
18. Quelle qualité minimale garantit-on (règle de curation) ?
19. Comment source-t-on *activement* les bons dossiers (anti-sélection adverse) ?

**Entrepreneurs**
20. Quel segment précis cible-t-on (« solide mais mal préparé ») ?
21. Comment lève-t-on la peur fiscale du partage de données ?
22. Quel taux de conversion diagnostic→pack rend le modèle viable ?

**Opérations**
23. Combien de dossiers un consultant senior peut-il porter ?
24. Quels SLA tient-on réellement ?
25. Comment éviter la surcharge d'inbound non qualifié ?

**Technologie**
26. Quelles briques achète-t-on (VDR, KYC, e-sign) et lesquelles précisément ?
27. Architecture multi-pays/multi-devise dès le départ ou plus tard ?
28. Quel est le strict minimum à construire en interne au MVP ?

**Données & GTM**
29. Qui possède la donnée et comment la monétise-t-on (market intel) sans risque ?
30. Quel moteur d'acquisition entrepreneur (contenu, prescripteurs, DFI, incubateurs) ?

---

# 20. Décisions structurantes à prendre

| Décision | Options | Recommandée | Justification | Risque si erreur |
|---|---|---|---|---|
| Positionnement | SaaS / Marketplace / **Boutique tech-enabled** | **Boutique tech-enabled** | Réalité économique et réglementaire | Survalorisation, désillusion des financeurs du projet |
| Cible entrepreneur | Tout-venant / **« Solide mais mal préparé »** / startups tech | **« Solide mais mal préparé »** | Là où le cabinet ajoute une valeur facturable | Promesse diluée, flux infinançable |
| Cible financeur | Equity PE/VC / **Multi-instruments (dette/DFI/blended)** | **Multi-instruments** | Le missing middle est surtout dette/DFI | Promesse inadaptée à la demande |
| Pays prioritaires | National / **2 UEMOA + 1 CEMAC** / pan-africain | **2 UEMOA + 1 CEMAC** où le cabinet a un réseau | Densité de réseau > couverture | Dispersion, flux trop mince |
| Niveau de gratuité | Généreux / **Qualifiant** / payant d'emblée | **Qualifiant** (gratuit = prise de conscience) | Évite l'inbound non qualifié | Surcharge ops ou no-show |
| Niveau d'automatisation | Tout auto / **Manuel-d'abord** / tout manuel | **Manuel-d'abord, automatiser ce qui scale** | Prouver avant de construire | Sur-build prématuré |
| Rôle du cabinet dans le matching | Auto / **Semi (validation humaine)** / manuel | **Semi — validation humaine obligatoire** | Qualité + responsabilité | Faux positifs, perte de confiance |
| Modèle de rémunération | Success fee seul / **Hybride ancré sponsoring** / abonnement seul | **Hybride, ancré sur sponsoring + packs** | Lisse le cash, réduit le risque | Dépendance au success fee |
| Qui paie d'abord | Entrepreneur / Investisseur / **Institution** | **Institution (DFI/banque) + ticket entrepreneur** | Solvabilité immédiate | 12-18 mois sans revenus |
| Architecture technique | Monolithe custom / **Buy + build ciblé** | **Buy (VDR/KYC/e-sign) + build (funnel/score/données)** | Concentre l'effort sur le moat | Coûts et délais explosent |
| Confidentialité | Ouverte / **Graduée + anonymisée** | **Graduée + anonymisée + non-circonvention** | Confiance = condition d'existence | Fuite = mort réputationnelle |
| Périmètre MVP | 4 lots / **Couche 1 seule** | **Couche 1 seule (funnel + conversion)** | Focalisation, time-to-proof | 9-15 mois avant 1er euro |

---

# 21. Recommandations finales

**Faut-il lancer le projet ?** **Oui — mais pas le construire tel qu'il est cadré.** Lancer un **pilote services-first, à couche unique, co-financé par une institution**, avec une couche techno mince. La vision est bonne ; c'est le *séquencement* et le *périmètre* qu'il faut corriger.

**Sous quelles conditions ?** (1) Geler le MVP sur la couche 1 ; (2) sécuriser l'avis juridique sur l'intermédiation ; (3) ancrer un sponsor DFI/banque ; (4) cible financeur élargie aux instruments de dette ; (5) stratégie de **sourcing actif** anti-sélection adverse.

**Avec quel MVP ?** La **couche 1 du cadrage** (funnel entrepreneur : qualification → readiness → conversion vers packs), tout le reste manuel. **Pas les 4 lots.**

**Promesse de valeur prioritaire :** rendre les PME *bancables* (livrable maîtrisable et facturable), pas promettre du financement.

**Cible initiale :** entrepreneurs « solides mais mal préparés » dans 2 pays UEMOA + 1 CEMAC où le cabinet a un réseau ; 10-20 investisseurs design-partners (dont financeurs de dette/DFI) ; 1 sponsor institutionnel.

**Modèle économique initial :** programme sponsorisé (ancre) + packs de préparation (wedge) + ticket d'engagement entrepreneur ; retainer/success fee et abonnement investisseur en V1, après preuve.

**Fonctions à repousser :** moteur de matching, teaser auto, VDR propriétaire, NDA workflow, pipeline outillé, DD, market intelligence, recommandations auto.

**Preuves de marché à obtenir :** complétion du funnel ≥ 40 % ; ≥ 15 % diagnostic→pack payant ; ≥ 3 packs vendus ; ≥ 30 % teaser→intérêt investisseur ; ≥ 1 entrée en DD/term sheet ; 1 programme sponsorisé signé.

**Risques à surveiller en priorité :** (1) sélection adverse ; (2) personne ne paie (willingness-to-pay entrepreneur) ; (3) surcharge opérationnelle du cabinet ; (4) requalification réglementaire de l'intermédiation ; (5) flux adressable trop mince (TAM).

### Les 10 actions des 30 prochains jours
1. Geler le périmètre du MVP 90 jours sur la seule couche 1 (note de cadrage signée).
2. Nommer explicitement le segment entrepreneur cible et le message anti-« pay-to-play ».
3. Commander un avis juridique ciblé (intermédiation/démarchage, success fee, investisseur qualifié, données).
4. Chiffrer le TAM réel (PME 0,5-10 M$ CA) sur 2-3 pays.
5. Identifier et engager 10-20 investisseurs design-partners (inclure dette/DFI).
6. Ouvrir 1-2 discussions de programme sponsorisé (DFI/banque/agence).
7. Construire la grille de readiness (dimensions, pondérations, **gating documentaire**).
8. Définir la stratégie de **sourcing actif** des bons dossiers (banques, incubateurs, prescripteurs).
9. Spécifier l'usage de l'IA comme *accélérateur de préparation* (extraction, mapping SYSCOHADA), pas comme produit.
10. Rédiger les modèles : teaser, NDA + non-circonvention, catalogue de packs prix.

### Les 10 livrables pour passer en phase projet
1. Note de périmètre MVP gelé (arbitrage 4-lots → couche 1).
2. Étude TAM + ciblage pays/secteurs.
3. Mémo juridique (zones rouge/grise/verte + formulations + disclaimers).
4. Grille de readiness documentée + politique de visibilité du score.
5. Architecture tarifaire (6 offres) + scripts commerciaux.
6. Liste engagée de design-partners investisseurs + règle de curation.
7. Term sheet de programme sponsorisé (au moins en discussion).
8. Modèle opérationnel (rôles, SLA, plafond dossiers/consultant).
9. Matrice de permissions + politique de confidentialité/consentement.
10. Funnel entrepreneur en ligne (couche 1) + reporting cabinet.

### Proposition de valeur resserrée
> « Nous transformons des PME africaines *potentiellement* finançables en dossiers réellement investissables — puis nous les présentons, préparées et filtrées, aux bons financeurs. On paie la *préparation*, jamais une promesse de financement. »

### MVP recommandé en une phrase
> Un funnel entrepreneur en ligne (qualification → readiness → conversion vers packs de préparation), opéré manuellement pour le reste et co-financé par un sponsor institutionnel — pas une plateforme biface.

### Le plus gros piège à éviter
> **Construire la plateforme biface (les 4 lots) avant d'avoir prouvé manuellement l'économie du deal et l'adoption des deux faces.** Aucune des trois hypothèses critiques — les entrepreneurs viennent, ils paient la préparation, les investisseurs s'engagent sur un dealflow curé — n'est encore validée. Inversez l'ordre : **vendez d'abord à la main, codez ensuite ce qui scale.**

---

*Revue établie sur la seule base du cadrage AMOA fourni. Les éléments réglementaires sont indicatifs et doivent être validés par des avocats spécialisés UEMOA/CEMAC/OHADA. Coller la version la plus récente des specs permettra d'affiner les points marqués comme à confirmer.*


