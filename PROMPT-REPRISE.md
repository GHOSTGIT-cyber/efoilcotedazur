# PROMPT DE REPRISE — Session eFoil Côte d'Azur (site principal)

Colle ce prompt en début de nouvelle session.

---

## Contexte projet

Tu reprends le développement du site statique **eFoil Côte d'Azur** (location/initiation eFoil à Mandelieu-la-Napoule, Côte d'Azur).

- **Dossier** : `d:\efoilcotedazur`
- **Branche git** : `main` (toujours vérifier avec `git branch --show-current` avant toute écriture)
- **Repo GitHub** : `https://github.com/GHOSTGIT-cyber/efoilcotedazur`
- **Preview GitHub Pages** : `https://ghostgit-cyber.github.io/efoilcotedazur/`
- **Preview locale** : `http://127.0.0.1:8080/`
- **Stack** : HTML/CSS/JS pur, zero framework, mobile-first (91% trafic)

---

## Règles git (multi-session)

```
main         → d:\efoilcotedazur    ← TON DOSSIER (site Mandelieu)
beauvallon   → d:\efoil-beauvallon  (autre session, ne pas toucher)
croix-valmer → d:\efoil-croix-valmer (autre session, ne pas toucher)
```

1. Avant toute écriture : `git branch --show-current` → doit afficher `main`
2. `git add <fichiers-explicites>` — jamais `git add -A`
3. Cycle push :
   ```
   git pull --rebase
   git add <fichiers> && git commit -m "..."
   git pull --rebase && git push origin main
   ```

---

## Fichiers clés

| Fichier | Rôle |
|---|---|
| `index.html` | Version orange (hero poster = hero-0611-poster.webp) |
| `index-bleu.html` | Version bleue (même structure, palette bleu/orange inversée) |
| `assets/css/efca.css` | CSS complet — source de vérité |
| `assets/js/efca.js` | Carrousel avis, reveal scroll, CTA tracking |
| `assets/js/efca-reservation.js` | Tunnel réservation (fallback simulation si pas de WP) |
| `assets/js/efca-dashboard.js` | Dashboard admin (fallback sampleData) |
| `assets/js/efca-config.js` | EFCA_CONFIG : apiBase, fallbackMode, unitPrice |
| `wordpress/efca-reservation.php` | Plugin WP : CPT, REST API, PAYMENT_MODE flag |
| `reservation.html` | Tunnel 3 étapes (noindex, DÉMO banner) — ne pas modifier |
| `dashboard.html` | Dashboard front (noindex) — ne pas modifier |
| `assets/img/logo.webp` | Logo fond transparent (25 Ko, 1522×868) |
| `assets/video/hero.mp4` | Vidéo hero (71 Mo, depuis 0611.mp4) |

---

## ⚠️ Point critique — CSS inline dans `<head>`

`index.html` et `index-bleu.html` contiennent un bloc `<style>` inline (~60 lignes) qui redéfinit le hero et les primitives critiques. **Il écrase `efca.css` au premier rendu.**

Si tu modifies le hero dans `efca.css`, tu DOIS aussi modifier le bloc inline correspondant (lignes ~80–90 de chaque fichier). Les règles concernées :
- `.efca-hero` (min-height, align-items, padding-block)
- `.efca-hero::after` (gradient)
- `.efca-hero__inner` (max-width, margin-inline, animation)

---

## Palette de marque (FINALE — ne pas changer)

| Token | Valeur | Usage |
|---|---|---|
| `--efca-color-primary` | `#F4631F` | Orange — CTA, accents forts |
| `--efca-color-accent` | `#00A7C7` | Turquoise — liens, "e" du logo |
| `--efca-color-ink` | `#0F2830` | Pétrole sombre — titres, dark sections |

Logo : "e" turquoise + "FOIL CÔTE D'AZUR" orange.

---

## État du site au moment du départ

### Structure de page (ordre des sections)
1. Hero (vidéo bg, contenu bas-gauche, logo blanc, slide-up)
2. Co-brand Lift France
3. Pourquoi nous + Chiffres clés
4. L'expérience eFoil
5. Comment ça se passe (4 étapes avec photos moniteur Dubai)
6. Offre & Tarifs (3 cartes prix)
7. Encadrement & Confiance
8. Esprit Côte d'Azur
9. **Reel Strip** (6 reels horizontaux — commence par "eFoil en un mot")
10. Gamme Lift
11. Galerie (mur d'images)
12. **Vivez la session** (3 reels verticaux 9:16, fond sombre — NE PAS TOUCHER)
13. Cover CTA "Prêt à voler ?"
14. FAQ
15. **Lieu & Accès** (adresse + fiche Google + carte)
16. Mur d'avis Google (carousel)
17. Réserver
18. Footer

### Assets vidéo
- `assets/video/hero.mp4` — 71 Mo (hero background)
- `assets/video/reel-superyachts.mov` / `reel-session.mov` / `reel-cote.mov` — section Vivez la session
- `assets/video/reel-oneword.mov` / `reel-saintropez.mov` / `reel-community.mov` / `reel-station.mov` / `reel-islote.mov` / `reel-muntanya.mov` — reel strip

### Assets images clés
- `assets/img/logo.webp` — logo fond transparent
- `assets/img/hero-0611-poster.webp` — poster hero
- `assets/img/cdz-01.webp` … `cdz-12.webp` — 12 photos site
- `assets/img/step-briefing/materiel/session/progress.webp` — photos étapes process
- `assets/img/reel-*-poster.webp` — 9 posters vidéos

---

## Ce qui reste à faire (par priorité)

### 🔴 Urgent — placeholders à remplacer
```
{{LIEN_FICHE_GOOGLE}}  → URL fiche Google Business eFoil Côte d'Azur
{{LIEN_ITINERAIRE}}    → URL Google Maps itinéraire vers Plage des Dauphins
{{LIEN_MENTIONS}}      → Page mentions légales
{{LIEN_CGV}}           → Page CGV
```
Les chercher avec grep : `grep -n "{{" index.html`

### 🔴 Avis Google réels
Chercher `<!-- AVIS À INJECTER -->` dans `index.html` — 3 emplacements à remplir avec de vrais verbatims Google.

### 🟡 À valider avec le client
- Horaires : "9 h – 19 h (saison)" — *à confirmer*
- Âge minimum (FAQ)
- Politique annulation (FAQ)
- Décider entre version orange ou bleue (ou les deux)

### 🟡 Technique
- Compresser `hero.mp4` 71 Mo → ~10 Mo (ffmpeg : `ffmpeg -i hero.mp4 -vcodec h264 -crf 28 -vf scale=1280:-2 hero-opt.mp4`)
- Ajouter `.webm` pour Chrome
- Retirer le bandeau "Orange / Bleu" avant mise en prod

### 🟢 Déploiement
- Activer GitHub Pages : repo → Settings → Pages → Branch: main → Save
- SFTP vers OVH pour mise en ligne prod (remplace WP actuel)
- Connecter WP : remplacer `apiBase` dans `efca-config.js` + activer `efca-reservation.php`

---

## NAP (identique partout — ne jamais paraphraser)
```
Plage des Dauphins, Bd du Midi Louise Moreau, 06150 Mandelieu-la-Napoule · 06 35 30 50 67
```
