# RÉCAP — point de reprise (handoff) · 2026-06-12

> Fichier de reprise après le passage en **git worktree** (déplacement du dépôt + fermeture des sessions).
> ⚠️ Déplacer le dossier **change l'identité du projet Claude** : la mémoire auto (ancien projet `d--efoilcotedazur`)
> ne se chargera **pas** automatiquement dans le nouveau chemin. **Ce fichier est la source de vérité** pour repartir.

---

## 1. État du dépôt (vérifié le 2026-06-12)

- Remote : `https://github.com/GHOSTGIT-cyber/efoilcotedazur.git` (public).
- **Tout est committé ET poussé.** `croix-valmer-landings` et `main` étaient **SYNCHRO avec origin**.
- Seul non suivi : `medias/logo/` (pas lié à Croix-Valmer — ne pas y toucher).

3 produits dans le même dépôt :
| Produit | Fichiers | Branche cible |
|---|---|---|
| **Site principal** (eFoil Côte d'Azur, Mandelieu) | `index.html`, `index-bleu.html`, `reservation.html`, `dashboard.html`, `assets/` | `main` |
| **Beauvallon / COMO** | `como-beauvallon-*.html`, `*-LIVRABLE.md`, médias COMO | `beauvallon` (à créer) |
| **Croix-Valmer** | `croix-valmer.html`, `croix-valmer-como.html`, `medias/web/cv/`, `tools/cv_aerial_media.py` | `croix-valmer-landings` |

---

## 2. Travail Croix-Valmer déjà livré (branche `croix-valmer-landings`)

- **`croix-valmer.html`** — page UNIQUE, DA « hybride cinéma + marque EFCA » (Inter, **orange `#F4631F` / turquoise `#00A7C7`**,
  boutons pilule, rating bar, vagues SVG, logo), namespace `.cvx-`, hero **photo aérienne** plein écran + ken-burns.
  **Bascule de thème orange ⇄ bleu** via bouton header → `[data-theme]` + swap du hero + `localStorage`.
  Marque = **« eFoil Croix-Valmer »** (PAS « Côte d'Azur » ; le domaine `efoilcotedazur.fr` reste, lui).
- **`croix-valmer-como.html`** — DA éditoriale teal/Archivo (style COMO), namespace `.cv-`.
- **Photos 100 % aériennes** : set `medias/web/cv/` (`aer-01..37` + `hero-{orange,bleu,como}{,-v}`) généré par
  `tools/cv_aerial_media.py` depuis la curation `efca-photo-tri.json` (packs `aerien`/`top`/`sunset`/`lieu`,
  **sans riders classiques**). Pas de vidéos (pas encore prêtes) → heros en photo.
- Preview : `https://raw.githack.com/GHOSTGIT-cyber/efoilcotedazur/croix-valmer-landings/croix-valmer.html`

Reste à faire (idées) : brancher `BOOKING_BLOCK`, remplir `{{PRIX}}` / `{{TÉLÉPHONE}}` / avis Google réels,
vraies photos de Gigaro quand dispo, vidéos quand prêtes.

---

## 3. Migration worktree — à exécuter (FENÊTRES/SESSIONS FERMÉES pour le déplacement)

**Cible (tout regroupé, plus rien à la racine `D:\`) :**
```
D:\efoil\
   efoilcotedazur\   -> branche main                  (session « eFoil Côte d'Azur »)
   beauvallon\       -> branche beauvallon            (session « Beauvallon »)
   croix-valmer\     -> branche croix-valmer-landings (session « Croix-Valmer »)
```

**Étapes :**
1. Fermer toutes les fenêtres VSCode / sessions.
2. Créer `D:\efoil\` puis déplacer le dossier **entier** `D:\efoilcotedazur` → `D:\efoil\efoilcotedazur` (le `.git` part avec).
3. Rouvrir `D:\efoil\efoilcotedazur`, puis :
   ```bash
   cd /d/efoil/efoilcotedazur
   git checkout main
   git fetch origin
   git worktree add        ../croix-valmer  croix-valmer-landings
   git worktree add -b beauvallon ../beauvallon  main
   git worktree list      # doit lister 3 worktrees
   ```
4. Ouvrir les 3 dossiers, chacun dans **sa** fenêtre VSCode (une fenêtre = un dossier = une branche = une session).

---

## 4. Règles permanentes (anti-écrasement entre sessions)

- Chaque session **reste dans son dossier** et **ne fait jamais `git checkout <autre-branche>`** ailleurs.
- **Vérifier `git branch --show-current`** avant toute écriture (doit = la branche de la session).
- **Ne committer que ses propres fichiers** : `git add <tes-fichiers>` — **jamais `git add -A`**.
- **Pas de PR.** Sur `main` : `git pull --rebase` avant `git push`.
- `git fetch origin` pour voir le travail des autres (le `.git` est commun aux 3 worktrees).

---

## 5. Reprise de la session « Croix-Valmer »

- **Dossier** : `D:\efoil\croix-valmer` · **branche** : `croix-valmer-landings`.
- Lire ce fichier (la mémoire auto ne suivra pas le changement de chemin).
- Repartir de l'état §2. Vérifier `git branch --show-current` = `croix-valmer-landings`, puis travailler.
