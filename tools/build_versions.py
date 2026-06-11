#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Génère les éditions de la landing eFoil COMO Le Beauvallon à partir du template
de base (como-beauvallon-efoil.html, qui contient les placeholders MEDIA_*),
en remplaçant chaque slot par la vraie photo/vidéo (medias/web/ + medias/videos…).

Usage : python tools/build_versions.py   (après tools/optimize_media.py)
Sortie : como-beauvallon-v1-coucher-de-soleil.html / v2-le-domaine / v3-escapade

Pour créer/modifier une édition : édite EDITIONS (héros, respirations, galerie).
Le slot CARTE reste un placeholder (c'est une iframe Google Maps, pas une photo).
"""
import re, os
from PIL import Image

BASE = 'como-beauvallon-efoil.html'
VIDEO = 'medias/videos-cotedazur/Cotedezur_Awaking_Subtitled.MP4'  # ⚠ 108 Mo, à compresser avant prod

base = open(BASE, encoding='utf-8').read()

def dims(name):
    with Image.open(f'medias/web/{name}.webp') as im: return im.size
def esc(s): return s.replace('"', '&quot;')

def img_fill(name, alt, lazy=True):
    w, h = dims(name)
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    return f'<img class="cb-fill" src="medias/web/{name}.webp" width="{w}" height="{h}"{l} alt="{esc(alt)}">'
def img_media(name, ratio, alt):
    w, h = dims(name)
    return (f'<img class="cb-media cb-ratio-{ratio}" src="medias/web/{name}.webp" '
            f'width="{w}" height="{h}" loading="lazy" decoding="async" alt="{esc(alt)}">')
def video_fill(poster, alt):
    w, h = dims(poster)
    return (f'<video class="cb-fill" muted loop playsinline preload="metadata" '
            f'poster="medias/web/{poster}.webp" width="{w}" height="{h}" data-cb-autoplay '
            f'aria-label="{esc(alt)}"><source src="{VIDEO}" type="video/mp4"></video>')

def replace_slot(html, tag, markup):
    pat = re.compile(r'<div class="cb-ph[^"]*"[^>]*>\s*<div class="cb-ph__inner">'
                     r'<span class="cb-ph__tag">' + re.escape(tag) + r'</span>.*?</div>\s*</div>', re.DOTALL)
    html, n = pat.subn(lambda m: markup, html, count=1)
    assert n == 1, f"slot {tag}: {n} remplacement(s)"
    return html

ALT = {
 'hero-sunset':"Au coucher du soleil, des riders en eFoil glissent devant la silhouette de Saint-Tropez sur le golfe embrasé.",
 'hero-domaine':"Deux riders volent sur leur eFoil au-dessus du golfe, devant le domaine et ses pins parasols.",
 'hero-formation':"Plusieurs riders en formation volent sur leurs eFoils au-dessus du golfe de Saint-Tropez.",
 'lieu-domaine':"Le domaine au bord du golfe : deux riders en vol devant la plage et les pins parasols.",
 'beach-terrasse':"La terrasse de la base face à la mer, planches eFoil prêtes.",
 'beach-ponton':"Préparation au ponton avant la session : planches et télécommandes.",
 'breath-sunset':"Silhouettes de riders foilant sur le golfe au coucher du soleil.",
 'breath-redrock':"Riders en vol devant les roches rouges de l'Estérel.",
 'breath-golfe':"Riders en vol sur l'eau calme du golfe.",
 'exp-formation':"Riders volant en silence au-dessus du golfe.",
 'ride-women':"Deux rideuses en eFoil sur l'eau calme, reflets du matin.",
 'ride-lerins-orange':"Rider en vol sur une planche Lift orange devant le fort de Sainte-Marguerite.",
 'ride-lerins-green':"Rideuse souriante en vol sur une planche Lift verte.",
 'ride-esterel':"Couple partageant une planche, en vol devant le massif rouge de l'Estérel.",
 'ride-redrock':"Trois riders en vol devant les roches rouges.",
 'ride-formation':"Riders en formation au-dessus du golfe.",
 'session-briefing':"Briefing au ponton : prise en main de la télécommande.",
 'session-gear':"Équipement : planches Lift et télécommandes.",
 'session-water':"Premiers mètres à l'eau, accompagné d'un moniteur.",
 'session-flight':"Le vol : la planche s'élève au-dessus du golfe.",
}
A = lambda n: ALT[n]

COMMON = [
 ('MEDIA_LIEU',     lambda: img_media('lieu-domaine','43',A('lieu-domaine'))),
 ('MEDIA_BEACH_1',  lambda: img_media('beach-terrasse','169',A('beach-terrasse'))),
 ('MEDIA_BEACH_2',  lambda: img_media('beach-ponton','34',A('beach-ponton'))),
 ('MEDIA_SESSION_1',lambda: img_media('session-briefing','169',A('session-briefing'))),
 ('MEDIA_SESSION_2',lambda: img_media('session-gear','169',A('session-gear'))),
 ('MEDIA_SESSION_3',lambda: img_media('session-water','169',A('session-water'))),
 ('MEDIA_SESSION_4',lambda: img_media('session-flight','169',A('session-flight'))),
]
GAL_DEFAULT = ['ride-women','ride-redrock','ride-lerins-orange','ride-formation','ride-esterel']
GAL_SCENIC  = ['ride-lerins-orange','ride-redrock','ride-lerins-green','ride-formation','ride-esterel']
GAL_RATIOS  = ['34','43','34','43','34']

EDITIONS = {
 'v1-coucher-de-soleil': dict(label="Coucher de soleil",
    hero=('img','hero-sunset'),  broll1='breath-sunset', exp=('img','exp-formation'),
    broll2='breath-redrock', gallery=GAL_DEFAULT),
 'v2-le-domaine': dict(label="Le domaine (vidéo)",
    hero=('video','hero-domaine'), broll1='breath-redrock', exp=('video','exp-formation'),
    broll2='breath-sunset', gallery=GAL_DEFAULT),
 'v3-escapade': dict(label="Escapade",
    hero=('img','hero-formation'), broll1='breath-redrock', exp=('img','exp-formation'),
    broll2='breath-golfe', gallery=GAL_SCENIC),
}

if __name__ == '__main__':
    for key, cfg in EDITIONS.items():
        h = base.replace(
            '<title>eFoil au golfe de Saint-Tropez — sessions au départ du domaine COMO Le Beauvallon</title>',
            f'<title>eFoil · COMO Le Beauvallon — golfe de Saint-Tropez · Édition {cfg["label"]}</title>')
        h = h.replace('cb-lieu__fig cb-parallax','cb-lieu__fig').replace('cb-beach__fig cb-parallax cb-fade','cb-beach__fig cb-fade')
        kind, name = cfg['hero']
        h = replace_slot(h,'MEDIA_HERO_VIDEO', video_fill(name,A(name)) if kind=='video' else img_fill(name,A(name),lazy=False))
        kind, name = cfg['exp']
        h = replace_slot(h,'MEDIA_EXP_VIDEO', video_fill(name,A(name)) if kind=='video' else img_fill(name,A(name)))
        h = replace_slot(h,'MEDIA_BROLL_1', img_fill(cfg['broll1'],A(cfg['broll1'])))
        h = replace_slot(h,'MEDIA_BROLL_2', img_fill(cfg['broll2'],A(cfg['broll2'])))
        for tag, fn in COMMON: h = replace_slot(h, tag, fn())
        for i,(nm,rt) in enumerate(zip(cfg['gallery'],GAL_RATIOS),1):
            h = replace_slot(h, f'MEDIA_RIDE_{i}', img_media(nm,rt,A(nm)))
        out = f'como-beauvallon-{key}.html'
        open(out,'w',encoding='utf-8').write(h)
        print(f"  → {out}")
