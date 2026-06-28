# DealIQ — Charte graphique (guide développeur)

> Version 1.1 · 2026 · « Le signal avant le bruit. »
> Plateforme d'intelligence et d'enrichissement du deal flow — zone UEMOA.

Ce document est la source de vérité pour le design des produits DealIQ.
Les noms de tokens sont identiques côté design (Figma) et côté code.

---

## 1. Principes

| Principe | Implication produit |
|----------|---------------------|
| **Précis** | Données en monospace, chiffres alignés (tabulaires), hiérarchie nette. On ne décore pas un score, on le rend lisible. |
| **Vif** | Lecture en un coup d'œil. L'or signale ce qui compte ; le reste reste calme et au second plan. |
| **Ancré** | L'or évoque la valeur et l'héritage aurifère de la région : crédibilité internationale, racine locale. |

---

## 2. Couleurs

### Palette

| Token | Hex | Nom | Usage |
|-------|-----|-----|-------|
| `--encre` | `#0C1C2B` | Encre | Fond principal, barres, terminal |
| `--or` | `#E7A23C` | Or signal | Scores, accents, actions clés |
| `--cedre` | `#2FA08C` | Cèdre | Positif, vérifié, croissance |
| `--papier` | `#F4F0E6` | Papier | Fond clair, surfaces de lecture |
| `--brume` | `#8794A1` | Brume | Texte secondaire, libellés, états neutres |

### Teintes de support

| Token | Hex | Usage |
|-------|-----|-------|
| `--encre-2` | `#122738` | Surfaces sur fond encre (cartes) |
| `--encre-3` | `#193147` | Bordures internes, pistes de jauge |
| `--or-clair` | `#F4C97E` | Or sur fond très sombre, hover |
| `--papier-2` | `#EDE7D7` | Séparateurs, fonds de tags clairs |
| `--ligne-sombre` | `#22394C` | Bordures sur fond encre |
| `--ligne-claire` | `#E2DAC6` | Bordures sur fond papier |
| `--texte-clair` | `#F4F0E6` | Texte sur fond sombre |
| `--texte-sombre` | `#13212C` | Texte sur fond clair |
| `--texte-doux` | `#5B6B78` | Texte secondaire sur fond clair |

### Proportions d'usage

```
Encre 60%  ·  Neutres 28%  ·  Or 8%  ·  Cèdre 4%
```

L'or est **rare et précieux** : ne jamais l'utiliser comme fond de grande surface ni
pour du texte courant. Réservé aux scores, accents et call-to-action.

### Sémantique des couleurs de score

| Plage IQ | Niveau | Couleur | Token |
|----------|--------|---------|-------|
| 80–100 | Fort signal | Or | `--or` `#E7A23C` |
| 55–79 | Prometteur | Cèdre | `--cedre` `#2FA08C` |
| 0–54 | À surveiller | Brume | `--brume` `#8794A1` |

---

## 3. Typographie

Trois rôles, trois familles. Charger via Google Fonts.

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

| Rôle | Famille | Token | Graisses | Emploi |
|------|---------|-------|----------|--------|
| Display | Space Grotesk | `--display` | 500 / 600 / 700 | Titres, mot-symbole, grands chiffres d'impact |
| Texte | Inter | `--texte` | 400 / 500 / 600 | Paragraphes, fiches, listes |
| Données | IBM Plex Mono | `--mono` | 400 / 500 / 600 | Scores, montants, tickers, dates, identifiants |

**Règle d'or** : toute donnée (score, montant, ticker, date, ID) se compose **toujours
en monospace tabulaire** — `IQ 87 · €2.4M · ROUND SEED · ABJ → DKR`.

### Échelle type (web)

| px | Rôle | Famille |
|----|------|---------|
| 12 | Légende / libellé mono | Mono / Inter |
| 16 | Corps | Inter |
| 24 | Sous-titre | Display / Inter |
| 40 | Titre de section | Display 600 |
| 50+ | Titre hero | Display 500–600, `letter-spacing: -.02em` |

---

## 4. Logo

Le monogramme est un **anneau ouvert avec un nœud doré** : il lit à la fois comme un
« Q » (IQ) et comme un cadran de scoring — le geste central de la plateforme.

**À faire**
- Espace de protection ≥ la hauteur du « Q » autour du logo.
- Taille minimale : 24 px (monogramme), 110 px (lockup).
- « IQ » toujours en or ; « Deal » dans la couleur de texte du fond.

**À éviter**
- Étirer, incliner, ajouter une ombre portée.
- Recolorer l'anneau ou poser l'or sur un fond clair vif.
- Coller le logo sur une image chargée sans plaque de fond.

