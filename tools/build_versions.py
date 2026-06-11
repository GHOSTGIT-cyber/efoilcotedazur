#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Génère les éditions de la landing eFoil COMO Le Beauvallon depuis le template
(como-beauvallon-efoil.html), en remplaçant chaque slot MEDIA_* par la vraie
photo/vidéo (medias/web/). Lance d'abord tools/optimize_media.py.

Sortie : como-beauvallon-v1-coucher-de-soleil / v2-le-domaine / v3-escapade .html
Slot CARTE = laissé en placeholder (iframe Google Maps).
"""
import re, os
from PIL import Image

BASE = 'como-beauvallon-efoil.html'
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
def video_fill(alt):
    w, h = dims('hero-video-poster')
    return (f'<video class="cb-fill" muted loop playsinline preload="metadata" '
            f'poster="medias/web/hero-video-poster.webp" width="{w}" height="{h}" data-cb-autoplay '
            f'aria-label="{esc(alt)}"><source src="medias/web/hero-video.mp4" type="video/mp4"></video>')

def replace_slot(html, tag, markup):
    pat = re.compile(r'<div class="cb-ph[^"]*"[^>]*>\s*<div class="cb-ph__inner">'
                     r'<span class="cb-ph__tag">' + re.escape(tag) + r'</span>.*?</div>\s*</div>', re.DOTALL)
    html, n = pat.subn(lambda m: markup, html, count=1)
    assert n == 1, f"slot {tag}: {n} remplacement(s)"
    return html

ALT = {
 'hero-sunset':"Au coucher du soleil, des riders en eFoil glissent devant la silhouette de Saint-Tropez.",
 'hero-grandevue':"Vue aérienne du domaine COMO Le Beauvallon : le palace Belle Époque, la pinède, la plage et le ponton sur le golfe.",
 'hero-formation':"Riders en formation volant sur leurs eFoils au-dessus du golfe de Saint-Tropez.",
 'lieu-chateau':"Le palace Belle Époque du domaine COMO Le Beauvallon, dans les pins, au coucher du soleil.",
 'beach-parasols':"Le beach club du domaine : parasols dorés et vue sur le golfe de Saint-Tropez.",
 'beach-loungers':"Transats et parasols du beach club face à la mer.",
 'exp-silence':"Des riders glissent en silence sur le golfe au coucher du soleil.",
 'exp-apesanteur':"Deux riders portés par leur aile au-dessus du golfe, devant le domaine.",
 'exp-rythme':"Un moniteur accompagne un débutant lors de ses premiers vols.",
 'breath-sunset':"Vue drone : des riders en eFoil sur le golfe au coucher du soleil.",
 'breath-redrock':"Riders en vol devant les roches rouges de l'Estérel.",
 'breath-golfe':"Riders en vol sur l'eau calme du golfe.",
 'ride-women':"Deux rideuses en eFoil sur l'eau calme, reflets du matin.",
 'ride-redrock':"Trois riders en vol devant les roches rouges.",
 'ride-lerins-orange':"Rider sur une planche Lift orange devant le fort de Sainte-Marguerite.",
 'ride-formation':"Riders en formation au-dessus du golfe.",
 'ride-esterel':"Couple partageant une planche, en vol devant le massif rouge de l'Estérel.",
 'ride-yacht':"Riders en eFoil devant le port et ses yachts.",
 'ride-esterel-vert':"Riders au pied des roches rouges de l'Estérel.",
 'ride-lerins-green':"Rideuse souriante en vol sur une planche Lift verte.",
 'session-briefing':"Briefing au ponton : prise en main de la télécommande.",
 'session-gear':"Équipement : planches Lift et télécommandes.",
 'session-water':"Premiers mètres à l'eau, accompagné d'un moniteur.",
 'session-flight':"Le vol : la planche s'élève au-dessus du golfe.",
}
A = lambda n: ALT[n]
VIDEO_ALT = "Vue drone au coucher du soleil : des riders en eFoil glissent sur le golfe de Saint-Tropez."

COMMON = [
 ('MEDIA_LIEU',     lambda: img_media('lieu-chateau','43',A('lieu-chateau'))),
 ('MEDIA_BEACH_1',  lambda: img_media('beach-parasols','169',A('beach-parasols'))),
 ('MEDIA_BEACH_2',  lambda: img_media('beach-loungers','34',A('beach-loungers'))),
 ('MEDIA_EXP_1',    lambda: img_media('exp-silence','169',A('exp-silence'))),
 ('MEDIA_EXP_2',    lambda: img_media('exp-apesanteur','43',A('exp-apesanteur'))),
 ('MEDIA_EXP_3',    lambda: img_media('exp-rythme','34',A('exp-rythme'))),
 ('MEDIA_SESSION_1',lambda: img_media('session-briefing','169',A('session-briefing'))),
 ('MEDIA_SESSION_2',lambda: img_media('session-gear','169',A('session-gear'))),
 ('MEDIA_SESSION_3',lambda: img_media('session-water','169',A('session-water'))),
 ('MEDIA_SESSION_4',lambda: img_media('session-flight','169',A('session-flight'))),
]
GALLERY = ['ride-women','ride-redrock','ride-lerins-orange','ride-formation',
           'ride-esterel','ride-yacht','ride-esterel-vert','ride-lerins-green']
GAL_RATIOS = ['34','43','34','43','34','34','34','34']

EDITIONS = {
 'v1-coucher-de-soleil': dict(label="Coucher de soleil",
    hero=('video',None), broll1='breath-redrock', broll2='breath-golfe'),
 'v2-le-domaine': dict(label="Le domaine",
    hero=('img','hero-grandevue'), broll1='breath-sunset', broll2='breath-redrock'),
 'v3-escapade': dict(label="Escapade",
    hero=('img','hero-formation'), broll1='breath-redrock', broll2='breath-sunset'),
}

if __name__ == '__main__':
    for key, cfg in EDITIONS.items():
        h = base.replace(
            '<title>eFoil au golfe de Saint-Tropez — sessions au départ du domaine COMO Le Beauvallon</title>',
            f'<title>eFoil · COMO Le Beauvallon — golfe de Saint-Tropez · Édition {cfg["label"]}</title>')
        h = h.replace('cb-lieu__fig cb-parallax','cb-lieu__fig').replace('cb-beach__fig cb-parallax cb-fade','cb-beach__fig cb-fade')
        kind, name = cfg['hero']
        h = replace_slot(h,'MEDIA_HERO_VIDEO', video_fill(VIDEO_ALT) if kind=='video' else img_fill(name,A(name),lazy=False))
        h = replace_slot(h,'MEDIA_BROLL_1', img_fill(cfg['broll1'],A(cfg['broll1'])))
        h = replace_slot(h,'MEDIA_BROLL_2', img_fill(cfg['broll2'],A(cfg['broll2'])))
        for tag, fn in COMMON: h = replace_slot(h, tag, fn())
        for i,(nm,rt) in enumerate(zip(GALLERY,GAL_RATIOS),1):
            h = replace_slot(h, f'MEDIA_RIDE_{i}', img_media(nm,rt,A(nm)))
        out = f'como-beauvallon-{key}.html'
        open(out,'w',encoding='utf-8').write(h)
        left = len(re.findall(r'cb-ph__tag">MEDIA_', h))
        print(f"  -> {out}   (placeholders MEDIA restants: {left})")
