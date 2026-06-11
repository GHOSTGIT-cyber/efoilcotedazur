# Landing eFoil · COMO Le Beauvallon — Livrable

Page one-page cinématique (golfe de Saint-Tropez). Bloc HTML autonome pour Gutenberg `wp:html`.
Fichier : [`como-beauvallon-efoil.html`](como-beauvallon-efoil.html) — prévisualisable en local
(`python -m http.server` puis ouvrir le fichier ; les polices retombent sur le système tant que
les woff2 ne sont pas déposés).

> ⚠️ **DA v2.1 = continuité COMO beach-club (chaude).** Le visiteur arrive depuis comohotels.com et ne
> doit pas sentir de rupture : fonds **crème / sable**, ambiance **summer / golden hour**, accent
> **terracotta `#cf5836`** (CTA, signature, détails) + **jaune-soleil `#e0a92e`** (parasols). **Zéro bleu
> en aplat** ; sombre limité au **warm espresso `#2b2419`** (réservation + footer). Le turquoise Lift est
> sorti du chrome — il ne reste qu'**un seul glint discret** (clin d'œil foil, sur « Matériel Lift »).
> **COMO est une marque tierce** : mention « au départ du ponton du domaine COMO Le Beauvallon » sans
> logo ni co-marque. Droits d'usage du nom **et des visuels COMO** (beach club, aérien) à clearer avant
> mise en ligne publique — la preview/itération interne, c'est autre chose.

---

## 0) Éditions montées avec les vraies photos/vidéos

À partir du template (placeholders) `como-beauvallon-efoil.html`, **3 éditions** de la **même page Beauvallon** (DA chaude identique), câblées avec les médias du dossier `medias/`. Elles diffèrent par le **héros** et l'ambiance :

| Fichier | Héros | Respirations | Galerie / mood |
|---|---|---|---|
| `como-beauvallon-v1-coucher-de-soleil.html` | Coucher de soleil St-Tropez (silhouettes) | sunset + roches rouges | mix golfe / Lérins / Estérel |
| `como-beauvallon-v2-le-domaine.html` | **Vidéo** Côte d'Azur (poster = riders devant le domaine) + **vidéo de fond** dans la scène « Expérience » | roches rouges + sunset | mix |
| `como-beauvallon-v3-escapade.html` | Formation au-dessus du golfe | roches rouges + golfe | Lérins / Estérel (fort, roche rouge) |

**Pipeline reproductible** (relancer quand tu ajoutes/remplaces des photos) :
1. `python tools/optimize_media.py` → recadre + compresse en WebP web (`medias/web/`, 20 fichiers ≈ 3,8 Mo). Édite `SRC`/`JOBS` pour changer une photo ou un cadrage (vfocus/hfocus).
2. `python tools/build_versions.py` → régénère les 3 HTML. Édite `EDITIONS` pour changer héros/galerie ou créer une 4ᵉ version.

**Photos** : tous les `<img>` ont `width`/`height` (anti-CLS), `alt` descriptif, `loading="lazy"` sous le fold (héros en `fetchpriority="high"`).

**⚠️ Vidéos — à compresser avant prod.** Pas de ffmpeg sur la machine de build : la vidéo de fond est câblée telle quelle (`<video preload="metadata" poster=… data-cb-autoplay>` → lecture **desktop only**, mobile = poster) en pointant le `.MP4` source **lourd (~108 Mo)**. À remplacer par un export web compressé. Exemple :
```bash
# boucle hero ~10 s, 1080p, sans son, ~3–5 Mo (mp4 + webm)
ffmpeg -i medias/videos-cotedazur/CotedeZur_Awaking.mov -t 10 -an -vf "scale=1920:-2" -c:v libx264 -crf 24 -movflags +faststart hero.mp4
ffmpeg -i medias/videos-cotedazur/CotedeZur_Awaking.mov -t 10 -an -vf "scale=1920:-2" -c:v libvpx-vp9 -crf 34 -b:v 0 hero.webm
# version 9:16 pour mobile : reel vertical déjà dispo (Lift_Cotedezur_Awaking_Vertical.MP4)
```
(La vidéo « Awaking » horizontale propre est en `.mov` — non lisible en navigateur ; le `.MP4` câblé a des sous-titres incrustés. Réexporter une version web propre.)

**Chemins** : les éditions référencent `medias/web/…` en **relatif** (preview locale OK). Pour WordPress, téléverser `medias/web/` (+ la vidéo compressée) vers `/assets/…` et adapter les chemins (ou laisser relatif si servi depuis le même dossier).

---

## 1) Intégration WordPress (`wp:html`)

1. Dans l'éditeur, ajouter un bloc **HTML personnalisé**.
2. Coller **uniquement** le contenu entre `===== BLOC wp:html — DÉBUT =====` et `===== FIN =====`
   (le `<!doctype>`, `<head>` et le reset de preview restent en dehors).
3. Le bloc est **autonome** : il embarque ses `@font-face`, son CSS, son grain (data-uri) et son JS.
4. **Recommandé (LCP)** : ajouter ces 2 `preload` dans le `<head>` du thème (functions.php / `wp_head`) :
   ```html
   <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/archivo-latin-standard-normal.woff2" crossorigin>
   <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Switzer-Regular.woff2" crossorigin>
   ```