### Variantes
- **Lockup principal** — fond Encre, mot-symbole clair.
- **Version claire** — mot-symbole encre sur Papier.
- **Monogramme seul** — avatar, favicon, app.

---

## 5. Tokens (CSS)

À coller dans le `:root` global, ou exporter en variables de thème (JS/Tailwind/SCSS).

```css
:root {
  /* Couleurs */
  --encre: #0C1C2B;
  --encre-2: #122738;
  --encre-3: #193147;
  --or: #E7A23C;
  --or-clair: #F4C97E;
  --cedre: #2FA08C;
  --papier: #F4F0E6;
  --papier-2: #EDE7D7;
  --brume: #8794A1;
  --ligne-sombre: #22394C;
  --ligne-claire: #E2DAC6;
  --texte-clair: #F4F0E6;
  --texte-sombre: #13212C;
  --texte-doux: #5B6B78;

  /* Score */
  --score-fort: var(--or);
  --score-prometteur: var(--cedre);
  --score-surveiller: var(--brume);

  /* Typographie */
  --display: "Space Grotesk", system-ui, sans-serif;
  --texte: "Inter", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, monospace;

  /* Formes */
  --radius-sm: 8px;
  --radius: 16px;
  --radius-lg: 20px;

  /* Largeur de contenu */
  --mesure: 1120px;
}
```

### Équivalent JS / design tokens

```json
{
  "color": {
    "encre": "#0C1C2B",
    "or": "#E7A23C",
    "cedre": "#2FA08C",
    "papier": "#F4F0E6",
    "brume": "#8794A1"
  },
  "font": {
    "display": "Space Grotesk",
    "text": "Inter",
    "mono": "IBM Plex Mono"
  },
  "radius": { "sm": 8, "md": 16, "lg": 20 },
  "score": { "strong": 80, "promising": 55 }
}
```

---

## 6. Composants

### Score IQ

Objet de marque central. Présent partout : avatar, fiche, liste, export.

```
function scoreColor(iq) {
  if (iq >= 80) return "var(--or)";      // fort signal
  if (iq >= 55) return "var(--cedre)";   // prometteur
  return "var(--brume)";                 // à surveiller
}
```

- Jauge circulaire 0–100, piste `--encre-3`, remplissage `--or`, `stroke-linecap: round`.
- Le nombre se compose en `--mono` 600.
- Animer le remplissage à l'apparition (≈1,6 s, easing `cubic-bezier(.2,.7,.2,1)`).

### Cartes / surfaces
- Fond clair : `#fff`, bordure `--ligne-claire`, `border-radius: var(--radius)`.
- Fond sombre : `--encre-2`, bordure `--ligne-sombre`.
- Ombre portée uniquement sur les surfaces flottantes : `0 24px 60px -34px rgba(12,28,43,.5)`.

### Tags / badges
- Mono 11 px, `padding: 4px 10px`, `border-radius: 7px`.
- Neutre : fond `--papier-2`, texte `--texte-doux`.
- Positif : fond `rgba(47,160,140,.14)`, texte `#1d6f60`.
- Négatif : fond `rgba(206,86,74,.14)`, texte `#b5402f`.

### Barre d'app
- Fond `--encre`, hauteur ~60 px, mot-symbole clair, recherche en mono `--brume`.

---

## 7. Mouvement

- **Apparition au scroll** : `opacity 0→1` + `translateY(16px→0)`, `transition .7s ease`,
  déclenché par `IntersectionObserver` (threshold ~0.12), délais échelonnés 0/90/180 ms.
- **Jauge / barres de score** : remplissage animé à l'entrée.
- **Compteurs** : count-up easeOut sur les scores et grands chiffres.
- **États live** : pastille `--cedre` clignotante (badge « LIVE »).
- **Respecter `prefers-reduced-motion: reduce`** : couper toutes les animations,
  afficher les états finaux directement.

---

## 8. Voix & ton

> Analyste, pas commercial. On informe pour décider plus vite : phrases courtes,
> verbes concrets, chiffres devant.

**On dit**
- « 12 dossiers à qualifier cette semaine. » — précis, actionnable.
- « IQ 87 · forte traction, peu de dilution. » — la donnée d'abord.
- « Aucun signal pour l'instant. Lancez un sourcing. » — l'état vide invite à agir.

**On évite**
- « La meilleure plateforme révolutionnaire ! » — superlatifs creux.
- « Oups, une erreur est survenue. » — vague, sans solution.
- Jargon système exposé à l'analyste (webhook, payload…).

---

*Charte graphique DealIQ v1.1 · proposition · 2026.*
