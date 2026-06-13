# Prompt de reprise — session « Landing eFoil COMO Le Beauvallon »

> Colle ce bloc dans une nouvelle session Claude Code pour reprendre exactement où on en est.
> (Une migration vers des **git worktrees** est prévue : la session Beauvallon vivra dans `D:\efoil\beauvallon` sur la branche **`beauvallon`**. Tant que ce n'est pas fait, le travail est dans `d:\efoilcotedazur` sur **`main`**.)

---

Tu reprends la **session « COMO Le Beauvallon »** : une landing page one-page pour une base de location d'**eFoil** au départ du ponton du domaine **COMO Le Beauvallon**, golfe de Saint-Tropez. DA chaude « beach-club » (crème/sable, accent **terracotta**, secondaire **or**, sombre = espresso ; **zéro bleu**), typo **Archivo Expanded + Switzer**, namespace CSS `.cb-`.

## 0. AVANT TOUTE ACTION (dépôt partagé par 3 sessions → risque d'écrasement)
1. `git branch --show-current`. Tu dois être sur **`beauvallon`** (post-migration worktree, dossier `D:\efoil\beauvallon`) **ou** `main` (pré-migration, dossier `d:\efoilcotedazur`). **Jamais** travailler sur `croix-valmer-landings` (autre session).
2. Ne pousser QUE tes fichiers : `git add <fichiers précis>`, **jamais `git add -A`**. **Pas de PR.**
3. Ne **jamais** committer les originaux lourds (>100 Mo = rejet GitHub). `.gitignore` exclut les dossiers sources ; **seul `medias/web/` part en ligne**.
4. Pour chaque livrable, **toujours donner 2 liens** : local `http://localhost:8000/<fichier>` (lancer `python -m http.server 8000` en arrière-plan) **et** en ligne `https://raw.githack.com/GHOSTGIT-cyber/efoilcotedazur/<branche>/<fichier>`.
5. Lis d'abord **`RECAP-SESSION-beauvallon.md`** (état détaillé) à la racine.

## 1. État actuel
- **5 éditions** générées depuis le template `como-beauvallon-efoil.html` (placeholders `MEDIA_*`) :
  - `como-beauvallon-v1-coucher-de-soleil.html` = **V1, base retenue** (héros = **boucle vidéo drone** coucher de soleil `medias/web/hero-video.mp4`).
  - v2 (grande vue château), v3 (château + ordre revu), **v4-full-drone** (tout aérien, *photos appréciées du client*), v5 (palette claire/typo fine).
  - `como-beauvallon-efca-bleu.html` = style efoilcotedazur bleu → **ABANDONNÉ** (jugé moche).
- `reservation-beauvallon.html` = page réservation, formulaire → confirmation, **sans paiement** (front-only, à brancher). Tous les CTA « Réserver » des éditions y pointent.
- `trieur-photos.html` = trieur de photos. **Catégories = emplacements exacts (slots)** de la page (Héros, Lieu, Beach aérien, Beach parasols, Exp. silence/apesanteur/rythme, Pour qui 1→4, Déroulé 1→4, Le spot, **Galerie qui défile**, À proscrire) + **annotation par photo** (double-clic) + **export/import JSON**.
- Médias : `medias/web/` = WebP optimisés (slots nommés + `pool/` 96 keepers + `pool-drone/` 36 aériens + `hero-video.mp4` + posters). Teinte chaude COMO appliquée (variable CSS `--cb-warm`, réglable).

## 2. Pipeline reproductible (outils `tools/`)
- `tools/packs.json` = **le tri du client** (packs par catégorie) = source de vérité de la curation.
- `python tools/apply_packs.py` → régénère `medias/web/` (slots + pools) depuis `packs.json`, **exclut les « à proscrire »**, grade chaud auto.
- `python tools/build_versions.py` → régénère les éditions depuis le template.
- `python tools/build_sorter.py` → régénère `trieur-photos.html` (+ vignettes `medias/thumbs/`).
- `python tools/drone_slots.py` → slots/pool aériens (édition full-drone).

## 3. CE QU'IL FAUT FAIRE (objectif en cours)
**Uniformiser en UNE seule version, à partir de V1**, dès que le client envoie son nouveau **JSON de tri** (par slots, depuis `trieur-photos.html`) :
1. Mettre **les bonnes photos aux bons endroits** selon son JSON (mettre à jour `tools/packs.json` ou un mapping slot→photo, puis `apply_packs.py` + `build_versions.py`).
2. Privilégier ses **plans drone** (il les aime).
3. **Toutes les galeries doivent défiler toutes seules** (auto-scroll/auto-fade) — **supprimer les zones à scroll horizontal manuel** — et **exploiter TOUTES les photos** gardées.
4. **Supprimer les autres éditions** (v2/v3/v4/v5 + efca-bleu) pour ne garder qu'**une version**.
5. Réservation : brancher le formulaire sur un backend (REST WordPress / CPT `reservation` / Odoo / email).
6. Tokens `{{…}}` à remplir (téléphone, prix, avis Google réels, modèle Lift, n° de voie). **Droits images COMO** à clearer avant prod publique.

## 4. Conventions DA (rappel)
- Crème/sable, terracotta (CTA/accent), or (secondaire), espresso (booking/footer). **Zéro bleu/teal en aplat.** Turquoise Lift = 1 seul glint discret.
- Teinte chaude « coucher de soleil » assumée sur les photos (`--cb-warm`).
- Pas d'emoji, pas d'icônes génériques, contrastes AA, `prefers-reduced-motion` respecté, fallback no-JS.

→ **Première action recommandée :** vérifier la branche, lancer le serveur local, redonner les 2 liens (V1 + trieur + réservation), puis **demander/attendre le JSON de tri** du client pour finaliser la V1.