5. **GSAP** : chargé depuis cdnjs en `defer`. Si CDN bloqué → l'init révèle tout le contenu (fallback OK).
   Pour 100 % self-host : télécharger `gsap.min.js` + `ScrollTrigger.min.js` (3.13.0) dans `/vendor/`
   et remplacer les 2 `src` CDN.

---

## 2) Polices woff2 self-host (aucun appel Google Fonts)

À déposer dans **`/assets/fonts/`** (chemins déjà câblés dans les `@font-face` du bloc).

| Rôle | Famille CSS | Fichier woff2 | Poids / largeur | Source | Licence |
|---|---|---|---|---|---|
| **Display** | `Archivo Expanded` | `archivo-latin-standard-normal.woff2` | variable `wght 200–400` + `wdth 62–125 %` (on utilise `font-stretch:125%` = Expanded) | Fontsource — pkg `@fontsource-variable/archivo`, fichier `files/archivo-latin-standard-normal.woff2` | **OFL 1.1** (self-host + commercial libres) |
| **Corps** | `Switzer` (400) | `Switzer-Regular.woff2` | 400 | [fontshare.com/fonts/switzer](https://www.fontshare.com/fonts/switzer) → *Download Family* (ZIP) → `Fonts/WEB/fonts/` | **ITF Free Font License** (self-host + commercial OK ; revente/redistribution interdites) |
| **Corps** | `Switzer` (500) | `Switzer-Medium.woff2` | 500 | idem | idem |

- ⚠️ **Ne pas** prendre `archivo-latin-wght-normal.woff2` (axe poids seul, largeur figée → pas d'Expanded).
  Le fichier `…-standard-…` expose les **deux** axes (`font-weight 100 900` + `font-stretch 62% 125%`).
- Alternative corps possible : **General Sans** (Fontshare, même licence) — `GeneralSans-Regular.woff2`,
  `GeneralSans-Medium.woff2`. Pour l'utiliser, changer `--cb-ff-body` et les `@font-face`.
- Tailles approx : Switzer/General Sans ≈ 25–40 Ko/woff2 ; Archivo variable `standard` ≈ 40–55 Ko (un seul
  fichier couvre toutes graisses/largeurs). Subset **latin** déjà inclus.

---

## 3) Slots médias (placeholders stylés dans la maquette — remplacer par les rushes étalonnés)

> **Grade commun obligatoire** : cinématique, **golden-hour / summer**, dominante chaude (sable, doré,
> terracotta), saturation −10/−15 %, voile chaud, grain fin. **Jamais de bleu froid dominant.** Décliner
> chaque plan clé en **16:9 ET 9:16**. Pas de GoPro fisheye, pas de bleu tropical sursaturé, pas de foule.
> Placeholders de maquette = **tons chauds sable/doré + grain** (jamais bleus).

| Slot | Ratio | Résolution conseillée | Contenu |
|---|---|---|---|
| `MEDIA_HERO_VIDEO` | 16:9 + 9:16 | 1920×1080 / 1080×1920 (≤3–5 Mo, webm+mp4) | Drone, pull-back lent révélant le rider en vol sur le golfe + domaine + pins |
| `MEDIA_HERO_POSTER` | 16:9 | frame 4K → WebP | Poster (= LCP). `fetchpriority="high"`, `width/height` |
| `MEDIA_LIEU` | 4:3 (ou 16:9) | 1600×1200 WebP | Domaine / ponton / eau, calme du matin (parallax léger) |
| `MEDIA_BEACH_1` | 16:9 | 1920×1080 WebP | Beach club : transats, parasols, sable, golden hour (réf. COMO « Beauvallon Sur Mer ») |
| `MEDIA_BEACH_2` | 3:4 | 1200×1600 WebP | Le ponton privé (départ des sessions) |
| `MEDIA_BROLL_1` | 16:9 | 1920×1080 | La lame du mât qui trace une ligne nette, reflets dorés |
| `MEDIA_EXP_VIDEO` | 16:9 | 1920×1080 (fond pinné, mute/loop) | Rider en vol, plan large et lent (tenu pendant le scroll-through) |
| `MEDIA_RIDE_1..5` | mix 3:4 / 4:3 | ~1200 px côté long, WebP | Détail rider, matériel Lift, spot à différentes lumières, élan du ponton |
| `MEDIA_SESSION_1..4` | 16:9 | 1280×720 WebP | Briefing → équipement → à l'eau → vol |
| `CARTE` | — | iframe Google Maps `loading="lazy"` | Domaine COMO Le Beauvallon, Grimaud |
| `REVIEWS` | — | texte | 3 avis Google **réels** (Places API ou collage manuel, RGPD) |
| `BOOKING_BLOCK` | — | — | Module réservation (REST / CPT `reservation` ou Odoo) dans `#cb-booking` |

**Perf médias** : poster WebP en LCP, vidéos `preload="metadata"` + `mute/loop/playsinline`,
**autoplay désactivé sur mobile** (poster + lecture conditionnelle JS, pattern fourni en commentaire),
images sous le fold `loading="lazy"` + `width/height` (anti-CLS).

---

## 4) Placeholders à remplir (tokens `{{…}}`)

| Token | Où | À mettre |
|---|---|---|
| `{{PRIX}}` | réservation, FAQ, JSON-LD | tarif indicatif « dès … » |
| `{{TÉLÉPHONE}}` / `{{TÉLÉPHONE_E164}}` / `{{EMAIL}}` | spot, footer, JSON-LD, `href tel:` | NAP — **même numéro partout** (texte lisible + E.164) |
| `{{ÂGE_MINI}}` | FAQ + JSON-LD | âge minimum réel |
| `{{HORAIRES}}` | footer (+ `openingHoursSpecification` JSON-LD) | horaires saison réels |
| `{{NOTE}}` / `{{NB_AVIS}}` | preuve sociale (+ `aggregateRating` **si avis réels**) | note Google + nb d'avis |
| `{{AVIS_1..3}}` / `{{CLIENT_1..3}}` | preuve sociale | verbatims Google réels |
| `{{LIEN_INSTAGRAM}}` / `{{LIEN_FICHE_GOOGLE}}` / `{{LIEN_MENTIONS}}` | footer, JSON-LD `sameAs` | URLs |
| `{{MODELE_LIFT}}` (commentaire) | section « Pour qui » | préciser **Lift4** ou **LIFT5** selon la flotte réelle |
| N° de voie (Bd des Collines) | NAP + JSON-LD | numéro exact (non publié — à confirmer) |

**Faits vérifiés utilisés** : Grimaud `83310`, golfe de Saint-Tropez, ponton/plage privés, pinède Belle
Époque, transfert bateau « 8 min » (chiffre officiel COMO), géo ≈ `43.291, 6.599`. **À reconfirmer avant
prod** : adresse au n° près, téléphone, date d'ouverture (formulée prudemment), modèle Lift.

---

## 5) JSON-LD (séparé, prêt à injecter)

Déjà présent dans le bloc. Version standalone (valide, **sans commentaire interne** — JSON n'en autorise pas) :

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness", "SportsActivityLocation"],
      "@id": "https://www.efoilcotedazur.fr/beauvallon/#base",
      "name": "eFoil Côte d'Azur — base du golfe de Saint-Tropez",
      "description": "Sessions d'eFoil encadrées au départ du ponton du domaine COMO Le Beauvallon, golfe de Saint-Tropez.",
      "url": "https://www.efoilcotedazur.fr/beauvallon/",
      "image": "https://www.efoilcotedazur.fr/assets/img/og-beauvallon.jpg",
      "telephone": "{{TÉLÉPHONE_E164}}",
      "priceRange": "€€€",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Boulevard des Collines",
        "addressLocality": "Grimaud",
        "postalCode": "83310",
        "addressRegion": "Var",
        "addressCountry": "FR"
      },
      "geo": { "@type": "GeoCoordinates", "latitude": 43.291, "longitude": 6.599 },
      "areaServed": "Golfe de Saint-Tropez",
      "sameAs": ["{{LIEN_INSTAGRAM}}", "{{LIEN_FICHE_GOOGLE}}"],
      "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "09:00", "closes": "19:00"
      }]
    }
  ]
}
```
> `aggregateRating` : ajouter **uniquement si des avis réels existent**, comme vrai JSON
> (`,"aggregateRating":{"@type":"AggregateRating","ratingValue":"{{NOTE}}","reviewCount":"{{NB_AVIS}}"}`),
> après `openingHoursSpecification`. Le `FAQPage` complet est dans le bloc HTML.

---

## 6) À vérifier en navigateur réel (Windows, scrollbar visible)

- **Section épinglée** (`.cb-pin`, full-bleed + ScrollTrigger pin) : confirmer qu'aucun **saut horizontal**
  de quelques px n'apparaît à l'entrée/sortie du pin. `overflow-x:clip` sur `.cb-root` couvre le débord
  `100vw` ; si un saut subsiste, passer la section pinnée en `width:100%` ou activer `scrollbar-gutter:stable`.
- **prefers-reduced-motion** et **JS désactivé** : tout le contenu doit rester visible (aucun titre clippé).
- **Mobile ≤480** : vérifier qu'aucun titre ne déborde à 360/320 px.
- **Lighthouse mobile** après dépôt des polices + recompression vidéo (cible LCP < 2 s).

---

## 7) Qualité (vérifié au build)

JSON-LD valide · un seul `<h1>` · 0 emoji · 0 appel Google Fonts · **0 bleu en aplat** (vérifié) · CTA
terracotta · turquoise réduit à **un seul glint** · CSS 100 % namespacé `.cb-` · focus clavier visible
(anneau espresso + halo terracotta) · **contrastes AA recalculés sur la palette chaude** (corps 7.4:1,
liens 5.1:1, CTA blanc/terracotta 5.7:1, gold/espresso 7.2:1) · reveals masqués qui s'animent réellement
(fix unité `yPercent`) · fallback no-JS / reduced-motion sûr · **13 sections** (Beach Club ajouté).
